import geopandas as gpd
import pandas as pd
import numpy as np

def aggregate(data,source_geography,target_geography):

    if source_geography == 'blocks':
        source_areas = 0
        source_col = 0
    elif source_geography == 'tracts':
        source_areas = 0
        source_col = 0
    elif source_geography == 'ookla':
        source_areas = 0
        source_col = 0
    else:
        raise Exception("Did not specify valid source geography.")

    if target_geography == 'tracts':
        target_areas = 0
        target_col = 0
    elif target_geography == 'neighborhoods':
        target_areas = 0
        target_col = 0
    elif target_geography == 'wards':
        target_areas = 0
        target_col = 0
    else:
        raise Exception("Did not specify valid source geography.")

    price_col = 'price' #?

    # source: https://gis.stackexchange.com/questions/326408/how-aggregate-data-in-a-geodataframe-by-the-geometry-in-a-geoseries
    overlap = gpd.overlay(source_geography,target_geography)
    overlap['area'] = overlap.area
    weighted_mean = lambda x: np.average(x, weights=overlap.loc[x.index, "area"])
    values = {source_col: {'weighted_mean' : weighted_mean} }
    output = overlap.groupby(target_col).agg(values)
    output.columns = output.columns.droplevel()

def map(data,target_geography):
    if target_geography == 'tracts':
        pass
    if target_geography == 'neighborhoods':
        pass
    if target_geography == 'wards':
        pass