# broadbandequity

This repository contains the datasets and codebooks used in the City of Chicago Broadband Equity Project from the Data Science Clinic (Winter 2022). Additional work was also done during the Autumn 2022 Quarter.

Authors: Lena Diasti, Drew Keller, Amy Maldonado, Nick Ross (Autumn 2022)

 * [Goals](#goals)
 * [Installation](#installation)
 * [Sources](#sources)

---

#### Deliverables Winter 2023

We are looking to build a set of jupyter notebooks to generate maps for the specified metro areas. We are looking to move beyond description and look at association/causal inference analysis. We want to connect our data to sociodemographic factors and use multi-level modeling. We also want to build the pipeline to include data at the neighborhood as well as census tract. This code should be standardized, generalizeable, and reproducible. For that reason, we will use docker.


People Winter 2023:
+ Kaya Borlase borlasekn@uchicago.edu
+ Brendon Krall bkrall36@uchicago.edu
+ Victoria Kielb vkielb@uchicago.edu
+ Maia Boyd mboyd6@uchicago.edu

Mentor: James Turk

TA: Kenia Godinez Nogueda

---

#### Deliverables Autumn 2022

We are looking to build a set of jupyter notebooks which generate maps, similar to what was produced last year, for the specified metro areas to demonstrate the extent of internet equity. These notebooks should rely on a standardized set of libraries (to also be written) which avoid code repetition as well as use docker for code reproducibility purposes.

People Autumn 2022:
+ Sam Pavlekovsky spavlekovsky@uchicago.edu
+ Maia Boyd mboyd6@uchicago.edu
+ Bruno Xie brunoxie@uchicago.edu
+ Christelle Inema inema@uchicago.edu
+ Kaya Borlase borlasekn@uchicago.edu
+ Kamran Ahmed kamranahmed@uchicago.edu

Mentors: Evelyn Campbelle and Nick Ross

---

#### Goals

+ Fetch and combine City, Census, and FCC data sources relevant to internet access in Chicago
+ Produce descriptive analysis and visualizations of state of access across the city
+ Enable continued work with datasets via reusuable functions

---

#### Docker

There is a dockerfile in the repo. To build the file, build the repository using the command:

```docker build . -t broadband --platform=linux/amd64```

Once the docker file is built, you can run the following command in order to run your jupyter notebook. This will also mount the current directory inside the container.

```docker run --platform=linux/amd64 -p 8888:8888 -v ${PWD}:/tmp broadband```

Once this is running you should be able to access the notebook by going to your web browser and going to 

```http://127.0.0.1:8888/```

If you need to add a package via pip, use the file ```requirements.txt``` which has a basic set of packages installed. Add the package and version and then rebuild the container in order to add it.

If you want to run an interactive terminal, you can run the following command. Note that running an interactive terminal is required to run the data generation for the internet access map (the national map).

```docker run  --platform=linux/amd64 -it -v ${PWD}:/tmp broadband /bin/bash```

For example, if you want to generate the internet access data, do the following:

  * Start an interactive terminal using the docker run command above
  * Go to the internet-access-map directory (```cd internet-access-map```)
  * Run get_data (```./get_data.sh```)
  * Run merge_data (```./merge_data.sh```)

This will create the merged dataset

#### Usage
Once installed, access modules from the main directory via relative imports - for example, `from data_pipeline import fetch_census_data`. If working in a subdirectory, modify `sys.path` to enable imports, such as with `sys.path[0] = os.path.join(os.path.abspath(''),'..')`. (For examples, see first code cells in analysis notebooks.)

---

#### Notes

There are note in the notes subdirectory. These notes are not on the technical aspect, but on the research and decision-making part of the project. This folder contain notes on the Broadband Equity Data Science Clinic Project. It contains the following:
+ [Planning Notes](planning-notes) is a folder that contains planning notes taken over the course of the two quarters
+ [Frequently Asked Questions](faq.md) is a file that contains frequently asked questions that aid in the understanding of the analysis work
+ [Data Description and EDA](Data-description-and-EDA.md) is a file that contains information on how the data was gathered and the exploratory data analysis that was performed.
+ [Project Goals Winter 2023](goals-w23.md) is a file containing the goals for the Data Science Clinic Project Winter 2023 cohort

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
 * [Internet Access Map](#internet-access-map)
 * [Lib](#lib)
 * [Neighborhood Data WIP](#neighborhood-data-wip)
 * [Neighborhood Data](#neighborhood-data)
 * [Notebooks](#notebooks)
 * [Notes](#notes)
 * [Tests](#tests)
 * [Visualizations](#visualizations)
 * [Additional Files](#additional-files)
 
---

#### Analysis

This folder contains notebooks used to analyze the data. 
+ [acs_aggregate_analysis.ipynb](analysis/acs_aggregate_analysis.ipynb) is a Jupyter notebook used to import, clean, analyze, merge, and visualize summaries of the fetched aggregate ACS, CCVI, and Hardship data for a community area level analysis. 
+ [acs_individual_analysis.ipynb](analysis/acs_individual_analysis.ipynb) is a Jupyter notebook used to import, clean, analyze, merge, and visualize summaries of the fetched individual ACS data for a household level analysis. 
+ [acs_visualizations.ipynb](analysis/acs_visualizations.ipynb) is a Jupyter notebook used to import and visualize fetched aggregate ACS data. 
+ [cps_analysis.ipynb](analysis/cps_analysis.ipynb) is a Jupyter notebook  used to import, clean, analyze, merge, and visualize summaries of the fetched Current Population Survey (CPS) data. 
+ [fcc_analysis.ipynb](analysis/fcc_analysis.ipynb) is a Jupyter notebook used to import, clean, analyze, merge, and visualize summaries of the fetched FCC data. 

---

#### Data

This folder contains the raw and processed data used in our analysis. 
+ [CMAP_2019_comm_data.csv](data/CMAP_2019_comm_data.csv) is a csv with Community Area information for spatial validation.
+ [comm_areas.csv](data/comm_areas.csv) and [tracts_comm_areas.csv](data/tracts_comm_areas.csv) are csvs used to crosswalk Census tracts to Chicago community areas for ACS data analysis.
+ [acs5_aggregate.csv](data/acs5_aggregate.csv) is a csv with ACS 5-year aggregate data.
+ [acs5_indvidual.csv](data/acs5_individual.csv) is a csv with ACS 5-year individual data.
+ [acs5_profile.csv](data/acs5_profile.csv) is a csv with ACS 5-year profile data.
+ [cps_individual.csv](data/cps_individual.csv) is a csv with the CPS individual data.
+ [chicago_internet.csv](data/chicago_internet.csv) is a csv of the final table showing total populations, number of households, broadband access, and sociodemographics by Chicago community area. 
+ [covid_index.csv](data/covid_index.csv) is a csv of the CCVI scores.
+ [hardship_index.csv](data/hardship_index.csv) is a csv of the hardship scores.
+ [fcc_acs_combined_community_areas](data/fcc_acs_combined_community_areas) and [fcc_acs_combined_tracts](data/fcc_acs_combined_tracts) are csvs containing combined ACS and FCC data at a community area and tract level, respectively.
+ [chicago_block_list.csv](data/chicago_block_list.csv) is a csv containing a list of 2010s Chicago Census block numbers.
+ [standard_neighborhood_df.csv](data/standard_neighborhood_df.csv) is a dataframe containing all fcc data at the neighborhood letter. It has the following attributes: City Name, Neighborhood Name, Number of Census Tracts, Population, Households, Neighborhood Size, % Black, % Hispanic, % >25 College Degree, Avg household income, % Broadband Access, % > 100MB Access, Devices per capita, geometry

Note: _Raw_ FCC Form 477 data is not included in the repository due to size (`chi_fcc.csv` is .gitignore'd). Please see the code cells at the beginning of [fcc_analysis.ipynb](analysis/fcc_analysis.ipynb) to fetch, filter, and write `chi_fcc.csv` locally.

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

#### Lib

This folder contains the libraries for the pipeline to standardize the census data from different cities. It contains the following files:
+ [standard_dataframe.py](lib/standard_dataframe.py) is code that takes the neighborhood shapefiles for different cities and merges it with the fcc data to produce Geospatial visualizations and a standard dataframe.

---

#### Neighborhood Data

This folder contains the neighborhood geojson and/or shapefiles that were used in the analysis. The cities included in the analysis are:
+ Austin
+ Baltimore
+ Boston
+ Chicago
+ Dallas
+ Denver
+ Detroit
+ Houston
+ Indianapolis
+ Los Angeles
+ Louisville
+ New York City
+ Phoenix
+ Portland
+ San Diego
+ San Francisco
+ San Jose
+ Seattle
+ Washington, D.C.

---

#### Neighborhood Data WIP

This folder contains the neighborhood geojson and/or shapefiles that were not fit for analysis. These files were incomplete, inaccurate, or had noise. The cities that were not included in the neighborhood-level standard dataframe (and thus need further inspection are):
+ Albuquerque
+ Bston
+ Charlotte
+ El Paso
+ Jacksonville
+ Las Vegas
+ Memphis
+ Milwaukee
+ Nashville
+ New York City
+ Philadelphia
+ San Antonio

---

#### Notebooks

This folder contains notebooks for use in the broadband equity project.  These were created during Fall 2022 and Winter 2023. Each notebook contains information on running the code within it to reproduce the analysis, dataframes, and visualizations. It contains the following:
+ [Work In Progress Folder](notebooks/wip): This folder contains code used by participants in the Data Science Clinic. It is not cleaned and is kept for archival purposes
+ [Inequality Measures](inequality_measures.ipynb): This notebook computes and produces inequality measures for each city from the standard dataframes.
+ [Neighborhood Boxplots](neighborhood_boxplots.ipynb): This notebook produces boxplots showing the range of neighborhood-level broadband access for each city
+ [Standard Dataframe Notebook](standard_df_notebook.ipynb): This notebook goes through how to run the standard_dataframe.py library and produce geospatial visualizations as well as standard dataframes.



inequality_measures.ipynb

neighborhood_boxplots.ipynb

standard_df_notebook.ipynb

---

#### Tests

This folder contains notebooks and shapefiles to validate areal interpolation.
+ [neighborhood_spatial_validation.ipynb](tests/neighborhood_spatial_validation.ipynb) is a notebook previously used to inspect some of the neighborhoods that were producing outlier results via areal interpolation. This problem was resolved (we determined it was due to lake area being included in geographies) but we are leaving this notebook in the repository for documentation purposes.
+ [spatial_operations_validation.ipynb](tests/spatial_operations_validation.ipynb) is a notebook demonstrating that our areal interpolation functions produce extensive and intensive statistics similar to known values.
+ [tract_validation_and_masking.ipynb](tests/tract_validation_and_masking.ipynb) is a notebook previously used to mask tract boundaries, removing a duplicated tract number (specifically, the tract of O'Hare community area that lies in DuPage County). It no longer fully functions now that we have made the change, but we are retaining it in the repository for documentation purposes.
+ [validation_data](tests/validation_data) is a csv with community-area population estimates to validate areal interpolation.

---

#### Visualizations

This folder contains visualizations produced by our libraries. We have the following types of visualizations:
+ [Boxplot Visualizations](visualizations/boxplot_visualizations): This folder contains boxplots showing the range of broadband adoption at the neighborhood level within cities
+ "City-census-cleaned.png": Contains geospatial visualization for broadband access for a given city at the census tract level, controlling for overlap duplication
+ "City-census.png": Contains geospatial visualization for broadband access for a given city at the census tract level, with no control for overlap duplication
+ "City-neighborhood-cleaned.png": Contains geospatial visualization for broadband access for a given city at the neighborhood boundary level, controlling for overlap duplication
+ "City-neighborhood.png": Contains geospatial visualization for broadband access for a given city at the census tract level, with no control for overlap duplication

---

#### Additional Files

+ [config.ini](config.ini) sets the variable, date, and geography parameters for the data handling functions (including data fetching and mapping). 