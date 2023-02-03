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
        city_merged_df_copy = city_merged_df[['state',
                                             'county',
                                             'STATEFP',
                                             'COUNTYFP',
                                             'geometry',
                                             "Estimate!!Total: TOTAL POPULATION",
                                             "Estimate!!Total: SEX BY AGE",
                                             "Estimate!!Total:!!Male: SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!Under 5 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!5 to 9 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!10 to 14 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!15 to 17 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!18 and 19 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!20 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!21 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!22 to 24 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!25 to 29 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!30 to 34 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!35 to 39 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!40 to 44 years SEX BY AGE",
                                             "Estimate!!Total:!!Male:!!45 to 49 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!50 to 54 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!55 to 59 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!60 and 61 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!62 to 64 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!65 and 66 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!67 to 69 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!70 to 74 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!75 to 79 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!80 to 84 years SEX BY AGE", 
                                             "Estimate!!Total:!!Male:!!85 years and over SEX BY AGE", 
                                             "Estimate!!Total:!!Female: SEX BY AGE", 
                                             "Estimate!!Total:!!Female:!!Under 5 years SEX BY AGE", 
                                             "Estimate!!Total:!!Female:!!5 to 9 years SEX BY AGE", 
                                             "Estimate!!Total:!!Female:!!10 to 14 years SEX BY AGE", 
                                             "Estimate!!Total:!!Female:!!15 to 17 years SEX BY AGE", 
                                             "Estimate!!Total:!!Female:!!18 and 19 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!20 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!21 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!22 to 24 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!25 to 29 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!30 to 34 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!35 to 39 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!40 to 44 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!45 to 49 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!50 to 54 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!55 to 59 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!60 and 61 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!62 to 64 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!65 and 66 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!67 to 69 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!70 to 74 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!75 to 79 years SEX BY AGE",
                                             "Estimate!!Total:!!Female:!!80 to 84 years SEX BY AGE", 
                                             "Estimate!!Total:!!Female:!!85 years and over SEX BY AGE",
                                             "Estimate!!Total:!!Not Hispanic or Latino: HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!White alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Black or African American alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!American Indian and Alaska Native alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Asian alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Native Hawaiian and Other Pacific Islander alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Some other race alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Two or more races: HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Two or more races:!!Two races including Some other race HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Not Hispanic or Latino:!!Two or more races:!!Two races excluding Some other race, and three or more races HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino: HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!White alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Black or African American alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!American Indian and Alaska Native alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Asian alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Native Hawaiian and Other Pacific Islander alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Some other race alone HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Two or more races: HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Two or more races:!!Two races including Some other race HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total:!!Hispanic or Latino:!!Two or more races:!!Two races excluding Some other race, and three or more races HISPANIC OR LATINO ORIGIN BY RACE",
                                             "Estimate!!Total: HISPANIC OR LATINO ORIGIN",
                                             "Estimate!!Total:!!Not Hispanic or Latino HISPANIC OR LATINO ORIGIN",
                                             "Estimate!!Total:!!Hispanic or Latino HISPANIC OR LATINO ORIGIN",
                                             "Estimate!!Total living in area 1 year ago: GEOGRAPHICAL MOBILITY IN THE PAST YEAR (NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE) FOR RESIDENCE 1 YEAR AGO IN THE UNITED STATES",
                                             "Estimate!!Total: PLACE OF BIRTH BY YEAR OF ENTRY FOR THE FOREIGN-BORN POPULATION",
                                             "Estimate!!Median household income in the past 12 months (in 2020 inflation-adjusted dollars) MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2020 INFLATION-ADJUSTED DOLLARS)",
                                             "Estimate!!Median family income in the past 12 months--!!Total: MEDIAN FAMILY INCOME FOR FAMILIES WITH GRANDPARENT HOUSEHOLDERS AND/OR SPOUSES LIVING WITH OWN GRANDCHILDREN UNDER 18 YEARS BY RESPONSIBILITY FOR OWN GRANDCHILDREN AND PRESENCE OF PARENT OF GRANDCHILDREN",
                                             "Estimate!!Median family income in the past 12 months (in 2020 inflation-adjusted dollars) MEDIAN FAMILY INCOME IN THE PAST 12 MONTHS (IN 2020 INFLATION-ADJUSTED DOLLARS)",
                                             "Estimate!!Total: RECEIPT OF SUPPLEMENTAL SECURITY INCOME (SSI), CASH PUBLIC ASSISTANCE INCOME, OR FOOD STAMPS/SNAP IN THE PAST 12 MONTHS BY HOUSEHOLD TYPE FOR CHILDREN UNDER 18 YEARS IN HOUSEHOLDS",
                                             "Estimate!!Gini Index GINI INDEX OF INCOME INEQUALITY",
                                             "Estimate!!Median gross rent MEDIAN GROSS RENT (DOLLARS)",
                                             "Estimate!!Total:!!Car, truck, or van - drove alone: MEANS OF TRANSPORTATION TO WORK BY AGE FOR WORKPLACE GEOGRAPHY",
                                             "Estimate!!Total:!!Car, truck, or van - carpooled: MEANS OF TRANSPORTATION TO WORK BY AGE FOR WORKPLACE GEOGRAPHY",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab): MEANS OF TRANSPORTATION TO WORK BY AGE FOR WORKPLACE GEOGRAPHY",
                                             "Estimate!!Total:!!Walked: MEANS OF TRANSPORTATION TO WORK BY AGE FOR WORKPLACE GEOGRAPHY",
                                             "Estimate!!Total:!!Taxicab, motorcycle, bicycle, or other means: MEANS OF TRANSPORTATION TO WORK BY AGE FOR WORKPLACE GEOGRAPHY",
                                             "Estimate!!Total:!!Worked from home: MEANS OF TRANSPORTATION TO WORK BY AGE FOR WORKPLACE GEOGRAPHY",
                                             "Estimate!!Aggregate travel time to work (in minutes): AGGREGATE TRAVEL TIME TO WORK (IN MINUTES) OF WORKERS BY PLACE OF WORK--STATE AND COUNTY LEVEL",
                                             "Estimate!!Total: MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van: MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Drove alone MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Carpooled: MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Carpooled:!!In 2-person carpool MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Carpooled:!!In 3-person carpool MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Carpooled:!!In 4-person carpool MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Carpooled:!!In 5- or 6-person carpool MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Car, truck, or van:!!Carpooled:!!In 7-or-more-person carpool MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab): MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab):!!Bus MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab):!!Subway or elevated rail MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab):!!Long-distance train or commuter rail MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab):!!Light rail, streetcar or trolley (carro público in Puerto Rico) MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Public transportation (excluding taxicab):!!Ferryboat MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Taxicab MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Motorcycle MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Bicycle MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Walked MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Other means MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total:!!Worked from home MEANS OF TRANSPORTATION TO WORK",
                                             "Estimate!!Total: ALLOCATION OF SCHOOL ENROLLMENT FOR THE POPULATION 3 YEARS AND OVER",
                                             "Estimate!!Total:!!Not allocated ALLOCATION OF SCHOOL ENROLLMENT FOR THE POPULATION 3 YEARS AND OVER"]]
    
    city_merged_df_copy['City'] = city
    
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
