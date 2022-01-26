"""Fetchs December 2020 FCC fixed broadband deployment data."""

from config import config
import requests
import pandas as pd
import os

# Source/docs:
# https://opendata.fcc.gov/Wireline/Fixed-Broadband-Deployment-Data-December-2020/hicn-aujz
# https://dev.socrata.com/foundry/opendata.fcc.gov/hicn-aujz

FCC_URL = "https://opendata.fcc.gov/resource/hicn-aujz.json"

def fcc_fixed():
    """Returns dataframe of Dec 2020 fixed broadband data from Form 477.
    
    Raises:
        Exception: for responses other than 200 (OK) and 204 (empty)
    """

    try:
        data = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/fcc_fixed.csv'), index_col = 0)
    except:
        request = FCC_URL + "?$limit=5000&$$app_token=" + config['API Keys']['FCCAppToken']
        response = requests.get(request)
        try:
            response = response.json()
        except:
            print(response)
        data = pd.DataFrame(columns=response[0], data=response[1:])
        data.to_csv(os.path.join(os.path.dirname(__file__), '../data/fcc_fixed.csv'))    
    return data
