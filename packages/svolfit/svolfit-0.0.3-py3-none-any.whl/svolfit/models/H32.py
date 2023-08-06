import numpy as np

from svolfit.models.svol_model import svol_model
from svolfit.models.Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.model_utils import meanvariance

from svolfit.models.H32_utils import H32_lncondassetprob

#-------------------------------------

class H32_tree(svol_model):
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

class H32_treeX2(svol_model):
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

class H32_grid(Heston_grid):
    def __init__(self, series,dt, model, method,options):
# need this to call the super/super... 
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

# override/extend Heston defs
        mu=0.0
        sigma=0.1
        if( len(self.series) > 1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.lamb=0.4

        self.workingpars_names=['mu','sigma','rho','alpha','xi']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5)]

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
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        theta=1.0/(sigma*sigma)
        eta=xi/sigma
        t_alpha=(alpha-xi*xi)/(sigma*sigma)
        t_theta=alpha/t_alpha

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                t_theta=pardict[x]
            if( x=='rho' ):
                rho=pardict[x]
            if( x=='alpha' ):
                t_alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
# this sucks: the model needs a v0, but the optimiation doesn't...
            if( x=='v0' ):
                v0=pardict[x]

        alpha=t_alpha*t_theta
        theta=(t_alpha+eta*eta)/alpha
        sigma=1.0/np.sqrt(theta)
        xi=eta*sigma

        self.workingpars[0]=mu
        self.workingpars[1]=sigma
        self.workingpars[2]=rho
        self.workingpars[3]=alpha
        self.workingpars[4]=xi
        self.frozen_u0=v0/theta

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars[1]
        rho=self.workingpars[2]

        corrmatrix=np.array([[1.0,rho],[rho,1.0]])
#TODO: best choice based on pars?
        Nperstep=8

        assetval=1.0
        varianceval=self.frozen_u0/(sigma*sigma)

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        theta=1.0/(sigma*sigma)
        eta=xi/sigma
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =1.0/variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12
        
        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5/sim_variance)*dt+np.sqrt(dt/sim_variance)*Zs[0,cc,:]
            sim_variance=np.power(np.sqrt(sim_variance)-0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

        sim_asset=np.exp(sim_asset)
        sim_variance=1.0/sim_variance
        return sim_asset,sim_variance

    def get_reportingpars(self):
# need to call this to get the super/super call happening...
        super().get_reportingpars()

        ret={}

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        theta=1.0/(sigma*sigma)
        eta=xi/sigma
        q=2.0*alpha/(xi*xi)
        t_alpha=(alpha-xi*xi)/(sigma*sigma)
        t_theta=alpha/t_alpha

        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

# note 1/u:
        v0=sigma*sigma/u0
        vT=sigma*sigma/uT
    
        vpath=sigma*sigma/self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=t_theta
        ret['rep_rho']=rho
        ret['rep_alpha']=t_alpha
        ret['rep_eta']=eta

        ret['misc_q']=q
        ret['misc_theta']=theta
        ret['misc_eta']=eta
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
    
            lncondprob_calc=lambda yasset,u_prev,u_this,lncp: H32_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
        
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)

        return


#-------------------------------------


    
