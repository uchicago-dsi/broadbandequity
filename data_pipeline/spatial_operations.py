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

def aggregator(x,method,overlap,original_areas,original_pops,source_geography):
    """Returns functions for areal interpolation.

    Args:
        x (series): variable of interest
        method (str): 'areal mean', 'areal sum', 'pop mean', 'pop sum' to select aggregation method
            (use mean for intensive statistics, sum for extensive statistics)
            (use areal for areal-based weighting, use pop for population-based weighting)
        overlap (gdf): intersection of source and target geographies
        original_areas (dict): area of each source geography
        original_pops (dict): population of each source geography
        source_geography (str): source geography level
    
    Returns:
        func: for use in pd.agg

    WARNING: Have not fully thought through "population-weighted sum", not sure if it makes sense.
    Returns on the order of population^2 when I test on population (but does that actually make sense??)
    """

    if method == "areal mean":
        # weighted average of variable across subgeographies
        # where weights are proportion of supergeography area contributed by each subgeography
        # weights = overlapping_area
        return np.average(x,weights=overlap.loc[x.index, 'area'])

    elif method == 'areal sum':
        # dot product of variables and weights across subgeographies
        # where weights are fraction of each subgeography's area that is in the supergeography
        weights = pd.Series(
            [overlap.loc[index,'area']/
            original_areas[overlap.loc[index,source_geography]] for index,items in x.items()])
        return np.dot(x,weights)

    elif method == 'pop mean':
        # weighted average of variable across subgeographies
        # where weights are proportion of supergeography pop. contributed by each subgeography
        # in other words, weights are each subgeography's area in supergeography times pop. density 
        # weights = overlapping_area * population / original_area
        return np.average(
            x,
            weights = pd.Series(
                [overlap.loc[index,'area']*original_pops[overlap.loc[index,source_geography]]/
                original_areas[overlap.loc[index,source_geography]] for index,items in x.items()]
                )
            )

    elif method == 'pop sum':
        # dot product of variables and weights across subgeographies
        # where weights are fraction of each subgeography's area that is in the supergeography
        # times that subgeography's population density
        weights = pd.Series(
            [overlap.loc[index,'area']*original_pops[overlap.loc[index,source_geography]]/
            (original_areas[overlap.loc[index,source_geography]])**2 for index,items in x.items()])
        return np.dot(x,weights)

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

    # construct dictionaries with areas and populations of original geographies
    original_areas = dict(source_geo[[source_geography,'area']].values)
    original_pops = dict(source_geo[[source_geography,'estimated total population']].values)
    
    output = []
    for variable, method in variables.items():
        aggregation_function = lambda x: aggregator(x,method,overlap,original_areas,original_pops,source_geography)
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
    'household computers per person':'pop mean',
    'estimated total population':'pop sum'},
    source_geography='tract',target_geography='community_area')


pdb.set_trace()
