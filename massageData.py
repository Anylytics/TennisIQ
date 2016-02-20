# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 07:57:46 2016

@author: guiltyspark
"""

import numpy as np

import csv
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import numpy as np
import itertools
import pprint

pp = pprint.PrettyPrinter(indent=4)

matchData = []

# Read The Data 

with open('Data/pbp_matches_atp_main_current.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        matchData.append(row)



for idx, row in enumerate(matchData[1:]):
    if idx>0:
        break
    print row