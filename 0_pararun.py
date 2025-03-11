import numpy as np
import os
import math
import cmath
from subprocess import call
import multiprocessing as mp
import threading as td
import re
from random import randint, seed

def randn(nseed=11358913111, low=1, high=int(2E8)):
    '''Return a random int number'''
    result = randint(low, high)
    return result

def copyfile(eventID=0, dest='/DATA/data02/miaoheng/data/Ini_XeXe_5440/data0'):
    parent = os.getcwd()
    if not os.path.exists(dest):
        os.makedirs(dest)
    home = f'{dest}/event{eventID}'
    call(['cp', '-r', 'origin/', home])
    os.chdir(home)
    with open('exec', 'r') as f:
        fexec = f.read()
    ran = randn()
    fexec = re.sub(r'nseed_runtime=\d+', f'nseed_runtime={ran}', fexec)
    try:
        with open('exec', 'w') as f:
            f.write(fexec)
    except Exception as e:
        print('change exec failed:', e)

    with open('input.ampt', 'r') as f:
        finpu = f.read()
    ran1 = randn()
    finpu = re.sub(r'8\t\t! random seed for parton cascade',
                   f'{ran1}  ! random seed for parton cascade', finpu)
    finpu = re.sub(r'53153523\t! random seed for HIJING',
                   f'{randn()}  ! random seed for HIJING', finpu)
    with open('input.ampt', 'w') as f:
        f.write(finpu)
    os.chdir(parent)

def modseed():
    with open('exec', 'r') as f:
        lines = f.readlines()
    lines[4] = f"nseed_runtime={randn()}\n"
    with open('exec', 'w') as f:
        f.writelines(lines)
    
    with open('input.ampt', 'r') as f:
        lines = f.readlines()
    lines[28] = f"{randn()}\t! random seed for HIJING\n"
    lines[29] = f"{randn()}\t! random seed for parton cascade\n"
     
    with open('input.ampt', 'w') as f:
        f.writelines(lines)

def make_event(eventID=0, dest='/DATA/data02/miaoheng/data/Ini_XeXe_5440/data0'):
    '''Submit AMPT job with different random seed'''
    
    parent = os.getcwd()
    home = f'{dest}/event{eventID}'
    os.chdir(home)
    print(os.getcwd())
    while True:
        call('./exec', shell=True)
        data = np.loadtxt("./ana/ampt.dat")
        if len(data) == 50:
            break
        else:
            modseed()
    call('rm -rf ./ana/dn*.dat ./ana/*.oscar ./ana/zpc.dat', shell=True)
    call(f'mv -v ./ana ../ana_{eventID}', shell=True)
    os.chdir("../")
    call("ls")
    
    call(f"rm -rfv event{eventID}", shell=True)
    call('rm -rf ./ana/dn*.dat ./ana/*.oscar ./ana/zpc.dat', shell=True)
    call('rm -rf ./ana/jet_distribution.dat ./ana/version ./ana/zpc.res', shell=True)

    os.chdir(parent)

def collect(eventsID, fin='../1', fou='../data2'):
    '''Collect parton distributions from different events and put them in one folder.'''
    try:
        os.chdir(os.path.abspath(fin))
        os.mkdir(fou)
    except Exception as e:
        print('Directory exists or mkdir error:', e)
    i = 0
    for ID in range(eventsID):
        try:
            with open(f'ana_{ID}/tau0p2.txt', 'r') as f:
                ftau0p2 = f.read()
            with open(f'ana_{ID}/initial_parton_sm.dat', 'r') as f:
                finitial_patron = f.read()
            with open(f'ana_{ID}/ampt.dat', 'r') as f:
                amptbnp = f.read()
            events = ftau0p2.split('#Epxpypztxyz')
            events_ini = finitial_patron.split('#PIDPXPYPZMASSXYZ')
            bnaprt = amptbnp.split('\n')
            
            for j in range(len(events) - 1):
                try:
                    s = events[j].strip()
                    s2 = events_ini[j + 1].strip()
                    bnpt = bnaprt[j].strip().split()
                except Exception as e:
                    print(ID, len(events_ini), j + 1, e)
                    #exit(0)
                    
                if s != '' and len(events) == 51 and len(events_ini) == 51:
                    try:
                        nlines = len(s.split('\n'))
                        with open(f'{fou}/P{i}.txt', 'w') as fout:
                            print(nlines, bnpt[3], int(bnpt[4]) + int(bnpt[5]), file=fout)
                            print(s, file=fout)
                        print(f'write event {i} succeed', bnpt)
                        with open(f'{fou}/P{i}_ini.dat', 'w') as fout2:
                            print(s2, file=fout2)
                        i += 1
                    except Exception as e:
                        print('Cannot open file for write:', e)
            
        except IOError as e:
            print('Cannot open file event', ID, '/ana/tau0p2.txt', e)

if __name__ == '__main__':
    import sys
    NEVENT = 10
    n_th = 8
    dest = '../data0'
    if len(sys.argv) == 2:
        if sys.argv[1] == '0':
            for i in range(NEVENT):
                copyfile(eventID=i, dest=dest)
            pool = mp.Pool(processes=n_th)
            for i in range(NEVENT):
                pool.apply_async(make_event, args=(i, dest))
                #make_event(i, dest)
            pool.close()
            pool.join()
        else:
            collect(NEVENT,
                    fin=os.path.abspath('../data0'),
                    fou=os.path.abspath('../data1'))
    else:
        print("Usage: python ParallizeAMPT.py 0   to make event")
        print("Usage: python ParallizeAMPT.py 1   to change format")
