# Data

This folder contains csv and zip files for a standard dataframe that has census tract and neigborhood level data for 22 cities. The folder contains the following subfolders:

### ACS_DATA
This folder contains json files with column variables used in ACS API data requests called in [acs_data.ipynb](notebooks/acs_data.ipynb) and csv files that contain the outputs of those requests. The 2013-2017 and 2017-2021 ACS data was used because they both contained all relevant interned related data and the 2017 data captures pre-pandemic internet access while the 2021 data captures pre,current and post-pandemic. The folder contains the following files:
+ [acs_5yr_2016.csv](data/acs_data/acs_5yr_2016.csv) is from the 2012-2016 ACS aggregate at the census tract level for 13 states (TX, MD, MA, IL, CO, MI, ID, CA, KY, AR, OR, WA, DC). This data is not used in the standard dataframe and futher analysis because internet access information was not collected in this ACS aggregate.
+ [acs_5yr_2017.csv](data/acs_data/acs_5yr_2017.csv) is from the 2013-2017 ACS aggregate at the census tract level for the 13 states mentioned above with over 100 column variables.
+ [acs_5yr_2021.csv](data/acs_data/acs_5yr_2021.csv) is from the 2017-2021 ACS aggregate at the census tract level for the 13 states mentioned above with over 100 column variables.
+ [2017_columns.json](data/acs_data/2017_columns.json) is the column variables and corresponding names used in the ACS 2013-2017 API requests.
+ [2021_columns.json](data/acs_data/2021_columns.json) is the column variables and corresponding names used in the ACS 2017-2021 API requests.
+ [acs_categories.json](data/acs_data/acs_categories.json) is a mapping of column names to categories which is used to calculate percentages in the standard dataframe.

### ARCHIVED_CHICAGO_DATA
This folder contains ...

### BOUNDARY-SHAPEFILES
This folder contains ...

### STANDARD_DATAFRAMES
This folder contains ...
+ [standard_acs_censustract_df_2016.zip](data/standard_acs_censustract_df_2016.zip) TODO
+ [standard_acs_censustract_df_2017.zip](data/standard_acs_censustract_df_2017.zip) TODO
+ [standard_acs_censustract_df_2021.zip](data/standard_acs_censustract_df_2021.zip) TODO
+ [standard_neighborhood_df.csv](data/standard_neighborhood_df.csv) TODO

### TIGER-CENSUS-DATA
This folder contains