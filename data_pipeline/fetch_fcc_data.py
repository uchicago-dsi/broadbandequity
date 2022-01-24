"""Fetchs December 2020 FCC fixed broadband deployment data."""

from config import config
import requests
import pandas as pd

# Source/docs:
# https://opendata.fcc.gov/Wireline/Fixed-Broadband-Deployment-Data-December-2020/hicn-aujz
# https://dev.socrata.com/foundry/opendata.fcc.gov/hicn-aujz

FCC_URL = "https://opendata.fcc.gov/resource/hicn-aujz.json"

def fixed_broadband():
    """Returns dataframe of Dec 2020 fixed broadband data from Form 477."""

    request = FCC_URL + "?$limit=5000&$$app_token=" + config['API Keys']['FCCAppToken']
    response = requests.get(request)
    try:
        response = response.json()
    except:
        print(response)
    return pd.DataFrame(columns=response[0], data=response[1:])