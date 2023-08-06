import numpy as np

from scipy.stats import ncx2

from svolfit.models.svol_model import svol_model
from svolfit.models.model_utils import meanvariance

from svolfit.models.HestonNandi_utils import Constraint_Feller,Constraint_Feller_grad

class HestonNandi_v(svol_model):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        mu=0.0
        sigma=0.1
        (mu,sigma)=meanvariance(np.array(self.series),dt)
        alpha=2.0
        xi=1.0
        u0=1.0

        self.eps=-1.0

#TODO: better if this weren't model-specific...
        for x in options:
            if( x=='init_mu' ):
                mu=options[x]
            if( x=='init_sigma' ):
                sigma=options[x]
            if( x=='init_rho' ):
                if( options[x] <= 0.0 ):
                    self.eps=-1.0
                else:
                    self.eps=1.0
            if( x=='init_alpha' ):
                alpha=options[x]
            if( x=='init_xi' ):
                xi=options[x]
            if( x=='init_u0' ):
                u0=options[x]

        self.workingpars_names=['mu','sigma','alpha','xi','u0']
        self.workingpars=np.array([mu,sigma,alpha,xi,u0])
        self.workingpars_diffs=[0.0001,0.0001,0.001,0.0001,0.0001]

        alpha_min=np.minimum(2.0/((self.Nobs-1)/252.0),1.0)
#                 [hmu, hsigma, rho, alpha, xi,u0]
        self.workingpars_bounds=[(-0.5,0.5), (0.05, 0.5), (alpha_min, 20.0), (0.1, 4.0),(0.1,3.0)]

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
        alpha=self.workingpars[2] 
        xi=self.workingpars[3]
        u0=self.workingpars[4]

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
        ret['rep_rho']=self.eps
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
            alpha=self.workingpars[2] 
            xi=self.workingpars[3]
            u0=self.workingpars[4]

            q=2.0*alpha/(xi*xi)
 
            eps = self.eps
            dt=self.dt

            if(alpha*dt<1.0e-8):
                self.c=2.0/(xi*xi*dt)
            else:
                self.c=-q/np.expm1(-alpha*dt)

# populate the u vector here, calculate probs elsewhere:
            coeff_dt=(mu-eps*alpha*sigma/xi)*dt        
            coeff_udt=(eps*alpha*sigma/xi-sigma*sigma/2.0)*dt        
            coeff_du=eps*sigma/xi
            coeff_du+=(eps*alpha*sigma/xi-sigma*sigma/2.0)*dt/2.0
            
            self.upath[0]=u0
            for cc in range(1,self.Nobs):
                self.upath[cc]=self.upath[cc-1]+(self.yasset[cc-1]-coeff_dt-coeff_udt*self.upath[cc-1])/coeff_du
            utol=1.0e-6
            self.upath=np.maximum(utol,self.upath)

        return

    def get_constraints(self):
        cons=[]

        con={}
        con['type']='ineq'
        con['fun']=lambda x: Constraint_Feller(x)
        con['jac']=lambda x: Constraint_Feller_grad(x)
       
        cons.append(con)
        
        return cons

    def calculate(self):

#        mu=self.workingpars[0] 
#        sigma=self.workingpars[1]
        alpha=self.workingpars[2] 
        xi=self.workingpars[3]
#        u0=self.workingpars[4]

        q=2.0*alpha/(xi*xi)

        Nret=self.Nobs-1
        
        dt=self.dt
        c=self.c
        Nret=self.Nobs-1
        
        lnprobs=np.zeros(Nret)
        
        lnprobs[:]=ncx2.logpdf(2.0*c*self.upath[1:Nret+1],2.0*q,2.0*c*np.exp(-alpha*dt)*self.upath[0:Nret])
        lnprobs[:]+=np.log(2.0*c)
        
        value=np.sum(lnprobs)/Nret

        self.objective_value = -value
        self.current=True
        self.numfunevals+=1

        return
    
    def variancepath(self):
        return 
    
    
    