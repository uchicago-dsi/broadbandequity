# broadbandequity

This repository contains the datasets and codebooks used in the City of Chicago Broadband Equity Project from the Data Science Clinic (Winter 2022).  
Authors: Lena Diasti, Drew Keller, Amy Maldonado

---
### Contents

 * [Goals](#goals)
 * [Installation](#installation)
 * [Tabular summary of broadband access at the community level](#tabular-summary-of-broadband-access-at-the-community-level)
 * [Spatial analysis](#spatial-analysis) 
 
---
### Goals

We are looking to get creative in mapping broadband disparities.
+ Census data is one resource we’d like to leverage further – whether creating heat maps, visualizing trends, or creating an interactive dashboard, there is potential to further bring data on inequities to light in an easy-to-use, digestible way.
+ What other ways can we define and demonstrate the digital divide? Some examples: Ookla speed test data can tell us the level of service different communities receive from their providers. FCC Form 477 data can show us where providers formally offer wired service.

---
### Installation

You will need the following packages and libraries to be able to run the code:
+ pandas
+ numpy
+ geopandas
+ matplotlib
+ descartes
+ requests
+ notebook

---
### Tabular summary of broadband access at the community level 

We fetched publicly available datasets from the American Community Survey (ACS) 5-year estimates, Community Population Survey (ACS), and Federal Communications Commissions (FCC) via APIs to analyze broadband access and sociodemographic variables on the Community Area level. 

All of the fetching scripts can be found in the [data_pipeline](data_pipeline) folder. 
+ [config.ini](config.ini) contains the specific variables we wanted from the datasets and the geography criteria (Cook County, IL). 
+ [fetch_census_data.py](data_pipeline/fetch_census_data.py) is the script used to fetch ACS and CPS data
+ [fetch_fcc_data.py](data_pipeline/fetch_fcc_data.py) is the script used to fetch FCC data

The fetched data was written into csv files found in the [data](data) folder. 
+ [acs5_aggregate.csv](data/acs5_aggregate.csv) is the csv with ACS 5-year aggregate data 
+ [acs5_profile.csv](data/acs5_profile.csv) is the csv with ACS 5-year profile data 
+ [fcc_fixed.csv](data/fcc_fixed.csv) is the csv with the fetched FCC data 

Note: we ran into some issues with using the API for FCC data. As a backup, we manually [downloaded](https://www.fcc.gov/general/broadband-deployment-data-fcc-form-477) the csv file for IL. Because of its large size, we narrowed it down to Cook County, IL, selected the most relevant columns, and exported it as a new csv [chi_fcc.csv](data/chi_fcc.csv). The code used to do this can be found in the [agg_data.ipynb](agg_data.ipynb). 

Additional files:
+ [chi_tracts.csv](data/chi_tracts.csv) is the csv we used to map Census tracts to Chicago community areas provided by [Rob Paral](http://robparal.blogspot.com/2012/04/census-tracts-in-chicago-community.html). 
+ [access_comm_area.csv](data/access_comm_area.csv) is the csv of the final table showing total population and number of households, broadband access, and sociodemographics by Chicago community area. 
+ [agg_data.ipynb](agg_data.ipynb) is the Jupyter notebook containing the code used to wrangle, merge, analyze, and export summaries of the fetched data. 

---
### Spatial analysis









