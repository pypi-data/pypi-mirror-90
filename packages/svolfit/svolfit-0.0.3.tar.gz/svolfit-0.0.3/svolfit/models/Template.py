from svolfit.models.svol_model import svol_model

class Template(svol_model):
    def __init__(self, series,dt, model, method,options):
        super().__init__(series,dt, model, method,options)
        return

    def _init_d(self):
        return

    def initpars_reporting(self,pardict):
# this alters self.working_pars, so make sure it's called after they are init'd
        return

    def get_structure(self):
        return '',0.0,'',0.0,[],0
    
    def sim_step(self,asset,variance,Zs):
        return [],[]

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
    
    
    