import numpy as np
import pandas as pd 
import multiprocessing as mp

from svolfit import svolfit

def gridanalysis(NAME,FILES,SERIES,ow_start,ow_finish,windows,stride,NumProc,dt, model='Heston', method = 'grid', modeloptions={}):

    success=False
    
    if(NumProc > 1 ):
        if( NumProc>mp.cpu_count() ):
            NumProc=mp.cpu_count()-1
        pool=mp.Pool(processes=NumProc)

    
    windowsizes=np.sort(windows)[::-1]
    
    sols=[]
    solsm=[]
    for FILE in FILES:
        print(FILE)

        TS = pd.read_csv(FILE,index_col=0)

        if( ow_start < 0 ):
            ow_start=0
        if( (ow_finish <= ow_start)|(ow_finish > len(TS)) ):
            ow_finish = len(TS)
        
        for cw in range(0,len(windowsizes)):
            print(str(cw))
    
            NObs=ow_finish-ow_start+1
            Ninit=1
            if(stride>0):
                Ninit=int((NObs-windowsizes[cw]-1)/stride+1)

            for cc in range(0,Ninit):
                print(str(cc)+' of '+str(Ninit))
                start=ow_start+cc*stride
                finish=ow_start+cc*stride+(windowsizes[cw]+1)
                TS_window=TS[start:finish].copy()

                for cseries in range(0,len(SERIES)):        
                    series=np.array(TS_window[SERIES[cseries]].copy())
        
                    RunPars={}
                    RunPars['Name']=NAME
                    RunPars['FILE']=FILE
                    RunPars['SeriesName']=SERIES[cseries]
                    RunPars['ow_start']=ow_start
                    RunPars['ow_finish']=ow_finish
                    RunPars['start']=start
                    RunPars['finish']=finish
                    RunPars['offset']=start-ow_start
                    RunPars['stride']=stride
                    RunPars['Nobs']=windowsizes[cw]
       
                    if(NumProc > 1 ):
                        pool.apply_async(svolfit,args=(series.copy(), dt, model, method, modeloptions.copy(), RunPars.copy()),callback=lambda x: solsm.append(x) )
                    else:
                        (rpdict,sol)=svolfit( series, dt, model, method, modeloptions.copy(), RunPars.copy() )
                        ssl={}
                        ssl.update(rpdict)
                        ssl.update(sol)
                        sols.append(ssl)
    
    
    if(NumProc > 1 ):
        pool.close()
        pool.join()
        for x in solsm:
            ssl={}
            ssl.update(x[0])
            ssl.update(x[1])
            sols.append(ssl)
    
    sols=pd.DataFrame(sols)
    if( len(sols)==0 ):
        print('no results')
        return
    sols.sort_values(['RunInfo_FILE','RunInfo_Nobs','RunInfo_SeriesName','RunInfo_offset'],ignore_index=True,inplace=True)
    
    if('ts_upath' in sols):
        upaths = pd.DataFrame(sols.ts_upath.tolist(),index=sols.index)
        upaths.columns=['upath_'+str(x) for x in upaths.columns]
        upaths.T.to_csv(NAME+'_'+model+'_'+method+'_raw_upaths.csv')

    if('ts_vpath' in sols):
        vpaths = pd.DataFrame(sols.ts_vpath.tolist(),index=sols.index)
        vpaths.columns=['vpath_'+str(x) for x in vpaths.columns]        
        vpaths.T.to_csv(NAME+'_'+model+'_'+method+'_raw_vpaths.csv')

    sols.drop(['ts_upath','ts_vpath'],axis=1,inplace=True)

    sols.to_csv(NAME+'_'+model+'_'+method+'_raw.csv')

    success=True
    
    return success

