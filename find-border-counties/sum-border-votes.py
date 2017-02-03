#!/usr/bin/env python3

import os

def load_distances():
    '''Returns a dict mapping cntyvtd to distance from mexico (in meters)'''
    ret = {}

    with open('./distance-from-mexico.csv') as f:
        for i, line in enumerate(f):
            if i == 0: continue

            cells = line.split(',')
            ret[cells[0]] = int(cells[1].strip())

    return ret

#max_distance = 160934 # 100 miles
#max_distance = 40234 # 25 miles
max_distance = 0

with open('../data/results.csv') as f:
    distances = load_distances()
    trump = 0
    clinton = 0

    trump_elpaso = 0
    clinton_elpaso = 0

    for i, line in enumerate(f):
        if i == 0: continue

        cells = line.split(',')
        cntyvtd = cells[0]

        if cntyvtd not in distances:
            print("Skipping %s" % cntyvtd)
            continue

        if distances[cntyvtd] <= max_distance:
            trump += int(cells[1])
            clinton += int(cells[2])

            if cntyvtd[0:3] == '141':
                trump_elpaso += int(cells[1])
                clinton_elpaso += int(cells[2])

    print("All Precincts within %d miles of border: Trump %d, Clinton %d" % (max_distance, trump, clinton))
    print("Only El Paso precincts: Trump %d, Clinton %d" % (trump_elpaso, clinton_elpaso))
