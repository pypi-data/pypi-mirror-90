import numpy as np
from math import factorial
from scipy.special import ndtri

from scipy.stats import norm
from scipy.stats import t as tdist
from scipy.special import gammaln

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.MertonJD_utils import MertonJD_lncondassetprob

#---------------------------------------------

class MertonJD_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
        mu=0.0
        sigma=0.1
        if( len(self.series)> 1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)

        lamb = 20.0
        gamm = 0.0
        omeg = 0.02

        self.workingpars_names=['mu','sigma','lambda','gamma','omega']
        self.workingpars=np.array([mu,sigma,lamb,gamm,omeg])
        self.workingpars_diffs=[0.0001,0.0001,0.01,0.001, 0.001]

        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]

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
        sigma=self.workingpars[1]
        lamb=self.workingpars[2]
        gamm=self.workingpars[3] 
        omeg=self.workingpars[4]
        
        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='sigma' ):
                sigma=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        self.workingpars[0]=mu
        self.workingpars[1]=sigma
        self.workingpars[2]=lamb
        self.workingpars[3]=gamm
        self.workingpars[4]=omeg

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars[1]

        corrmatrix=np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars[0] 
#        sigma=self.workingpars[1]
        lamb=self.workingpars[2]
        gamm=self.workingpars[3] 
        omeg=self.workingpars[4]
        
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
        sigma=self.workingpars[1]
        lamb = self.workingpars[2]
        gamm = self.workingpars[3]
        omeg = self.workingpars[4]

        theta=sigma*sigma

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_sigma']=sigma
#        ret['u0']=u0
#        ret['uT']=uT
        ret['misc_theta']=theta
        ret['misc_v0']=v0
        ret['misc_vT']=vT

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
            sigma=self.workingpars[1]
            lamb = self.workingpars[2]
            gamm = self.workingpars[3]
            omeg = self.workingpars[4]
    
            Nret=self.Nobs-1
    
            self.grid_lncondprob_mid = np.zeros((Nret,1))
    
            lncondprob_calc=lambda yasset,lncp: MertonJD_lncondassetprob(yasset,self.dt,mu,sigma,lamb,gamm,omeg,lncp)
    
            lncondprob_calc(self.yasset,self.grid_lncondprob_mid)
            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        lamb = self.workingpars[2]
        gamm = self.workingpars[3]
        omeg = self.workingpars[4]

        lncondprob_mid = self.grid_lncondprob_mid
#        value = logsumexp(lncondprob_mid)/Nret
        value = np.sum(lncondprob_mid)/Nret

        if( np.isnan(value) == True ):
            print(value,mu,sigma)
            print(value)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

#        print(value,mu,sigma,lamb,gamm,omeg)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.ones(Nret+1)

        return 
