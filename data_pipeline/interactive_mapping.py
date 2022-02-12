"""Leaflet-based mapping (requires ipyleaflet)."""

from ipyleaflet import Map, GeoData,LayersControl
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spatial_operations 


def interactive_map(data,variable,target_geography=None):
    """Interactively maps single variable on given geography (1-var choropleth).

    Args:
        data (df): (geo)dataframe with variable of interest
        variable (str): column of dataframe to map
        target_geography (opt): geographical level to map on if passing non-geo dataframe
    
    Future additions:
        - automatically convert to target_geography via aggregate function if needed
        - map multiple variables at once
        - better legend etc
    """

    if 'geometry' not in data.columns:  # see if we already have a geodataframe
        if target_geography is None:
            raise ValueError("When passing a non-geo dataframe, must specify target geography.")
        data = spatial_operations.geographize(data,target_geography)
    
    m = Map(center=(41.84,-87.6),zoom = 10)