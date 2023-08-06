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

cc=0
models.append('Template')
methods.append('tree')
testpars.append(
    {}
    )

cc=1
models.append('GBM')
methods.append('analytic')
testpars.append(
    {'rep_mu': 0.01542585774471747, 'rep_sigma': 0.05512169247825324, 'misc_theta': 0.00303840098166712, 'misc_v0': 0.00303840098166712, 'misc_vT': 0.00303840098166712, 'misc_GBM_mu': 0.016652991518886752, 'misc_GBM_sigma': 0.055184064089833784}
    )
cc=2
models.append('HestonNandi')
methods.append('v')
testpars.append(
    {'rep_mu': 0.49999999999999994, 'rep_theta': 0.0054656717131093486, 'misc_rho': -1.0, 'rep_alpha': 19.999999999999986, 'rep_eta': 0.007393018134097433, 'misc_q': 3999.9999999999964, 'rep_v0': 0.005469789922271396, 'rep_vT': 0.005594363384161544}
    )
cc=3
models.append('MertonJD')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.034241223633602776, 'rep_sigma': 0.05139082648785998, 'misc_theta': 0.002641017047105331, 'misc_v0': 0.002641017047105331, 'misc_vT': 0.002641017047105331, 'rep_lambda': 19.99736439726318, 'rep_gamma': -0.0010686514095786003, 'rep_omega': 0.004691971323224507}
    )
cc=4
models.append('PureJump')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.37784034161927893, 'rep_lambda': 355.94092239176194, 'rep_gamma': -0.0008140312476703669, 'rep_omega': 0.0024720947028657337}
    )

cc=5
models.append('Heston')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.031598578372465116, 'rep_theta': 0.0031625449896207154, 'rep_rho': 0.3783686034802998, 'rep_alpha': 3.2654036384020606, 'rep_eta': 0.03593784165348757, 'misc_q': 15.99188281772672, 'rep_v0': 0.0037384545754480065, 'rep_vT': 0.0029216493740896183}
    )
cc=6
models.append('Heston')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.03055071749984695, 'rep_theta': 0.003132865268790383, 'rep_rho': 0.3607679427218266, 'rep_alpha': 4.233093285968648, 'rep_eta': 0.04028996174265257, 'misc_q': 16.33939015419114, 'rep_v0': 0.004270168559368956, 'rep_vT': 0.002914018962491343}
    )
cc=7
models.append('Heston')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.03411855836869871, 'rep_theta': 0.003156592911928414, 'rep_rho': 0.48495286998294873, 'rep_alpha': 3.3384898883577567, 'rep_eta': 0.03799206422445619, 'misc_q': 14.602017222890494, 'rep_v0': 0.004408771967202047, 'rep_vT': 0.0030085719536116946}
    )

cc=8
models.append('Bates')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03422833361276888, 'rep_theta': 0.0027382181331400525, 'rep_rho': 0.6529567921776389, 'rep_alpha': 3.6955486226220393, 'rep_eta': 0.0217535938499926, 'rep_lambda': 10.40610204852361, 'rep_gamma': -0.0009817805020765262, 'rep_omega': 0.005687613305845231, 'misc_q': 42.767604667203855, 'rep_v0': 0.003044847932439241, 'rep_vT': 0.002812925126122225}
    )
cc=9
models.append('Bates')
methods.append('tree')
testpars.append(
    {'rep_mu': 0.03328002173593035, 'rep_theta': 0.0026031493337724657, 'rep_rho': 0.6585982546638651, 'rep_alpha': 10.985996928482411, 'rep_eta': 0.028655676721350994, 'rep_lambda': 18.61790067418388, 'rep_gamma': -0.0007515905135513218, 'rep_omega': 0.004813668154764279, 'misc_q': 69.65418477428888, 'rep_v0': 0.002654347209891931, 'rep_vT': 0.0027475755837688136}
    )
cc=10
models.append('Bates')
methods.append('treeX2')
testpars.append(
    {'rep_mu': 0.019484937625758654, 'rep_theta': 0.0025000000000000005, 'rep_rho': 0.8566802984507665, 'rep_alpha': 20.0, 'rep_eta': 0.024300232437840134, 'rep_lambda': 21.509548490911214, 'rep_gamma': -0.0005722540153894941, 'rep_omega': 0.0047449863010841095, 'misc_q': 169.34763833224156, 'rep_v0': 0.0025080995497863677, 'rep_vT': 0.002670570783168483}
    )

cc=11
models.append('H32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03531985140108286, 'rep_theta': 0.0036560879044557114, 'rep_rho': 0.4464775394228347, 'rep_alpha': 567.7257315252865, 'rep_eta': 11.197458003023403, 'misc_q': 11.055859788118669, 'misc_theta': 333.92290005932324, 'misc_eta': 11.197458003023403, 'rep_v0': 0.004306499124928703, 'rep_vT': 0.0029017052927327084}
    )

cc=12
models.append('B32')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.035316384905647216, 'rep_theta': 0.002994645321556647, 'rep_rho': 0.4465158873830807, 'rep_alpha': 2.075661338529547, 'rep_eta': 0.03353400423955311, 'rep_lambda': 0.001543846573955615, 'rep_gamma': 0.0002326736137745283, 'rep_omega': 0.003101563825045725, 'misc_q': 11.055058753629762, 'rep_v0': 0.004306091163224677, 'rep_vT': 0.002901430409445504}
    )

cc=13
models.append('GARCHdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.03042537186423229, 'rep_theta': 0.003169068293374862, 'rep_rho': 0.32992493777168147, 'rep_alpha': 3.697982718742663, 'rep_eta': 0.7331282453343007, 'misc_q': 13.760523902903858, 'rep_v0': 0.004275322841112933, 'rep_vT': 0.002897869549584506}
    )

cc=14
models.append('GARCHjdiff')
methods.append('grid')
testpars.append(
    {'rep_mu': 0.0336612712350063, 'rep_theta': 0.00282576813071708, 'rep_rho': 0.5132488597550273, 'rep_alpha': 2.108449201909646, 'rep_eta': 0.37211176066711865, 'rep_jumpintensity': 9.866931505831824, 'rep_jumpmean': -0.0009034060922315556, 'rep_jumpvolatility': 0.005422464131795289, 'misc_q': 30.454140389054718, 'rep_v0': 0.0033744381195861097, 'rep_vT': 0.0027682060213376834}
    )

#for cc in range(0,len(models)):
#for cc in [8,9,10,11,12,14]:
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
