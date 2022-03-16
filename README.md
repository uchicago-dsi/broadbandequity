# broadbandequity

This repository contains the datasets and codebooks used in the City of Chicago Broadband Equity Project from the Data Science Clinic (Winter 2022).  
Authors: Lena Diasti, Drew Keller, Amy Maldonado

 * [Goals](#goals)
 * [Installation](#installation)
 * [Sources](#sources)

---

#### Goals

We are looking to get creative in mapping broadband disparities.
+ Census data is one resource we’d like to leverage further – whether creating heat maps, visualizing trends, or creating an interactive dashboard, there is potential to further bring data on inequities to light in an easy-to-use, digestible way.
+ What other ways can we define and demonstrate the digital divide? Some examples: Ookla speed test data can tell us the level of service different communities receive from their providers. FCC Form 477 data can show us where providers formally offer wired service.
+ Data preparation: clean and align the data from different sources, remove duplicates and impute missingness
+ Feature extraction: retrieve important features which are able to identify the broadband disparities
+ Spatial data science: incorporate spatial data to showcase the geopolitical and non-geographical relationships in broadband extent
+ Data Visualization: create maps, plots, and dashboards (preferably interactive) to deliver the trends and insights

---

#### Installation

You will need the following packages and libraries to be able to run the code:
+ pandas
+ numpy
+ geopandas
+ matplotlib
+ descartes
+ requests
+ notebook
+ seaborn
+ sklearn

---

#### Sources

We fetched our data for analysis from the following sources:
+ American Community Survey (ACS) 2015-2019 data
  + [Individual](https://api.census.gov/data/2019/acs/acs5/pums/variables.html)
  + [Aggregate](https://api.census.gov/data/2019/acs/acs5/variables.html)
  + [Profile](https://api.census.gov/data/2019/acs/acs5/profile/variables.html) 
+ [Current Population Survey (CPS) data](https://api.census.gov/data/2019/cps/internet/nov/variables.html)
+ [Federal Communications Commission (FCC) Form 477 2020 data](https://www.fcc.gov/general/broadband-deployment-data-fcc-form-477)
+ Chicago Data Portal
  + [Chicago Community Area Boundaries](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6)
  + [Census Tract Boundaries](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Tracts-2010/5jrd-6zik)
  + [Covid Community Vulnerability Index (CCVI)](https://data.cityofchicago.org/Health-Human-Services/Chicago-COVID-19-Community-Vulnerability-Index-CCV/xhc6-88s9)
  + [Hardship Index](https://data.cityofchicago.org/Health-Human-Services/hardship-index/792q-4jtu)

---

## Contents

 * [Analysis](#analysis)
 * [Data](#data)
 * [Data Pipeline](#data-pipeline) 
 * [Geo](#geo)
 * [Tests](#tests)
 * [Additional Files](#additional-files)
 
---

#### Analysis

This folder contains all the notebooks with our code used to analyze the data. 
+ [acs_aggregate_analysis.ipynb](analysis/acs_aggregate_analysis.ipynb) is the Jupyter notebook containing the code used to import, clean, analyze, merge, and visualize summaries of the fetched aggregate ACS,CCVI, and Hardship data for a community area level analysis. 
+ [acs_individual_analysis.ipynb](analysis/acs_individual_analysis.ipynb) is the Jupyter notebook containing the code used to import, clean, analyze, merge, and visualize summaries of the fetched individual ACS data for a household level analysis. 
+ [acs_visualizations.ipynb](analysis/acs_visualizations.ipynb) is the Jupyter notebook containing the code used to import and visualize the fetched aggregate ACS data. 
+ [cps_analysis.ipynb](analysis/cps_analysis.ipynb) is the Jupyter notebook containing the code used to import, clean, analyze, merge, and visualize summaries of the fetched Current Population Survey (CPS) data. 
+ [fcc_analysis.ipynb](analysis/fcc_analysis.ipynb) is the Jupyter notebook containing the code used to import, clean, analyze, merge, and visualize summaries of the fetched FCC data. 

---

#### Data

This folder contains all the csv files used in our analysis. 
+ [CMAP_2019_comm_data.csv](data/CMAP_2019_comm_data.csv) is the csv with Community Area information for spatial validation
+ [acs5_aggregate.csv](data/acs5_aggregate.csv) is the csv with ACS 5-year aggregate data 
+ [acs5_indvidual.csv](data/acs5_individual.csv) is the csv with ACS 5-year individual data 
+ [acs5_profile.csv](data/acs5_profile.csv) is the csv with ACS 5-year profile data 
+ [chicago_internet.csv](data/chicago_internet.csv) is the csv of the final table showing total populations, number of households, broadband access, and sociodemographics by Chicago community area. 
+ [comm_areas.csv](data/comm_areas.csv) and [tracts_comm_areas.csv](data/tracts_comm_areas.csv) are the csvs we used to map Census tracts to Chicago community areas for ACS data analysis
+ [covid_index.csv](data/covid_index.csv) is the csv of the CCVI scores.
+ [cps_individual.csv](data/cps_individual.csv) is the csv with the CPS individual data
+ [fcc_acs_combined_community_areas](data/fcc_acs_combined_community_areas) and [fcc_acs_combined_tracts](data/fcc_acs_combined_tracts) are the csvs we used to map Census tracts to Chicago community areas for FCC data analysis.
+ [fcc_fixed.csv](data/fcc_fixed.csv) is the csv with the fetched FCC data.
+ [hardship_index.csv](data/hardship_index.csv) is the csv of the hardship scores.

---

#### Data Pipeline

This folder contains all the scripts used to fetch the data for our analysis. 
+ [data_pipeline_how_to.ipynb](data_pipeline/data_pipeline_how_to.ipynb) is the Jupyter notebook with a tutorial on how to use the fetching scripts
+ [fetch_census_data.py](data_pipeline/fetch_census_data.py) is the script used to fetch ACS and CPS data
+ [fetch_fcc_data.py](data_pipeline/fetch_fcc_data.py) is the script used to fetch FCC data
+ [interactive_mapping.py](data_pipeline/interactive_mapping.py) is the script used to fetch interactive mapping data
+ [spatial_operations.py](data_pipeline/spatial_operations.py) is the script used to fetch Chicago block, community areas, and wards boundaries data

---

#### Geo

This folder contains all the shapefiles for spatial analysis.
+ The "blocks" files are the block-level data
+ The "community_areas" files are the community area level data
+ The "tracts" files are the Census tracts data
+ The "wards" files are the Chciago wards data
+ [fix_block_shapes.ipynb](geo/fix_block_shapes.ipynb) is the notebook to modify the Chicago Data Portal's block shapefiles so that they do not contain parts of Lake Michigan.
+ [fix_ohare_shape.ipynb](geo/fix_ohare_shape.ipynb) is the notebook to modify the Chicago Data Portal's community area shapefiles so that the O'Hare shapefile does not contain the single tract that it has in DuPage County


---

#### Tests

This folder contains notebooks and shapefiles to validate areal interpolation.
+ [neighborhood_spatial_validation.ipynb](tests/neighborhood_spatial_validation.ipynb) is the notebook previously used to inspect some of the neighborhoods that were producing outlier results via areal interpolation. This problem was resolved (we determined it was due to lake area being included in geographies) but we are leaving this notebook in the repository for documentation purposes.
+ [spatial_operations_validation.ipynb](tests/spatial_operations_validation.ipynb) is the notebook is to demonstrate that our areal interpolation functions produce extensive and intensive statistics similar to known values.
+ [tract_validation_and_masking.ipynb](tests/tract_validation_and_masking.ipynb) is the notebook previously used to mask tract boundaries, removing a duplicated tract number (specifically, the tract of O'Hare community area that lies in DuPage County). It no longer fully functions now that we have made the change, but we are retaining it in the repository for documentation purposes.
+ [validation_data](tests/validation_data) is the csv with community area geographic boundaries to validate areal interpolation

---

#### Additional Files

+ [config.ini](config.ini) contains the specific variables we wanted from the ACS and CPS datasets from our geography criteria (Cook County, IL). 



