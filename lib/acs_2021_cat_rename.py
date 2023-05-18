#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:35:05 2023

@author: chandlerhall
"""


import os
import sys
### add system path to get other library directories
sys.path[0] = os.path.join(os.path.abspath(''),'..')

import geopandas
import warnings
import pandas as pd
import zipfile
import glob
import json
warnings.filterwarnings('ignore')

# Read in the ACS_categories file for percentage calculation
ACS_CAT_FILE_2017 = open(f"{sys.path[0]}/data/acs_data/acs_categories_2017.json", "r")
ACS_CAT_2017 = json.load(ACS_CAT_FILE_2017)


ACS_CAT_2021 = {k.replace(u'17', '21') : v.replace(u'17', '21') for k, v in ACS_CAT_2017.items()}

with open(f'{sys.path[0]}//data/acs_data/acs_categories_2021.json', 'w') as f:
    json.dump(ACS_CAT_2021, f)
    
    
ACS_CAT_FILE_2021 = open(f"{sys.path[0]}/data/acs_data/acs_categories_2021.json", "r")
ACS_CAT_2021 = json.load(ACS_CAT_FILE_2021) 

# Read in the ACS columns of interest
FILE_2021 = open(f"{sys.path[0]}/data/acs_data/2021_columns.json", "r")
COL_2021 = list(json.load(FILE_2021).values())

with zipfile.ZipFile(f'{sys.path[0]}/data/standard_dataframes/standard_acs_censustract_df_2021.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{sys.path[0]}/data/standard_dataframes/')
ACS_2021_MERGED_FILE = f"{sys.path[0]}/data/standard_dataframes/standard_acs_censustract_df_2021.geojson"
acs_2021_standard_df = geopandas.read_file(ACS_2021_MERGED_FILE)


def get_percentages(city_df):
    
    city_df_copy = city_df.copy()
    

    for col in COL_2021:
        if col == "Estimate!!Total: TOTAL POPULATION":
            continue
        if col in ACS_CAT_2021.keys():
            curr_col_perc = city_df[col] / city_df_copy['Est_Total: TOTAL POPULATION_tct21']
            perc_key = f"PERC {col}"
            city_df_copy[perc_key] = curr_col_perc
    return city_df_copy


acs_2021_standard_df = get_percentages(acs_2021_standard_df)

acs_2021_standard_df.to_csv(f"{sys.path[0]}/data/standard_dataframes/standard_acs_censustract_df_2021.csv", index=False)
acs_2021_standard_df.to_file(f"{sys.path[0]}/data/standard_dataframes/standard_acs_censustract_df_2021.geojson", driver="GeoJSON")
