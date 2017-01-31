#!/usr/bin/env node

'use strict'

const fs = require('fs')

const Red = 'Romney'
const Blue = 'Obama'

const CountyNameToCode = {}
fs.readFileSync('county-name-to-code.tsv', 'utf-8')
  .split(/\r?\n/)
  .forEach(s => {
    const [ name, code ] = s.split(/\t/)
    CountyNameToCode[name] = code
  })

function newResult() {
  const ret = {}
  ret[Red] = 0
  ret[Blue] = 0
  return ret
}

const Results = {} // hash of cntyvtd => { Trump, Clinton }
fs.readFileSync('2012_General_Election_Returns.csv', 'utf-8')
  .split(/\r?\n/)
  .slice(1) // nix header
  .map(s => s.split(/,/))
  .filter(a => a[4] === 'President')
  .forEach(a => {
    const cntyvtd = a[3]
    if (!Results.hasOwnProperty(cntyvtd)) Results[cntyvtd] = newResult()
    Results[cntyvtd][a[5]] = +a[8]
  })

fs.readFileSync('Hudspeth.csv', 'utf-8')
  .split(/\r?\n/)
  .slice(1) // nix header
  .map(s => s.split(/,/))
  .forEach(a => {
    Results[a[0]] = {}
    Results[a[0]][Red] = +a[1]
    Results[a[0]][Blue] = +a[2]
  })

function color(result) {
  if (result[Red] > 2 * result[Blue]) return '#f66'
  if (result[Blue] > 2 * result[Red]) return '#66f'
  if (result[Red] > result[Blue]) return '#faa'
  if (result[Blue] > result[Red]) return '#aaf'
  return '#ddd'
}

const Rows = Object.keys(Results)
  .map(k => [ k, color(Results[k]) ].join(','))

const Csv = `CNTYVTD,color\n${Rows.join('\n')}\n`
fs.writeFileSync('results.csv', Csv)
