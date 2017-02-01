#!/bin/sh

curl 'http://apps.azsos.gov/results/2016/General/!File%20Type%20Descriptions.xlsx' -o result-descriptions.xlsx

for county in "Apache" "Cochise" "Coconino" "Gila" "Graham" "Greenlee" "La Paz" "Maricopa" "Mohave" "Navajo" "Pima" "Pinal" "Santa Cruz" "Yavapai" "Yuma"; do
  escaped=${county/ /%20}
  curl "http://apps.azsos.gov/results/2016/General/$escaped.txt" -o "$county.txt"
done
