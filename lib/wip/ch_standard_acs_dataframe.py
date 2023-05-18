#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 13:07:48 2023

@author: chandlerhall
"""

import os
import sys
### add system path to get other library directories
sys.path[0] = os.path.abspath('') #.join(os.path.abspath(''),'..')
sys.path[0]

import geopandas
import warnings
import pandas as pd
import math
import statistics
import matplotlib.pyplot as plt
import contextily as cx
import zipfile
import glob
import json
warnings.filterwarnings('ignore')

## This good city list are the cities that we want to complete the merge on - we have 35 cities currently
GOOD_CITY_LIST = ['arlington', 'atlanta','austin', 'bakersfield', 'boston', 'chicago', 'dallas', 'denver', 'detroit', 'el-paso', 'fort-worth', 'fresno', 'houston', 'indianapolis', 'kansas-city', 'los-angeles', 'louisville', 'memphis', 'mesa', 'minneapolis', 'new-york-city', 'oklahoma-city', 'omaha', 'philadelphia', 'phoenix', 'portland', 'sacramento', 'san-antonio', 'san-diego', 'san-jose', 'seattle', 'tulsa', 'tuscon', 'washington-dc', 'wichita']

## Dictionary: city:state
CITY_DICT = {'arlington':'texas',
             'atlanta':'georgia',
             'austin':'texas',
             'bakersfield':'california',
             'boston':'massachusetts',
             'chicago':'illinois',
             'dallas':'texas',
             'denver':'colorado',
             'detroit':'michigan',
             'el-paso':'texas',
             'fort-worth':'texas',
             'fresno':'california',
             'houston':'texas',
             'indianapolis':'indiana',
             'kansas-city':'kansas',
             'los-angeles':'california',
             'louisville':'kentucky',
             'memphis': 'tennessee',
             'mesa': 'arizona',
             'minneapolis':'minnesota',
             'new-york-city':'new-york',
             'oklahoma-city':'oklahoma',
             'omaha':'nebraska',
             'philadelphia':'pennsylvania',
             'phoenix':'arizona',
             'portland':'oregon',
             'sacramento':'california',
             'san-antonio':'texas',
             'san-diego':'california',
             'san-jose':'california',
             'seattle':'washington',
             'tulsa':'oklahoma',
             'tuscon':'arizona',
             'washington-dc':'dc',
             'wichita':'kansas'}

# Create dictionary to locate city shapefiles
GOOD_CITY_SHAPEFILE_LOCATIONS = {}
for city in CITY_DICT:
    GOOD_CITY_SHAPEFILE_LOCATIONS.update({city:{'location':f'{sys.path[0]}/data/boundary-shapefiles/city-boundaries/{city}/{city}-boundaries/{city}-boundaries.shp','state':f'{CITY_DICT[city]}'}})
    
# These are the directory locations of the city neighborhood shapefiles allow us to merge with the neighborhood boundary data
GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS = {
    "seattle": { "location" : "/tmp/data/boundary-shapefiles/neighborhood-boundaries/seattle/seattle_ccn/City_Clerk_Neighborhoods.shp", "nhood_col" : 'HOODS_'},
    "denver": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/denver/denver_1.0.32/statistical_neighborhoods.shp", "nhood_col": "NBHD_NAME"},
    "washington-dc": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/washington-dc/DC_shapefile/Neighborhood_Clusters.shp", "nhood_col": "NAME"},
    "boston": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/boston/Boston_Neighborhoods/Boston_Neighborhoods.shp", "nhood_col": "Name"},
     "portland": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/portland/portland-neighborhood-boundaries/Neighborhood_Boundaries.shp", "nhood_col": "ID"},
    "houston": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/houston/Houston/Houston.shp", "nhood_col": "SNBNAME"},
    "indianapolis": { "location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/indianapolis/Indy_Neighborhoods/Indy_Neighborhoods.shp", "nhood_col": "NAME"},
    "los-angeles": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/los-angeles/Los Angeles/Los Angeles.shp", "nhood_col": "display_na"},
    "phoenix": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/phoenix/phoenix/Villages.shp", "nhood_col": "NAME"},
    "san-francisco": { "location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/san-francisco/SF Find Neighborhoods/geo_export_f62da660-837f-478c-9ba4-ceb40e9ed8eb.shp", "nhood_col": "name"},
    "austin": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/austin/Neighborhoods/geo_export_81d98617-c469-49e1-9bf6-3ef25c07d0c6.shp", "nhood_col": "neighname"},
    "dallas": { "location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/dallas/Councils/Councils.shp", "nhood_col": "COUNCIL"},
    "san-jose": { "location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/san-jose/Zip_Code_Boundary/Zip_Code_Boundary.shp","nhood_col": "ZIPCODE"},
    "san-diego": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/san-diego/CommunityPlanningAreas/cmty_plan_datasd.shp","nhood_col": "cpname"},
    "baltimore": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/baltimore/neighborhoods/baltimore.shp","nhood_col": "Name"},
    "detroit": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/detroit/neighborhoods/detroit.shp", "nhood_col": "name"},
    "louisville": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/louisville/neighborhoods/louisville.shp", "nhood_col": "NH_NAME"},
    "new-york-city": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/new-york-city/nycd_22a/nycd.shp", "nhood_col": "BoroCD"},
    "chicago": {"location": "/tmp/data/boundary-shapefiles/neighborhood-boundaries/chicago/neighborhoods/geo_export_24517513-d42b-43b9-a525-49bfe729d213.shp", "nhood_col": "pri_neigh" }
    }

# Read in the ACS columns of interest
FILE_2021 = open(f"{sys.path[0]}/data/acs_data/2021_columns.json", "r")
COL_2021 = list(json.load(FILE_2021).values())
FILE_2017 = open(f"{sys.path[0]}/data/acs_data/2017_columns.json", "r")
COL_2017 = list(json.load(FILE_2017).values())

# Read in the ACS_categories file for percentage calculation
ACS_CAT_FILE_2017 = open(f"{sys.path[0]}/data/acs_data/acs_categories_2017.json", "r")
ACS_CAT_2017 = json.load(ACS_CAT_FILE_2017)
ACS_CAT_FILE_2021 = open(f"{sys.path[0]}/data/acs_data/acs_categories_2021.json", "r")
ACS_CAT_2021 = json.load(ACS_CAT_FILE_2021)

def merge_data(city_df, ctract_df,  merged_df_path):
    '''
    This function takes the city boundary data and census level data, merges them, and writes
    the merged df to a specified file location.
    
    Inputs:
      nhood_df: dataframe to go on outside (in this case neighborhood df)
      ctract_df: dataframe to go within the other df (census tract fcc_df)
      merged_df_path (str): Path to put the new merged dataframe
      nhood_col (str): String indicator of the name of the column for neighborhood IDs
    Returns:
      merged_df: merged dataframe, which this functions saves as csv to file location
    '''
    
    # get city into correct crs
    city_df = city_df.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
    
    # should work if geographies are in the same format
    merged_df = geopandas.sjoin(ctract_df, city_df, how="inner", op='intersects')
    #merged_df = merged_df.drop_duplicates(subset='GEOID', keep=False)
    merged_df.rename(columns={"TRACTCE":"tract", "STATEFP":"state", "COUNTYFP":"county"}, inplace = True)
    merged_df['tract'] = merged_df['tract'].astype(int)
    merged_df = merged_df.drop_duplicates(subset='GEOID', keep='first')
    merged_df.to_file(merged_df_path, driver="GeoJSON")
    return merged_df.copy()

def get_percentages(city_df, year):
    '''
    This function prepares a merged dataframe with ACS columns and computes
    the percentages of total households in each of the columns of interest
    
    Inputs:
      city_df: the standard city dataframe merge with ACS data
    
    Outputs:
      city_df_copy: The dataframe with columns for percentages added on
    '''
    
    city_df_copy = city_df.copy()
    
    if year == '2021':
        for col in COL_2021:
            if col == 'Est_Total: TOTAL POPULATION_tct21':
                continue
            if col in ACS_CAT_2021.keys():
                curr_col_perc = city_df[col] / city_df_copy['Est_Total: TOTAL POPULATION_tct21']
                perc_key = f"PERC {col}"
                city_df_copy[perc_key] = curr_col_perc
    else:
        for col in COL_2017:
            if col == 'Est_Total: TOTAL POPULATION_tct17':
                continue
            if col in ACS_CAT_2017.keys():
                curr_col_perc = city_df[col] / city_df_copy['Est_Total: TOTAL POPULATION_tct17']
                perc_key = f"PERC {col}"
                city_df_copy[perc_key] = curr_col_perc
        
    return city_df_copy

def get_race_percentages(city_df, year):
    '''
    This function computes the proper percentages for the race columns and adds
    percentage columns to the dataframe
    
    Inputs:
      city_df: The ACS merged city-level dataframe
      
    Outputs:
      acs_df: The ACS merged city-level dataframe with race percentages
    '''
    # cleaning column names
    if year == '2021':
        RACE_CAT_FILE = open(f"{sys.path[0]}/lib/race_categories_2021.json", "r")
        str_yr = "_tct21"
    else:
        RACE_CAT_FILE = open(f"{sys.path[0]}/lib/race_categories_2017.json", "r")
        str_yr = "_tct17"
    RACE_CAT = json.load(RACE_CAT_FILE)
    acs_df_clean = city_df.rename(columns=RACE_CAT)
    # applying cleaned column names to original dataset
    acs_df = acs_df_clean.copy()
    # cleaning column names v2 and conglomerating "Other" race
    acs_df[f'Non-Hispanic Other{str_yr}'] = acs_df[f'Not H/L: Native Hawaiian / PI alone{str_yr}'] + acs_df[f'Not H/L: Other race alone{str_yr}'] + acs_df[f'Not H/L: Two or more races{str_yr}']
    
    # creating total population column
    acs_df[f'Total Race Population{str_yr}'] = acs_df[f'Hispanic (of any race){str_yr}'] + acs_df[f'Non-Hispanic White{str_yr}'] + acs_df[f'Non-Hispanic Black{str_yr}'] + acs_df[f'Non-Hispanic Asian{str_yr}'] + acs_df[f'Non-Hispanic American Indian{str_yr}'] + acs_df[f'Non-Hispanic Other{str_yr}']
    
    # creating race pct columns per census tract
    acs_df[f'% Hispanic (of any race){str_yr}'] = ((acs_df[f'Hispanic (of any race){str_yr}']/acs_df[f'Total Race Population{str_yr}']))
    acs_df[f'% Non-Hispanic White{str_yr}'] = ((acs_df[f'Non-Hispanic White{str_yr}']/acs_df[f'Total Race Population{str_yr}']))
    acs_df[f'% Non-Hispanic Black{str_yr}'] = ((acs_df[f'Non-Hispanic Black{str_yr}']/acs_df[f'Total Race Population{str_yr}']))
    acs_df[f'% Non-Hispanic Asian{str_yr}'] = ((acs_df[f'Non-Hispanic Asian{str_yr}']/acs_df[f'Total Race Population{str_yr}']))
    acs_df[f'% Non-Hispanic American Indian{str_yr}'] = ((acs_df[f'Non-Hispanic American Indian{str_yr}']/acs_df[f'Total Race Population{str_yr}']))
    acs_df[f'% Non-Hispanic Other{str_yr}'] = ((acs_df[f'Non-Hispanic Other{str_yr}']/acs_df[f'Total Race Population{str_yr}']))
    
    return acs_df
    

def get_standard_df(city_merged_df, year, city):
    '''
    This function prepares a merged dataframe into the standard format so it 
    is ready to go into the standard_censustract_dataframe
    
    Inputs:
      city_merged_df
    Outputs:
      city_standard_df
    '''
    if year == '2021':
        cols_of_int = ['tract', 'state', 'county', 'GEOID'] + ['geometry'] + COL_2021
    else:
        cols_of_int = ['tract', 'state', 'county', 'GEOID'] + ['geometry'] + COL_2017

    city_merged_df_copy = city_merged_df[cols_of_int]

    city_merged_df_copy.insert(0, 'City', city)
    #city_merged_df_copy = city_merged_df_copy.rename({'STATEFP': 'State ID', 'COUNTYFP': 'County ID'}, axis='columns')
    
    # CALL TO RACE FUNCTION HERE!!
    city_merged_df_copy = get_race_percentages(city_merged_df_copy, year)
    
    #need to solve percentages issue still
    city_merged_df_copy = get_percentages(city_merged_df_copy, year)
    
    return city_merged_df_copy

    
    
def plot_boxplots(city_fcc_df, nhood_col, title):
    '''
    Plot basic boxplot for city_fcc_df.
    
    Inputs:
      city_fcc_df (Pandas): City fcc df (neighborhood data merged with FCC data)
      nhood_col (str): Column name for neighborhood indicators
      title (str): Title for boxplot figure
    
    Outputs:
      Boxplot
    '''
    
    city_fcc_df.boxplot(column='f_broadband', by='geoid', rot=90, figsize=(15,10), grid=False,
                       fontsize=8, color='green')
    plt.ylabel('f_broadband')
    plt.xlabel('Neighborhood Indicator')
    plt.title(title)
    plt.suptitle('')
    


def get_neighborhood_proportions(standard_city_df, city_nhood):
    '''
    Compute proportion of census tracts that overlap neighborhood and
    add a new column to the dataframe
    
    Inputs:
      standard_city_df (dataframe)
      city_nhood (dataframe)
      
    Outputs:
      ctract_overlaps (list)
    '''
    ctract_overlaps = []
    for index, ctract in standard_city_df.iterrows():
        if ctract['Neighborhood']:
            curr_nhood = city_nhood.loc[city_nhood['Neighborhood'] == ctract['Neighborhood']]
            curr_intersection = curr_nhood['geometry'].buffer(0).intersection(ctract['geometry'].buffer(0))
            overlap = curr_intersection.area / ctract['geometry'].area
            try:
                ctract_overlaps.append(overlap.item())
            except:
                ctract_overlaps.append(pd.NA)
        else:
            ctract_overlaps.append(pd.NA)
    
    return ctract_overlaps


def checking_ids(standard_df):
    checking_ids = {
        "arlington": {"state": 48, "county": [439]}, # Tarrant
        "atlanta": {"state": 13, "county": [121, 89]}, # Fulton, DeKalb
        "austin": {"state": 48, "county": [209, 453, 491]}, # Hays, Travis, Williamson
        "bakersfield": {"state": 6, "county": [29]}, # Kern
        "baltimore": {"state": 24, "county": [510]}, # Baltimore city (independent; not in Baltimore County)
        "boston": {"state": 25, "county": [25]}, # Suffolk
        "chicago": {"state": 17, "county": [31, 43]}, # Cook, DuPage
        "colorado-city": {"state": 8, "county": [101]}, # Pueblo
        "dallas": {"state": 48, "county": [113, 85, 121]}, # Dallas, Collin, Denton
        "denver": {"state": 8, "county": [31]}, # Denver
        "detroit": {"state": 26, "county": [163]}, # Wayne
        "el-paso": {"state": 48, "county": [141]}, # El Paso
        "fort-worth": {"state": 48, "county": [121, 367, 439]}, # Denton, Parker, Tarrant
        "fresno": {"state": 6, "county": [19]}, # Fresno
        "houston": {"state": 48, "county": [201, 157, 339]}, # Harris, Fort Bend, Montgomery
        "indianapolis": {"state": 18, "county": [97]}, # Marion
        "kansas-city": {"state": 29, "county": [95, 47, 165, 37]}, # Jackson, Clay, Platte, Cass
        "long-beach": {"state": 6, "county": [37]}, # Los Angeles
        "los-angeles": {"state": 6, "county": [37]}, # Los Angeles
        "louisville": {"state": 21, "county": [111]}, # Jefferson
        "memphis": {"state": 47, "county": [157]}, # Shelby
        "mesa": {"state": 4, "county": [13]}, # Maricopa
        "miami": {"state": 12, "county": [86]}, # Miami-Dade
        "minneapolis": {"state": 27, "county": [53]}, # Hennepin
        "new-york-city": {"state": 36, "county": [47, 81, 61, 5, 85]}, # Kings, Queens, New York, Bronx, Richmond
        "oakland": {"state": 6, "county": [1]}, # Alameda
        "oklahoma-city": {"state": 40, "county": [109, 27, 17, 125]}, # Oklahoma, Cleveland, Canadian, Pottawatomie
        "omaha": {"state": 31, "county": [55]}, # Douglas
        "philadelphia": {"state": 42, "county": [101]}, # Philadelphia
        "phoenix": {"state": 4, "county": [13]}, # Maricopa
        "portland": {"state": 41, "county": [51, 5, 67]}, # Multnomah, Clackamas, Washington
        "raleigh": {"state": 37, "county": [183, 63]}, # Wake, Durham
        "sacramento": {"state": 6, "county": [67]}, # Sacramento
        "san-antonio": {"state": 48, "county": [29, 325]}, # Bexar, Medina
        "san-diego": {"state": 6, "county": [73]}, # San Diego
        "san-jose": {"state": 6, "county": [85]}, # Santa Clara
        "seattle": {"state": 53, "county": [33]}, # King
        "tulsa": {"state": 40, "county": [143, 113, 131, 145]}, # Tulsa, Osage, Rogers, Wagoner
        "tuscon": {"state": 4, "county": [19]}, # Pima
        "virginia-beach": {"state": 51, "county": [810]}, # Virginia Beach city (independent)
        "washington-dc": {"state": 11, "county": [1]}, # DC
        "wichita": {"state": 20, "county": [173]} # Sedgwick
    }

    id_check = []

    for index, row in standard_df.iterrows():
        curr_city = row['City']
        if (row['state'] == checking_ids[curr_city]['state']) & (row['county'] in checking_ids[curr_city]['county']):
            id_check.append(1)
        else:
            id_check.append(0)

    standard_df['Correct tract and county?'] = id_check
    return standard_df


def generate_dataframe_and_plots( city_name_str = None, year='2021'):
    '''
    THIS IS THE FUNCTION THAT SHOULD BE CALLED FROM OUTSIDE OF THE CODE
    This code creates a standard ACS dataframe for a group of cities of interest.
    For each city, it merges city boundary data, Census Tract TIGER data, ACS Data, 
    and city neighborhood boundaries data. It cleans this dataframe and computes percentages
    for given columns. It then combines all of the city-level merged dataframes into a single
    standard ACS dataframe which is written into the data folder of the repository in both 
    geojson and csv formats.
    
    Inputs:
      city_name_str (opt): if we want to only look at one city of interest
      year (opt): Year of 5 yr ACS merge to do
    
    Outputs:
      Displays maps of the TIGER-level census tracts for each city (for error checking)
      Write the standard ACS dataframes to files in the data folder
    '''
    
    if city_name_str is not None:
        city_name_list = [city_name_str]    
    else:
        city_name_list = GOOD_CITY_LIST

    # create list of standard city dataframes (to later be merged together into one)
    standard_city_dataframes = []
    
    # read in the data to be merged
    state_tiger_path = f"/tmp/data/TIGER-census-data/{year}/"
    acs_data = pd.read_csv(f'/tmp/data/acs_data/acs_5yr_{year}.csv')
    acs_data = acs_data.groupby(['tract', 'county', 'state']).mean().reset_index()
    
    # go through each city and compute the standard_city_df
    for idx, city in enumerate( city_name_list):
        print(f"Running {city}, {idx+1} of {len(city_name_list)}")
        # read in city boundary shapefile
        city_shapefile_df = geopandas.read_file(GOOD_CITY_SHAPEFILE_LOCATIONS[city]["location"])
        city_shapefile_df = city_shapefile_df.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})

        ### CREATE MERGED DATAFRAME
        ## "middle merge"
        # read in state data:
        state = GOOD_CITY_SHAPEFILE_LOCATIONS[city]["state"]
        state_tiger_shapefile_path = f"{state_tiger_path}{state}/{state}.shp"
        state_tiger_data = geopandas.read_file(state_tiger_shapefile_path)
        # merge city boundary data with TIGER data
        city_tiger_merge = merge_data(city_shapefile_df, state_tiger_data, f"/tmp/data/boundary-shapefiles/city-boundaries/{city}/city-tiger-merge-{year}.geojson")
        
        ## Initial Merge with ACS data
        # merge with ACS data
        acs_data['tract'] = acs_data['tract'].astype(int)
        acs_data['state'] = acs_data['state'].astype(int)
        acs_data['county'] = acs_data['county'].astype(int)
        city_tiger_merge['tract'] = city_tiger_merge['tract'].astype(int)
        city_tiger_merge['state'] = city_tiger_merge['state'].astype(int)
        city_tiger_merge['county'] = city_tiger_merge['county'].astype(int)
        city_acs_merge_df = pd.merge(city_tiger_merge, acs_data,  how='left', 
                                                   left_on=['tract','county', 'state'], right_on=['tract','county', 'state'])
        # clean up standard dataframe data
        standard_city_df = get_standard_df(city_acs_merge_df, year, city)
        
        ## Merge with neighborhood boundaries (if we have data for them)
        if city in GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS.keys():
            city_nhood = geopandas.read_file(GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS[city]['location'])
            city_nhood.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
            standard_city_df.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
            city_nhood = city_nhood[[GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS[city]['nhood_col'], 'geometry']]
            city_nhood = city_nhood.rename({GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS[city]['nhood_col']: 'Neighborhood'}, axis='columns')
            if 'index_right' in standard_city_df.columns:
                standard_city_df = standard_city_df.drop('index_right', axis=1)
            standard_city_df = geopandas.sjoin(standard_city_df, city_nhood, how="left", op='intersects')
            nhood_overlaps = get_neighborhood_proportions(standard_city_df, city_nhood)
            standard_city_df['% of Tract within Neighborhood'] = nhood_overlaps
            if 'index_right' in standard_city_df.columns:
                standard_city_df = standard_city_df.drop('index_right', axis=1)
        else:
            standard_city_df['Neighborhood'] = pd.NA
            standard_city_df['% of Tract within Neighborhood'] = pd.NA
        
        ## save city merged dataframe to a file
        standard_city_df.to_file(f"/tmp/data/boundary-shapefiles/city-boundaries/{city}/city-acs-merge-{year}.geojson", driver="GeoJSON")
        
        
        ## add to the list of standard city dataframes
        standard_city_dataframes.append(standard_city_df)
        
        # produce plot of TIGER level data for error checking            
        city_tiger_vis = city_tiger_merge.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', )
        cx.add_basemap(city_tiger_vis, crs=city_tiger_merge.crs, source=cx.providers.Stamen.TonerLite, zoom=12)
        city_tiger_vis.set_title(f"{city} {year} TIGER merge visualization")

        print("\n")
    
    # concatenate all of the standard city level dataframes into a single dataframe
    std_acs_censustract_df = pd.concat(standard_city_dataframes)
    
    # CALL TO ID CHECK FUNCTION
    std_acs_censustract_df = checking_ids(std_acs_censustract_df)
    
    # replace implausibly small numbers
    num = std_acs_censustract_df._get_numeric_data()
    num[num < 0] = pd.NA
    
    std_acs_censustract_df.to_csv(f"/tmp/data/standard_dataframes/standard_acs_censustract_df_{year}.csv", index=False)
    std_acs_censustract_df.to_file(f"/tmp/data/standard_dataframes/standard_acs_censustract_df_{year}.geojson", driver="GeoJSON")