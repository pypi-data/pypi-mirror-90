import numpy as np

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

        mu=0.0
        (mu,sigma)=meanvariance(np.array(self.series),dt)

        jumpintensity = 10.0
        jumpmean = 0.0
        jumpvolatility = 0.02

        self.workingpars_names=['mu','jumpintensity','jumpmean','jumpvolatility']
        self.workingpars=np.array([mu,jumpintensity,jumpmean,jumpvolatility])
        self.workingpars_diffs=[0.0001,0.0001,0.0001, 0.0001]

#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5),(0.0,1000.0),(-0.1,0.1),(0.002,0.1)]

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
        self.upath=np.zeros(self.Nobs)

        return

    def initpars_reporting(self,pardict):
# this alters self.working_pars, so make sure it's called after they are init'd
        return

    def get_structure(self):
        return '','',[],0
    
    def sim_step(self):
        return 

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 

        jumpintensity = self.workingpars[1]
        jumpmean = self.workingpars[2]
        jumpvolatility = self.workingpars[3]

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=u0
        vT=uT
    
        vpath=self.upath

        ret['rep_mu']=mu
#        ret['u0']=u0
#        ret['uT']=uT
        ret['misc_v0']=v0
        ret['misc_vT']=vT

        ret['rep_jumpintensity']=jumpintensity
        ret['rep_jumpmean']=jumpmean
        ret['rep_jumpvolatility']=jumpvolatility

        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret
    
    def workingpars_update(self,workingpars):
        super().workingpars_update(workingpars)

        if( self.current==False):
# update all grid quantities to be cached:
#TODO: struct-ify?
            mu=self.workingpars[0] 

            jumpintensity = self.workingpars[1]
            jumpmean = self.workingpars[2]
            jumpvolatility = self.workingpars[3]
    
            Nret=self.Nobs-1
    
            self.grid_lncondprob_mid = np.zeros((Nret,1))
    
            lncondprob_calc=lambda yasset,lncp: PureJump_lncondassetprob(yasset,self.dt,mu,jumpintensity,jumpmean,jumpvolatility,lncp)
    
            lncondprob_calc(self.yasset,self.grid_lncondprob_mid)
            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
    
        jumpintensity = self.workingpars[1]
        jumpmean = self.workingpars[2]
        jumpvolatility = self.workingpars[3]

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

        self.upath=np.ones(Nret+1)

        return 
