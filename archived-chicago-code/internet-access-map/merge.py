#!/usr/bin/env python


#### Import....

import pandas as pd
import geopandas as gpd

print("Loading aggregated datasets...\n")
#### Load the preprocessed FCC data.

fcc = pd.read_csv("data/fcc_constructed.csv.gz")

#### Load the ACS data.

acs = pd.read_csv("data/acs_2019.csv.gz")

#### Load Ookla data -- fixed-line.

ookla_agg = pd.read_csv("data/ookla_agg.csv.gz")

#### Load geometry
print("Datasets loaded. Loading geometry...\n")
tracts = gpd.read_file("data/cb_2019_us_tract_500k.zip").to_crs(epsg = 4326)

tracts["geoid"]  = tracts["GEOID"].astype(int)
tracts["state"]  = tracts["STATEFP"].astype(int)
tracts["county"] = tracts["COUNTYFP"].astype(int)
tracts["tract"]  = tracts["TRACTCE"].astype(int)
tracts.query("state < 57", inplace = True)

tracts = tracts[["geoid", "state", "county", "tract", "geometry"]].copy()

print("Geometry loaded. Merging...\n")
#### Merge them all together. 

tracts_all = tracts.merge(fcc, how = "left")\
                   .merge(acs, how = "left")\
                   .merge(ookla_agg, how = "left")

tracts_all.loc[tracts_all.f_broadband < 0, "f_broadband"] = None
tracts_all.loc[tracts_all.f_computer  < 0, "f_computer"]  = None
tracts_all.loc[tracts_all.f_ba        < 0, "f_ba"]        = None
tracts_all.loc[tracts_all.f_black     < 0, "f_black"]     = None
tracts_all.loc[tracts_all.f_hispanic  < 0, "f_hispanic"]  = None
tracts_all.loc[tracts_all.mhi         < 0, "mhi"]         = None

tracts_all["tests_per_cap"]   = (tracts_all["tests"]   / tracts_all["population"]).round(3) # Should be 'ntests'?
tracts_all["devices_per_cap"] = (tracts_all["devices"] / tracts_all["population"]).round(3)

tracts_all["geoid"] = tracts_all.geoid.apply("{:011d}".format)

tracts.sort_values("geoid", inplace = True)

print("Merging completed. Saving file...\n")
#### Write to file.

output = tracts_all[["geoid", 
                     "n_isp", "n_dn10", "n_dn100",  "n_dn250",
                     "n_fiber_100u", "fiber_100u_exists", 
                     "max_dn", "max_up", 
                     "f_broadband", "f_computer", "f_ba", "f_black", "f_hispanic", 
                     "mhi", "log_mhi", "population", "households",
                     "tests", "devices", "d_mbps", "u_mbps", "lat_ms",
                     "tests_per_cap", "devices_per_cap",
                     "geometry"]]

print(f"Number of Census Tracts: {output.geoid.nunique()}")

output.to_file("data/broadband.geojson", driver = "GeoJSON")
output.drop("geometry", axis = 1).to_csv("data/broadband.csv.gz", index = False)
print("Done. File saved.")
