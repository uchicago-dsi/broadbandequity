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
            plt.rcParams['figure.figsize'] = [8, 10]
            data.plot(column=variable,legend=True, vmin=0, vmax=1)
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
        plt.ylabel(y_lab)
        plt.legend(bbox_to_anchor=(1.1, 1.05), ncol=3);
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

    plt.rcParams['figure.figsize'] = [15, 10]
    plt.pie(cols_of_int.values(), labels=cols_of_int.keys(), labeldistance=None, colors = mcolors)
    plt.legend(bbox_to_anchor=(-.2, .1), loc='lower left', borderaxespad=0)
    plt.title(title, fontsize=15, y=1.0, pad=-23)
    plt.show();
    

def stacked_bar(city_subset, year = 2021):
    '''
    This produces a stacked barchart for the cities of interest broadband connectivity ranges
    '''
    
    n = len(list(set(city_subset['City'])))

    cities = []
    zero_ten = [0]*n
    ten_twenty = [0]*n
    twenty_thirty = [0]*n
    thirty_forty = [0]*n
    forty_fifty = [0]*n
    fifty_sixty = [0]*n
    sixty_seventy = [0]*n
    seventy_eighty = [0]*n
    eighty_ninety = [0]*n
    ninety_hundred = [0]*n
    cat_of_int = "% with Internet"
    if year == 2021:
        col = 'PERC Est_Total: With an Internet subscription: PRESENCE AND TYPES OF INTERNET SUBSCRIPTIONS IN HOUSEHOLD_tct21'
    else:
        col = 'PERC Est_Total: With an Internet subscription: PRESENCE AND TYPES OF INTERNET SUBSCRIPTIONS IN HOUSEHOLD_tct17'

    for loc, city in enumerate(set(city_subset['City'])):
        curr_df = city_subset[city_subset['City'] == city]
        cities.append(city)

        rows = curr_df.shape[0]

        for i in curr_df[col]:
            if i <= .1:
                zero_ten[loc] = zero_ten[loc] + 1
            elif .1 < i <= .2:
                ten_twenty[loc] = ten_twenty[loc] + 1
            elif .2 < i <= .3:
                twenty_thirty[loc] = twenty_thirty[loc] + 1
            elif .3 < i <= .4:
                thirty_forty[loc] = thirty_forty[loc] + 1
            elif .4 < i <= .5:
                forty_fifty[loc] = forty_fifty[loc] + 1
            elif .5 < i <= .6:
                fifty_sixty[loc] = fifty_sixty[loc] + 1
            elif .6 < i <= .7:
                sixty_seventy[loc] = sixty_seventy[loc] + 1
            elif .7 < i <= .8:
                seventy_eighty[loc] = seventy_eighty[loc] + 1
            elif .8 < i <= .9:
                eighty_ninety[loc] = eighty_ninety[loc] + 1
            elif .9 < i <= 1:
                ninety_hundred[loc] = ninety_hundred[loc] + 1
        total = zero_ten[loc] + ten_twenty[loc] + twenty_thirty[loc] + thirty_forty[loc] + forty_fifty[loc] + fifty_sixty[loc] + sixty_seventy[loc] + seventy_eighty[loc] + eighty_ninety[loc] + ninety_hundred[loc]
        zero_ten[loc] = zero_ten[loc] / total
        ten_twenty[loc] = ten_twenty[loc] / total
        twenty_thirty[loc] = twenty_thirty[loc] / total
        thirty_forty[loc] = thirty_forty[loc] / total
        forty_fifty[loc] = forty_fifty[loc] / total
        fifty_sixty[loc] = fifty_sixty[loc] / total
        sixty_seventy[loc] = sixty_seventy[loc] / total
        seventy_eighty[loc] = seventy_eighty[loc] / total
        eighty_ninety[loc] = eighty_ninety[loc] / total
        ninety_hundred[loc] = ninety_hundred[loc] / total            

    mcolors = ['red', 'orange', 'yellow', 'lightgreen', 'green', 'deepskyblue', 'blue', 'navy', 'violet', 'purple']

    y0 = np.array(zero_ten)
    y1 = np.array(ten_twenty)
    y2 = np.array(twenty_thirty)
    y3 = np.array(thirty_forty)
    y4 = np.array(forty_fifty)
    y5 = np.array(fifty_sixty)
    y6 = np.array(sixty_seventy)
    y7 = np.array(seventy_eighty)
    y8 = np.array(eighty_ninety)
    y9 = np.array(ninety_hundred)

    # plot bars in stack manner
    plt.rcParams['figure.figsize'] = [15, 10]
    plt.bar(cities, y0, color='red')
    plt.bar(cities, y1, bottom=y0, color='orange')
    plt.bar(cities, y2, bottom=y0+y1, color='yellow')
    plt.bar(cities, y3, bottom=y0+y1+y2, color='lightgreen')
    plt.bar(cities, y4, bottom=y0+y1+y2+y3, color='green')
    plt.bar(cities, y5, bottom=y0+y1+y2+y3+y4, color='deepskyblue')
    plt.bar(cities, y6, bottom=y0+y1+y2+y3+y4+y5, color='blue')
    plt.bar(cities, y7, bottom=y0+y1+y2+y3+y4+y5+y6, color='navy')
    plt.bar(cities, y8, bottom=y0+y1+y2+y3+y4+y5+y6+y7, color='violet')
    plt.bar(cities, y9, bottom=y0+y1+y2+y3+y4+y5+y6+y7+y8, color='purple')
    plt.xlabel("Cities")
    plt.ylabel("Average internet access of census tract in the cities")
    plt.legend(["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"])
    plt.title("Tract Level Internet Access Inequality", fontsize=17)
    plt.xticks(rotation=90)
    plt.show()


    
