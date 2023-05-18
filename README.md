# broadbandequity

This repository contains the datasets and codebooks used in the City of Chicago Broadband Equity Project from the Data Science Clinic (Winter 2023). Additional work was also done during the Autumn 2022 Quarter.

Authors: Lena Diasti, Drew Keller, Amy Maldonado, Nick Ross (Autumn 2022)

 * [Goals](#goals)
 * [Installation](#installation)
 * [Sources](#sources)

---

#### Deliverables Spring 2023

This quarter's project involved merging and cleaning the 2013-2017 American Community Survey (ACS) datasets with the CDC’s PLACES dataset by census tracts, creating spatial visualizations of health indicators, and conducting an exploratory analysis report of the observed relationship between broadband connectivity and a constructed health index. The code accompanying the newly merged dataset should be standardized, generalizable, and reproducible. 

People Spring 2023:
+ Victoria Kielb vkielb@uchicago.edu
+ Chandler Hall cgwhall@uchicago.edu
+ Sarah Lueling slueling@uchicago.edu

Mentor: James Turk

TA: Kenia Godinez Nogueda

---

#### Deliverables Winter 2023

We are looking to build a set of jupyter notebooks to generate maps for the specified metro areas. We are looking to move beyond description and look at association/causal inference analysis. We want to connect our data to sociodemographic factors and use multi-level modeling. We also want to build the pipeline to include data at the neighborhood as well as census tract. This code should be standardized, generalizeable, and reproducible. 


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
+ American Community Survey (ACS) 2017 and 2021 5 yr estimades
  + [Individual 2017](https://api.census.gov/data/2017/acs/acs5/pums/variables.html)
  + [Aggregate 2017](https://api.census.gov/data/2017/acs/acs5/variables.html)
  + [Profile 2017](https://api.census.gov/data/2017/acs/acs5/profile/variables.html) 
  + [Individual 2021](https://api.census.gov/data/2021/acs/acs5/pums/variables.html)
  + [Aggregate 2021](https://api.census.gov/data/2021/acs/acs5/variables.html)
  + [Profile 2021](https://api.census.gov/data/2021/acs/acs5/profile/variables.html) 
+ [TIGER State Census Tract Data](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
+ City Data Portals (more information in README's in data folder
  + City Shapefile Boundaries
  + City Neighborhood Boundaries

---

## Contents

 * [Archived Chicago Code](#archived-chicago-code)
 * [Data](#data)
 * [Lib](#lib)
 * [Notebooks](#notebooks)
 * [Notes](#notes)
 * [Visualizations](#visualizations)
 * [Additional Files](#additional-files)
 

---

#### Data

This folder contains the raw and processed data used in our analysis. More information is included in the data folder. It contains the following sets of data:
+ [acs_data](data/acs_data): Pulled ACS 5-year estimate data and columns of interest for 2017 and 2021 5 yr estimates
+ [archived_chicago_data](data/archived_chicago_data): Archived Chicago data from before the data science clinic projects
+ [boundary-shapefiles](data/boundary-shapefiles): SHP files for cities of interest. This includes city boundary data and census tract dataframes
+ [standard_dataframes](data/standard_dataframes): Standard dataframes produced for analysis. These dataframes combine neighorhood, census tract, and ACS dataframes for all cities into a single dataframe
+ [TIGER-census-data](data/TIGER-census-data): State-based TIGER shapefiles for states for both 2017 and 2021.


---

#### Lib

This folder contains the libraries for the pipeline to standardize and visualize the census data from different cities. It contains the following files:
+ [race_categories_2017.json](lib/race_categories_2017.json) is a file that contains the different race categories and their new names for 2017, used in the standard ACS dataframe calculations.
+ [race_categories_2021.json](lib/race_categories_2021.json) is a file that contains the different race categories and their new names for 2021, used in the standard ACS dataframe calculations.
+ [standard_acs_dataframe.py](lib/standard_acs_dataframe.py) is code that creates the standard ACS dataframe for a given 5 yr estimate and cities of interest. This is the most up to data standard_dataframe.py code
+ [visualizations.py](lib/visualizations.py) is code that creates visualizations of interest for the standard ACS dataframe
+ [wip](lip/wip/) is a directory containing archived versions of the standard_df code, including code to produce neighborhood level and census tract level standard dataframes

---

#### Census Tract Data

This folder contains the census tract geojson and/or shapefiles that were used in the analysis. The cities included in the analysis are:
+ Arlington
+ Atlanta
+ Austin
+ Bakersfield
+ Baltimore
+ Boston
+ Chicago
+ Colorado City
+ Dallas
+ Denver
+ Detroit
+ El Paso
+ Fort Worth
+ Fresno
+ Houston
+ Indianapolis
+ Kansas City
+ Long Beach
+ Los Angeles
+ Louisville
+ Memphis
+ Mesa
+ Miami
+ Minneapolis
+ New York City
+ Oakland
+ Oklahoma City
+ Omaha
+ Philadelphia
+ Phoenix
+ Portland
+ Raleigh
+ Sacramento
+ San Antonio
+ San Diego
+ San Francisco
+ San Jose
+ Seattle
+ Tulsa
+ Tucson
+ Virginia Beach
+ Washington, D.C.
+ Wichita

---

#### Census Tract Data WIP

This folder contains the census tract geojson and/or shapefiles that were not fit for analysis. These files were incomplete, inaccurate, or had noise. The cities that were not included in the census-tract-level standard dataframe (and thus need further inspection are):
+ Baltimore
+ San Francisco

---

#### Neighborhood Data

This folder contains the neighborhood geojson and/or shapefiles that were used in the analysis. The cities included in the analysis are:
+ Atlanta
+ Austin
+ Baltimore
+ Chicago
+ Dallas
+ Denver
+ Detroit
+ Houston
+ Indianapolis
+ Kansas City
+ Long Beach
+ Los Angeles
+ Louisville
+ Miami
+ Minneapolis
+ Oakland
+ Phoenix
+ Portland
+ Raleigh
+ Sacramento
+ San Diego
+ San Francisco
+ San Jose
+ Seattle
+ Tucson
+ Washington, D.C.

---

#### Neighborhood Data WIP

This folder contains the neighborhood geojson and/or shapefiles that were not fit for analysis. These files were incomplete, inaccurate, or had noise. The cities that were not included in the neighborhood-level standard dataframe (and thus need further inspection are):
+ Albuquerque
+ Boston
+ Charlotte
+ Columbus
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
+ [Standard Dataframe Notebook](standard_tiger_df_notebook.ipynb): This notebook goes through how to run the standard_tiger_dataframe.py library and produce the standard ACS merged dataframe
+ [ACS Data Notebooks](acs_data.ipynb): This notebook goes through and pull the ACS columns of interest from the ACS census data for 2021 and 2017 5 yr estimates
+ [ACS Race Percentage Notebook](acs_race_pct_final.ipynb): This notebook contains code to clean the race columns in the dataframe. This is not necessary to use when running to create the standard dataframe as the code has been merged into lib/standard_tiger_df.py
+ [ACS Visualizations Notebook](ACS_Visualizations.ipynb): This notebook exhibits how to display cloropleth maps for a given column of interest in our dataframes
+ [ACS Policy Memos Notebook](ACS_policymemo_visualizations.ipynb): This notebook produces visualizations of interest for the policy memo that can be sent out to policy stakeholders

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
