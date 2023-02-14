#!/usr/bin/env python

import geopandas as gpd
import numpy as np
import pandas as pd
#### Load Ookla data -- fixed-line.

print("Load Ookla Data...\n")
ookla  = gpd.read_file("data/2022-01-01_performance_fixed_tiles.zip")
print("Ookla Data Loaded. Processing...\n")
ookla.to_crs(epsg = 2163, inplace = True)

ookla["avg_d_mbps"] = ookla["avg_d_kbps"] / 1000
ookla["avg_u_mbps"] = ookla["avg_u_kbps"] / 1000

#### Load and format tract geodata.
print("Loading Census Tract Shape Files...\n")
tracts = gpd.read_file("data/cb_2019_us_tract_500k.zip")
print("Census Tracts Loaded. Processing...\n")
tracts.to_crs(epsg = 2163, inplace = True)

tracts["geoid"] = tracts["GEOID"].astype(int)

tracts["geoid"]  = tracts["GEOID"].astype(int)
tracts["state"]  = tracts["STATEFP"].astype(int)
tracts["county"] = tracts["COUNTYFP"].astype(int)
tracts["tract"]  = tracts["TRACTCE"].astype(int)
tracts.query("state < 57", inplace = True)

tracts = tracts[["geoid", "state", "county", "tract", "geometry"]].copy()

tracts.sort_values("geoid", inplace = True)

#### Merge Ookla to tracts.
print("Processing completed. Merging Ookla and Census Tract Data...\n")
ookla_tracts = gpd.sjoin(ookla, tracts, predicate = "intersects", how = "inner")
ookla_tracts.drop("index_right", axis = 1, inplace = True)
ookla_tracts.reset_index(drop = True, inplace = True)

ookla_tracts = ookla_tracts.merge(tracts[["geoid", "geometry"]].rename(columns = {"geometry" : "trgeom"}))
ookla_tracts["int_area"] = ookla_tracts.intersection(ookla_tracts.set_geometry("trgeom")).area
ookla_tracts["fr_area"] = ookla_tracts["int_area"] / ookla_tracts.area
ookla_tracts["ndevices"] = ookla_tracts["devices"] * ookla_tracts["fr_area"]
ookla_tracts["ntests"]   = ookla_tracts["tests"] * ookla_tracts["fr_area"]

#### Aggregate the Ookla tests, with weighted averages.
print("Merging completed. Aggregating Ookla Data...\n")
test_weighted_mean = lambda x: np.average(x, weights = ookla_tracts.loc[x.index, "ntests"])

ookla_agg = \
ookla_tracts.groupby("geoid").agg(tests   = pd.NamedAgg("ntests", "sum"),
                                  devices = pd.NamedAgg("ndevices", "sum"),
                                  d_mbps  = pd.NamedAgg("avg_d_mbps", test_weighted_mean),
                                  u_mbps  = pd.NamedAgg("avg_u_mbps", test_weighted_mean),
                                  lat_ms  = pd.NamedAgg("avg_lat_ms", test_weighted_mean))

ookla_agg = ookla_agg.round(2)
ookla_agg.reset_index(inplace = True)
print("Aggregating completed. Saving file...\n")
print(f"Number of Census Tracts: {ookla_agg.geoid.nunique()}")
ookla_agg.to_csv("data/ookla_agg.csv.gz", index = False)
print("Done. File saved.\n")
