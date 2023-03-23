### Notebooks Directory

This directory contains notebooks for use in the broadband equity project

The notebooks in this directory contains cleaned code that produces deliverable dataframes and visualizations created during Fall 2022 and Winter 2023. Each deliverable notebook contains information on running the code within it to reproduce the analysis done during the Data Science Clinic Fall of 2022 and Winter 2023.

It contains the following:
+ [Work In Progress Folder](notebooks/wip): This folder contains code used by participants in the Data Science Clinic. It is not cleaned and is kept for archival purposes
+ [Inequality Measures](inequality_measures.ipynb): This notebook computes and produces inequality measures for each city from the standard dataframes.
+ [Neighborhood Boxplots](neighborhood_boxplots.ipynb): This notebook produces boxplots showing the range of neighborhood-level broadband access for each city
+ [Standard Dataframe Notebook](standard_tiger_df_notebook.ipynb): This notebook goes through how to run the standard_tiger_dataframe.py library and produce the standard ACS merged dataframe
+ [ACS Data Notebooks](acs_data.ipynb): This notebook goes through and pull the ACS columns of interest from the ACS census data for 2021 and 2017 5 yr estimates
+ [ACS Race Percentage Notebook](acs_race_pct_final.ipynb): This notebook contains code to clean the race columns in the dataframe. This is not necessary to use when running to create the standard dataframe as the code has been merged into lib/standard_tiger_df.py
+ [ACS Visualizations Notebook](ACS_Visualizations.ipynb): This notebook exhibits how to display cloropleth maps for a given column of interest in our dataframes
+ [ACS Policy Memos Notebook](ACS_policymemo_visualizations.ipynb): This notebook produces visualizations of interest for the policy memo that can be sent out to policy stakeholders