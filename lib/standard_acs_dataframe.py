import os
import sys
### add system path to get other library directories
sys.path[0] = os.path.join(os.path.abspath(''),'..')

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

import data_pipeline.spatial_operations as so

## This good city list are the cities that we want to complete the merge on
GOOD_CITY_LIST = [ 'boston', 'chicago', 'denver', 'detroit', 'houston', 'indianapolis', 'los-angeles', 'louisville','new-york-city','phoenix','portland','san-diego','san-jose','seattle','washington-dc']
GOOD_CITY_SHAPEFILE_LOCATIONS = {
    "boston": { "location" : "/tmp/city-data/boston/boston-boundaries/City_of_Boston_Boundary.shp", "state": "massachussetts"},
    "chicago": { "location" : "/tmp/city-data/chicago/chicago-boundaries/chicago_boundaries.shp", "state": "illinois"},
    "denver": { "location" : "/tmp/city-data/denver/denver-boundaries/county_boundary.shp", "state": "colorado"},
    "detroit": { "location" : "/tmp/city-data/detroit/detroit-boundaries/City_of_Detroit_Boundary.shp", "state": "michigan"},
    "houston": { "location" : "/tmp/city-data/houston/houston-boundaries/City_of_Houston_City_Limits_(Full_and_Limited_Purpose_Areas).shp", "state": "texas"},
    "indianapolis": { "location" : "/tmp/city-data/indianapolis/indianapolis-boundaries/Cities_and_Towns.shp", "state": "indiana"},
    "los-angeles": { "location" : "/tmp/city-data/los-angeles/los-angeles-boundaries/los-angeles-boundaries.shp", "state": "california"},
    "louisville": { "location" : "/tmp/city-data/louisville/louisville boundaries/louisville_boundaries.shp", "state": "kentucky"},
    "new-york-city": { "location" : "/tmp/city-data/new-york-city/nyc borough boundaries/nyc borough boundaries.shp", "state": "new-york"},
    "phoenix": { "location" : "/tmp/city-data/phoenix/phoenix boundaries/phoenix boundaries.shp", "state": "arizona"},
    "portland": { "location" : "/tmp/city-data/portland/portland-boundaries/portland-boundaries.shp", "state": "oregon"},
    "san-diego": { "location" : "/tmp/city-data/san-diego/san-diego-boundaries/san-diego-boundaries.shp", "state": "california"},
    "san-jose": { "location" : "/tmp/city-data/san-jose/san-jose-boundaries/san-jose-boundaries.shp", "state": "california"},
    "seattle": { "location" : "/tmp/city-data/seattle/seattle-boundaries/seattle-boundaries-v3.shp", "state": "washington"},
    "washington-dc": { "location" : "/tmp/city-data/washington-dc/washington-dc-boundaries/washington-dc-boundaries.shp", "state": "dc"},
}

# These city neighborhood shapefiles allow us to merge with the neighborhood boundary data
GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS = {
    "seattle": { "location" : "/tmp/neighborhood-data/seattle/seattle_ccn/City_Clerk_Neighborhoods.shp", "nhood_col" : 'HOODS_'},
    "denver": {"location": "/tmp/neighborhood-data/denver/denver_1.0.32/statistical_neighborhoods.shp", "nhood_col": "NBHD_NAME"},
    "washington-dc": {"location": "/tmp/neighborhood-data/washington-dc/DC_shapefile/Neighborhood_Clusters.shp", "nhood_col": "NAME"},
    "boston": {"location": "/tmp/neighborhood-data/boston/Boston_Neighborhoods/Boston_Neighborhoods.shp", "nhood_col": "Name"},
     "portland": {"location": "/tmp/neighborhood-data/portland/portland-neighborhood-boundaries/Neighborhood_Boundaries.shp", "nhood_col": "ID"},
    "houston": {"location": "/tmp/neighborhood-data/houston/Houston/Houston.shp", "nhood_col": "SNBNAME"},
    "indianapolis": { "location": "/tmp/neighborhood-data/indianapolis/Indy_Neighborhoods/Indy_Neighborhoods.shp", "nhood_col": "NAME"},
    "los-angeles": {"location": "/tmp/neighborhood-data/los-angeles/Los Angeles/Los Angeles.shp", "nhood_col": "display_na"},
    "phoenix": {"location": "/tmp/neighborhood-data/phoenix/phoenix/Villages.shp", "nhood_col": "NAME"},
    "san-francisco": { "location": "/tmp/neighborhood-data/san-francisco/SF Find Neighborhoods/geo_export_f62da660-837f-478c-9ba4-ceb40e9ed8eb.shp", "nhood_col": "name"},
    "austin": {"location": "/tmp/neighborhood-data/austin/Neighborhoods/geo_export_81d98617-c469-49e1-9bf6-3ef25c07d0c6.shp", "nhood_col": "neighname"},
    "dallas": { "location": "/tmp/neighborhood-data/dallas/Councils/Councils.shp", "nhood_col": "COUNCIL"},
    "san-jose": { "location": "/tmp/neighborhood-data/san-jose/Zip_Code_Boundary/Zip_Code_Boundary.shp","nhood_col": "ZIPCODE"},
    "san-diego": {"location": "/tmp/neighborhood-data/san-diego/CommunityPlanningAreas/cmty_plan_datasd.shp","nhood_col": "cpname"},
    "baltimore": {"location": "/tmp/neighborhood-data/baltimore/neighborhoods/baltimore.shp","nhood_col": "Name"},
    "detroit": {"location": "/tmp/neighborhood-data/detroit/neighborhoods/detroit.shp", "nhood_col": "name"},
    "louisville": {"location": "/tmp/neighborhood-data/louisville/neighborhoods/louisville.shp", "nhood_col": "NH_NAME"},
    "new-york-city": {"location": "/tmp/neighborhood-data/new-york-city/nycd_22a/nycd.shp", "nhood_col": "BoroCD"},
    "chicago": {"location": "/tmp/neighborhood-data/chicago/neighborhoods/geo_export_24517513-d42b-43b9-a525-49bfe729d213.shp", "nhood_col": "pri_neigh" }
    }

# Read in the ACS columns of interest
FILE_2021 = open("/tmp/acs_data/2021_columns.json", "r")
COL_2021 = list(json.load(FILE_2021).values())
FILE_2017 = open("/tmp/acs_data/2017_columns.json", "r")
COL_2017 = list(json.load(FILE_2017).values())

# Read in the ACS_categories file for percentage calculation
ACS_CAT_FILE = open("/tmp/acs_data/acs_categories.json", "r")
ACS_CAT = json.load(ACS_CAT_FILE)
    

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
    merged_df.rename(columns={"TRACTCE":"tract"}, inplace = True)
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
    
    percentages = {}
    
    city_df_copy = city_df.copy()
    
    if year == '2021':
        for col in COL_2021:
            if col == "Estimate!!Total: TOTAL POPULATION":
                continue
            if col in ACS_CAT.keys():
                total_est = ACS_CAT[col]
                curr_col_perc = city_df[col] / city_df[total_est]
                perc_key = f"PERC {col}"
                city_df_copy[perc_key] = curr_col_perc
    else:
        for col in COL_2017:
            if col == "Estimate!!Total: TOTAL POPULATION": #potentially skip over race columns here
                continue
            if col in ACS_CAT.keys():
                total_est = ACS_CAT[col]
                curr_col_perc = city_df[col] / city_df[total_est]
                perc_key = f"PERC {col}"
                city_df_copy[perc_key] = curr_col_perc
        
    return city_df_copy


def get_race_percentages(city_df):
    '''
    This function computes the proper percentages for the race columns and adds
    percentage columns to the dataframe
    
    Inputs:
      city_df: The ACS merged city-level dataframe
      
    Outputs:
      acs_df: The ACS merged city-level dataframe with race percentages
    '''
    # cleaning column names
    RACE_CAT_FILE = open("/tmp/lib/race_categories.json", "r")
    RACE_CAT = json.load(RACE_CAT_FILE)
    acs_df_clean = city_df.rename(columns=RACE_CAT)
    # applying cleaned column names to original dataset
    acs_df = acs_df_clean.copy()
    # cleaning column names v2 and conglomerating "Other" race
    acs_df['Hispanic (of any race)'] = acs_df['H/L']
    acs_df['Non-Hispanic White'] = acs_df['Not H/L: White alone']
    acs_df['Non-Hispanic Black'] = acs_df['Not H/L: Black alone']
    acs_df['Non-Hispanic Asian'] = acs_df['Not H/L: Asian alone']
    acs_df['Non-Hispanic American Indian'] = acs_df['Not H/L: American Indian/Native alone']
    acs_df['Non-Hispanic Other'] = acs_df['Not H/L: Native Hawaiian / PI alone'] + acs_df['Not H/L: Other race alone'] + acs_df['Not H/L: Two or more races']
    
    # creating total population column
    acs_df['Total Race Population'] = acs_df['H/L'] + acs_df['Not H/L: White alone'] + acs_df['Not H/L: Black alone'] + acs_df['Not H/L: Asian alone'] + acs_df['Not H/L: American Indian/Native alone'] + acs_df['Non-Hispanic Other']
    
    # creating race pct columns per census tract
    acs_df['% Hispanic (of any race)'] = ((acs_df['Hispanic (of any race)']/acs_df['Total Race Population']))
    acs_df['% Non-Hispanic White'] = ((acs_df['Non-Hispanic White']/acs_df['Total Race Population']))
    acs_df['% Non-Hispanic Black'] = ((acs_df['Non-Hispanic Black']/acs_df['Total Race Population']))
    acs_df['% Non-Hispanic Asian'] = ((acs_df['Non-Hispanic Asian']/acs_df['Total Race Population']))
    acs_df['% Non-Hispanic American Indian'] = ((acs_df['Non-Hispanic American Indian']/acs_df['Total Race Population']))
    acs_df['% Non-Hispanic Other'] = ((acs_df['Non-Hispanic Other']/acs_df['Total Race Population']))
    
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
        cols_of_int = ['tract', 'state', 'county', 'STATEFP', 'COUNTYFP'] + ['geometry'] + COL_2021
    else:
        cols_of_int = ['tract', 'state', 'county', 'STATEFP', 'COUNTYFP'] + ['geometry'] + COL_2017

    city_merged_df_copy = city_merged_df[cols_of_int]

    city_merged_df_copy.insert(0, 'City', city)
    
    # CALL TO RACE FUNCTION HERE!!
    city_merged_df_copy = get_race_percentages(city_merged_df_copy)
    
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
    state_tiger_path = f"/tmp/state-data/{year}/"
    acs_data = pd.read_csv(f'/tmp/acs_data/acs_5yr_{year}.csv')
    acs_data = acs_data.groupby('tract').mean().reset_index()
    
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
        city_tiger_merge = merge_data(city_shapefile_df, state_tiger_data, f"/tmp/city-data/{city}/city-tiger-merge-{year}.geojson")
        
        ## Initial Merge with ACS data
        # merge with ACS data
        city_acs_merge_df = city_tiger_merge.merge(acs_data, how='left', on='tract')
        # clean up standard dataframe data
        standard_city_df = get_standard_df(city_acs_merge_df, year, city)
        
        ## Merge with neighborhood boundaries (if we have data for them)
        if city in GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS.keys():
            city_nhood = geopandas.read_file(GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS[city]['location'])
            city_nhood = city_nhood[[GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS[city]['nhood_col'], 'geometry']]
            city_nhood = city_nhood.rename({GOOD_CITY_NHOOD_SHAPEFILE_LOCATIONS[city]['nhood_col']: 'Neighborhood'}, axis='columns')
            standard_city_df = geopandas.sjoin(standard_city_df, city_nhood, how="inner", op='intersects')
        else:
            standard_city_df['Neighborhood'] = pd.NA
        
        ## save city merged dataframe to a file
        standard_city_df.to_file(f"/tmp/city-data/{city}/city-acs-merge-{year}.geojson", driver="GeoJSON")
        
        
        ## add to the list of standard city dataframes
        standard_city_dataframes.append(standard_city_df)
        
        # produce plot of TIGER level data for error checkings               
        city_tiger_vis = city_tiger_merge.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', )
        cx.add_basemap(city_tiger_vis, crs=city_tiger_merge.crs, source=cx.providers.Stamen.TonerLite, zoom=12)
        city_tiger_vis.set_title(f"{city} {year} TIGER merge visualization")

        print("\n")
    
    # concatenate all of the standard city level dataframes into a single dataframe
    std_acs_censustract_df = pd.concat(standard_city_dataframes)
    std_acs_censustract_df.to_csv(f"/tmp/data/standard_acs_censustract_df_{year}.csv")
    std_acs_censustract_df.to_file(f"/tmp/data/standard_acs_censustract_df_{year}.geojson", driver="GeoJSON")
