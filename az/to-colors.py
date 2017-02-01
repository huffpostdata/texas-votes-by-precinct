#!/usr/bin/env python3

# File formats are in "result-descriptions.xlsx"

def dump(out, county, precincts):
    for precinct, votes in precincts.items():
        if votes['Trump'] > 2 * votes['Clinton']: color = '#f66'
        elif votes['Trump'] > votes['Clinton']: color = '#faa'
        elif votes['Clinton'] > 2 * votes['Trump']: color = '#66f'
        elif votes['Clinton'] > votes['Trump']: color = '#aaf'
        else: color = '#ddd'

        out.write('%s %s,%s\n' % (county, precinct, color))

def process_electionware(out, county):
    precincts = {}

    with open(county + '.txt', 'rt') as f:
        for line in f:
            if not line[111:167].strip().lower() == 'presidential electors': continue

            party = line[101:104]
            if party == 'REP': name = 'Trump'
            elif party == 'DEM': name = 'Clinton'
            else: continue

            precinct = line[7:11]

            if precinct not in precincts:
                precincts[precinct] = {}
            precincts[precinct][name] = int(line[11:17])

    dump(out, county, precincts)

def process_gems(out, county):
    precincts = {}

    with open(county + '.txt', 'rt', encoding='windows-1252') as f:
        for line in f:
            cells = [ s.replace('"', '') for s in line.split(',') ]

            if cells[5] != 'U.S. PRESIDENT' and cells[5] != 'Presidential Electors': continue
            if cells[20] != 'Total': continue

            if cells[17] == 'DEM': name = 'Clinton'
            elif cells[17] == 'REP': name = 'Trump'
            else: continue

            if len(cells[1]) > 5: continue
            if len(cells[1]) > 4: raise ("Precinct number %s does not fit expectation of 2 chars" % precinct)
            precinct = '%04d' % int(cells[1])

            if precinct not in precincts: precincts[precinct] = {}
            precincts[precinct][name] = int(cells[22])

    dump(out, county, precincts)

def process_wineds(out, county):
    precincts = {}

    with open(county + '.txt', 'rt', encoding='windows-1252') as f:
        for i, line in enumerate(f):
            if i == 0: continue

            cells = line.split('\t')
            if cells[8] != 'Presidential Electors': continue

            if cells[1][0:3] == 'DEM': name = 'Clinton'
            elif cells[1][0:3] == 'REP': name = 'Trump'
            else: continue

            precinct = cells[0][0:4]
            if precinct not in precincts: precincts[precinct] = {}
            precincts[precinct][name] = int(cells[9])

    dump(out, county, precincts)

def process_openelect(out, county):
    precincts = {}

    with open(county + '.txt', 'rt', encoding='windows-1252') as f:
        for line in f:
            if line[0] != '1': continue

            cells = line.split(',')
            if cells[6] != 'PRESIDENTIAL ELECTOR': continue

            if cells[8] == '(DEM)': name = 'Clinton'
            elif cells[8] == '(REP)': name = 'Trump'
            else: continue

            precinct = '0' + cells[2][0:3]
            if precinct not in precincts: precincts[precinct] = { 'Clinton': 0, 'Trump': 0 }
            # Assumption: the number of votes for a candidate is the sum of
            # 'P' votes (provisional), 'C' votes (vote center), and 'E' votes (early)
            # So we use "+=" here to sum it all
            precincts[precinct][name] += int(cells[10])

    dump(out, county, precincts)

def process(out, county, logic):
    if logic == 'ElectionWare': process_electionware(out, county)
    elif logic == 'GEMS': process_gems(out, county)
    elif logic == 'WinEDS': process_wineds(out, county)
    else: process_openelect(out, county)

def main():
    results = []

    with open('az-results.csv', 'w') as out:
        out.write('PrecinctKey,color\n')

        process(out, 'Apache', 'ElectionWare')
        process(out, 'Cochise', 'ElectionWare')
        process(out, 'Coconino', 'GEMS')
        process(out, 'Gila', 'ElectionWare')
        process(out, 'Graham', 'ElectionWare')
        process(out, 'Greenlee', 'ElectionWare')
        process(out, 'La Paz', 'GEMS')
        process(out, 'Maricopa', 'WinEDS')
        process(out, 'Mohave', 'ElectionWare')
        process(out, 'Navajo', 'ElectionWare')
        process(out, 'Pima', 'ElectionWare')
        process(out, 'Pinal', 'ElectionWare')
        process(out, 'Santa Cruz', 'ElectionWare')
        process(out, 'Yavapai', 'OpenElect')
        process(out, 'Yuma', 'GEMS')

if __name__ == '__main__':
    main()
