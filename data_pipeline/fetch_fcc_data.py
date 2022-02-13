"""Fetchs December 2020 FCC fixed broadband deployment data."""

from config import config
import requests
import pandas as pd
import os

# Source/docs:
# https://opendata.fcc.gov/Wireline/Fixed-Broadband-Deployment-Data-December-2020/hicn-aujz
# https://dev.socrata.com/foundry/opendata.fcc.gov/hicn-aujz

FCC_URL = "https://opendata.fcc.gov/resource/hicn-aujz.json"

def fcc_fixed(force_api_call=False):
    """Returns dataframe of Dec 2020 fixed broadband data from Form 477.

    Args:
    force_api_call (optional): When True, calls relevant API and writes local CSV.
        Otherwise, will preferentially just read local CSV. Defaults to False.

    Returns:
        data: pandas dataframe
    
    Raises:
        Exception: for responses other than 200 (OK) and 204 (empty)
    """

    csv_address = os.path.join(os.path.dirname(__file__), '../data/fcc_fixed.csv')
    while True:
        if force_api_call:
            request = FCC_URL + "?stateabbr=IL&$$app_token=" + config['API Keys']['FCCAppToken']
            response = requests.get(request)
            try:
                response = response.json()
            except:
                print(response)
            data = pd.DataFrame(columns=response[0], data=response[1:])
            data.to_csv(csv_address)   
            return data 
        try:
            data = pd.read_csv(csv_address, index_col = 0)
            return data
        except:
            force_api_call = True

fcc_fixed(force_api_call=True)