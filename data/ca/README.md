Shapefiles from: https://github.com/datadesk/california-2016-election-precinct-maps
(Clone and run `for f in shapefiles/*.shp; do ogr2ogr -update -append merged.shp $f -f "ESRI Shapefile"; done;`)

all_precinct-results.csv from https://github.com/datadesk/california-2016-election-precinct-maps as well
