#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:10:41 2023

@author: chandlerhall
"""
import zipfile
import os
import pandas as pd
import numpy as np
import sys

############
# load standard dataframes
os.chdir('/Users/chandlerhall/Desktop/Github/broadbandequity')

### Correlations

df = pd.read_csv('data/standard_dataframes/standard_merged_2017.csv')

# Comprehensive index variable list 
hlth_indx_vars = ['health_arthritis_inv', 'health_cancer_inv', 'health_KdnyDisease_inv', 'health_PulDisease_inv', 'health_HrtDisease_inv', 'health_asthma_inv', 'health_diab_inv',
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


corr_report = []
for col in hlth_indx_vars:
    corr = df['inter_conrate'].corr(df[col])
    corr_report.append(corr)
 
    
indexes = ['health_indx', 'health_indx_outcomes', 'health_indx_behav', 'health_indx_prev']
for col in indexes:
    corr = df['inter_conrate'].corr(df[col])
    corr_report.append(corr)

   
col_list = hlth_indx_vars + indexes
    
corr_report_df = pd.DataFrame({'Health Variables': col_list,
                               'Correlations': corr_report})


corr_report_df.to_csv('data/corr_report.csv', index = False)
