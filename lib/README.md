#### Lib

This folder contains the libraries for the pipeline to standardize the census data from different cities. It contains the following files:

+ [race_categories.json](lib/race_categories.json) is a file that contains the different race categories and their new names, used in the standard ACS dataframe calculations.
+ [standard_acs_dataframe.py](lib/standard_acs_dataframe.py) is code that creates the standard ACS dataframe for a given 5 yr estimate and cities of interest. This is the most up to data standard_dataframe.py code
+ [wip](lip/wip/) is a directory containing archived versions of the standard_df code, including code to produce neighborhood level and census tract level standard dataframes