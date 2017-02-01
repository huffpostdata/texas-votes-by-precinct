#!/bin/sh

BY_PRECINCT='by-precinct.csv'

echo 'NAME10,Trump,Clinton' > $BY_PRECINCT

for county_num in $(seq 1 33); do
  fips=$(printf "%02d" $county_num)
  filename_html="$fips.html"
  [ -f $filename_html ] || curl "http://electionresults.sos.state.nm.us/resultsPREC.aspx?type=FED&rid=4067&cty=$fips%20&osn=100" -o $filename_html
  county_name=$(grep MainContent_uwgCounty $filename_html | sed -e "s/.*'divRace'>\([^>]*\)<.*/\\1/g")
  echo "$fips: $county_name"
  filename_xlsx="$fips.xlsx"
  [ -f $filename_xlsx ] || curl "http://electionresults.sos.state.nm.us/ResultsExport.aspx?rid=4067&osn=100&pty=&name=President%20and%20Vice%20President%20of%20the%20United%20States&cty=$fips&cat=PREC" -o $filename_xlsx
  filename_csv="$fips.csv"
  [ -f $filename_csv ] || soffice --headless --convert-to csv $filename_xlsx --outdir .
  grep -i '^\(PRECINCT \|PCT \|PREC \|\)[[:digit:]]\{1,3\}[, ]' $filename_csv \
    | sed -e "s/\(PRECINCT \|PCT \|PREC \|\)0*\([1-9][0-9]*\)[^,]*,[^,]*,[^,]*,\([^,]*\),\([^,]*\).*/$county_name County Precinct \2,\3,\4/i" \
    >> $BY_PRECINCT
done

./render-colors.py
