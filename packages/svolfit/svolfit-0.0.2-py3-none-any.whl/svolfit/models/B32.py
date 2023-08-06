import numpy as np

from svolfit.models.svol_model import svol_model
from svolfit.models.Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.model_utils import meanvariance

from svolfit.models.B32_utils import B32_lncondassetprob

#-------------------------------------

class B32_tree(svol_model):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        
        return

    def get_reportingpars(self):
        super().get_reportingpars()
        ret={}
        return ret

    def workingpars_update(self,workingpars):
        super().workingpars_update(workingpars)
        return

    def calculate(self):
        self.current=False
        return
    
    def variancepath(self):
        return 

#-------------------------------------

class B32_treeX2(svol_model):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        
        return

    def get_reportingpars(self):
        super().get_reportingpars()
        ret={}
        return ret

    def workingpars_update(self,workingpars):
        super().workingpars_update(workingpars)
        return

    def calculate(self):
        self.current=False
        return
    
    def variancepath(self):
        return 

#-------------------------------------

class B32_grid(Heston_grid):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)

# override/extend Heston defs
        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        jumpintensity = 0.0
        jumpmean = 0.0
        jumpvolatility = 0.0

        self.workingpars_names=['mu','sigma','rho','alpha','xi','jumpintensity','jumpmean','jumpvolatility']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,jumpintensity,jumpmean,jumpvolatility])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001, 0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]
        
        return

    def initpars_reporting(self,pardict):
# this alters self.working_pars, so make sure it's called after they are init'd
        return

    def get_structure(self):
        return '','',[],0
    
    def sim_step(self):
        return 

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        theta=sigma*sigma
        eta=xi*sigma
        q=2.0*alpha/(xi*xi)

        jumpintensity = self.workingpars[5]
        jumpmean = self.workingpars[6]
        jumpvolatility = self.workingpars[7]

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

# note 1/u:
        v0=sigma*sigma/u0
        vT=sigma*sigma/uT
    
        vpath=sigma*sigma/self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=theta
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta

        ret['rep_jumpintensity']=jumpintensity
        ret['rep_jumpmean']=jumpmean
        ret['rep_jumpvolatility']=jumpvolatility

        ret['misc_q']=q
#        ret['u0']=u0
#        ret['uT']=uT
        ret['rep_v0']=v0
        ret['rep_vT']=vT
        ret['ts_vpath']=vpath
        ret['ts_upath']=self.upath

        return ret

    def workingpars_update(self,workingpars):
        super().workingpars_update(workingpars)

        if( self.current==False):
        
    # switch consdasset prob calculation:
            mu=self.workingpars[0] 
            sigma=self.workingpars[1]
            rho=self.workingpars[2]
            alpha=self.workingpars[3] 
            xi=self.workingpars[4]

            jumpintensity = self.workingpars[5]
            jumpmean = self.workingpars[6]
            jumpvolatility = self.workingpars[7]

            lncondprob_calc=lambda yasset,u_prev,u_this,lncp: B32_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,jumpintensity,jumpmean,jumpvolatility,lncp)
        
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

        return


#-------------------------------------


    