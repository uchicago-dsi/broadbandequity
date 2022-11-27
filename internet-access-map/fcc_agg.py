#!/usr/bin/env python 

import pandas as pd
import numpy as np

print("Loading FCC data...\n")

fcc = pd.read_csv("data/fcc_redux.csv.gz",  
                  usecols = ["provider", "geoid", "tech", "max_dn_mbps", "max_up_mbps"])

print("Data loaded.\nConstructing variables...\n")

# Download Speeds >= Certain threshold
fcc.loc[:, 'max_dn_mbps_ge_1' ]   = fcc.loc[:, 'max_dn_mbps' ] >= 1
fcc.loc[:, 'max_dn_mbps_ge_10' ]  = fcc.loc[:, 'max_dn_mbps' ] >= 10
fcc.loc[:, 'max_dn_mbps_ge_100' ] = fcc.loc[:, 'max_dn_mbps' ] >= 100
fcc.loc[:, 'max_dn_mbps_ge_250' ] = fcc.loc[:, 'max_dn_mbps' ] >= 250

# Upload Speeds >= Certain threshold
fcc.loc[:, 'max_up_mbps_ge_100' ] = fcc.loc[:, 'max_up_mbps' ] >= 100

# Upload Speeds >= 100 & Using Fiber
fcc.loc[:, 'fiber_100u'] = 0
fcc.loc[(fcc.loc[:, 'max_up_mbps'] >= 100) & (fcc.loc[:, 'tech'] == 5), 'fiber_100u'] = 1
fcc.loc[:, 'fiber_100e'] = fcc.loc[:, 'fiber_100u']

# Create column with download and upload speeds >= 1 with 0s otherwise
fcc.loc[:, 'max_dn_ge_1'] = fcc.loc[:, 'max_dn_mbps']
fcc.loc[:, 'max_up_ge_1'] = fcc.loc[:, 'max_up_mbps']
fcc.loc[(fcc.loc[:, 'max_dn_mbps'] < 1), 'max_dn_ge_1'] = 0
fcc.loc[(fcc.loc[:, 'max_dn_mbps'] < 1), 'max_up_ge_1'] = 0

# Aggregation
# For each geoid, calculate the sum (total, using this technology) / max (across the available data) 
ret_df = fcc.groupby('geoid', as_index = False).agg( {'max_dn_mbps_ge_1' : 'sum',\
                                                    'max_dn_mbps_ge_10'  : 'sum',\
                                                    'max_dn_mbps_ge_100' : 'sum',\
                                                    'max_dn_mbps_ge_250' : 'sum',\
                                                    'max_up_mbps_ge_100' : 'sum',\
                                                    'max_dn_ge_1'        : 'max',\
                                                    'max_up_ge_1'        : 'max',\
                                                    'fiber_100e'         : 'max',\
                                                    'fiber_100u'         : 'max'})


# For each tract, calculate the mean / max of speeds
ret_df.loc[:, 'tract'] = ret_df.loc[:, 'geoid'] // 10000
ret_df = ret_df.groupby('tract', as_index=False).agg( {'max_dn_mbps_ge_1'   : 'mean',\
                                                       'max_dn_mbps_ge_10'  : 'mean',\
                                                       'max_dn_mbps_ge_100' : 'mean',\
                                                       'max_dn_mbps_ge_250' : 'mean',\
                                                       'max_up_mbps_ge_100' : 'mean',\
                                                       'max_up_ge_1'        : 'mean',\
                                                       'max_dn_ge_1'        : 'mean',\
                                                       'fiber_100u'         : 'mean',\
                                                       'fiber_100e'         : 'mean'})

# Rename the columns for readability
ret_df = ret_df.rename( columns = { 'max_dn_mbps_ge_1'  : 'n_isp',\
                                   'max_dn_mbps_ge_10'  : 'n_dn10',\
                                   'max_dn_mbps_ge_100' : 'n_dn100',\
                                   'max_dn_mbps_ge_250' : 'n_dn250' ,\
                                   'max_up_mbps_ge_100' : 'n_up100',\
                                   'fiber_100u'         : 'n_fiber_100u',\
                                   'fiber_100e'         : 'fiber_100u_exists',\
                                   'max_up_ge_1'        : 'max_up',\
                                   'max_dn_ge_1'        : 'max_dn'}) 

ret_df.set_index(ret_df.tract, inplace = True)
ret_df.drop(columns=['tract'], inplace=True)
ret_df = ret_df.round(3)



'''
blocks = fcc.geoid.drop_duplicates().sort_values().reset_index(drop = True)
blocks = pd.Series(data = np.zeros(blocks.shape[0]), index = blocks, name = "zero").astype(int)
blocks = blocks.reset_index()

fcc['tract'] = fcc['geoid'] // 10000


def get_var(query, agg_fn, name, varname):

    df_bl = fcc.query(query).groupby("geoid")[varname].apply(agg_fn).reset_index(name = name)

    # Ensure that the blocks are there,
    #  even if they don't have observations!
    df_bl = df_bl.merge(blocks, how = "outer")
    df_bl[name] = df_bl[name].fillna(0)
    # Why does this occur twice?
    df_bl["tract"] = df_bl['geoid'] // 10000
    df_tr = df_bl.groupby("tract")[name].mean()

    print(name)
    
    return df_tr


nisp  = get_var(name = "n_isp",   varname = "provider", agg_fn = pd.Series.count, query = "max_dn_mbps >= 1")
dn10  = get_var(name = "n_dn10",  varname = "provider", agg_fn = pd.Series.count, query = "max_dn_mbps >= 10")
dn100 = get_var(name = "n_dn100", varname = "provider", agg_fn = pd.Series.count, query = "max_dn_mbps >= 100")
dn250 = get_var(name = "n_dn250", varname = "provider", agg_fn = pd.Series.count, query = "max_dn_mbps >= 250")
up100 = get_var(name = "n_up100", varname = "provider", agg_fn = pd.Series.count, query = "max_up_mbps >= 100")


fiber_exists = get_var(name = "fiber_100u_exists", varname = "provider", agg_fn = lambda x: 1,
                       query = "(max_up_mbps >= 100) & (tech == 5)")
# How are these different?
fiber_100u = get_var(name = "n_fiber_100u", varname = "provider", agg_fn = pd.Series.count, 
                     query = "(max_up_mbps >= 100) & (tech == 5)")

max_dn = get_var(name = "max_dn", varname = "max_dn_mbps", agg_fn = pd.Series.max, query = "(max_dn_mbps > 1)")
max_up = get_var(name = "max_up", varname = "max_up_mbps", agg_fn = pd.Series.max, query = "(max_dn_mbps > 1)")


constr_tracts = pd.concat([nisp, dn10, dn100, dn250, fiber_100u, fiber_exists, max_dn, max_up], axis = 1)
constr_tracts = constr_tracts.round(3)
constr_tracts.sort_index(inplace = True)
constr_tracts.index.name = "geoid"

'''


print("Completed. Saving file...\n")
print(f"Number of census tracts: {ret_df.index.nunique()}\n")
ret_df.to_csv("data/fcc_constructed.csv.gz")  
print("Done. File saved.\n")