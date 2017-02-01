#!/usr/bin/env python3

with open('by-precinct.csv', 'rt') as f:
    with open('nm-results.csv', 'wt') as out:
        for i, line in enumerate(f):
            if len(line) == 0: next
            if i == 0:
                out.write('NAME10,color\n')
                continue
            print(line.strip())
            name, trump_s, clinton_s = line.strip().split(',')
            trump = int(trump_s)
            clinton = int(clinton_s)

            color = None
            if trump >= 2 * clinton: color = '#f66'
            elif clinton >= 2 * trump: color = '#66f'
            elif trump > clinton: color = '#faa'
            elif clinton > trump: color = '#aaf'
            else: color = '#ddd'

            # Fix names that the Shapefile gets wrong
            name = name.replace('Dona Ana', 'Doa Ana')

            out.write('%s,%s\n' % (name, color))
