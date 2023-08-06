import numpy as np

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.GBM_utils import GBM_lncondassetprob

#---------------------------------------------

class GBM_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)

        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)

        self.workingpars_names=['mu','sigma']
        self.workingpars=np.array([mu,sigma])
        self.workingpars_diffs=[0.0001,0.0001]

#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5)]

        if 'init' in options:
            self.initpars_reporting(options['init'])

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

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='sigma' ):
                sigma=pardict[x]

        self.workingpars[0]=mu
        self.workingpars[1]=sigma

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        corrmatrix=np.array([1.0])
        Nperstep=1

        sigma=self.workingpars[1]

        assetval=1.0
        varianceval=sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep

    def sim_step(self,asset,variance,Zs):

        mu=self.workingpars[0]
        sigma=self.workingpars[1]

        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       

        
        dt=self.dt/Nperstep
        for cs in range(0,Nperstep):
            sim_asset+=(mu-sigma*sigma/2.0)*dt+sigma*np.sqrt(dt)*Zs[0,cs,:]

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance


    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]

        theta=sigma*sigma

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_sigma']=sigma
        ret['misc_theta']=theta
#        ret['u0']=u0
#        ret['uT']=uT
        ret['misc_v0']=v0
        ret['misc_vT']=vT

        (GBM_mu,GBM_sigma)=meanvariance(np.array(self.series),self.dt)
        ret['misc_GBM_mu']=GBM_mu
        ret['misc_GBM_sigma']=GBM_sigma


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

            Nret=self.Nobs-1
    
            self.grid_lncondprob_mid = np.zeros((Nret,1))
    
            lncondprob_calc=lambda yasset,lncp: GBM_lncondassetprob(yasset,self.dt,mu,sigma,lncp)
    
            lncondprob_calc(self.yasset,self.grid_lncondprob_mid)
            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]

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

#        print(value,mu,sigma)
#        print(value)

        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        self.upath=np.ones(Nret+1)

        return 
