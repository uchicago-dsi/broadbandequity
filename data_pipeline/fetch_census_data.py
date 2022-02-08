"""Fetchs aggregate/individual 5-year ACS data and individual CPS data."""

from config import config
import ast
import requests
import pandas as pd
import os

API_URL = "https://api.census.gov"
ACS5_AGG_URL = f"/data/{config['Dates']['Census']}/acs/acs5"
ACS5_PROF_URL = f"/data/{config['Dates']['Census']}/acs/acs5/profile"
ACS5_IND_URL = f"/data/{config['Dates']['Census']}/acs/acs5/pums"
CPS_IND_URL = f"/data/{config['Dates']['Census']}/cps/internet/nov"

def call_api(dataset_url,geography_url):
    """Requests data from census API.

    Args:
        dataset_url (str): specifies which census dataset to request
        geography_url (str): specifies which geographies to request

    Returns:
        dataframe containing requested dataset

    Raises:
        Exception: for any unsuccessful API responses
    """

    # finish constructing API request:
    variables = ast.literal_eval(config['Variables'][dataset_url])
    variables_url = "?get="+",".join(variables)
    key_url = "&key="+config['API Keys']['CensusAPIKey']
    request = API_URL + dataset_url + variables_url + geography_url + key_url

    # send request and convert to dataframe:
    response = requests.get(request)
    try:
        response = response.json()
        data = pd.DataFrame(columns=response[0], data=response[1:])
    except:
        raise Exception(response)
    return data.rename(columns=variables)

def acs5_aggregate(force_api_call=False):
    """Returns dataframe of 5-year ACS aggregate data for tracts in Cook County.

    Args:
        force_api_call (bool, optional): When True, calls relevant API and writes local CSV.
            Otherwise, will preferentially just read local CSV. Defaults to False.

    Returns:
        data: pandas dataframe
    
    Set variables of interest in config.ini.
    """

    csv_address = os.path.join(os.path.dirname(__file__), '../data/acs5_aggregate.csv')
    while True:
        if force_api_call:
            geography_url = "&for=tract:*"+"&in=state:"+config['Geography']['State_FIPS']+"&in=county:"+config['Geography']['County_FIPS']
            data = call_api(ACS5_AGG_URL, geography_url)
            data.to_csv(csv_address)
            return data
        try:  # access data stored locally, or if we just wrote it, check that it wrote correctly
            data = pd.read_csv(csv_address, index_col = 0)
            return data
        except:
            force_api_call = True

def acs5_profile(force_api_call=False):
    """Returns dataframe of 5-year ACS aggregate data for tracts in specified county.

    Args:
    force_api_call (bool, optional): When True, calls relevant API and writes local CSV.
        Otherwise, will preferentially just read local CSV. Defaults to False.

    Returns:
        data: pandas dataframe
    
    Set variables of interest in config.ini.
    """

    csv_address = os.path.join(os.path.dirname(__file__), '../data/acs5_profile.csv')
    while True:
        if force_api_call:
            geography_url = "&for=tract:*"+"&in=state:"+config['Geography']['State_FIPS']+"&in=county:"+config['Geography']['County_FIPS']
            data = call_api(ACS5_PROF_URL, geography_url)
            data.to_csv(csv_address)
            return data
        try:  # access data stored locally, or if we just wrote it, check that it wrote correctly
            data = pd.read_csv(csv_address, index_col = 0)
            return data
        except:
            force_api_call = True

def acs5_individual(force_api_call=False):
    """Returns dataframe of 5-year ACS microdata for PUMAs in specified county.

    Args:
    force_api_call (bool, optional): When True, calls relevant API and writes local CSV.
        Otherwise, will preferentially just read local CSV. Defaults to False.

    Returns:
        data: pandas dataframe
    
    Set variables of interest in config.ini.
    """

    csv_address = os.path.join(os.path.dirname(__file__), '../data/acs5_individual.csv')
    while True:
        if force_api_call:
            geography_url = "&for=public%20use%20microdata%20area:*"+"&in=state:"+config['Geography']['State_FIPS']
            data = call_api(ACS5_IND_URL, geography_url)
            data.to_csv(csv_address, '../data/acs5_individual.csv')
            return data
        try:
            data = pd.read_csv(csv_address, index_col = 0)
            return data
        except:
            force_api_call = True

def cps_individual(force_api_call=False):
    """Returns dataframe of CPS internet supplement microdata for counties in specified state.

    Args:
    force_api_call (bool, optional): When True, calls relevant API and writes local CSV.
        Otherwise, will preferentially just read local CSV. Defaults to False.

    Returns:
        data: pandas dataframe
    
    Set variables of interest in config.ini.
    """

    csv_address = os.path.join(os.path.dirname(__file__), '../data/cps_individual.csv')
    while True:
        if force_api_call:
            geography_url = "&for=county:*"+"&in=state:"+config['Geography']['State_FIPS']
            data = call_api(CPS_IND_URL,geography_url)
            data.to_csv(os.path.join(os.path.dirname(__file__), '../data/cps_individual.csv'))
            return data
        try:
            data = pd.read_csv(csv_address, index_col = 0)
            return data
        except:
            force_api_call = True