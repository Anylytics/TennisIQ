# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:25:41 2016

@author: guiltyspark
"""
import pandas as pandas
import numpy as np
import scipy.stats as spstats
import csv
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import numpy as np
import itertools
import pprint
from datetime import datetime
import re

pp = pprint.PrettyPrinter(indent=4)

players = []

# Read The Data 
with open('Processed/players.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        players.extend(row)
        