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

    WARNING: Slow (due to API response) and returns 3.4M data points.

    Args:
    force_api_call (bool, optional): When True, calls relevant API and writes local CSV.
        Otherwise, will preferentially just read local CSV. Defaults to False.

    Returns:
        data: pandas dataframe
    
    Raises:
        Exception: for responses other than 200 (OK) and 204 (empty)
    """

    csv_address = os.path.join(os.path.dirname(__file__), '../data/fcc_fixed.csv')
    while True:
        if force_api_call:
            data_list = []
            offset = 0
            while True:  # have to "page" through the FCC data
                geography_url = "?stateabbr=" + config['Geography']['State_Abbr']
                # 50,000 is the max limit per page; order is needed to ensure pages do not contain duplicate data
                paging_url = f"&$order=logrecno&$limit=50000&$offset={offset}"
                token_url = "&$$app_token=" + config['API Keys']['FCCAppToken']
                request = FCC_URL + geography_url + paging_url + token_url
                response = requests.get(request)
                try:
                    response = response.json()
                    data_list.append(pd.DataFrame(columns=response[0], data=response[1:]))
                except:
                    print(response)
                offset += 49999  # advances to the next page
                if data_list[-1].shape[0]<49999:  # once we don't get a full response, we've reached the last page
                    data = pd.concat(data_list)
                    data.to_csv(csv_address)   
                    return data
        try:
            data = pd.read_csv(csv_address, index_col = 0)
            return data
        except:
            force_api_call = True