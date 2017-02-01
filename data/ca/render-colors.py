#!/usr/bin/env python3

with open('all_precinct_results.csv', 'rt') as f:
    with open('ca-results.csv', 'wt') as out:
        for i, line in enumerate(f):
            if len(line) == 0: next
            if i == 0:
                out.write('pct16,color\n')
                continue
            name, trump_s, clinton_s, *_ = line.strip().split(',')
            trump = int(float(trump_s))
            clinton = int(float(clinton_s))

            color = None
            if trump >= 2 * clinton: color = '#f66'
            elif clinton >= 2 * trump: color = '#66f'
            elif trump > clinton: color = '#faa'
            elif clinton > trump: color = '#aaf'
            else: color = '#ddd'

            out.write('%s,%s\n' % (name, color))
