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

max_distance = 160934 # 100 miles
max_distance = 40234 # 25 miles
max_distance = 0

with open('../data/tx-results.csv') as f:
    distances = load_distances()
    n = 0
    total = 0
    trump = 0
    clinton = 0

    n_elpaso = 0
    total_elpaso = 0
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
            n += 1
            total += int(cells[6])
            trump += int(cells[1])
            clinton += int(cells[2])

            if cntyvtd[0:3] == '141':
                n_elpaso += 1
                total_elpaso += int(cells[6])
                trump_elpaso += int(cells[1])
                clinton_elpaso += int(cells[2])

    print("%d Precincts within %d meters of border: total %d, Trump %d, Clinton %d" % (n, max_distance, total, trump, clinton))
    print("Only %d El Paso precincts: total %d, Trump %d, Clinton %d" % (n, total_elpaso, trump_elpaso, clinton_elpaso))
