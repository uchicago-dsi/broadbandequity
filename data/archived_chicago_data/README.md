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

Note: _Raw_ FCC Form 477 data is not included in the repository due to size (`chi_fcc.csv` is .gitignore'd). Please see the code cells at the beginning of [fcc_analysis.ipynb](analysis/fcc_analysis.ipynb) to fetch, filter, and write `chi_fcc.csv` locally.