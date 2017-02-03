Well, that was harder than it looked.

## What it does

It answers the question: "Which Texas voting tabulation districts are within
100 miles of Mexico?"

## Usage

`make && ./a.out > distance-from-mexico.csv`

## Why C++?

It should be simple: compute the distance of each polygon from Mexico.

The complication: that means A) computing the closest *points* in each polygon
and B) figuring out how many meters sit between those points. That's hard
because handy geometry libraries that compute the distance between polygons tend
to return an *integer*, not the *points*. And we don't have enough information
to convert the integer to meters. (If the distances were small we could maybe
approximate ... but they aren't, so we can't.)

GEOS's C and C++ libraries calculate the nearest points, but the wrappers are a
mess to install and use. Might as well go with straight C/C++.
