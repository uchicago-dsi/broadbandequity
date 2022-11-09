"""Spatial manipulations for pandas dataframes."""

# shapefile sources:
# blocks, community areas, wards: City of Chicago Data Portal https://data.cityofchicago.org
# (blocks masked via tracts to remove water-only areas)
# (community areas masked to remove non-Cook-County part of O'Hare)
# tracts: "Chicago Data Guy" blog http://robparal.blogspot.com/2014/01/chicago-tract-shapefile-with-acs-data.html
# note: these tract shapefiles are same as ACS, but masked to city limits within Cook County
# the City of Chicago tract shapefiles include some areas outside the city limits, and more problematically, parts of the lake
# for this reason, DO NOT rely on aggregation from tracts that uses City of Chicago tract shapefiles directly

import geopandas as gpd
import matplotlib.pyplot as plt
from numbers import Number
import numpy as np
import os
import pandas as pd
from shapely.errors import ShapelyDeprecationWarning
import warnings

current_file = os.path.dirname(__file__)
# geo_codes = {'shapefile geography name' : 'user-facing geography name'}
geo_codes = {'blockce10':'individual_block',
             'tractce10':'tract',
             'tract_bloc' : 'block',
             'TRACT':'tract',
             'community':'community_area',
             'community_' : 'community_area',
             'ward':'ward'
            }
PROJECTION = 4326  # epsg:4326

def duplicate_areas(data,geography):
    """Returns True if data's geography column contains duplicates, else False."""

    return len(data.reset_index()[geography]) != len(set(data.reset_index()[geography]))

def reproject(geodataframe,projection):
    """Reprojects geodataframe into specified EPSG projection."""

    if geodataframe.crs['init'] != f'epsg:{str(projection)}':
        geodataframe = geodataframe.to_crs(epsg=projection)
    
    return geodataframe

def fix_chicago_geography_types(data,geography):
    """Chicago-specific: ensures geography columns are correct types."""

    if geography != 'community_area':  # community areas have string names
        data[geography] = data[geography].astype(int)
    else:
        data[geography] = data[geography].astype(str)

    return data

def get_shapefile(geography):
    """Returns geodataframe with specified geography geometries.

    Args:
        geography (str): currently supports "block", "tract", "community_area", and "ward"
    
    Returns:
        geodataframe

    Raises:
        Exception if shapefiles can't be found/read.
    """

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
        # For some reason, below line prints deprecation warning for some but not all geometries
        # (for example, for community_areas but not for tracts)
        # ShapelyDeprecationWarning: __len__ for multi-part geometries is deprecated and will be removed in Shapely 2.0.
        try:
            geo = reproject(gpd.read_file(current_file+'/../geo/'+geography+'s.shp'),PROJECTION)
        except:
            raise Exception("Failed to find valid shapefiles.")
    geo = geo.rename(columns=geo_codes)
    geo = fix_chicago_geography_types(geo,geography)  # ensure column names are right types

    return geo

def geographize(data,target_geography):
    """Converts dataframe to geodataframe with geometries.

    Args:
        data (df): dataframe to add spatial information to
            If a geodataframe is passed, it's returned without modification
            (Other than possibly adding an "area" column)
        target_geography (str): column of data with spatial information
    
    Returns:
        geodataframe
            Always contains at least "geometry" and "area" columns

    Raises:
        ValueError if dataframe contains a column called "area".
            Note: certain other columns that may appear in geodataframes may cause errors as well.

    Future addition: target_geography can take geography levels not in data,
        and function will call aggregate function if needed.

    Issue: Geographize won't re-geographize a dataframe to a new areal level. 

    Important: Note that, if passed a dataframe with geographies outside the shapefile area,
        this function will remove those rows. (For example: if we are working with a shapefile
        of Chicago tracts and we pass a df with tracts outside Chicago, those rows will not
        be returned.)
    """

    if 'geometry' in data.columns:  # see if we already have a geodataframe
        return data
    if 'area' in data.columns: 
        raise ValueError(
            "Dataframe already contains an 'area' column. This will collide with the new geodataframe's area column. "
            "Recommended action: rename the area column (eg, 'area_old') then retry."
            )

    data = fix_chicago_geography_types(data,target_geography)  # ensure column names are right types
    geo = get_shapefile(target_geography)
    output = geo.set_index(target_geography).join(data.set_index(target_geography),how='inner',rsuffix='_')

    if duplicate_areas(data,target_geography):
        print(
            'Warning: You have multiple data points for the same geographical unit. '
            'Consider combining these data points and trying again.'
            )

    output['area'] = output.area

    return output.reset_index()

def aggregator(x,method,overlap,source_geography,original_areas,original_pops):
    """Returns functions for areal interpolation.

    Args:
        x (series): variable of interest
        method (str): 'areal mean', 'areal sum', 'pop mean', 'pop sum' to select aggregation method
            (use mean for intensive statistics, sum for extensive statistics)
            (use areal for areal-based weighting, use pop for population-based weighting)
        overlap (gdf): intersection of source and target geographies
        source_geography (str): source geography level
        original_areas (dict): area of each source geography
        original_pops (dict): population of each source geography
    
    Returns:
        func: for use in pd.agg
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
        # where weights are proportion of supergeography population contributed by each subgeography
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
        # where weights are fraction of each subgeography's population that is in the supergeography
        # this is the same thing as areal sum, because the same fraction of each subgeography's
        # population and area are in the supergeography (we assume homogeneity in subgeographies)
        print("Note: Population-weighted sum is equivalent to areal-weighted sum.")
        weights = pd.Series(
            [overlap.loc[index,'area']/
            original_areas[overlap.loc[index,source_geography]] for index,items in x.items()])
        return np.dot(x,weights)

def aggregate(data,variables,target_geography,source_geography):
    """Calculates statistic at new geographical level via areal interpolation.

    Args:
        data (df): (geo)dataframe with statistics at original geographical level
            Must have a "population" or "estimated total population" column to do population-weighted mean
            Cannot have multiple observations per geographical unit
        variables (dict): dictionary with keys = numeric-type columns in data to convert,
            values = 'areal mean', 'areal sum', 'pop mean', 'pop sum' to select aggregation method
            (use mean for intensive statistics, sum for extensive statistics)
            (use areal for areal-based weighting, use pop for population-based weighting)
        target_geography: geographical level to convert to
        source_geography: column of data with original spatial information
    
    Returns:
        dataframe

    Raises:
        ValueErrors for invalid arguments

    Future modifications:
        - should be able to make the source_geography argument optional when data is a geodataframe
    """

    # References: 
    # https://pysal.org/tobler/generated/tobler.area_weighted.area_interpolate.html (mimicking core functionality)
    # https://gis.stackexchange.com/questions/326408/how-aggregate-data-in-a-geodataframe-by-the-geometry-in-a-geoseries
    # https://stackoverflow.com/questions/31521027/groupby-weighted-average-and-sum-in-pandas-dataframe

    # validate arguments
    if duplicate_areas(data,source_geography):
        raise ValueError(
            'You have multiple data points for the same geographical unit. '
            'Combine these data points and try again.'
            )
    if 'geometry' not in data.columns:  # see if we already have a geodataframe
        if source_geography is None:  # only raised in future functionality
            raise ValueError("When passing a non-geo dataframe, must specify target geography.")
    if 'pop mean' in variables.values():
        if 'population' in data.columns:
            pop_source = 'population'
        elif 'estimated total population' in data.columns:
            pop_source = 'estimated total population'
        else:
            raise ValueError("Data must have a population column to calculate pop-weighted mean.")
    else:
        pop_source = None  # no population required for areal-weighted operations
    for variable in variables:
        if not variable in data.columns:  # ensure all variables are actually present in the dataframe
            raise ValueError(f'{variable} is not a column in the passed dataframe.')
        if not isinstance(data[variable][0],Number):  # ensure all passed variables 
            raise ValueError(f'{variable} is not a numeric-type column. Consider converting and trying again.')

    # first, find the intersection of the source and target geometries
    source_geo = geographize(data,source_geography)
    target_geo = get_shapefile(target_geography)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
        # For some reason, below line prints deprecation warning for some but not all geometries
        # (for example, for community_areas but not for tracts)
        # ShapelyDeprecationWarning: __len__ for multi-part geometries is deprecated and will be removed in Shapely 2.0.
        overlap = gpd.overlay(source_geo,target_geo,how='intersection')
    source_geo['area'] = source_geo.area
    overlap['area'] = overlap.area

    # construct dictionaries with areas and populations of original geographies
    original_areas = dict(source_geo[[source_geography,'area']].values)
    if pop_source is not None:  # if we need the population dictionary
        original_pops = dict(source_geo[[source_geography,pop_source]].values)
    else:
        original_pops = None  # not used

    # aggregate each variable using aggregation function
    output = []
    for variable, method in variables.items():
        aggregation_function = lambda x: aggregator(x,method,overlap,source_geography,original_areas,original_pops)
        output.append(
            overlap.groupby(target_geography)
            .agg(variable=(variable,aggregation_function))
            .reset_index()
            .rename(columns={'variable':variable})
            .set_index(target_geography)
            )

    # combine aggregated variables into single dataframe
    if len(output) > 1:  # avoid returning error if we're only aggregating one variable
        output[0] = output[0].join(output[1:])
    return output[0].reset_index()  # for consistency, don't index by geography in output

def simple_map(data,variable,target_geography,title=None,output_file_name=None, **kwargs):
    """Statically maps single variable on given geography (1-var choropleth).

    Args:
        data (df): (geo)dataframe with variable of interest
        variable (str): column of dataframe to map
        target_geography (str): geographical level to map on
        title (str, optional): title (defaults to variable name)

    Note: You do currently have to specify target_geography even when passing a geodataframe.
    
    Future additions:
        - optional target_geography when using geodataframe
        - automatically convert to target_geography via aggregate function if needed
        - map multiple variables at once
    """

    # validate arguments
    if duplicate_areas(data,target_geography):
        raise ValueError(
            'You have multiple data points for the same geographical unit. '
            'Combine these data points and try again.'
            )
    if 'geometry' not in data.columns:  # see if we already have a geodataframe
        if target_geography is None:  # future validation
            raise ValueError("When passing a non-geo dataframe, must specify target geography.")
        data = geographize(data,target_geography)

    # plot
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
        # For some reason, below line prints deprecation warning for some but not all geometries
        # (for example, for community_areas but not for tracts)
        # ShapelyDeprecationWarning: __len__ for multi-part geometries is deprecated and will be removed in Shapely 2.0.
        try:
            data.plot(column=variable,legend=True)
        except KeyError:
            raise ValueError('Specified variable not in dataframe.') from None

    # title and display
    if title is None:
        title = variable
    plt.title(title)

    if output_file_name is not None:
        plt.savefig(output_file_name, kwargs)
    else:
        plt.show()

