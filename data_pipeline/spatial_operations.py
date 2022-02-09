"""Spatial manipulations for internet and census data."""

import pdb

import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

current_file = os.path.dirname(__file__)
# geo_codes = {'shapefile geography name' : 'user-facing geography name'}
geo_codes = {'blockce10':'block',
             'tractce10':'tract',
             'community':'community_area',
             'ward':'ward'
            }

def get_shapefile(geography):
    """Returns geodataframe with specified geography geometries.

    Args:
        geography (str): currently supports "block", "tract", "community_area", and "ward"
    
    Returns:
        geodataframe
    """

    # note: for some reason, below line prints deprecation warning for some (but not all geometries)
    # (for example, for community_areas but not for tracts)
    # ShapelyDeprecationWarning: __len__ for multi-part geometries is deprecated and will be removed in Shapely 2.0.
    geo = gpd.read_file(current_file+'/../geo/'+geography+'s.shp')
    geo = geo.rename(columns=geo_codes)
    if geography != 'community_area':  # community areas have string names
        geo[geography] = geo[geography].astype(int)
    return geo

def geographize(data,target_geography):
    """Converts dataframe to geodataframe with geometries.

    Args:
        data (df): dataframe to add spatial information to
        target_geography (str): column of data with spatial information
    
    Returns:
        geodataframe

    Future addition: target_geography can take geography levels not in data,
        and function will call aggregate function if needed.
    """

    geo = get_shapefile(target_geography)
    return geo.join(data.set_index(target_geography),on=target_geography)

def areal_mean_aggregator(x):
    return np.average(x, weights=overlap.loc[x.index, 'area'])

def areal_sum():
    pass

def pop_sum():
    pass

def pop_mean():
    pass

def aggregate(data,variables,source_geography,target_geography):
    """Calculates statistic at new geographical level with areal-based weighting.

    Args:
        data (df): dataframe with statistics at original geographical level
        variables (dict): dictionary with keys = columns in data to convert,
            values = 'areal mean', 'areal sum', 'pop mean', 'pop sum' to select aggregation method
            (use mean for intensive statistics, sum for extensive statistics)
            (use areal for areal-based weighting, use pop for population-based weighting)
        source_geography: column of data with original spatial information
        target_geography: geographical level to convert to
    
    Returns:
        dataframe
    """

    # References: 
    # https://gis.stackexchange.com/questions/326408/how-aggregate-data-in-a-geodataframe-by-the-geometry-in-a-geoseries
    # https://stackoverflow.com/questions/31521027/groupby-weighted-average-and-sum-in-pandas-dataframe

    # first, find the intersection of the source and target geometries
    source_geo = geographize(data,source_geography)
    target_geo = get_shapefile(target_geography)
    overlap = gpd.overlay(source_geo,target_geo,how='intersection')
    source_geo['area'] = source_geo.area
    overlap['area'] = overlap.area
    # construct dictionary with areas of original geographies
    original_areas = dict(source_geo[[source_geography,'area']].values)
    
    output = []
    for variable, method in variables.items():
        if method == 'areal mean':
            #aggregation_function = lambda x: np.average(x, weights=overlap.loc[x.index, 'area'])
            aggregation_function = areal_mean_aggregator
        elif method == 'areal sum':
            # area-weighted sum... or my initial attempt at it? 
            # here's the problem: we need to multiply each intersection-area's value by the proportion
            # of its *original* area it consists of. So we need to reference the source geographies.
            # But .agg() passes all the points at once to the aggregation_function, so just using a dictionary doesn't work
            # since a dictionary can't hash a list/array. So I'm trying vectorize but not sure what values are getting passed currently.
            aggregation_function = np.vectorize(lambda x: np.dot(x,overlap.loc[x,'area'])/original_areas[overlap.loc[x,source_geography]])
        elif method == 'pop mean':
            raise NotImplementedError
        elif method == 'pop sum':
            raise NotImplementedError
        output.append(
            overlap.groupby(target_geography)
            .agg(variable=(variable,aggregation_function))
            .reset_index()
            .rename(columns={'variable':variable})
            .set_index(target_geography)
            )
    if len(output) > 1:  # avoid returning error if we're only aggregating one variable
        output[0] = output[0].join(output[1:])  # combine different variables' dfs
    return output[0]

def map(data,variable,target_geography):
    """Maps single variable on given geography.

    Args:
        data (df): dataframe with variable of interest
        variable (str): column of dataframe to map
        target_geography: geographical level to map on
    
    Future additions:
        - automatically convert to target_geography via aggregate function if needed
        - map multiple variables at once
        - better legend etc
    """

    geo = geographize(data,target_geography)
    geo.plot(column=variable,legend=True)
    plt.show()

# testing
from fetch_census_data import acs5_aggregate
data = acs5_aggregate()
data['household computers per person']=data['estimated total has a computer']/data['estimated total population']


test = aggregate(
    data,variables={
    'household computers per person':'areal mean',
    'estimated total population':'areal mean'},
    source_geography='tract',target_geography='community_area')


pdb.set_trace()
