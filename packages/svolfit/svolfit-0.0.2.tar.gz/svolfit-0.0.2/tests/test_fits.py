import numpy as np
import pandas as pd
import os

from svolfit import svolfit
    
dt=1.0/252.0
FILE='test_path.csv'
SERIES='asset'

dir_name = os.path.dirname(__file__)
file_path = os.path.join(dir_name, 'data', FILE)

#TODO: need to test that test data file exists...
series=pd.read_csv(file_path)
series=series[SERIES].to_numpy()
#print(series)

#TODO: test vpath as well...?

models=[]
methods=[]
testpars=[]

models.append('Template')
methods.append('tree')
testpars.append(
    {}
    )

models.append('GBM')
methods.append('analytic')
testpars.append(
    {'rep_mu': 0.01542585774471747, 'rep_sigma': 0.05512169247825324, 'misc_theta': 0.00303840098166712, 'misc_v0': 0.00303840098166712, 'misc_vT': 0.00303840098166712, 'misc_GBM_mu': 0.016652991518886752, 'misc_GBM_sigma': 0.055184064089833784}
    )
models.append('HestonNandi')
methods.append('v')
testpars.append(
    {'rep_mu': -0.5, 'rep_theta': 0.09116625083360252, 'rep_rho': -1.0, 'rep_alpha': 0.6666666666666694, 'rep_eta': 0.030193749491191885, 'misc_q': 133.3333333332132, 'rep_v0': 0.00912574170844385, 'rep_vT': 0.05810649317126487}
    )
models.append('MertonJD')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03347013368019067, 'rep_theta': 0.0028511638994011615, 'misc_v0': 0.0028511638994011615, 'misc_vT': 0.0028511638994011615, 'rep_jumpintensity': 1.5726619477670725, 'rep_jumpmean': -0.010785947829484681, 'rep_jumpvolatility': 0.0021}
    )
models.append('PureJump')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.37784980841053506, 'misc_v0': 1.0, 'misc_vT': 1.0, 'rep_jumpintensity': 355.9409162865344, 'rep_jumpmean': -0.0008139495440064259, 'rep_jumpvolatility': 0.0024720326241349736}
    )

models.append('Heston')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.031598578372465116, 'rep_theta': 0.0031625449896207154, 'rep_rho': 0.3783686034802998, 'rep_alpha': 3.2654036384020606, 'rep_eta': 0.03593784165348757, 'misc_q': 15.99188281772672, 'rep_v0': 0.0037384545754480065, 'rep_vT': 0.0029216493740896183}
    )
models.append('Heston')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.03055071749984695, 'rep_theta': 0.003132865268790383, 'rep_rho': 0.3607679427218266, 'rep_alpha': 4.233093285968648, 'rep_eta': 0.04028996174265257, 'misc_q': 16.33939015419114, 'rep_v0': 0.004270168559368956, 'rep_vT': 0.002914018962491343}
    )
models.append('Heston')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.03411855836869871, 'rep_theta': 0.003156592911928414, 'rep_rho': 0.48495286998294873, 'rep_alpha': 3.3384898883577567, 'rep_eta': 0.03799206422445619, 'misc_q': 14.602017222890494, 'rep_v0': 0.004408771967202047, 'rep_vT': 0.0030085719536116946}
    )

models.append('Bates')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03629507199787237, 'rep_theta': 0.002788222179037243, 'rep_rho': 0.6554003444511729, 'rep_alpha': 2.1565325673898528, 'rep_eta': 0.01746580072521935, 'rep_jumpintensity': 9.881484212656488, 'rep_jumpmean': -0.000989518647430321, 'rep_jumpvolatility': 0.005626334604352059, 'misc_q': 39.4217947715374, 'rep_v0': 0.003011643103236992, 'rep_vT': 0.002917529256260836}
    )
models.append('Bates')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.03512465101845133, 'rep_theta': 0.0029279402427590225, 'rep_rho': 0.3498022589163152, 'rep_alpha': 6.695152107431421, 'rep_eta': 0.03315143313510526, 'rep_jumpintensity': 1.089966313235409, 'rep_jumpmean': -0.011001221107887366, 'rep_jumpvolatility': 0.002, 'misc_q': 35.673690272306715, 'rep_v0': 0.003414465729620618, 'rep_vT': 0.0029279402436796905}
    )
models.append('Bates')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.03389436563426533, 'rep_theta': 0.003153236308380956, 'rep_rho': 0.4819321411707735, 'rep_alpha': 3.3922821186565333, 'rep_eta': 0.0381677327571819, 'rep_jumpintensity': 7.43329726125106e-16, 'rep_jumpmean': 0.02101471531707188, 'rep_jumpvolatility': 0.006994325019346036, 'misc_q': 14.685399043407097, 'rep_v0': 0.004401734819103718, 'rep_vT': 0.00300461829960417}
    )

models.append('H32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.035319851283899334, 'rep_theta': 0.0029947032665145605, 'rep_rho': 0.4464775392335281, 'rep_alpha': 2.075655179989457, 'rep_eta': 0.03353306401273929, 'misc_q': 11.055859822435137, 'rep_v0': 0.00430649913663229, 'rep_vT': 0.0029017053006185484}
    )

models.append('B32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03531638498310953, 'rep_theta': 0.0029946453221853095, 'rep_rho': 0.446515888178378, 'rep_alpha': 2.075661338592072, 'rep_eta': 0.03353400430578841, 'rep_jumpintensity': 0.0015438467976698468, 'rep_jumpmean': 0.00023267361580830406, 'rep_jumpvolatility': 0.0031015640884938865, 'misc_q': 11.055058712612349, 'rep_v0': 0.004306091148023715, 'rep_vT': 0.002901430399203145}
    )

models.append('GARCHdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03042537186423229, 'rep_theta': 0.003169068293374862, 'rep_rho': 0.32992493777168147, 'rep_alpha': 3.697982718742663, 'rep_eta': 0.7331282453343007, 'misc_q': 13.760523902903858, 'rep_v0': 0.004275322841112933, 'rep_vT': 0.002897869549584506}
    )

models.append('GARCHjdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03365915250373231, 'rep_theta': 0.002825696048736639, 'rep_rho': 0.5131999368186246, 'rep_alpha': 2.1084405116735807, 'rep_eta': 0.37217254460500154, 'rep_jumpintensity': 9.866935536366924, 'rep_jumpmean': -0.0009029963045800695, 'rep_jumpvolatility': 0.005420733639371999, 'misc_q': 30.44406806394848, 'rep_v0': 0.0033774685556112387, 'rep_vT': 0.002770604300314069}
    )

#for cc in range(0,len(models)):
#    print(models[cc]+' '+methods[cc])
#    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
#    print(pars)
#    print(junk['success'])


def compare(testpars,pars):

# a bit subtle -- seems a couple of these (5,8) are not so stable numerically
# 1e-8 is what i've seen as differences between math libraries, leave this here
# and look into the failures at some point...
#TODO: investigate
#    fittol=1.0e-4 # would pass...
    fittol=1.0e-6
    passed=True    
    for x in testpars:
        if( x in pars ):
            if( np.abs(testpars[x]-pars[x]) > fittol ):
                passed = False
        else:
            passed = False

    return passed

def test_0():
    cc=0
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert not pars

def test_1():
    cc=1
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_2():
    cc=2
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_3():
    cc=3
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_4():
    cc=4
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_5():
    cc=5
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_6():
    cc=6
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_7():
    cc=7
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_8():
    cc=8
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_9():
    cc=9
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_10():
    cc=10
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_11():
    cc=11
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_12():
    cc=12
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_13():
    cc=13
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)

def test_14():
    cc=14
    (pars,junk)=svolfit( series, dt, model=models[cc], method = methods[cc] )
    assert compare(testpars[cc],pars)
