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
import zipfile
import glob
warnings.filterwarnings('ignore')

import data_pipeline.spatial_operations as so

### use glob to create a list of cities which are in the neighborhoo-data directory
#GOOD_CITY_LIST = [x.split('/')[2] for x in glob.glob('../city-data/*/')]
GOOD_CITY_LIST = ['chicago']
GOOD_CITY_SHAPEFILE_LOCATIONS = {
    "chicago": { "location" : "/tmp/city-data/chicago/chicago_boundaries.shp"}
    }


#if len( [x for x in GOOD_CITY_LIST if x not in GOOD_CITY_SHAPEFILE_LOCATIONS.keys()] ) > 0:
    #print(f"Warning: cities do not have shapefiles {[x for x in GOOD_CITY_LIST if x not in GOOD_CITY_SHAPEFILE_LOCATIONS.keys()]} ")

### This is the result of the merging that can be found in the
### internet access map directory. Takes a long time.
## if file doesn't exist then unzip
if os.path.exists("/tmp/data/broadband.geojson"):
    FCC_MERGED_FILE = "/tmp/data/broadband.geojson"
else:
    with zipfile.ZipFile('/tmp/data/broadband.zip', 'r') as zip_ref:
        zip_ref.extractall('/tmp/data/')

FCC_MERGED_DF = geopandas.read_file(FCC_MERGED_FILE)
    

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
    merged_df.to_file(merged_df_path, driver="GeoJSON")
    
    print("Population before merge: " + str(sum(merged_df.drop_duplicates(subset='geometry')['population'])))
    print("Population after merge: " + str(sum(merged_df['population'])))
    return merged_df.copy()

        
def get_nhood_avgs_nodups(city_df, city_fcc_df, nhood_col):
    '''
    Updates df to have a column for the average broadband for each census tract
    
    Input:
      city_df (Pandas DF): Neighborhood dataframe for the city of interest
      city_fcc_df (Pandas DF): merged dataframe from neighborhood and broadband data
      nhood_col (str): String indicator of the name of the column for neighborhod IDs
    '''
    
    normal_avgs = []
    a = city_fcc_df.drop_duplicates(subset='geometry')
    for nhood in city_df[nhood_col]:
        ctracts = a.loc[city_fcc_df[nhood_col] == nhood]
        nhood_avg = 0
        null_bband = 0
        for tract in list(ctracts['f_broadband']):
            if not math.isnan(tract):
                nhood_avg = nhood_avg + float(tract)
            else:
                null_bband += 1
        if null_bband == len(ctracts['f_broadband']):
            normal_avgs.append(math.nan)
        else:
            normal_avgs.append(nhood_avg / (len(ctracts['f_broadband']) - null_bband))
    
    city_df['bband_avg'] = normal_avgs
    

def get_nhood_avgs(city_df, city_fcc_df, nhood_col):
    '''
    Updates df to have a column for the average broadband for each census tract
    
    Input:
      city_df (Pandas DF): Neighborhood dataframe for the city of interest
      city_fcc_df (Pandas DF): merged dataframe from neighborhood and broadband data
      nhood_col (str): String indicator of the name of the column for neighborhod IDs
    '''
    
    normal_avgs = []
    for nhood in city_df[nhood_col]:
        ctracts = city_fcc_df.loc[city_fcc_df[nhood_col] == nhood]
        nhood_avg = 0
        null_bband = 0
        for tract in list(ctracts['f_broadband']):
            if not math.isnan(tract):
                nhood_avg = nhood_avg + float(tract)
            else:
                null_bband += 1
        if null_bband == len(ctracts['f_broadband']):
            normal_avgs.append(math.nan)
        else:
            normal_avgs.append(nhood_avg / (len(ctracts['f_broadband']) - null_bband))
    
    city_df['bband_avg'] = normal_avgs


def get_helper( column_name, c_tracts, calc=None ):
    '''
    Given census tracts for a neighborhood, calculate a statistic on a column handling na's
    consistently
    '''

    if column_name not in c_tracts.columns:
        raise Exception(f"Column {column_name} not found in c_tracts dataframe")

    valid_ctracts = [i for i in c_tracts[column_name] if not math.isnan(i)]
    if valid_ctracts:
        if calc is None:
            return statistics.mean(valid_ctracts)
        else:
            return calc( valid_ctracts )
    else:
        return math.nan

def standard_city_data(city_name, city_nhood_df, city_fcc_df, nhood_col):
    '''
    Function to take city neighborhood data and census tract data and prepare it to be 
    put into a standard dataframe for analyses.
    
    We will pull the following columns for the data: city name, neighborhood name, population,
    % broadband access, average income, ethnic/racial composition columns, # of census tracts,
    % fiber access, % > 100 MB access, Devices per person, % below poverty level, % people over 65,
    high school %, college %, geographic size of neighborhood (area), broadband adoption
    
    We create the standard data frame for the given city and write it to a specified location
      This will later be merged with other cities to have one large standard dataframe
      
    Inputs:
      city_name (str): Name of the city of interest
      city_fcc_df (Pandas DF): merged dataframe from neighborhood and broadband data
      nhood_col (str): String indicator of the name of the column for neighborhod IDs
    '''
    city_names = []
    nhood_name = []
    nhood_size = []
    no_census_tracts = []
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
    #perc_below_pov_line = [] --- how should I calculate this?
    #perc_over_age65 = [] --- not in fcc_data (ACS data)
    #perc_hs_diploma = [] --- not in fcc_data (ACS data)
        
    for nhood in set(city_fcc_df[nhood_col]):
        c_tracts = city_fcc_df.loc[city_fcc_df[nhood_col] == nhood]
        city_names.append(city_name)
        nhood_name.append(nhood)
        no_census_tracts.append(len(c_tracts))
        population.append(get_helper('population', c_tracts, lambda x : sum(x)))
        nhood_size.append(sum(geopandas.GeoSeries(c_tracts['geometry']).area))
        households.append(sum([i for i in c_tracts['households'] if not math.isnan(i)]))
        perc_black.append(get_helper('f_black', c_tracts))
        perc_hispanic.append(get_helper('f_hispanic', c_tracts))
        perc_college_degree.append(get_helper( 'f_ba', c_tracts))
        avg_income.append(get_helper( 'mhi', c_tracts))
        perc_broadband.append(get_helper('f_broadband', c_tracts))
        perc_100mb_access.append(get_helper( 'n_fiber_100u', c_tracts))
        devices_per_person.append(get_helper( 'devices_per_cap', c_tracts))
        nhood_geo = city_nhood_df.loc[city_nhood_df[nhood_col] == nhood]
        if not nhood_geo.empty:
            geometry.append(nhood_geo['geometry'].iloc[0])
        else:
            geometry.append(math.nan)
    
    standard_city_df = pd.DataFrame({
            'City Name': city_names,
            'Neighborhood Name': nhood_name,
            'Number of Census Tracts': no_census_tracts,
            'Population': population,
            'Households': households,
            'Neighborhood Size': nhood_size,
            '% Black': perc_black,
            '% Hispanic': perc_hispanic,
            '% >25 College Degree': perc_college_degree,
            'Avg household income': avg_income,
            '% Broadband Access': perc_broadband,
            '% > 100MB Access': perc_100mb_access,
            'Devices per capita': devices_per_person,
            'geometry': geometry
        })
    
    return standard_city_df.copy()
    
    
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
    
    city_fcc_df.boxplot(column='f_broadband', by=nhood_col, rot=90, figsize=(15,10), grid=False,
                       fontsize=8, color='green')
    plt.ylabel('f_broadband')
    plt.xlabel('Neighborhood Indicator')
    plt.title(title)
    plt.suptitle('')


def generate_dataframe_and_plots( city_name_str = None):

    return_dict = {}
    return_dict_clean = {}

    if city_name_str is not None:
        city_name_list = [city_name_str]    
    else:
        city_name_list = GOOD_CITY_LIST

    standard_city_dataframes = []
    
    for idx, city in enumerate( city_name_list):
        print(f"Running {city}, {idx} of {len(city_name_list)}")
        city_shapefile_df = geopandas.read_file(GOOD_CITY_SHAPEFILE_LOCATIONS[city]["location"])
        city_shapefile_df = city_shapefile_df.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})

        city_fcc_merged_df = merge_data(city_shapefile_df, FCC_MERGED_DF, f"/tmp/city-data/{city}/city-merged.geojson")

        return_dict[city] = city_fcc_merged_df
        
        #so.simple_map(city_fcc_merged_df.drop_duplicates(subset='geometry'), 'f_broadband', 'geoid', f"{city.title()} broadband by census tract", output_file_name=f"/tmp/visualizations/{city}-census.png")
        #so.simple_map(city_fcc_merged_df_cleaned.drop_duplicates(subset='geometry'), 'f_broadband', 'geoid', f"{city.title()} broadband by census tract (cleaned)", output_file_name=f"/tmp/visualizations/{city}-census-cleaned.png")
        
        ## create standard_df and produce neighborhood plots
        #standard_city_df = standard_city_data(city, city_shapefile_df, city_fcc_merged_df, GOOD_CITY_SHAPEFILE_LOCATIONS[city]["nhood_col"])
        #standard_city_dataframes.append(standard_city_df)
        
        
        #so.simple_map(geopandas.GeoDataFrame(standard_city_df), '% Broadband Access', 'Neighborhood Name', f'{city.title()} broadband by Neighborhood Boundary', f"/tmp/visualizations/{city}-neighborhood.png")
        #so.simple_map(geopandas.GeoDataFrame(standard_city_df_cleaned), '% Broadband Access', 'Neighborhood Name', f'{city.title()} broadband by Neighborhood Boundary (cleaned)', f"/tmp/visualizations/{city}-neighborhood-cleaned.png")
        
        #print("\n")
     
    
    #std_neighborhood_df = pd.concat(standard_city_dataframes)
    #std_neighborhood_df.to_csv("/tmp/data/standard_neighborhood_df.csv")

    #return return_dict