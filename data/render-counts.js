#!/usr/bin/env node

'use strict'

const fs = require('fs')

const Filename = '2016_General_Election_Returns.csv'
const VrtFilename = '2016_General_Election_VRTO.csv'
const Red = 'Trump'
const Blue = 'Clinton'

function newResult() {
  const ret = { total: 0, winVotes: 0 }
  ret[Red] = 0
  ret[Blue] = 0
  return ret
}

const Results = {} // hash of cntyvtd => { Trump, Clinton }

fs.readFileSync(VrtFilename, 'utf-8')
  .split(/\r?\n/)
  .slice(1) // nix header
  .map(s => s.split(/,/))
  .forEach(a => {
    const cntyvtd = a[3]
    const population = +a[4]
    const registered = +a[5]
    const percentSpanishSurname = +a[6]
    const turnout = +a[7]

    const o = {
      population: population,
      registered: registered,
      percentSpanishSurname: percentSpanishSurname,
      turnout: turnout,
      winVotes: 0
    }

    o[Red] = 0
    o[Blue] = 0
    Results[cntyvtd] = o
  })

fs.readFileSync(Filename, 'utf-8')
  .split(/\r?\n/)
  .slice(1) // nix header
  .map(s => s.split(/,/))
  .filter(a => a[4] === 'President')
  .forEach(a => {
    const cntyvtd = a[3]
    const results = Results[cntyvtd]
    if (!results) throw new Error(`Missing metadata for cntyvtd '${cntyvtd}'`)
    const votes = +a[8]
    results[a[5]] = votes
    results.winVotes = Math.max(results.winVotes, votes)
  })

Object.keys(Results).forEach(cntyvtd => {
  const result = Results[cntyvtd]
  if (result[Red] > result[Blue] && result[Red] === result.winVotes) {
    result.winner = Red
  } else if (result[Blue] > result[Red] && result[Blue] === result.winVotes) {
    result.winner = Blue
  } else {
    result.winner = ''
  }
})

const Columns = [
  Red,
  Blue,
  'winner',
  'population',
  'registered',
  'turnout',
  'percentSpanishSurname'
]

const Rows = Object.keys(Results)
  .map(cntyvtd => [ cntyvtd ].concat(Columns.map(k => Results[cntyvtd][k])).join(','))

const Csv = `CNTYVTD,${Columns.join(',')}\n${Rows.join('\n')}\n`
fs.writeFileSync('tx-results.csv', Csv)
