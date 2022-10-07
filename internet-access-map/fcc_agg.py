#!/usr/bin/env python 

import pandas as pd
import numpy as np

print("Loading FCC data...\n")

fcc = pd.read_csv("data/fcc_redux.csv.gz",  
                  usecols = ["provider", "geoid", "tech", "max_dn_mbps", "max_up_mbps"])

print("Data loaded.\nConstructing variables...\n")

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
print("Completed. Saving file...\n")
constr_tracts = constr_tracts.round(3)
constr_tracts.sort_index(inplace = True)
constr_tracts.index.name = "geoid"
print(f"Number of census tracts: {constr_tracts.index.nunique()}\n")
constr_tracts.to_csv("data/fcc_constructed.csv.gz")  
print("Done. File saved.\n")
