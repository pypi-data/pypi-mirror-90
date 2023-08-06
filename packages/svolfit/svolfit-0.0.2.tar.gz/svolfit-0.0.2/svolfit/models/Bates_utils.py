import numpy as np

from scipy.special import logsumexp as splse
from math import factorial

def Bates_condassetprob_limit(y,u_prev,u_this,dt,rho,sigma,coeff_dt,coeff_iu,coeff_du,jumpintensity,jumpmean,jumpvolatility):

    probtol=1.0e-10
    
    du_tmp=u_this-u_prev
# assume average: doesn't seem to make a lot of difference
#    iu_tmp=(u_this+u_prev)*dt/2.0
    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))*dt/3.0
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)

#    yy_tmp=( y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
#    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))

    NumberTerms=11
    j_probs=np.array([ np.exp(-jumpintensity*dt)*np.power(jumpintensity*dt,cj)/factorial(cj) for cj in range(0,NumberTerms)])

    NumberTerms=np.argmax(j_probs<=probtol)
    j_probs=j_probs[0:NumberTerms]
    j_probs[NumberTerms-1]=1.0-np.sum(j_probs[0:NumberTerms-1])

    j_nj = np.array(range(0,NumberTerms))

    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,jumpvolatility*jumpvolatility*j_nj))
    j_yy_tmp=( np.subtract.outer(y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp,jumpmean*j_nj) )/j_vol_tmp
    
    j_condprob=np.exp(-0.5*j_yy_tmp*j_yy_tmp)/(j_vol_tmp*np.sqrt(2.0*np.pi))
    
    condprob=j_probs@j_condprob.T
    
    return condprob

def condprob_calc_exact(y,u_prev,u_this,dt,alpha,rho,sigma,xi,q,MI_f1,MI_f2,MI_f3,coeff_dt,coeff_iu,coeff_du):

    epsilon=alpha*dt/2.0    

    du_tmp=u_this-u_prev
    iu_tmp=MI_Calc(alpha,sigma,xi,q,dt,epsilon,MI_f1,MI_f2,MI_f3,u_prev,u_this)
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
    if( np.min(vol_tmp)<= 0.0 ):
        print(2,vol_tmp)
    yy_tmp=(y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp)/vol_tmp
    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))
    
    return condprob

def MI_Calc(alpha,sigma,xi,q,dt,epsilon,MI_f1,MI_f2,MI_f3,v1,v2):

    z_tol=1.0e-2

    iu_tmp=MI_f1*(v2+v1)*dt/3.0
    iu_tmp+=MI_f2*sigma*sigma*dt*epsilon/3.0

# the floor doesn't matter since the contribution is zeroed below
    epsoZ0=xi*xi*dt/(4.0*np.maximum( 1.0e-16, np.sqrt(v2*v1) ) )

#looks like this is robust enough that it will be very close to 1 or nan in the limit
    shoe = 1.0+epsilon*epsilon/6.0+epsilon*epsilon*epsilon*epsilon/120.0
    if( epsilon > 1.0e-4 ):
        shoe = np.sinh(epsilon)/epsilon
    z=epsoZ0/shoe
    MI_Rat=ive(q,z)/ive(q-1,z)
    np.nan_to_num(MI_Rat,nan=1.0,copy=False)

#     MI_Rat=1.0-epsoZ0*(2.0*q-1.0)/2.0+epsoZ0*epsoZ0*(2.0*q-1.0)*(2.0*q+1.0)/8.0

# # can have epsilon small when epsoZ0 is not -- currently not handled well... 
#     shoe = 1.0+epsilon*epsilon/6.0+epsilon*epsilon*epsilon*epsilon/120.0
#     if( epsilon > 1.0e-4 ):
#         shoe = np.sinh(epsilon)/epsilon
# #    z=2.0*alpha*np.sqrt(v2*v1)/(xi*xi)/np.sinh(epsilon)
#     z=epsoZ0/shoe
    
#     maskcond = np.logical_and( epsoZ0>z_tol, v1*v2>0.0 )
#     MI_Rat[maskcond]=ive(q,z[maskcond])/ive(q-1,z[maskcond])

    # if( len ( ive(q-1,z[maskcond]) ) > 0 ):
    #     if( np.min( ive(q-1,z[maskcond]) ) < 1.0e-12 ):
    #         print('ive')
    #         print(ive(q-1,z[maskcond]))    

    iu_tmp+=MI_f3*(np.sqrt(v2*v1)*dt/3.0)*MI_Rat

    return iu_tmp

#---------------------------------------------

def Bates_condassetprob_limitX2(y,u_prev,u_mid,u_this,dt,rho,sigma,coeff_dt,coeff_iu,coeff_du,jumpintensity,jumpmean,jumpvolatility):

    probtol=1.0e-10

    du_tmp=u_this-u_prev
    iu_tmp=(u_this+u_mid+np.sqrt(u_this*u_mid))*dt/3.0
    iu_tmp+=(u_mid+u_prev+np.sqrt(u_mid*u_prev))*dt/3.0

    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)

#    yy_tmp=( y-2.0*coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
#    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))

#    du_tmp=u_this-u_prev
## assume average: doesn't seem to make a lot of difference
##    iu_tmp=(u_this+u_prev)*dt/2.0
#    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))*dt/3.0
#    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)
#    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
#    if( RunTests==True ):
#        if( np.min(vol_tmp)<= 0.0 ):
#            print(2,vol_tmp)
##    yy_tmp=( y-coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp )/vol_tmp
##    condprob=np.exp(-0.5*yy_tmp*yy_tmp)/(vol_tmp*np.sqrt(2.0*np.pi))

    NumberTerms=11
    j_probs=np.array([ np.exp(-jumpintensity*dt)*np.power(jumpintensity*dt,cj)/factorial(cj) for cj in range(0,NumberTerms)])

    NumberTerms=np.argmax(j_probs<=probtol)
    j_probs=j_probs[0:NumberTerms]
    j_probs[NumberTerms-1]=1.0-np.sum(j_probs[0:NumberTerms-1])

    j_nj = np.array(range(0,NumberTerms))

    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,jumpvolatility*jumpvolatility*j_nj))
    j_yy_tmp=( np.subtract.outer(y-2.0*coeff_dt-coeff_iu*iu_tmp-coeff_du*du_tmp,jumpmean*j_nj) )/j_vol_tmp
    
    j_condprob=np.exp(-0.5*j_yy_tmp*j_yy_tmp)/(j_vol_tmp*np.sqrt(2.0*np.pi))
    
    condprob=j_probs@j_condprob.T
    
    return condprob

#---------------------------------------------

def Bates_lncondassetprob(y,u_prev,u_this,dt,rho,sigma,mu,alpha,xi,jumpintensity,jumpmean,jumpvolatility,lncp):

# calc probabilities first to determine the number of terms needed:    
    lnprobtol=np.log(1.0e-10)
    Njump=11
    j_lnprobs=np.zeros(Njump)
    j_lnprobs[0]=-jumpintensity*dt
    j_lnprobs[1:Njump]=np.array([-jumpintensity*dt+cj*np.log(jumpintensity*dt)-np.log(factorial(cj)) for cj in range(1,Njump)])
    Njump=np.argmax(j_lnprobs<=lnprobtol)
    j_lnprobs=j_lnprobs[0:Njump]
    j_lnprobs-=splse(j_lnprobs)

#--
    coeff_dt=(mu-alpha*rho*sigma/xi)*dt
    coeff_iu = rho*alpha*sigma/xi -sigma*sigma/2.0
    coeff_du = rho*sigma/xi
    
    du_tmp=u_this-u_prev
# assume average: doesn't seem to make a lot of difference
#    iu_tmp=(u_this+u_prev)*dt/2.0
    iu_tmp=(u_this+u_prev+np.sqrt(u_this*u_prev))*dt/3.0
    vol_tmp=np.sqrt(1.0-rho*rho)*sigma*np.sqrt(iu_tmp)

# checking all entries is slow!
#    vol_tmp[vol_tmp<1.0e-12]=1.0e-12
    if( vol_tmp[0]<1.0e-12 ):
#        print(vol_tmp[vol_tmp<1.0e-12])
        vol_tmp[0]=1.0e-12
    
    Nobs=len(y)
    Ngrid=len(u_this)

    j_nj = np.array(range(0,Njump))
    j_vol_tmp = np.sqrt(np.add.outer(vol_tmp*vol_tmp,jumpvolatility*jumpvolatility*j_nj))
   
    j_yy_tmp=np.zeros((Nobs,Ngrid,Njump))
    j_yy_tmp[:,:,:]=np.tile(y,(Njump,Ngrid,1)).T
    j_yy_tmp[:,:,:]-=np.tile(np.tile(coeff_dt+coeff_iu*iu_tmp+coeff_du*du_tmp,(Nobs,1)).T,(Njump,1,1)).T
    j_yy_tmp[:,:,:]-=np.tile(jumpmean*j_nj,(Nobs,Ngrid,1))
    j_yy_tmp[:,:,:]/=np.tile(j_vol_tmp,(Nobs,1,1))
    
# log-probs    
    j_yy_tmp[:,:,:]=-0.5*j_yy_tmp*j_yy_tmp-np.log(np.tile(j_vol_tmp,(Nobs,1,1)))-0.5*np.log(2.0*np.pi)

# add jump log-probs
    j_yy_tmp[:,:,:]+=np.tile(j_lnprobs,(Nobs,Ngrid,1))

# logsumexp to result in log prob for condasset unconditional on jumps
    lncp[:,:] = splse(j_yy_tmp,axis=2)
        
    return 
