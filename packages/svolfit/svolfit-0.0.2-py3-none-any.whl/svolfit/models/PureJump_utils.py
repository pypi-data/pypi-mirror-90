import numpy as np
from scipy.special import logsumexp as splse
from math import factorial

#-------------------------------------------------

def PureJump_lncondassetprob(y,dt,mu,jumpintensity,jumpmean,jumpvolatility,lncp):

    sigma=1.0e-12
# calc probabilities first to determine the number of terms needed:    
    lnprobtol=np.log(1.0e-16)
    Njump=21# can't do more than 21, the log(fact) overflows.
    j_lnprobs=np.zeros(Njump)
    j_lnprobs[0]=-jumpintensity*dt
    j_lnprobs[1:Njump]=np.array([-jumpintensity*dt+cj*np.log(jumpintensity*dt)-np.log(factorial(cj)) for cj in range(1,Njump)])
    Njump=np.maximum(1,np.argmax(j_lnprobs<=lnprobtol))
    j_lnprobs=j_lnprobs[0:Njump]
    j_lnprobs-=splse(j_lnprobs)

    coeff_dt=(mu-sigma*sigma/2.0)*dt
#    coeff_dt=mu*dt
    
    vol_tmp=sigma*np.sqrt(dt)
        
    Nobs=len(y)
    Ngrid=1

    j_nj = np.array(range(0,Njump))
    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,jumpvolatility*jumpvolatility*j_nj))
   
    j_yy_tmp=np.zeros((Nobs,Ngrid,Njump))
    j_yy_tmp[:,:,:]=np.tile(y,(Njump,Ngrid,1)).T
    j_yy_tmp[:,:,:]-=np.tile(np.tile(coeff_dt,(Nobs,1)).T,(Njump,1,1)).T
    j_yy_tmp[:,:,:]-=np.tile(jumpmean*j_nj,(Nobs,Ngrid,1))
    j_yy_tmp[:,:,:]/=np.tile(j_vol_tmp,(Nobs,1,1))
    
# log-probs    
    j_yy_tmp[:,:,:]=-0.5*j_yy_tmp*j_yy_tmp-np.log(np.tile(j_vol_tmp,(Nobs,1,1)))-0.5*np.log(2.0*np.pi)

# add jump log-probs
    j_yy_tmp[:,:,:]+=np.tile(j_lnprobs,(Nobs,Ngrid,1))

# logsumexp to result in log prob for condasset unconditional on jumps
    lncp[:,:] = splse(j_yy_tmp,axis=2)
        
    return 
    
