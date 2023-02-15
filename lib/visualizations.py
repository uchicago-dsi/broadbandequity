import geopandas as gpd
import matplotlib.pyplot as plt
from numbers import Number
import numpy as np
import os
import pandas as pd
from shapely.errors import ShapelyDeprecationWarning
import warnings

def duplicate_areas(data,geography):
    """Returns True if data's geography column contains duplicates, else False."""

    return len(data.reset_index()[geography]) != len(set(data.reset_index()[geography]))


def simple_map(data,variable,target_geography,title=None,output_file_name=None):
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
            plt.rcParams['figure.figsize'] = [10, 10]
            data.plot(column=variable,legend=True)
        except KeyError:
            raise ValueError('Specified variable not in dataframe.') from None

    # title and display
    if title is None:
        title = variable
    plt.title(title)

    if output_file_name is not None:
        plt.savefig(output_file_name)
    else:
        plt.show()