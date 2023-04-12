#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:35:05 2023

@author: chandlerhall
"""


import os
import sys
### add system path to get other library directories
sys.path[0] = os.path.join(os.path.abspath(''),'..')

import warnings
import pandas as pd
import zipfile
import glob
import json
warnings.filterwarnings('ignore')

# Read in the ACS_categories file for percentage calculation
ACS_CAT_FILE_2017 = open("tmpdata/acs_data/acs_categories_2017.json", "r")
ACS_CAT_2017 = json.load(ACS_CAT_FILE_2017)


ACS_CAT_2021 = {k.replace(u'17', '21') : v.replace(u'17', '21') for k, v in ACS_CAT_2017.items()}

with open('/tmp/data/acs_data/acs_categories_2021.json', 'w') as f:
    json.dump(ACS_CAT_2021, f)
    
    