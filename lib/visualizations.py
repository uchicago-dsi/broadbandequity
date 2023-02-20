import geopandas as gpd
import matplotlib.pyplot as plt
from numbers import Number
import numpy as np
import os
import pandas as pd
from shapely.errors import ShapelyDeprecationWarning
import warnings
import seaborn as sns

def duplicate_areas(data,geography):
    """Returns True if data's geography column contains duplicates, else False."""

    return len(data.reset_index()[geography]) != len(set(data.reset_index()[geography]))


# create choropleth function
def create_choropleth_grid(df1, df2, column, title):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12,12))
    
    from mpl_toolkits.axes_grid1 import make_axes_locatable
   
    # 2017 choropleth
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    
    df1.plot(ax=ax1, column=column, legend=True, cax=cax)
    ax1.axis('off')
    ax1.set_title(f'{2017 } title')

    # 2021 choropleth 
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='5%', pad=0.1)
                              
    df2.plot(ax=ax2, column=column, legend=True, cax=cax)
    ax2.axis('off')
    ax2.set_title(f'{2021 } title')
    
    fig.tight_layout();


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
    plt.axis('off')

    if output_file_name is not None:
        plt.savefig(output_file_name)
    else:
        plt.show()

def plot_scatter(data, x, y, by, title, x_lab, y_lab, line=False):
    '''
    Plot a scatterplot or regression plot for a given variable
    '''
    if not line:
        plt.figure()
        sns.scatterplot(data=data, x=x, y=y, hue=by, alpha=0.5)
        plt.title(title)
        plt.xlabel(x_lab)
        plt.ylabel(y_lab);
    else:
        plt.figure()
        sns.regplot(data=data, x=x, y=y)
        plt.title(title)
        plt.xlabel(x_lab)
        plt.ylabel(y_lab);

        
def plot_percentages(city_df, cat_of_int, col, title):
    '''
    Plot a pie chart  for a given category in the city
    '''
    cols_of_int = {
        f"0% to 10% {cat_of_int}": 0,
        f"10% to 20% {cat_of_int}": 0,
        f"20% to 30% {cat_of_int}": 0,
        f"30% to 40% {cat_of_int}": 0,
        f"40% to 50% {cat_of_int}": 0,
        f"50% to 60% {cat_of_int}": 0,
        f"60% to 70% {cat_of_int}": 0,
        f"70% to 80% {cat_of_int}": 0,
        f"80% to 90% {cat_of_int}": 0,
        f"90% to 100% {cat_of_int}": 0   
    }
    
    mcolors = ['red', 'orange', 'yellow', 'lightgreen', 'green', 'deepskyblue', 'blue', 'navy', 'violet', 'purple']
    city_df = city_df.drop_duplicates(subset="tract")

    for i in city_df[col]:
        if i <= .1:
            cols_of_int[f"0% to 10% {cat_of_int}"] = cols_of_int[f"0% to 10% {cat_of_int}"] + 1
        elif .1 < i <= .2:
            cols_of_int[f"10% to 20% {cat_of_int}"] = cols_of_int[f"10% to 20% {cat_of_int}"] + 1
        elif .2 < i <= .3:
            cols_of_int[f"20% to 30% {cat_of_int}"] = cols_of_int[f"20% to 30% {cat_of_int}"] + 1
        elif .3 < i <= .4:
            cols_of_int[f"30% to 40% {cat_of_int}"] = cols_of_int[f"30% to 40% {cat_of_int}"] + 1
        elif .4 < i <= .5:
            cols_of_int[f"40% to 50% {cat_of_int}"] = cols_of_int[f"40% to 50% {cat_of_int}"] + 1
        elif .5 < i <= .6:
            cols_of_int[f"50% to 60% {cat_of_int}"] = cols_of_int[f"50% to 60% {cat_of_int}"] + 1
        elif .6 < i <= .7:
            cols_of_int[f"60% to 70% {cat_of_int}"] = cols_of_int[f"60% to 70% {cat_of_int}"] + 1
        elif .7 < i <= .8:
            cols_of_int[f"70% to 80% {cat_of_int}"] = cols_of_int[f"70% to 80% {cat_of_int}"] + 1
        elif .8 < i <= .9:
            cols_of_int[f"80% to 90% {cat_of_int}"] = cols_of_int[f"80% to 90% {cat_of_int}"] + 1
        elif .9 < i <= 1:
            cols_of_int[f"90% to 100% {cat_of_int}"] = cols_of_int[f"90% to 100% {cat_of_int}"] + 1

    plt.rcParams['figure.figsize'] = [8, 10]
    plt.pie(cols_of_int.values(), labels=cols_of_int.keys(), labeldistance=None, colors = mcolors)
    plt.legend(bbox_to_anchor=(-.2, .1), loc='lower left', borderaxespad=0)
    plt.title(title, fontsize=15, y=1.0, pad=-23)
    plt.show();