import requests
import pandas as pd

# Specify dataset
# https://www.census.gov/data/developers/data-sets/census-microdata-api.ACS_5-Year_PUMS.html

api_url = "https://api.census.gov"
dataset_url = "/data/2019/acs/acs5"

# Specify variables:
# https://api.census.gov/data/2019/acs/acs5/variables.html

vars = {"B28002_004E" : "estimated total with broadband subscription"
    }

variables_url = "?get="+",".join(vars)

# Specify geography: 
# https://api.census.gov/data/2019/acs/acs5/geography.html

cook_fips = "031"  # 017031
il_fips = "17"
chicago_fips = "14000"

geography_url = "&for=tract:*"+"&in=state:"+il_fips+"&in=county:"+cook_fips

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
acs_data = pd.DataFrame(columns=response[0], data=response[1:])
print(acs5_data)

# What about 1 year data?
# https://www.census.gov/programs-surveys/acs/guidance/estimates.html
# Has congressional district but not tract as geography (look at variables)

# Could also do ACS PUMS (individual-level data but may only have 100k-person-area geographic precision?)