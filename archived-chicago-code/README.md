# Archived Chicago Code

This repository contains the datasets and codebooks used in the City of Chicago Broadband Equity Project from pre-Data Science Clinic Autumn 2022

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
  
  

## Contents

 * [Analysis](#analysis)
 * [Data Pipeline](#data-pipeline) 
 * [Geo](#geo)
 * [Internet Access Map](#internet-access-map)
 * [Tests](#tests)
 

--- 

#### Analysis

This folder contains notebooks used to analyze the data. 
+ [acs_aggregate_analysis.ipynb](analysis/acs_aggregate_analysis.ipynb) is a Jupyter notebook used to import, clean, analyze, merge, and visualize summaries of the fetched aggregate ACS, CCVI, and Hardship data for a community area level analysis. 
+ [acs_individual_analysis.ipynb](analysis/acs_individual_analysis.ipynb) is a Jupyter notebook used to import, clean, analyze, merge, and visualize summaries of the fetched individual ACS data for a household level analysis. 
+ [acs_visualizations.ipynb](analysis/acs_visualizations.ipynb) is a Jupyter notebook used to import and visualize fetched aggregate ACS data. 
+ [cps_analysis.ipynb](analysis/cps_analysis.ipynb) is a Jupyter notebook  used to import, clean, analyze, merge, and visualize summaries of the fetched Current Population Survey (CPS) data. 
+ [fcc_analysis.ipynb](analysis/fcc_analysis.ipynb) is a Jupyter notebook used to import, clean, analyze, merge, and visualize summaries of the fetched FCC data. 

---

#### Data Pipeline

This folder contains scripts used to fetch and manipulate data. 
+ [data_pipeline_how_to.ipynb](data_pipeline/data_pipeline_how_to.ipynb) is a tutorial on how to use the fetching and spatial operations scripts.
+ [fetch_census_data.py](data_pipeline/fetch_census_data.py) is a module to fetch ACS and CPS data via API.
+ [fetch_fcc_data.py](data_pipeline/fetch_fcc_data.py) is a module to fetch FCC data via API.
+ [interactive_mapping.py](data_pipeline/interactive_mapping.py) is preliminary work towards producing interactive maps.
+ [spatial_operations.py](data_pipeline/spatial_operations.py) is a module to match geography shapefiles with 
data, carry out aggregation from one geography to another, and produce simple choropleths.

---

#### Geo

This folder contains shapefiles for spatial analysis.
+ The "blocks" files are block geographies.
+ The "community_areas" files are community area geographies.
+ The "tracts" files are Census tract geographies.
+ The "wards" files are Chciago ward geographies.
+ [fix_block_shapes.ipynb](geo/fix_block_shapes.ipynb) is a notebook used to modify the Chicago Data Portal's block shapefiles so that they do not contain parts of Lake Michigan.
+ [fix_ohare_shape.ipynb](geo/fix_ohare_shape.ipynb) is a notebook used to modify the Chicago Data Portal's community area shapefiles so that the O'Hare shapefile does not contain the single tract that it has in DuPage County.

---

#### Internet Access Map

This folder contains code to download FCC Form 477 data, Ookla performance data, and ACS data and merge them into on national dataset at the census tract level for Chicago. It also contains a code to create a simple website with a map displaying the integrated dataset.

---

#### Tests

This folder contains notebooks and shapefiles to validate areal interpolation.
+ [neighborhood_spatial_validation.ipynb](tests/neighborhood_spatial_validation.ipynb) is a notebook previously used to inspect some of the neighborhoods that were producing outlier results via areal interpolation. This problem was resolved (we determined it was due to lake area being included in geographies) but we are leaving this notebook in the repository for documentation purposes.
+ [spatial_operations_validation.ipynb](tests/spatial_operations_validation.ipynb) is a notebook demonstrating that our areal interpolation functions produce extensive and intensive statistics similar to known values.
+ [tract_validation_and_masking.ipynb](tests/tract_validation_and_masking.ipynb) is a notebook previously used to mask tract boundaries, removing a duplicated tract number (specifically, the tract of O'Hare community area that lies in DuPage County). It no longer fully functions now that we have made the change, but we are retaining it in the repository for documentation purposes.
+ [validation_data](tests/validation_data) is a csv with community-area population estimates to validate areal interpolation.