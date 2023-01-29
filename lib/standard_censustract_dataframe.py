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
GOOD_CITY_LIST = ['chicago', 'los-angeles','louisville','new-york-city','phoenix','portland','san-diego','san-jose','seattle']
GOOD_CITY_SHAPEFILE_LOCATIONS = {
    "chicago": { "location" : "/tmp/city-data/chicago/chicago-boundaries/chicago_boundaries.shp", "state": "illinois"},
    "los-angeles": { "location" : "/tmp/city-data/los-angeles/los-angeles-boundaries/los-angeles-boundaries.shp", "state": "california"},
    "louisville": { "location" : "/tmp/city-data/louisville/louisville boundaries/louisville_boundaries.shp", "state": "kentucky"},
    "new-york-city": { "location" : "/tmp/city-data/new-york-city/nyc borough boundaries/nyc borough boundaries.shp", "state": "new-york"},
    "phoenix": { "location" : "/tmp/city-data/phoenix/phoenix boundaries/phoenix boundaries.shp", "state": "arizona"},
    "portland": { "location" : "/tmp/city-data/portland/portland-boundaries/portland-boundaries.shp", "state": "oregon"},
    "san-diego": { "location" : "/tmp/city-data/san-diego/san-diego-boundaries/san-diego-boundaries.shp", "state": "california"},
    "san-jose": { "location" : "/tmp/city-data/san-jose/san-jose-boundaries/san-jose-boundaries.shp", "state": "california"},
    "seattle": { "location" : "/tmp/city-data/seattle/seattle-boundaries/seattle-boundaries-v3.shp", "state": "washington"},    
}


#if len( [x for x in GOOD_CITY_LIST if x not in GOOD_CITY_SHAPEFILE_LOCATIONS.keys()] ) > 0:
    #print(f"Warning: cities do not have shapefiles {[x for x in GOOD_CITY_LIST if x not in GOOD_CITY_SHAPEFILE_LOCATIONS.keys()]} ")

### This is the result of the merging that can be found in the
### internet access map directory. Takes a long time.
## if file doesn't exist then unzip
#if os.path.exists("/tmp/data/broadband.geojson"):
#    FCC_MERGED_FILE = "/tmp/data/broadband.geojson"
#else:
#    with zipfile.ZipFile('/tmp/data/broadband.zip', 'r') as zip_ref:
#        zip_ref.extractall('/tmp/data/')

#FCC_MERGED_DF = geopandas.read_file(FCC_MERGED_FILE)
    

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
    merged_df.to_file(merged_df_path, driver="GeoJSON")
    
    return merged_df.copy()

        
def get_standard_df(city_merged_df, city_name):
    '''
    This function prepares a merged dataframe into the standard format so it 
    is ready to go into the standard_censustract_dataframe
    
    Inputs:
      city_merged_df

    Outputs:
      city_standard_df
    '''
    
    city_names = []
    geo_ids = []
    population = []
    households = []
    perc_black = []
    perc_hispanic = []
    perc_college_degree = []
    # missing other racial composition data (ACS data)
    avg_income = []
    perc_broadband = []
    perc_100mb_access = []
    devices_per_person = []
    geometry = []
    
    # parse through census tracts and get attributes of interest
    for c_tract in city_merged_df['geoid']:
        city_names.append(city_name)
        geo_ids.append('geoid')
        population.append('population')
        households.append('households')
        perc_black.append('f_black')
        perc_hispanic.append('f_hispanic')
        perc_college_degree.append('f_ba')
        avg_income.append('mhi')
        perc_broadband.append('f_broadband')
        perc_100mb_access.append('n_fiber_100u')
        devices_per_person.append('devices_per_cap')
        geometry.append('geometry')
        
    standard_city_df = pd.DataFrame({
            'City Name': city_names,
            'Census Tract ID': geo_ids,
            'Population': population,
            'Households': households,
            '% Black': perc_black,
            '% Hispanic': perc_hispanic,
            '% >25 College Degree': perc_college_degree,
            'Avg household income': avg_income,
            '% Broadband Access': perc_broadband,
            '% > 100MB Access': perc_100mb_access,
            'Devices per capita': devices_per_person,
            'geometry': geometry
        })

    
    
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

    return_dict = {}
    return_dict_clean = {}

    if city_name_str is not None:
        city_name_list = [city_name_str]    
    else:
        city_name_list = GOOD_CITY_LIST

    standard_city_dataframes = []
    
    state_tiger_path = f"/tmp/state-data/{year}/"
    
    for idx, city in enumerate( city_name_list):
        print(f"Running {city}, {idx} of {len(city_name_list)}")
        city_shapefile_df = geopandas.read_file(GOOD_CITY_SHAPEFILE_LOCATIONS[city]["location"])
        city_shapefile_df = city_shapefile_df.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})

        # create merged dataframe
        ### TO MERGE WITH BROADBAND DATA: city_fcc_merged_df = merge_data(city_shapefile_df, FCC_MERGED_DF, 
        ### f"/tmp/city-data/{city}/city-merged.geojson")
        # "middle merge"
        # read in state data:
        state = GOOD_CITY_SHAPEFILE_LOCATIONS[city]["state"]
        state_tiger_shapefile_path = f"{state_tiger_path}/{state}/{state}.shp"
        state_tiger_data = geopandas.read_file(state_tiger_shapefile_path)
        city_tiger_merge = merge_data(city_shapefile_df, state_tiger_data, f"/tmp/city-data/{city}/city-tiger-merge.geojson")
        return_dict[city] = city_tiger_merge
        
        # create standard dataframe
        #standard_city_df = get_standard_df(city_fcc_merged_df, city)
        standard_city_dataframes.append(city_tiger_merge)
        
        # produce plot
        ### so.simple_map(city_fcc_merged_df.drop_duplicates(subset='geometry'), 'f_broadband', 'geoid', f"{city.title()} broadband by census tract", output_file_name=f"/tmp/visualizations/{city}-census.png")                 
        city_tiger_vis = city_tiger_merge.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        cx.add_basemap(city_tiger_vis, crs=city_tiger_merge.crs, source=cx.providers.Stamen.TonerLite, zoom=12)

        print("\n")
     
    #std_censustract_df = pd.concat(standard_city_dataframes)
    #std_censustract_df.to_csv("/tmp/data/standard_censustract_df.csv")

    #return return_dict