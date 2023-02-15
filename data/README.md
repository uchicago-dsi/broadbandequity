# Data

This folder contains csv and zip files for a standard dataframe that has census tract and neigborhood level data for 22 cities. The folder contains the following subfolders:

### ACS_DATA
This folder contains json files with column variables used in ACS API data requests called in [acs_data.ipynb](notebooks/acs_data.ipynb) and csv files that contain the outputs of those requests. The 2013-2017 and 2017-2021 ACS data was used because they both contained all relevant interned related data and the 2017 data captures pre-pandemic internet access while the 2021 data captures pre,current and post-pandemic.
+ [acs_5yr_2016.csv](data/acs_data/acs_5yr_2016.csv) is from the 2012-2016 ACS aggregate at the census tract level for 13 states (TX, MD, MA, IL, CO, MI, ID, CA, KY, AR, OR, WA, DC). This data is not used in the standard dataframe and futher analysis because internet access information was not collected in this ACS aggregate.
+ [acs_5yr_2017.csv](data/acs_data/acs_5yr_2017.csv) is from the 2013-2017 ACS aggregate at the census tract level for the 13 states mentioned above with over 100 column variables.
+ [acs_5yr_2021.csv](data/acs_data/acs_5yr_2021.csv) is from the 2017-2021 ACS aggregate at the census tract level for the 13 states mentioned above with over 100 column variables.
+ [2017_columns.json](data/acs_data/2017_columns.json) is the column variables and corresponding names used in the ACS 2013-2017 API requests.
+ [2021_columns.json](data/acs_data/2021_columns.json) is the column variables and corresponding names used in the ACS 2017-2021 API requests.
+ [acs_categories.json](data/acs_data/acs_categories.json) is a mapping of column names to categories which is used to calculate percentages in the standard dataframe.

### ARCHIVED_CHICAGO_DATA
This folder contains all the data that was previously used in the Chicago analysis.

### BOUNDARY-SHAPEFILES
This folder contains city boundary and neighborhood boundary shapfiles that are later used to merge with ACS & TIGER data.
+ [city-boundaries/](data/boundary-shapefiles/city-boundaries/) This folder contains city boundary shapefiles for ___ citites.
+ [neighborhood-boundaries/](data/boundary-shapefiles/neighborhood-boundaries/) This folder contains neighborhood boundary shapefiles for ___ citites.

### STANDARD_DATAFRAMES
This folder contains ...
+ [standard_acs_censustract_df_2016.zip](data/standard_acs_censustract_df_2016.zip) TODO
+ [standard_acs_censustract_df_2017.zip](data/standard_acs_censustract_df_2017.zip) TODO
+ [standard_acs_censustract_df_2021.zip](data/standard_acs_censustract_df_2021.zip) TODO
+ [standard_neighborhood_df.csv](data/standard_neighborhood_df.csv) TODO

### TIGER-CENSUS-DATA
This folder contains TIGER census tract shapefile data for three different years which is used to merge with ACS data in order to create standard dataframes at census tract level.
+ [2016/](data/TIGER-census-data/2016/) This folder contains the 2016 TIGER census tract shapefiles for 13 states.
+ [2017/](data/TIGER-census-data/2017/) This folder contains the 2017 TIGER census tract shapefiles for 13 states.
+ [2021/](data/TIGER-census-data/2021/) This folder contains the 2021 TIGER census tract shapefiles for 13 states.