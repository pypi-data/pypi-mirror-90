import numpy as np
from math import factorial
from scipy.special import ndtri
from scipy.stats import norm
from scipy.stats import t as tdist

from svolfit.models.svol_model import svol_model
from svolfit.models.Heston import Heston_tree,Heston_treeX2,Heston_grid

from svolfit.models.model_utils import meanvariance

from svolfit.models.Bates_utils import Bates_condassetprob_limit,Bates_condassetprob_limitX2,Bates_lncondassetprob

#-------------------------------------

class Bates_tree(Heston_tree):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):

# override/extend Heston defs
        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.lamb=0.4

        lamb = 10.0
        gamm = 0.0
        omeg = 0.01

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0','lambda','gamma','omega']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0,lamb,gamm,omeg])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001,0.0001, 0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.1,3.0),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]

        if 'init' in self.options:
            self.initpars_reporting(self.options['init'])

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        if(Nret>0):
            self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
            self.upath=np.zeros(self.Nobs)

#TODO: expose these as options at some point?
            self.ProbFactor =1.09
            self.NormProbCalc='TDist'
            
            if( self.NormProbCalc == 'Normal' ):
                sigma_base=np.std(self.yasset,ddof=1)
                mu_base=np.mean(self.yasset)
                self.cprob_base=norm.pdf( self.yasset, loc=mu_base, scale=sigma_base )
            elif( self.NormProbCalc == 'TDist' ):
                (t_df,t_loc,t_scale)=tdist.fit(self.yasset)
                self.cprob_base=tdist.pdf(self.yasset,df=t_df,loc=t_loc,scale=t_scale)
            else:
                print('Unknown NormProbCalc -- Handle')
        # allow for a multiplier:
            self.cprob_base*=self.ProbFactor

        return

    def initpars_reporting(self,pardict):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        gamm = self.workingpars[7]
        omeg = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
        v0=theta*u0

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
        u0=v0/theta
        
        self.workingpars[0]=mu
        self.workingpars[1]=sigma
        self.workingpars[2]=rho
        self.workingpars[3]=alpha
        self.workingpars[4]=xi
        self.workingpars[5]=u0
        self.workingpars[6]=lamb
        self.workingpars[7]=gamm
        self.workingpars[8]=omeg

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        u0=self.workingpars[5]

        corrmatrix=np.array([[1.0,rho,0.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
#        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
#        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        gamm = self.workingpars[7]
        omeg = self.workingpars[8]

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
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

# add jumps to asset
            sim_asset+=gamm*njumps[cc,:]
            sim_asset+=omeg*np.sqrt(njumps[cc,:])*Zs[3,cc,:]

        sim_asset=np.exp(sim_asset)
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
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        gamm = self.workingpars[7]
        omeg = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
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

    # switch consdasset prob calculation:
            mu=self.workingpars[0] 
            sigma=self.workingpars[1]
            rho=self.workingpars[2]
            alpha=self.workingpars[3] 
            xi=self.workingpars[4]
#            u0=self.workingpars[5]
            lamb = self.workingpars[6]
            gamm = self.workingpars[7]
            omeg = self.workingpars[8]
    
            dt=self.dt
            
            CondProbCalc='Limit'
            if( CondProbCalc=='Limit' ):
                coeff_dt=(mu-alpha*rho*sigma/xi)*dt
                coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
                coeff_du = rho*sigma/xi
                self.condprob_calc=lambda yasset,u_prev,u_this: Bates_condassetprob_limit(yasset,u_prev,u_this,dt,rho,sigma,coeff_dt,coeff_iu,coeff_du,lamb,gamm,omeg)
        
                pass
            else:
                print('Unknown Calc -- Handle')                

        return

#-------------------------------------

class Bates_treeX2(Heston_treeX2):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
# override/extend Heston defs
        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.lamb=0.4
        self.dt2 = self.dt/2.0

        lamb = 10.0
        gamm = 0.0
        omeg = 0.01

        self.workingpars_names=['mu','sigma','rho','alpha','xi','u0','lambda','gamma','omega']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,u0,lamb,gamm,omeg])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001,0.0001, 0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.1,3.0),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]
        
        if 'init' in self.options:
            self.initpars_reporting(self.options['init'])

# precalculate anything that can absolutely be reused:
#TODO: ugly!!
        Nret=self.Nobs-1
        if(Nret>0):
            self.yasset=np.log( self.series[1:Nret+1]/self.series[0:Nret] )
            self.upath=np.zeros(self.Nobs)

#TODO: expose these as options at some point?
            self.ProbFactor =1.09
            self.NormProbCalc='TDist'
            
            if( self.NormProbCalc == 'Normal' ):
                sigma_base=np.std(self.yasset,ddof=1)
                mu_base=np.mean(self.yasset)
                self.cprob_base=norm.pdf( self.yasset, loc=mu_base, scale=sigma_base )
            elif( self.NormProbCalc == 'TDist' ):
                (t_df,t_loc,t_scale)=tdist.fit(self.yasset)
                self.cprob_base=tdist.pdf(self.yasset,df=t_df,loc=t_loc,scale=t_scale)
            else:
                print('Unknown NormProbCalc -- Handle')
        # allow for a multiplier:
            self.cprob_base*=self.ProbFactor

        return

    def initpars_reporting(self,pardict):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        gamm = self.workingpars[7]
        omeg = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
        v0=theta*u0

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
        u0=v0/theta
        
        self.workingpars[0]=mu
        self.workingpars[1]=sigma
        self.workingpars[2]=rho
        self.workingpars[3]=alpha
        self.workingpars[4]=xi
        self.workingpars[5]=u0
        self.workingpars[6]=lamb
        self.workingpars[7]=gamm
        self.workingpars[8]=omeg

        return

    def get_structure(self):
        assetname='asset'
        variancename='variance'

        sigma=self.workingpars[1]
        rho=self.workingpars[2]
        u0=self.workingpars[5]

        corrmatrix=np.array([[1.0,rho,0.0,0.0],[rho,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])
#TODO: best choice based on pars?
        Nperstep=4

        assetval=1.0
        varianceval=u0*sigma*sigma

        return assetname,assetval,variancename,varianceval,corrmatrix,Nperstep
    
    def sim_step(self,asset,variance,Zs):
        mu=self.workingpars[0] 
        sigma=self.workingpars[1]
#        rho=self.workingpars[2]
        alpha=self.workingpars[3] 
        xi=self.workingpars[4]
#        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        gamm = self.workingpars[7]
        omeg = self.workingpars[8]

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
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

# add jumps to asset
            sim_asset+=gamm*njumps[cc,:]
            sim_asset+=omeg*np.sqrt(njumps[cc,:])*Zs[3,cc,:]

        sim_asset=np.exp(sim_asset)
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
        u0=self.workingpars[5]
        lamb = self.workingpars[6]
        gamm = self.workingpars[7]
        omeg = self.workingpars[8]

        theta=sigma*sigma
        eta=xi*sigma
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

    # switch consdasset prob calculation:
            mu=self.workingpars[0] 
            sigma=self.workingpars[1]
            rho=self.workingpars[2]
            alpha=self.workingpars[3] 
            xi=self.workingpars[4]
            u0=self.workingpars[5]
            lamb = self.workingpars[6]
            gamm = self.workingpars[7]
            omeg = self.workingpars[8]
       
            dt2=self.dt2
            
            CondProbCalc='Limit'
            if( CondProbCalc=='Limit' ):
                coeff_dt=(mu-alpha*rho*sigma/xi)*dt2
                coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
                coeff_du = rho*sigma/xi
                self.condprob_calc=lambda yasset,u_prev,u_mid,u_this: Bates_condassetprob_limitX2(yasset,u_prev,u_mid,u_this,dt2,rho,sigma,coeff_dt,coeff_iu,coeff_du,lamb,gamm,omeg)
        
                pass
            else:
                print('Unknown Calc -- Handle')                

        return

#-------------------------------------

class Bates_grid(Heston_grid):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
# override/extend Heston defs
        mu=0.0
        sigma=0.1
        if( len(self.series)>1 ):
            (mu,sigma)=meanvariance(np.array(self.series),self.dt)
        rho=0.0
        alpha=2.0
        xi=1.0
        u0=1

        self.lamb=0.4

        lamb = 10.0
        gamm = 0.0
        omeg = 0.01

        self.workingpars_names=['mu','sigma','rho','alpha','xi','lambda','gamma','omega']
        self.workingpars=np.array([mu,sigma,rho,alpha,xi,lamb,gamm,omeg])
        self.workingpars_diffs=[0.0001,0.0001,0.0005,0.001,0.0001,0.0001,0.0001, 0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (-0.9,0.9), (alpha_min, 20.0), (0.1, 3.5),(0.0,100.0),(-0.1,0.1),(0.002,0.1)]
        
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
        Nperstep=4

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
            sim_variance=np.power(np.sqrt(sim_variance)+0.5*eta*np.sqrt(dt)*Zs[1,cc,:],2)+alpha*(theta-sim_variance)*dt-eta*eta*dt/4.0
            sim_variance=np.maximum(sim_variance,vmin)

# add jumps to asset
            sim_asset+=gamm*njumps[cc,:]
            sim_asset+=omeg*np.sqrt(njumps[cc,:])*Zs[3,cc,:]

        sim_asset=np.exp(sim_asset)
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
        lamb = self.workingpars[5]
        gamm = self.workingpars[6]
        omeg = self.workingpars[7]

        theta=sigma*sigma
        eta=xi*sigma
        q=2.0*alpha/(xi*xi)

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
        
    # switch consdasset prob calculation:
            mu=self.workingpars[0] 
            sigma=self.workingpars[1]
            rho=self.workingpars[2]
            alpha=self.workingpars[3] 
            xi=self.workingpars[4]
            lamb = self.workingpars[5]
            gamm = self.workingpars[6]
            omeg = self.workingpars[7]
     
            lncondprob_calc=lambda yasset,u_prev,u_this,lncp: Bates_lncondassetprob(yasset,u_prev,u_this,self.dt,rho,sigma,mu,alpha,xi,lamb,gamm,omeg,lncp)
        
# calculated in super, so done 2x?      
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map+1],self.grid_lncondprob_up)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map],self.grid_lncondprob_mid)
            lncondprob_calc(self.yasset,self.grid_u_grid,self.grid_u_grid[self.grid_i_map-1],self.grid_lncondprob_dn)
    

        return


#-------------------------------------


    
