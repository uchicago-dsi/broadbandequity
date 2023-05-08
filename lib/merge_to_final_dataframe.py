#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:41:24 2023

@author: chandlerhall
"""

import zipfile
import os
import pandas as pd
import numpy as np
import sys

os.chdir('/Users/chandlerhall/Desktop/Github/broadbandequity')

# load standard dataframes
#################################

# 2019 release CDC csv
if os.path.exists('data/CDC_PLACES/500_Cities__Local_Data_for_Better_Health__2019_release.csv'):
    cdc_clean = pd.read_csv('data/CDC_PLACES/500_Cities__Local_Data_for_Better_Health__2019_release.csv')
else:
    with zipfile.ZipFile('data/CDC_PLACES/500_Cities__Local_Data_for_Better_Health__2019_release.zip', 'r') as zip_ref:
        zip_ref.extractall('data/CDC_PLACES/')
    cdc_clean = pd.read_csv('data/CDC_PLACES/500_Cities__Local_Data_for_Better_Health__2019_release.csv')
    
# # 2022 release CDC csv
# if os.path.exists('data/CDC_PLACES/500_Cities__Local_Data_for_Better_Health__2019_release.csv'):
#     cdc_2022 = pd.read_csv('data/CDC_PLACES/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2022_release.csv')
# else:
#     with zipfile.ZipFile('data/CDC_PLACES/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2022_release.zip', 'r') as zip_ref:
#         zip_ref.extractall('data/CDC_PLACES/')
#     cdc_2022 = pd.read_csv('data/CDC_PLACES/PLACES__Local_Data_for_Better_Health__Census_Tract_Data_2022_release.csv')

# Standard Dataframe 2017
if os.path.exists('data/standard_dataframes/standard_acs_censustract_df_2017.csv'):
    df_2017 = pd.read_csv('data/standard_dataframes/standard_acs_censustract_df_2017.csv')
else:
    with zipfile.ZipFile('data/standard_dataframes/standard_acs_censustract_df_2017.zip', 'r') as zip_ref:
        zip_ref.extractall('data/standard_dataframes/')
    df_2017 = pd.read_csv('data/standard_dataframes/standard_acs_censustract_df_2017.csv')
    
    
# Social Vulnerability index
if os.path.exists('data/Social Vulnerability Index/SVI2016_US.csv'):
    svi = pd.read_csv('data/Social Vulnerability Index/SVI2016_US.csv')
else:
    with zipfile.ZipFile('data/Social Vulnerability Index/SVI2016_US.zip', 'r') as zip_ref:
        zip_ref.extractall('data/Social Vulnerability Index/')
    svi = pd.read_csv('data/Social Vulnerability Index/SVI2016_US.csv')

####################################


# Prep CDC Data for merge and merge
####################################
cdc = cdc_clean[cdc_clean ['GeographicLevel'] == 'Census Tract']

cdc = cdc.pivot(index=['UniqueID'], columns='Measure', values='Data_Value').reset_index()
cdc['UniqueID'] = cdc['UniqueID'].str[8:]

# Convert GEOID to string to add leading zero
df_2017['GEOID'] = df_2017['GEOID'].astype('string')

for index, val in enumerate(df_2017['GEOID']):
    if len(val) == 10:
        val = '0' + val
        df_2017.at[index, 'GEOID'] = val


# Merge with standard dataframe
standard_merged = pd.merge(df_2017, cdc, left_on='GEOID', right_on='UniqueID', how='inner')



# Construct Health Index Variables
####################################
standard_merged = standard_merged.rename(columns = {
    # Health Outcomes
    'Arthritis among adults aged >=18 Years': 'health_arthritis', #take inverse
    'Cancer (excluding skin cancer) among adults aged >=18 Years': 'health_cancer', #take inverse
    'Chronic kidney disease among adults aged >=18 Years': 'health_KdnyDisease', #take inverse
    'Chronic obstructive pulmonary disease among adults aged >=18 Years': 'health_PulDisease', #take inverse
    'Coronary heart disease among adults aged >=18 Years': 'health_HrtDisease', #take inverse
    'Current asthma among adults aged >=18 Years': 'health_asthma', #take inverse
    'Diagnosed diabetes among adults aged >=18 Years':'health_diab', #take inverse
    'High blood pressure among adults aged >=18 Years': 'health_HighBldPrs', #take inverse
    'High cholesterol among adults aged >=18 Years who have been screened in the past 5 Years': 'health_CholHigh', #take inverse
    'Mental health not good for >=14 days among adults aged >=18 Years':'health_GoodMent', #take inverse
    'Physical health not good for >=14 days among adults aged >=18 Years':'health_GoodPhys', #take inverse
    'Stroke among adults aged >=18 Years': 'health_stroke', #take inverse
    
    # Unhealthy Behaviors
    'Binge drinking among adults aged >=18 Years': 'behav_drink', #take inverse
    'Current smoking among adults aged >=18 Years': 'behav_smoking', #take inverse
    'No leisure-time physical activity among adults aged >=18 Years': 'behav_NoPhysAct', #take inverse
    'Obesity among adults aged >=18 Years': 'behav_obesity', #take inverse
    'Sleeping less than 7 hours among adults aged >=18 Years': 'behav_sleep', #take inverse
    
    
    #Preventative Care
    'Cholesterol screening among adults aged >=18 Years': 'prev_CholScreen',
    'Current lack of health insurance among adults aged 18–64 Years': 'prev_HlthInsur', #take inverse
    'Taking medicine for high blood pressure control among adults aged >=18 Years with high blood pressure': 'prev_BloodMed',
    'Visits to doctor for routine checkup within the past Year among adults aged >=18 Years': 'prev_DocVisit',
    'Mammography use among women aged 50–74 Years': 'prev_mammogram',
    'Papanicolaou smear use among adult women aged 21–65 Years': 'prev_smear',
    'Older adult men aged >=65 Years who are up to date on a core set of clinical preventive services: Flu shot past Year, PPV shot ever, Colorectal cancer screening':'prev_MenPrev',
    'Visits to dentist or dental clinic among adults aged >=18 Years': 'prev_DentVisits',
    'Fecal occult blood test, sigmoidoscopy, or colonoscopy among adults aged 50–75 Years': 'prev_tests',
    'Older adult women aged >=65 Years who are up to date on a core set of clinical preventive services: Flu shot past Year, PPV shot ever, Colorectal cancer screening, and Mammogram past 2 Years':'prev_WomPrev',
    
    #Internet connectivity
    'PERC Est_Total: With an Internet subscription: PRESENCE AND TYPES OF INTERNET SUBSCRIPTIONS IN HOUSEHOLD_tct17': 'inter_conrate'
    }
    )

# List of variables that need to be taken in inverse for indexing
inverse_vars = ['health_arthritis', 'health_cancer', 'health_KdnyDisease', 'health_PulDisease', 'health_HrtDisease', 'health_asthma', 'health_diab',
                  'health_HighBldPrs','health_CholHigh','health_GoodMent', 'health_GoodPhys','health_stroke','behav_drink','behav_smoking','behav_NoPhysAct',
                  'behav_obesity', 'prev_HlthInsur', 'behav_sleep']

# Comprehensive index variable list 
hlth_indx_vars = ['health_arthritis', 'health_cancer', 'health_KdnyDisease', 'health_PulDisease', 'health_HrtDisease', 'health_asthma', 'health_diab',
                  'health_HighBldPrs','health_CholHigh','health_GoodMent', 'health_GoodPhys','health_stroke','behav_drink','behav_smoking','behav_NoPhysAct',
                  'behav_obesity', 'prev_CholScreen','prev_HlthInsur', 'prev_BloodMed', 'prev_DocVisit', 'prev_DentVisits', 'behav_sleep', 'prev_mammogram',
                  'prev_smear',  'prev_MenPrev', 'prev_WomPrev', 'prev_tests']


for i in standard_merged.columns:
    if i in hlth_indx_vars:
        if i in inverse_vars:
            standard_merged[f'{i}_inv'] = 1-(standard_merged[i]/100)
            standard_merged[i] = (standard_merged[i]/100)
        else:
            standard_merged[i] = standard_merged[i]/100
            
            
            
# Comprehensive index variable list 
hlth_indx = ['health_arthritis_inv', 'health_cancer_inv', 'health_KdnyDisease_inv', 'health_PulDisease_inv', 'health_HrtDisease_inv', 'health_asthma_inv', 'health_diab_inv',
                  'health_HighBldPrs_inv','health_CholHigh_inv','health_GoodMent_inv', 'health_GoodPhys_inv','health_stroke_inv','behav_drink_inv','behav_smoking_inv','behav_NoPhysAct_inv',
                  'behav_obesity_inv', 'prev_CholScreen','prev_HlthInsur_inv', 'prev_BloodMed', 'prev_DocVisit', 'prev_DentVisits', 'behav_sleep_inv', 'prev_mammogram',
                  'prev_smear',  'prev_MenPrev', 'prev_WomPrev', 'prev_tests']

# index variable list: health outcomes
hlth_indx_outcomes = ['health_arthritis_inv', 'health_cancer_inv', 'health_KdnyDisease_inv', 'health_PulDisease_inv', 'health_HrtDisease_inv', 'health_asthma_inv', 'health_diab_inv',
                  'health_HighBldPrs_inv','health_CholHigh_inv','health_GoodMent_inv', 'health_GoodPhys_inv','health_stroke_inv']

# index variable list: unhealthy behaviors
hlth_indx_behav = ['behav_drink_inv','behav_smoking_inv','behav_NoPhysAct_inv','behav_obesity_inv', 'behav_sleep_inv']

# index variable list: preventative services
hlth_indx_prev = ['prev_CholScreen','prev_HlthInsur', 'prev_BloodMed', 'prev_DocVisit', 'prev_DentVisits','prev_mammogram','prev_smear',  'prev_MenPrev', 'prev_WomPrev', 'prev_tests']


# Comprehensive index, outcomes index, preventative services index
standard_merged['health_indx'] = standard_merged[hlth_indx].sum(axis=1)
standard_merged['health_indx_outcomes'] = standard_merged[hlth_indx_outcomes].sum(axis=1)
standard_merged['health_indx_behav'] = standard_merged[hlth_indx_behav].sum(axis=1)
standard_merged['health_indx_prev'] = standard_merged[hlth_indx_prev].sum(axis=1)

indexes = ['health_indx', 'health_indx_outcomes', 'health_indx_behav', 'health_indx_prev']

for indx in indexes:
    standard_merged[indx] = standard_merged[indx].replace(0, np.nan)




###################
##  Merge SVI data with standard dataframe
svi['FIPS'] = svi['FIPS'].astype('string')

for index, val in enumerate(svi['FIPS']):
    if len(val) == 10:
        val = '0' + val
        svi.at[index, 'FIPS'] = val

standard_merged_final = pd.merge(standard_merged, svi, left_on='GEOID', right_on='FIPS', how='inner')

# col_lst = list(standard_merged_final.columns)
# for e in col_lst:
#     print(e, '\n')


####################################
## Write to CSV 
standard_merged_final.to_csv('data/standard_dataframes/standard_merged_2017.csv.gz', compression='gzip', index=False)



