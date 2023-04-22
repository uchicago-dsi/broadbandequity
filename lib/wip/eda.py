#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:41:24 2023

@author: chandlerhall
"""

import zipfile
import os
import pandas as pd
import numpy
import sys

sys.path[0] = os.path


with zipfile.ZipFile(f'{sys.path[0]}/broadbandequity/Merge_ACS-CDC/Datasets-CDC ACS 2017 2021.zip', 'r') as zip_ref:
    zip_ref.extractall(f'{sys.path[0]}/broadbandequity/Merge_ACS-CDC/')

stand_df_2017 = pd.read_csv(f'{sys.path[0]}/broadbandequity/Merge_ACS-CDC/standard_acs_censustract_df_2017.csv')



# Explore Dataset
stand_df_2017.head()
stand_df_2017.columns

stand_df_2017['state'].unique()



############
# load standard dataframes
with zipfile.ZipFile(f'{sys.path[0]}/broadbandequity/data/standard_dataframes/standard_acs_censustract_df_2017.zip', 'r') as zip_ref:
    zip_ref.extractall(f'{sys.path[0]}/broadbandequity/data/standard_dataframes/')

df_2017 = pd.read_csv('/Users/chandlerhall/Desktop/Github/broadbandequity/data/standard_dataframes/standard_acs_censustract_df_2017.csv')


# Convert GEOID to string to add leading zero
df_2017['GEOID'] = df_2017['GEOID'].astype('string')

for index, val in enumerate(df_2017['GEOID']):
    if len(val) == 10:
        val = '0' + val
        df_2017.at[index, 'GEOID'] = val
        

# Load in cdc data
cdc = pd.read_csv('/Users/chandlerhall/Desktop/Github/broadbandequity/data/CDC_PLACES/500_Cities__Local_Data_for_Better_Health__2019_release.csv')
cdc.columns

# Reduce to Census Tract only rows
cdc = cdc[cdc['GeographicLevel'] == 'Census Tract']

# Define Measures of interest, reduce cdc dataset to only vars of interest
values_to_keep = ['Physical health not good for >=14 days among adults aged >=18 Years',
                  'Mental health not good for >=14 days among adults aged >=18 Years',
                  'Visits to dentist or dental clinic among adults aged >=18 Years', 
                    'Cholesterol screening among adults aged >=18 Years',
                 'Visits to doctor for routine checkup within the past Year among adults aged >=18 Years',
                  'Taking medicine for high blood pressure control among adults aged >=18 Years with high blood pressure',
                  'Fecal occult blood test, sigmoidoscopy, or colonoscopy among adults aged 50–75 Years',
                 'High cholesterol among adults aged >=18 Years who have been screened in the past 5 Years',
                 'Older adult women aged >=65 Years who are up to date on a core set of clinical preventive services: Flu shot past Year, PPV shot ever, Colorectal cancer screening, and Mammogram past 2 Years']

measure_values = list(cdc['Measure'].unique())

result = [val for val in measure_values if val in values_to_keep]

cdc = cdc[cdc['Measure'].isin(result)]
cdc = cdc[cdc['Year'] == 2017]



# Prepare cdc for pivot and then merge
cdc['UniqueID'] = cdc['UniqueID'].str[8:]
cdc_final = cdc.pivot(index=['UniqueID', 'GeoLocation'], columns='Measure', values='Data_Value').reset_index()

standard_merged = pd.merge(df_2017, cdc_final, left_on='GEOID', right_on='UniqueID', how='inner')






