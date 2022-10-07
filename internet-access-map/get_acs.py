#!/usr/bin/env python 

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm


fips = [ 2,  1,  5,  4,  6,  8,  9, 11, 10, 12, 13, 15, 19, 
        16, 17, 18, 20, 21, 22, 25, 24, 23, 26, 27, 29, 28,
        30, 37, 38, 31, 33, 34, 35, 32, 36, 39, 40, 41,
        42, 44, 45, 46, 47, 48, 49, 51, 50, 53, 55, 54, 56]


raw_var_dict =  {"B28001_002E" : "nhh_computer",
                 "B28002_004E" : "nhh_broadband",
                 "B28003_002E" : "nhh_computer_any_internet",
                 "B28003_003E" : "nhh_computer_and_dialup",
                 "B28003_004E" : "nhh_computer_and_broadband",
                 "B28003_005E" : "nhh_computer_no_internet",
                 "B28003_006E" : "nhh_no_computer",
                 "B28005_001E" : "den_age",
                 "B28005_002E" : "n_children",
                 "B28005_003E" : "n_children_computer",
                 "B28005_004E" : "n_children_computer_and_dialup",
                 "B28005_005E" : "n_children_computer_and_broadband",
                 "B28005_006E" : "n_children_computer_no_internet",
                 "B28005_007E" : "n_children_no_computer",
                }

prof_var_dict = {"DP05_0001E"  : "population", 
                 "DP02_0001E"  : "households", 
                 "DP02_0153PE" : "broadband", 
                 "DP02_0152PE" : "computer",     ## 
                 "DP05_0065PE" : "black",        ## Alone or in combination...
                 "DP05_0071PE" : "hispanic",     ## Hispanic of any race
                 "DP03_0062E"  : "mhi",
                 "DP02_0068PE" : "ba",

                 "DP02_0151E"  : "den_computers",
                 "DP02_0152E"  : "n_computer",
                 "DP02_0153E"  : "n_broadband",

                 "DP05_0033E"  : "den_black",
                 "DP05_0065E"  : "n_black",

                 "DP05_0070E"  : "den_hispanic",
                 "DP05_0071E"  : "n_hispanic",

                 "DP02_0059E"  : "den_ba",
                 "DP02_0068E"  : "n_ba",
                }

print("Querying Census API...\n")

# Revert back to 2019
prof_api = "https://api.census.gov/data/2019/acs/acs5/profile"
prof_var = "?get=" + ",".join(prof_var_dict)

raw_api  = "https://api.census.gov/data/2019/acs/acs5"
raw_var  = "?get=" + ",".join(raw_var_dict)

geo = "&for=tract:*&in=state:{:02d}&in=county:*"

prof, raw = [], []
for f in tqdm(fips):

    resp = requests.get(prof_api + prof_var + geo.format(f)).json()
    prof.append(pd.DataFrame(columns = resp[0], data = resp[1:]))

    resp = requests.get(raw_api + raw_var + geo.format(f)).json()
    raw.append(pd.DataFrame(columns = resp[0], data = resp[1:]))
    
    
prof = pd.concat(prof)
raw  = pd.concat(raw)

print("Querying completed.\n Processing variables...\n")

for df in [prof, raw]:

    df["geoid"] = (df.state + df.county + df.tract).astype(int)
    for v in ["state", "county", "tract"]: df[v] = df[v].astype(int)

acs = prof.merge(raw).reset_index()

acs.rename(columns = prof_var_dict, inplace = True)
acs.rename(columns = raw_var_dict,  inplace = True)

for v in prof_var_dict.values():
    
    if "den" in v or "n_" in v:
        acs[v] = acs[v].astype(int)
    else:
        acs[v] = acs[v].astype(float)

for v in raw_var_dict.values():  acs[v] = acs[v].astype(int)

for v in ["black", "hispanic", "ba", "broadband", "computer"]:
    acs["f_" + v] = (acs[v] / 100.).round(3)

acs["log_mhi"] = np.log(acs["mhi"]).round(2)

print("Processing completed. Saving file...\n")

geo_vars  = ['state', 'county', 'tract', 'geoid']
calc_vars = ['f_broadband', 'f_computer', 'f_ba', 'f_black', 'f_hispanic', 'log_mhi', 'mhi']

out_vars = geo_vars + calc_vars + list(prof_var_dict.values()) + list(raw_var_dict.values())

acs = acs[out_vars]

acs.reset_index(drop = True, inplace = True)
acs.sort_values("geoid", inplace = True)
print(f"Number of Census Tracts: {acs.geoid.nunique()}\n")
acs.to_csv("data/acs_2019.csv.gz", index  = False)
print("Done. File saved.\n")
