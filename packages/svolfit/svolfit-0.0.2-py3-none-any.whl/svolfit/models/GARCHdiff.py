import numpy as np

from svolfit.models.svol_model import svol_model
#from Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.model_utils import meanvariance,logsumexp

from svolfit.models.GARCHdiff_utils import GARCHdiff_lncondassetprob,GARCHdiff_griddefs
from svolfit.models.Heston_utils import Heston_pathprob

#-------------------------------------

class GARCHdiff_tree(svol_model):
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

class GARCHdiff_treeX2(svol_model):
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

class GARCHdiff_grid(svol_model):
    def __init__( self, series,dt, model, method,options ):
        super().__init__(series,dt, model, method,options)

        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)
        rho=0.0
        alpha=2.0
        xi=1.0

        self.lamb=0.5

        self.workingpars_names=['mu','sigma','rho','alpha','xi']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 4.0)]

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
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        theta=sigma*sigma
# here eta=xi
        eta=xi

        q=2.0*alpha/(xi*xi)

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
    
            tmp=GARCHdiff_griddefs(self.dt,alpha,xi,self.lamb)
            self.grid_i_lower=tmp[0]
            self.grid_i_upper=tmp[1]
            self.grid_i_map=tmp[2]
            self.grid_u_grid=tmp[3]
            self.grid_lnp_init=tmp[4]
            self.grid_pi3=tmp[5]
    
            self.grid_i_length=self.grid_i_upper-self.grid_i_lower + 1
    
            self.grid_lnp_prev = np.zeros(self.grid_i_length)
            self.grid_lnp_this = np.zeros(self.grid_i_length)
    
            Nret=self.Nobs-1
    
            self.grid_lncondprob_dn = np.zeros((Nret,self.grid_i_length))
            self.grid_lncondprob_mid = np.zeros((Nret,self.grid_i_length))
            self.grid_lncondprob_up = np.zeros((Nret,self.grid_i_length))
    
            self.grid_tmp_dn = np.zeros(self.grid_i_length)
            self.grid_tmp_mid = np.zeros(self.grid_i_length)
            self.grid_tmp_up = np.zeros(self.grid_i_length)
    
            lncondprob_calc=lambda yasset,u_prev,u_this,lncp: GARCHdiff_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lncp)
    
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)
            
        return


    def calculate(self):
   
        Nret=self.Nobs-1
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]

        lnp_init=self.grid_lnp_init
        pi3=self.grid_pi3

        lnp_prev = self.grid_lnp_prev
        lnp_this = self.grid_lnp_this

        pi_up=pi3[2,:]
        pi_mid=pi3[1,:]
        pi_dn=pi3[0,:]
    
        lncondprob_dn = self.grid_lncondprob_dn
        lncondprob_mid = self.grid_lncondprob_mid
        lncondprob_up = self.grid_lncondprob_up
    
        tmp_dn = self.grid_tmp_dn
        tmp_mid = self.grid_tmp_mid
        tmp_up = self.grid_tmp_up

        lnp_prev[:]=lnp_init.copy()
        Heston_pathprob(lnp_prev,lnp_this,lncondprob_dn,lncondprob_mid,lncondprob_up,pi_dn,pi_mid,pi_up,tmp_dn,tmp_mid,tmp_up)
        value = logsumexp(lnp_this)/Nret

#        print(value,value2)
#        print(mu,sigma,rho,alpha,xi)

    #    print(value)
        if( np.isnan(value) == True ):
            print(value,mu,sigma,rho,alpha,xi)
            print(value)
            value=np.inf
    
        self.objective_value = -value
        self.current=True
        self.numfunevals+=1
    
        return
        
    def variancepath(self):
        Nret=self.Nobs-1

        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
    
#        i_lower=self.grid_i_lower
#        i_upper=self.grid_i_upper
        i_length=self.grid_i_length
        i_map=self.grid_i_map
        u_grid=self.grid_u_grid
        lnp_init=self.grid_lnp_init
        pi3=self.grid_pi3

        lnp_prev = self.grid_lnp_prev
        lnp_this = self.grid_lnp_this

        pi_up=pi3[2,:]
        pi_mid=pi3[1,:]
        pi_dn=pi3[0,:]
    
        lncondprob_dn = self.grid_lncondprob_dn
        lncondprob_mid = self.grid_lncondprob_mid
        lncondprob_up = self.grid_lncondprob_up
    
        tmp_dn = self.grid_tmp_dn
        tmp_mid = self.grid_tmp_mid
        tmp_up = self.grid_tmp_up

        vplist=[]
        vilist=[]

        lnp_prev[:]=lnp_init.copy()

        for cc in range(0,Nret):
   
            tmp_up[:]=lncondprob_up[cc,:]+lnp_prev
            tmp_mid[:]=lncondprob_mid[cc,:]+lnp_prev
            tmp_dn[:]=lncondprob_dn[cc,:]+lnp_prev
    
            lnp_this[:] = np.zeros(i_length)
    
            lnp_this[3:i_length-3]=logsumexp( [tmp_up[2:i_length-4],tmp_mid[3:i_length-3],tmp_dn[4:i_length-2]] ,b=[pi_up[2:i_length-4],pi_mid[3:i_length-3],pi_dn[4:i_length-2]], axis=0 )
    
            lnp_this[0]=logsumexp( [tmp_dn[0],tmp_dn[1]] ,b=[pi_dn[0],pi_dn[1]], axis=0 )
            lnp_this[i_length-1]=logsumexp( [tmp_up[i_length-1],tmp_up[i_length-2]] ,b=[pi_up[i_length-1],pi_up[i_length-2]], axis=0 )
    
            lnp_this[1]=logsumexp( [tmp_mid[0],tmp_mid[1],tmp_dn[2]] ,b=[pi_mid[0],pi_mid[1],pi_dn[2]], axis=0 )
            lnp_this[i_length-2]=logsumexp( [tmp_mid[i_length-1],tmp_mid[i_length-2],tmp_up[i_length-3]] ,b=[pi_mid[i_length-1],pi_mid[i_length-2],pi_up[i_length-3]], axis=0 )
    
            lnp_this[2]=logsumexp( [tmp_up[0],tmp_up[1],tmp_mid[2],tmp_dn[3]] ,b=[pi_up[0],pi_up[1],pi_mid[2],pi_dn[3]], axis=0 )
            lnp_this[i_length-3]=logsumexp( [tmp_dn[i_length-1],tmp_dn[i_length-2],tmp_mid[i_length-3],tmp_up[i_length-4]] ,b=[pi_dn[i_length-1],pi_dn[i_length-2],pi_mid[i_length-3],pi_up[i_length-4]], axis=0 )
    
    #        print( lnp_this )        
    
            lnp_prev[:]=lnp_this
    
            vp=-np.inf*np.ones(i_length)
            vi=-np.ones(i_length,dtype=int)

            for c2 in range(0,i_length):
                if(tmp_mid[c2]+np.log(pi_mid[c2])>=vp[i_map[c2]]):
                    vp[i_map[c2]]=tmp_mid[c2]+np.log(pi_mid[c2])
                    vi[i_map[c2]]=c2
                if(tmp_dn[c2]+np.log(pi_dn[c2])>=vp[i_map[c2]-1]):
                    vp[i_map[c2]-1]=tmp_dn[c2]+np.log(pi_dn[c2])
                    vi[i_map[c2]-1]=c2
                if(tmp_up[c2]+np.log(pi_up[c2])>=vp[i_map[c2]+1]):
                    vp[i_map[c2]+1]=tmp_up[c2]+np.log(pi_up[c2])
                    vi[i_map[c2]+1]=c2
            vplist.append(vp)
            vilist.append(vi)
            
#        value = logsumexp(lnp_this)/Nret
#        print(value,self.objective_value)
        
#        print(mu,sigma,rho,alpha,xi)

    #    print(value)
#        if( np.isnan(value) == True ):
#            print(value,mu,sigma,rho,alpha,xi)
#            print(value)
#            value=np.inf

# prediction of the variance at end of path:    
        upath=np.zeros(Nret+1)
        entry_current=np.argmax(lnp_this)
        uT=u_grid[entry_current]
        upath[Nret]=uT
        for cpath in range (Nret-1,-1,-1):        
#            print(cpath)
            entry_current=vilist[cpath][entry_current]
            upath[cpath]=u_grid[entry_current]
#        print(uT)
    
# include in numfunevals even though this one will be a lot slower.
        self.numfunevals+=1
# don't change current -- it should be before here, and if this 
# fails then the grid should still be current.

        self.upath=upath

        return 
    