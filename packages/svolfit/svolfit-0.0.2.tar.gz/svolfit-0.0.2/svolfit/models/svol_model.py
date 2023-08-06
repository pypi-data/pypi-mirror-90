import numpy as np
from abc import ABC, abstractmethod

class svol_model(ABC):
    def __init__(self, series,dt, model, method,options):
        super().__init__()

        self.series=series.copy()
        self.dt=dt
        self.model=model
        self.method=method

        self.Nobs=len(self.series)

        self.workingpars_names=['tmp']
        self.workingpars=np.array([0.0])
        self.workingpars_diffs=np.array([0.01])
        self.workingpars_bounds=[(0,1)]

        self.objective_value=-1.0

        self.current=False

        self.numfunevals=0
        self.numgradevals=0

# for multithreaded grad calcs
        self.gradmodels=[]
        
        return

# generic abstract method -- needs to be implemented by concrete class
#    @abstractmethod
#    def AccruedAmount(self):
#        accrued=self.calc()
#        return accrued

    @abstractmethod
    def initpars_reporting(self,pardict):
        return

    @abstractmethod
    def get_structure(self):
        return '','',[],0
    
    @abstractmethod
    def sim_step(self,asset,variance,Zs):
        return [],[]

    def get_stats(self):
        stdict={}
        stdict['current']=self.current
        stdict['numfunevals']=self.numfunevals
        stdict['numgradevals']=self.numgradevals
        return stdict

#    @abstractmethod
    def get_workingpars(self):
        return (self.workingpars_names,self.workingpars,self.workingpars_bounds)

    def get_constraints(self):
        return []

    @abstractmethod
    def workingpars_update(self,workingpars):
# remember to call this...
        if(np.array_equal(workingpars,self.workingpars)==False):
            self.current=False
            self.workingpars[:]=workingpars
        return

    @abstractmethod
    def get_reportingpars(self):
# remember to call this...
        self.workingpars_update(self.workingpars)
        self.calculate()
        return {}

    def objective_calculate(self,workingpars):
 
        self.workingpars_update(workingpars)
        if( self.current == False ):
            self.calculate()
        
#        if(self.current==False):
#            print('how?')
        
        return self.objective_value

    @abstractmethod
    def calculate(self):
        return
    
    def calculate_gradient(self,workingpars):

#        print('grad in') 
        NPars=len(workingpars)

        grad=np.zeros(NPars)

        value_base = self.objective_calculate(workingpars)

        for cp in range(0,NPars):    
            wp_diff=workingpars.copy()
            wp_diff[cp]+=self.workingpars_diffs[cp]
            value_diff = self.objective_calculate(wp_diff)
            grad[cp]=(value_diff-value_base)/self.workingpars_diffs[cp]

        self.numgradevals+=1

#        print(workingpars)
#        print(grad)
#        print('grad out') 

        return grad
    
    @abstractmethod
    def variancepath(self):
        return 
    
    