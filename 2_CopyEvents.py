#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import sys
import numpy as np 
from glob import glob
from subprocess import call

#----------------------------------------------------------------------
def get_centlimit(fpath, cent='0_10'):
    c1, c2 = [i + '%' for i in cent.split('_')]
    with open(fpath, encoding='utf-8') as f:
        d = dict(line.split() for line in f.readlines())
        d['100%'] = 0
    return (int(d[c1]), int(d[c2]))

#----------------------------------------------------------------------
def CopyCentevent(ampt_dir, dest_dir, high_mul, low_mul, nchoose=3000):
    nevent = len(glob(os.path.join(ampt_dir, 'P*.txt')))
    nstart = 0    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    eventids = []
    for i in range(nevent):
        try:
            partons_data = os.path.join(ampt_dir, 'P%s.txt' % i)                              
            with open(partons_data, 'r', encoding='utf-8') as f:
                mul = f.readline().strip().split()
                if int(mul[0]) < high_mul and int(mul[0]) > low_mul:
                    mul.append(str(i))                                                    
                    eventids.append(mul)
                    print('eventid=', i, ' nparton=', mul)
                    nstart += 1
                    if nstart >= nchoose:
                        break        
        except Exception as e:
            print(f"Error processing event {i}: {e}")
            continue

    with open(os.path.join(dest_dir, 'eventids.txt'), 'w', encoding='utf-8') as f:
        for i in range(len(eventids)):
            print(int(eventids[i][3]),
                  float(eventids[i][1]),
                  float(eventids[i][2]),
                  float(eventids[i][0]),
                  file=f)

if __name__ == '__main__':
    cent0 = [0, 1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    system = "auau299"

    fpath = f'./centrality_nparton_{system}.dat'
    
    for cid in cent0:
        for cid2 in cent0:
            if cid2 > cid:
                cent = f"{cid}_{cid2}"
                print(f"{cid}_{cid2}")
                high_mul, low_mul = get_centlimit(fpath, cent)
                
                lgdir = os.path.abspath('../data1')
                dest_dir = os.path.abspath(f'../data2/{cent}')
                CopyCentevent(lgdir, dest_dir, high_mul, low_mul, 10000)
