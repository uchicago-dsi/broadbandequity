"""Leaflet-based mapping (requires ipyleaflet)."""

import ast
from .config import config
import geopandas as gpd
from ipyleaflet import Map, GeoData,LayersControl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from . import spatial_operations 

class InteractiveMap():
    """Interactive map object simplifying interaction with ipyleaflet.

    Args:
        data (df): (geo)dataframe
        target_geography (str, optional): geographical level to map on if passing non-geo dataframe

    Attributes:
        map: ipyleaflet Map object
        data: source (geo)dataframe
    """

    def __init__(self, data,target_geography=None):

        if 'geometry' not in data.columns:  # see if we already have a geodataframe
            if target_geography is None:
                raise ValueError("When passing a non-geo dataframe, must specify target geography.")
            data = spatial_operations.geographize(data,target_geography)
        
        map = Map(
            center = ast.literal_eval(config['Geography']['Map_Center']),
            zoom = ast.literal_eval(config['Geography']['Map_Zoom']))

        # remove adding this layer later - this is similar to what will be implemented in map_variable
        layer = GeoData(geo_dataframe=data,name=target_geography,hover_style={'fillColor': 'red' , 'fillOpacity': 0.2})
        map.add_layer(layer)
        map.add_control(LayersControl())

        self.map = map
        self.data = data

    def map(self):
        """Handles call to map method instead of accessing map attribute."""
        return self.map

    def map_variable(self,variable):
        """Adds a layer with choropleth (shaded map) of specified variable in (geo)dataframe."""
        raise NotImplementedError