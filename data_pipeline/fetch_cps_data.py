import requests
import pandas as pd

# Specify dataset
# https://www.census.gov/data/developers/data-sets/census-microdata-api.CPS.html
# Note that all CPS data is microdata (aka individual respondents)

api_url = "https://api.census.gov"
dataset_url = "/data/2019/cps/internet/nov"

# Specify variables:
# https://api.census.gov/data/2019/cps/internet/nov/variables.html

vars = {"HEEVRHOM" : "region"
    }

variables_url = "?get="+",".join(vars)

# Specify geography

cook_fips = "031"  # 017031
il_fips = "17"
chicago_fips = "14000"

geography_url = "&for=county:*"+"&in=state:"+il_fips
# note: CPS only has county-level data

# jamie's: "&for=tract:*&in=state:{:02d}&in=county:*"

# key db7beae177bf4d220d9d5fcb8907c57250054ddb

#api_key = "db7beae177bf4d220d9d5fcb8907c57250054ddb"
#key_url = "&key="+api_key

# Interact with api and read into dataframe

request = api_url + dataset_url + variables_url + geography_url
response = requests.get(request)
try:
    response = response.json()
except:
    print(response)
cps_data = pd.DataFrame(columns=response[0], data=response[1:])
print(cps_data)