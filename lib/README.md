#### Lib

This folder contains the libraries for the pipeline to standardize the census data from different cities. It contains the following files:

+ [race_categories_2017.json](lib/race_categories_2017.json) is a file that contains the different race categories and their new names for 2017, used in the standard ACS dataframe calculations.
+ [race_categories_2021.json](lib/race_categories_2021.json) is a file that contains the different race categories and their new names for 2021, used in the standard ACS dataframe calculations.
+ [standard_acs_dataframe.py](lib/standard_acs_dataframe.py) is code that creates the standard ACS dataframe for a given 5 yr estimate and cities of interest. This is the most up to data standard_dataframe.py code
+ [visualizations.py](lib/visualizations.py) is code that creates visualizations of interest for the standard ACS dataframe
+ [wip](lip/wip/) is a directory containing archived versions of the standard_df code, including code to produce neighborhood level and census tract level standard dataframes
+ [merge_to_final_dataframe](lib/merge_to_final_dataframe.py) is the code that creates the final standard dataframe that is ready for analysis, including ACS dataframe of 2017 5 yr estimate and cities of interest, CDC PLACES dataset variables, and Social Vulnerability Indexes and component variables
+ [corr_report](lib/corr_report.py) is the code that generates a correlation report of CDC PLACES health indicators and associated health index variables with internet connectivity rate
