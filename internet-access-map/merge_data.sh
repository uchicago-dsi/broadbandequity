#!/bin/bash 

# Run python scripts to aggregate each dataset to census tracts
# and merge into one dataset

echo "Processing FCC data..."
echo
./fcc_redux.py
echo "Aggregating FCC data..."
echo
./fcc_agg.py
echo "Pulling and processing ACS data..."
echo
./get_acs.py
echo "Aggregating Ookla data..."
echo
./ookla_agg.py
echo "Merging datasets and creating a geoJSON file..."
echo
# creates broadband.geojson and broadband.csv.gz
./merge.py