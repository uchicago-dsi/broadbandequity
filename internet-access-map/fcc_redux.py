#!/usr/bin/env python

import os
import pandas as pd

ifile = "data/fcc.csv.bz2"
ofile = "data/fcc_redux.csv.gz"

columns = ["Census Block FIPS Code", "DBA Name", "Provider ID", 
           "Technology Code", "Consumer", # "Business", 
           "Max Advertised Downstream Speed (mbps)", 
           "Max Advertised Upstream Speed (mbps)"]

col_dict = {"Provider ID" : "provider", "DBA Name" : "dba", 
            "Census Block FIPS Code" : "geoid", 
            "Technology Code" : "tech", 
            "Consumer" : "consumer", # "Business" : "business", 
            "Max Advertised Downstream Speed (mbps)" : "max_dn_mbps",
            "Max Advertised Upstream Speed (mbps)" : "max_up_mbps"}


chunkerator = pd.read_csv(ifile, chunksize = 1000000, usecols = columns)

if os.path.exists(ofile): os.remove(ofile)

providers = []

for ci, chunk in enumerate(chunkerator):

    chunk.rename(columns = col_dict, inplace = True)
    chunk.query("consumer == 1", inplace = True)
    chunk.query("geoid < 570000000000000", inplace = True)
    chunk.query("tech != 60", inplace = True) # satellite
    chunk.drop("consumer", axis = 1, inplace = True)
    chunk["tech"] = chunk.tech // 10
    chunk["dba"]  = chunk.dba.str.replace(",", "")

    print(ci, end = " ", flush = True)
    chunk.to_csv(ofile, mode = "a", compression = "gzip",
                 index = False, header = (ci == 0))
