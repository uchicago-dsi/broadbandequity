import requests
import pandas as pd

# Specify API URL
# https://opendata.fcc.gov/Wireline/Fixed-Broadband-Deployment-Data-December-2020/hicn-aujz
# https://dev.socrata.com/foundry/opendata.fcc.gov/hicn-aujz

api_url = "https://opendata.fcc.gov/resource/hicn-aujz.json"

# key ?

# Interact with api and read into dataframe

request = api_url
response = requests.get(request)
try:
    response = response.json()
except:
    print(response)
fcc_data = pd.DataFrame(columns=response[0], data=response[1:])
print(fcc_data)