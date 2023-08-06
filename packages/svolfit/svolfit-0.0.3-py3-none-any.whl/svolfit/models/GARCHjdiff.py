import numpy as np
from math import factorial
from scipy.special import ndtri

from svolfit.models.svol_model import svol_model
from svolfit.models.GARCHdiff import GARCHdiff_tree,GARCHdiff_treeX2,GARCHdiff_grid

from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.GARCHdiff_utils import GARCHdiff_griddefs
from svolfit.models.GARCHjdiff_utils import GARCHjdiff_lncondassetprob
from svolfit.models.Heston_utils import Heston_pathprob

#-------------------------------------

class GARCHjdiff_tree(GARCHdiff_tree):
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


#-------------------------------------

class GARCHjdiff_treeX2(GARCHdiff_treeX2):
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


#-------------------------------------

class GARCHjdiff_grid(GARCHdiff_grid):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0

        lamb = 10.0
        gamm = 0.1
        omeg = 0.2

        self.lamb=0.5

        self.workingpars_names=['mu','sigma','rho','alpha','xi','lambda','gamma','omega']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,lamb,gamm,omeg])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001, 0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 4.0),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]

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
        lamb = self.workingpars[5]
        gamm = self.workingpars[6]
        omeg = self.workingpars[7]

        theta=sigma*sigma
        eta=xi*sigma

        for x in pardict:
            if( x=='mu' ):
                mu=pardict[x]
            if( x=='theta' ):
                theta=pardict[x]
            if( x=='rho' ):
                rho=pardict[x]
            if( x=='alpha' ):
                alpha=pardict[x]
            if( x=='eta' ):
                eta=pardict[x]
# this sucks: the model needs a v0, but the optimiation doesn't...
            if( x=='v0' ):
                v0=pardict[x]
            if( x=='lambda' ):
                lamb=pardict[x]
            if( x=='gamma' ):
                gamm=pardict[x]
            if( x=='omega' ):
                omeg=pardict[x]

        sigma=np.sqrt(theta)
        xi=eta/sigma

        self.workingpars[0]=mu
        self.workingpars[1]=sigma
        self.workingpars[2]=rho
        self.workingpars[3]=alpha
        self.workingpars[4]=xi
        self.workingpars[5]=lamb
        self.workingpars[6]=gamm
        self.workingpars[7]=omeg
        self.frozen_u0=v0/theta
        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars[1]
        rho=self.workingpars[2]

        corrmatrix=np.array([[1.0,rho,0.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=16

        assetval=1.0
        varianceval=self.frozen_u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
#        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        lamb = self.workingpars[5]
        gamm = self.workingpars[6]
        omeg = self.workingpars[7]

        theta=sigma*sigma
        eta=xi*sigma
        
        Nperstep=np.shape(Zs)[1]
        sim_asset=np.log(asset)
        sim_variance =variance       
        
        dt=self.dt/Nperstep
        vmin=1.0e-12

# Zs[0,:,:]: diffusion driver
# Zs[1,:,:]: variance driver
# Zs[2,:,:]: jump indicator
# Zs[3,:,:]: jump size
        
        max_jumps=21        
        njumps=np.zeros(Nperstep,int)
# all sub-timesteps are the same:
        probs=np.array([ np.exp(-lamb*dt)*(lamb*dt)**cj/factorial(cj) for cj in range(0,max_jumps)])
# TODO: put the excess in the first bucket...
        probs=np.cumsum(probs)
        thresh=ndtri(probs)

        njumps=np.searchsorted(thresh,Zs[2,:,:])

        for cc in range(0,Nperstep):
            sim_asset+=(mu-0.5*sim_variance)*dt+np.sqrt(sim_variance*dt)*Zs[0,cc,:]
#            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
# euler only
            sim_variance+=alpha*(theta-sim_variance)*dt+eta*sim_variance*np.sqrt(dt)*Zs[1,cc,:]
            sim_variance=np.maximum(sim_variance,vmin)

# add jumps to asset
            sim_asset+=gamm*njumps[cc,:]
            sim_asset+=omeg*np.sqrt(njumps[cc,:])*Zs[3,cc,:]

        sim_asset=np.exp(sim_asset)
        return sim_asset,sim_variance

    def get_reportingpars(self):
        super().get_reportingpars()

        ret={}
        
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        theta=sigma*sigma
# here eta=xi
        eta=xi

        q=2.0*alpha/(xi*xi)

        lamb = self.workingpars[5]
        gamm = self.workingpars[6]
        omeg = self.workingpars[7]

# already called in super?
        self.variancepath()
        
        u0=self.upath[0]
        uT=self.upath[self.Nobs-1]

        v0=sigma*sigma*u0
        vT=sigma*sigma*uT
    
        vpath=sigma*sigma*self.upath

        ret['rep_mu']=mu
        ret['rep_theta']=theta
        ret['rep_rho']=rho
        ret['rep_alpha']=alpha
        ret['rep_eta']=eta

        ret['rep_lambda']=lamb
        ret['rep_gamma']=gamm
        ret['rep_omega']=omeg

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
# update all grid quantities to be cached:
#TODO: struct-ify?
            mu=self.workingpars[0] 
            sigma=self.workingpars[1]
            rho=self.workingpars[2]
            alpha=self.workingpars[3] 
            xi=self.workingpars[4]
            lamb = self.workingpars[5]
            gamm = self.workingpars[6]
            omeg = self.workingpars[7]
    
            lncondprob_calc=lambda yasset,u_prev,u_this,lncp: GARCHjdiff_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp)

# calculated in super, so done 2x?      
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)
            
        return


