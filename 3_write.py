#!/usr/bin/env python3
import numpy as np
import h5py
import os
from glob import glob

system = "auau299"
cent = []
cent0 = [0, 1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for cid in cent0:
    for cid2 in cent0:
        if cid2 > cid:
            cent_value = f"{cid}_{cid2}"
            print(cent_value)
            cent.append(cent_value)

eventlist = np.array([])

with h5py.File(f'{system}.h5', 'w') as f:
    for centid in cent:
        file_path = f'../data2/{centid}/eventids.txt'
        try:
           
            infor = np.loadtxt(file_path)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            continue

        f.create_dataset(f'cent/{centid}', data=infor)
        
        try:
            events, b, npart, nparton = np.loadtxt(file_path, unpack=True)
        except Exception as e:
            print(f"Error loading file {file_path} with unpack: {e}")
            continue
        
        eventlist = np.concatenate((eventlist, events))
    
    datalist = np.unique(eventlist)

    for eventid in datalist:
        print("Read:", eventid)
        event_file = f'../data1/P{int(eventid)}.txt'
        try:
            data = np.loadtxt(event_file, skiprows=1)
        except Exception as e:
            print(f"Error loading event file {event_file}: {e}")
            continue
        f.create_dataset(f'event{int(eventid)}', data=data)
        print(f"Event{int(eventid)} done", len(datalist), len(np.unique(datalist)))
