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

### use glob to create a list of cities which are in the neighborhoo-data directory
#GOOD_CITY_LIST = [x.split('/')[2] for x in glob.glob('../city-data/*/')]
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

FILE_2021 = open("/tmp/acs_data/2021_columns.json", "r")
COL_2021 = list(json.load(FILE_2021).values())

FILE_2017 = open("/tmp/acs_data/2017_columns.json", "r")
COL_2017 = list(json.load(FILE_2017).values())
    

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
            curr_col_perc = []
            for i in city_df[col]:
                curr_col_perc = i / city_df["Estimate!!Total: TOTAL POPULATION"]
            perc_key = f"PERC {col}"
            city_df_copy.insert(7, perc_key, curr_col_perc)
    else:
        for col in COL_2017:
            if col == "Estimate!!Total: TOTAL POPULATION":
                continue
            curr_col_perc = []
            for i in city_df[col]:
                curr_col_perc = i / city_df["Estimate!!Total: TOTAL POPULATION"]
            perc_key = f"PERC {col}"
            city_df_copy.insert(7, perc_key, curr_col_perc)
        
    return city_df_copy

    
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
        cols_of_int = ['state', 'county', 'STATEFP', 'COUNTYFP', 'geometry'] + COL_2021
    else:
        cols_of_int = ['state', 'county', 'STATEFP', 'COUNTYFP', 'geometry'] + COL_2017

    city_merged_df_copy = city_merged_df[cols_of_int]

    city_merged_df_copy.insert(0, 'City', city)
    
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

    if city_name_str is not None:
        city_name_list = [city_name_str]    
    else:
        city_name_list = GOOD_CITY_LIST

    standard_city_dataframes = []
    
    state_tiger_path = f"/tmp/state-data/{year}/"
    acs_data = pd.read_csv(f'/tmp/acs_data/acs_5yr_{year}.csv')
    acs_data = acs_data.groupby('tract').mean().reset_index()
    
    for idx, city in enumerate( city_name_list):
        print(f"Running {city}, {idx+1} of {len(city_name_list)}")
        city_shapefile_df = geopandas.read_file(GOOD_CITY_SHAPEFILE_LOCATIONS[city]["location"])
        city_shapefile_df = city_shapefile_df.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})

        ### CREATE MERGED DATAFRAME
        ## "middle merge"
        # read in state data:
        state = GOOD_CITY_SHAPEFILE_LOCATIONS[city]["state"]
        state_tiger_shapefile_path = f"{state_tiger_path}{state}/{state}.shp"
        state_tiger_data = geopandas.read_file(state_tiger_shapefile_path)
        city_tiger_merge = merge_data(city_shapefile_df, state_tiger_data, f"/tmp/city-data/{city}/city-tiger-merge-{year}.geojson")
        
        ## Initial Merge with ACS data
        city_acs_merge_df = city_tiger_merge.merge(acs_data, how='left', on='tract')
        standard_city_df = get_standard_df(city_acs_merge_df, year, city)
        standard_city_df.to_file(f"/tmp/city-data/{city}/city-acs-merge-{year}.geojson", driver="GeoJSON")
        
        # create standard dataframe
        standard_city_dataframes.append(standard_city_df)
        
        # produce plot
        ### so.simple_map(city_fcc_merged_df.drop_duplicates(subset='geometry'), 'f_broadband', 'geoid', f"{city.title()} broadband by census tract", output_file_name=f"/tmp/visualizations/{city}-census.png")                 
        city_tiger_vis = city_tiger_merge.plot(figsize=(10, 10), alpha=0.5, edgecolor='k', )
        cx.add_basemap(city_tiger_vis, crs=city_tiger_merge.crs, source=cx.providers.Stamen.TonerLite, zoom=12)
        city_tiger_vis.set_title(f"{city} {year} TIGER merge visualization")

        print("\n")
     
    std_acs_censustract_df = pd.concat(standard_city_dataframes)
    std_acs_censustract_df.to_csv(f"/tmp/data/standard_acs_censustract_df_{year}.csv")
