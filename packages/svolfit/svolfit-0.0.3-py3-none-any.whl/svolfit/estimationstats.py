import numpy as np

from svolfit.estimatestats.pathsim import pathsim
from svolfit.gridanalysis import gridanalysis
from svolfit.estimatestats.simparamstats import simparamstats

def estimationstats(NAME,Npaths,windows,stride,NumProcesses, dt, model, method, modeloptions ):

    Nsteps=np.max(windows)
    
    print('Running path simulation')
    (success,assetname,variancename)=pathsim(NAME,Nsteps,Npaths,windows,dt, model, method, modeloptions )
    ow_start=0
    ow_finish = -1
        
    if( success ):
        print('Fitting model')
        FILES=['SimPaths_'+NAME+'_'+model+'_'+method+'_'+assetname+'.csv']
        SERIES=[assetname+'_'+str(cc) for cc in range(0,Npaths)]
        success = gridanalysis(NAME,FILES,SERIES,ow_start,ow_finish,windows,stride,NumProcesses, dt, model, method, modeloptions )
    
        if( success ):
                
            print('Calculating Statistics and Reporting.')
            simparamstats(NAME+'_'+model+'_'+method,assetname,variancename)

    return