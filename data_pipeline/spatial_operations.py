"""Spatial manipulations for internet and census data."""

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

def aggregate(data,variables,source_geography,target_geography):
    """Calculates statistic at new geographical level with areal-based weighting.

    Args:
        data (df): dataframe with statistics at original geographical level
        variables (dict): dictionary with keys = columns in data to convert,
            values = 'mean' or 'sum' to select aggregation method for statistic
            (use mean for intensive statistics, sum for extensive statistics)
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
    # have not yet tested for multiple variables
    for variable, method in variables.items():
        if method == 'mean':
            # area-weighted mean
            aggregation_function = lambda x: np.average(x, weights=overlap.loc[x.index, 'area'])
        elif method == 'sum':
            # area-weighted sum... or my initial attempt at it? 
            # here's the problem: we need to multiply each intersection-area's value by the proportion
            # of its *original* area it consists of. So we need to reference the source geographies.
            # But .agg() passes all the points at once to the aggregation_function, so just using a dictionary doesn't work
            # since a dictionary can't hash a list/array. So I'm trying vectorize but not sure what values are getting passed currently.
            aggregation_function = np.vectorize(lambda x: np.dot(x,overlap.loc[x,'area'])/original_areas[overlap.loc[x,source_geography]])
        output.append(overlap.groupby(target_geography).agg(weighted_sum=(variable,aggregation_function)))
    return output[0].join(output[1:],on=target_geography)  # combine different variables' dfs

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