import configparser
import ast
import requests
import pandas as pd

API_URL = "https://api.census.gov"
IL_FIPS = "17"
COOK_FIPS = "031"  # 017031
CHICAGO_FIPS = "14000"

def get_config():
    config = configparser.ConfigParser()
    if not config.has_section('Data Pipeline'):
        config.read('config.ini')
    return config

def call_api(dataset_url,geography_url):
    config = get_config()
    variables_url = "?get="+",".join(ast.literal_eval(config['Data Pipeline'][dataset_url]))
    key_url = "&key="+config['API Keys']['CensusAPIKey']
    request = API_URL + dataset_url + variables_url + geography_url + key_url
    response = requests.get(request)
    try:
        response = response.json()
    except:
        raise Exception(response)
    return pd.DataFrame(columns=response[0], data=response[1:])

def acs5_aggregate():
    geography_url = "&for=tract:*"+"&in=state:"+IL_FIPS+"&in=county:"+COOK_FIPS
    return call_api("/data/2019/acs/acs5", geography_url)

def acs5_individual():
    return

# Specify dataset
# https://www.census.gov/data/developers/data-sets/census-microdata-api.ACS_5-Year_PUMS.html

# Specify geography: 
# https://api.census.gov/data/2019/acs/acs5/geography.html


# Interact with api and read into dataframe

# What about 1 year data?
# https://www.census.gov/programs-surveys/acs/guidance/estimates.html
# Has congressional district but not tract as geography (look at variables)

# Could also do ACS PUMS (individual-level data but may only have 100k-person-area geographic precision?)