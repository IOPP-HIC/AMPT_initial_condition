#!/usr/bin/env python3
import os
import numpy as np
from glob import glob

def get_multiplicity_list(dest_dir):
    multiplicities = []
    flist = glob(os.path.join(dest_dir, 'P*.txt'))
    print("Found {} files".format(len(flist)))
    
    for i, fpath in enumerate(flist):
        try:
            with open(fpath, 'r') as f:
                line = f.readline().strip()
        except Exception as e:
            print(f"Error reading file {fpath}: {e}")
            continue

        parts = line.split()
        if len(parts) < 3:
            print(f"Warning: File {fpath} does not contain enough data.")
            continue

        try:
            mul_value = int(parts[0])
        except ValueError as e:
            print(f"Error parsing multiplicity in file {fpath}: {e}")
            continue

        multiplicities.append(mul_value)
        print(i, line, fpath)
    
    multiplicities.sort(reverse=True)
    return multiplicities

def compute_centrality_boundaries(multiplicities, num_cent=100):
    boundaries = []
    n = len(multiplicities)
    for cent in range(num_cent):
        idx = int(n * cent / 100)
        idx = min(idx, n - 1)  
        boundaries.append((cent, multiplicities[idx]))
    return boundaries

def main():
    system = "auau299"
    dest_dir = os.path.abspath('../data1/')
    output_centrality = f'centrality_nparton_{system}.dat'

    multiplicities = get_multiplicity_list(dest_dir)
    if not multiplicities:
        print("No multiplicity data found!")
        return

    boundaries = compute_centrality_boundaries(multiplicities, num_cent=100)
    
    with open(output_centrality, 'w') as f:
        for cent, bound in boundaries:
            f.write(f"{cent}% {bound}\n")
    
    print("Centrality boundaries saved to", output_centrality)

if __name__ == '__main__':
    main()
