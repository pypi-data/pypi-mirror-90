import numpy as np
from math import factorial
from scipy.special import ndtri

from scipy.stats import norm
from scipy.stats import t as tdist
from scipy.special import gammaln

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.PureJump_utils import PureJump_lncondassetprob

#---------------------------------------------

class PureJump_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)

        return

    def _init_d(self):
        mu=0.0
        if( len(self.series) > 1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)

        lamb = 10.0
        gamm = 0.0
        omeg = 0.02

        self.workingpars_names=['mu','lambda','gamma','omega']
        self.workingpars=np.array([mu,lamb,gamm,omeg])
        self.workingpars_diffs=[0.0001,0.0001,0.0001, 0.0001]

#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]

        if 'init' in self.options:
            self.initpars_reporting(self.options['init'])

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        if(Nret>0):
            self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
            self.upath=np.zeros(self.Nobs)

        return

    def initpars_reporting(self,pardict):
        mu=self.workingpars[0] 
        lamb=self.workingpars[1]
        gamm=self.workingpars[2] 
        omeg=self.workingpars[3]
        
        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        self.workingpars[0]=mu
        self.workingpars[1]=lamb
        self.workingpars[2]=gamm
        self.workingpars[3]=omeg

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        corrmatrix=np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=0.0

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars[0] 
        lamb=self.workingpars[1]
        gamm=self.workingpars[2] 
        omeg=self.workingpars[3]
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        
        dt=self.dt/Nperstep

# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: jump indicator
# Zs[2,:,:]: jump size
        
        max_jumps=21        
        njumps=np.zeros(Nperstep,int)
# all sub-timesteps are the same:
        probs=np.array([ np.exp(-lamb*dt)*(lamb*dt)**cj/factorial(cj) for cj in range(0,max_jumps)])
# TODO: put the excess in the first bucket...
        probs=np.cumsum(probs)
        thresh=ndtri(probs)

        njumps=np.searchsorted(thresh,Zs[1,:,:])

        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*variance)*dt+np.sqrt(variance*dt)*Zs[0,cc,:]
            sim_asset+=gamm*njumps[cc,:]
            sim_asset+=omeg*np.sqrt(njumps[cc,:])*Zs[2,cc,:]

        sim_asset=np.exp(sim_asset)
        sim_variance =variance       

        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        lamb = self.workingpars[1]
        gamm = self.workingpars[2]
        omeg = self.workingpars[3]

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        vpath=self.upath

        ret['rep_mu']=mu

        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg

        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret
    
    def workingpars_update(self,workingpars):
        super().workingpars_update(workingpars)

        if( self.current==False):
# update all grid quantities to be cached:
#TODO: struct-ify?
            mu=self.workingpars[0] 
            lamb = self.workingpars[1]
            gamm = self.workingpars[2]
            omeg = self.workingpars[3]
    
            Nret=self.Nobs-1
    
            self.grid_lncondprob_mid = np.zeros((Nret,1))
    
            lncondprob_calc=lambda yasset,lncp: PureJump_lncondassetprob(yasset,self.dt,mu,lamb,gamm,omeg,lncp)
    
            lncondprob_calc(self.yasset,self.grid_lncondprob_mid)
            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        lamb = self.workingpars[1]
        gamm = self.workingpars[2]
        omeg = self.workingpars[3]

        lncondprob_mid = self.grid_lncondprob_mid
#        value = logsumexp(lncondprob_mid)/Nret
        value = np.sum(lncondprob_mid)/Nret

        if( np.isnan(value) == True ):
            print(value,mu)
            print(value)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,jumpintensity,jumpmean,jumpvolatility)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.zeros(Nret+1)

        return 
