"""Fetchs aggregate/individual 5-year ACS data and individual CPS data."""

from config import config
import ast
import requests
import pandas as pd

API_URL = "https://api.census.gov"
ACS5_AGG_URL = "/data/2019/acs/acs5"
ACS5_IND_URL = "/data/2019/acs/acs5/pums"
CPS_IND_URL = "/data/2019/cps/internet/nov"

def call_api(dataset_url,geography_url):
    """Requests data from census API.

    Args:
        dataset_url: specifies which census dataset to request
        geography_url: specifies which geographies to request

    Returns:
        dataframe containing requested dataset

    Raises:
        Exception: for non-OK API response
    """

    # finish constructing API request:
    variables_url = "?get="+",".join(ast.literal_eval(config['Variables'][dataset_url]))
    key_url = "&key="+config['API Keys']['CensusAPIKey']
    request = API_URL + dataset_url + variables_url + geography_url + key_url

    # send request and convert to dataframe:
    response = requests.get(request)
    try:
        response = response.json()
    except:
        raise Exception(response)
    return pd.DataFrame(columns=response[0], data=response[1:])

def acs5_aggregate():
    """Returns dataframe of 5-year ACS aggregate data for tracts in Cook County.
    
    Set variables of interest in config.ini.
    """

    geography_url = "&for=tract:*"+"&in=state:"+config['Geography']['IL_FIPS']+"&in=county:"+config['Geography']['COOK_FIPS']
    return call_api(ACS5_AGG_URL, geography_url)

def acs5_individual():
    """Returns dataframe of 5-year ACS microdata for tracts in Cook County.
    
    Set variables of interest in config.ini.
    """

    geography_url = "&for=public%20use%20microdata%20area:*"+"&in=state:"+config['Geography']['IL_FIPS']
    return call_api(ACS5_IND_URL,geography_url)

def cps_individual():
    """Returns dataframe of CPS internet supplement microdata for counties in Illinois.
    
    Set variables of interest in config.ini.
    """

    geography_url = "&for=county:*"+"&in=state:"+config['Geography']['IL_FIPS']
    return call_api(CPS_IND_URL,geography_url)