import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import pdb

current_file = os.path.dirname(__file__)
blocks = os.path.join(current_file, '../geo/blocks.shp')
community_areas = os.path.join(current_file, '../geo/community_areas.shp')
tracts = os.path.join(current_file, '../geo/tracts.shp')
wards = os.path.join(current_file, '../geo/wards.shp')

def aggregate(data,source_geography,target_geography):

    if source_geography == 'block':
        source_areas = 0
        source_col = 0
    elif source_geography == 'tract':
        source_areas = 0
        source_col = 0
    elif source_geography == 'ookla':
        source_areas = 0
        source_col = 0
    else:
        raise Exception("Did not specify valid source geography.")

    if target_geography == 'tract':
        target_areas = 0
        target_col = 0
    elif target_geography == 'neighborhood':
        target_areas = 0
        target_col = 0
    elif target_geography == 'ward':
        target_areas = 0
        target_col = 0
    else:
        raise Exception("Did not specify valid target geography.")

    price_col = 'price' #?

    # source: https://gis.stackexchange.com/questions/326408/how-aggregate-data-in-a-geodataframe-by-the-geometry-in-a-geoseries
    overlap = gpd.overlay(source_geography,target_geography)
    overlap['area'] = overlap.area
    weighted_mean = lambda x: np.average(x, weights=overlap.loc[x.index, "area"])
    values = {source_col: {'weighted_mean' : weighted_mean} }
    output = overlap.groupby(target_col).agg(values)
    output.columns = output.columns.droplevel()

def map(data,variable,target_geography):

    if target_geography == 'block':
        geo = gpd.read_file(blocks)
    elif target_geography == 'tract':
        geo = gpd.read_file(tracts)
        geo = geo.rename(columns={'tractce10':'tract'})
    elif target_geography == 'neighborhood':
        geo = gpd.read_file(community_areas)
        geo.join(data,on='commarea')
    elif target_geography == 'ward':
        geo = gpd.read_file(wards)
        geo.join(data,on='ward')
    else:
        raise Exception("Did not specify valid target geography.")

    geo[target_geography] = geo[target_geography].astype(int)
    geo = geo.join(data.set_index(target_geography),on=target_geography)
    geo.plot(column=variable,legend=True)
    plt.show()