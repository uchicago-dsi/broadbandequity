#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:10:41 2023

@author: chandlerhall
"""
import os
import pandas as pd
import sys
from scipy.stats import pearsonr


############
# load standard dataframes
os.chdir(os.path.join(os.path.abspath(''),'..'))

df_corr = pd.read_csv('data/standard_dataframe/standard_merged_2017.csv')



# Comprehensive index variable list 
hlth_indx_vars = ['health_arthritis_inv', 'health_cancer_inv', 'health_KdnyDisease_inv', 'health_PulDisease_inv', 'health_HrtDisease_inv', 'health_asthma_inv', 'health_diab_inv',
                  'health_HighBldPrs_inv','health_CholHigh_inv','health_GoodMent_inv', 'health_GoodPhys_inv','health_stroke_inv','behav_drink_inv','behav_smoking_inv','behav_NoPhysAct_inv',
                  'behav_obesity_inv', 'prev_CholScreen','prev_HlthInsur_inv', 'prev_BloodMed', 'prev_DocVisit', 'prev_DentVisits', 'behav_sleep_inv', 'prev_mammogram',
                  'prev_smear',  'prev_MenPrev', 'prev_WomPrev', 'prev_tests']




def run_correlations(df_corr, hlth_indx_vars, hlth_indx_behav, hlth_indx_prev):
    '''
    Using standard dataframe, run correlation report on all health indicators and internet connectivity, then save as csv to data folder

    Parameters
    ----------
    df_corr : pd.DataFrame
        2017 standard dataframe
    hlth_indx_vars : list
        Variables to include in correlation report

    Returns
    -------
    CSV of correlation report saved to data folder

    '''
    corr_report = []
    p_val = []
    for col in hlth_indx_vars:
        df_corr = df_corr.dropna(subset=[col])
        corr, p_value = pearsonr(df_corr['inter_conrate'], df_corr[col])
        corr_report.append(corr)
        p_val.append(p_value)
     
        
    indexes = ['health_indx', 'health_indx_outcomes', 'health_indx_behav', 'health_indx_prev']
    for col in indexes:
        corr, p_value = pearsonr(df_corr['inter_conrate'], df_corr[col])
        corr_report.append(corr)
        p_val.append(p_value)


    col_list = hlth_indx_vars + indexes
        
    corr_report_df = pd.DataFrame({'Health Variables': col_list,
                                   'Correlations': corr_report,
                                   'P-Values': p_val})


    corr_report_df.to_csv('data/corr_report.csv', index = False)
    return


run_correlations(df_corr, hlth_indx_vars)