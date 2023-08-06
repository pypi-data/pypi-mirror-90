import time
from scipy.optimize import minimize

from svolfit.models.model_factory import model_create

def svolfit( series, dt, model='Heston', method = 'grid', modeloptions={}, RunInfo={} ):

    sol_success=False
    sol_message='Incomplete'

    sol = {}
    sol['RunInfo_'+'model']=model
    sol['RunInfo_'+'method']=method
    sol['RunInfo_'+'dt']=dt

    for x in RunInfo:
        sol['RunInfo_'+x]=RunInfo[x]
    
    try:
        model=model_create(series, dt, model, method, modeloptions )
    except:
        sol['success']=sol_success
        sol['message']='Model creation failed.'
        sol['ts_upath']=[]
        sol['ts_vpath']=[]
        return {},sol
    
    (wpn,wp,wpb)=model.get_workingpars()
    for cc in range(0,len(wpn)):
        sol['init_wrk_'+wpn[cc]]=wp[cc]

    (rdict)=model.get_reportingpars()
    for x in rdict:
        if( x[0:4]=='rep_' ):
            sol['init_'+x]=rdict[x]


    mcons=model.get_constraints()

    opts={'disp': True, 'ftol': 1.0e-8}
    start_time = time.process_time()

    res = minimize(lambda x: model.objective_calculate(x), wp, jac=lambda x: model.calculate_gradient(x),method='SLSQP',bounds=wpb,constraints=mcons,options=opts)

    for x in res:
        sol['opt_'+x]=res[x]

    wp=res.x
    wpg=res.jac
    for cc in range(0,len(wp)):
        sol['wrk_'+wpn[cc]]=wp[cc]
        sol['wrk_grad_'+wpn[cc]]=wpg[cc]
    
    (rdict)=model.get_reportingpars()
    rpdict={}
    for x in rdict:
        if( (x[0:3] != 'ts_') ):
            rpdict[x]=rdict[x]
    if( 'ts_upath' in rdict ):
        sol['ts_upath']=rdict['ts_upath']
    else:
        sol['ts_upath']=[]
    if( 'ts_vpath' in rdict ):
        sol['ts_vpath']=rdict['ts_vpath']
    else:
        sol['ts_vpath']=[]
    
    elapsed_time = time.process_time() - start_time
    sol['proctime']=elapsed_time

#TODO: with diagnostics flag, check that value, grad/etc 
# matches on recalc?
#    grad=model.calculate_gradient(wp)
#    sol['gradient']=grad

# delete some of the vectors we dont need any more -- they make the dataframe ugly:
    dellist=['opt_x','opt_jac']
    for x in dellist:
        if( x in sol):
            del sol[x]        

# do last!
    stdict=model.get_stats()
    for x in stdict:
        sol['stat_'+x]=stdict[x]

    if( stdict['current'] == True ):
        sol_success=True
        sol_message='Optimization succeeded.'
    else:
        sol_success=False
        sol_message='Incorrect model state.'
        
    sol['success']=sol_success
    sol['message']=sol_message
    
    print(sol_success,sol['proctime'],sol['opt_fun'],RunInfo)
    
    return (rpdict,sol)

