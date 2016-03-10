# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:25:41 2016

@author: guiltyspark
"""
import shutil
import requests
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
with open('Data/RecentRanks.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader, None)
    for row in csvreader:
        players.append(row)
    
top50 = []
ranks = []
for player in players:
    if player[0][0:4] == '2015' and int(player[2])<=100:
        top50.append(player[1])
        ranks.append(int(player[2]))
        
npranks = np.array(ranks)

lastNames = []
for player in top50:
    lastNames.append(player.split(' ')[-1])
    
batIndex = lastNames.index('Agut')
lastNames[batIndex] = 'Bautista'
leoIndex = lastNames.index('Mayer')
lastNames[leoIndex] = 'mayerl'

for lastName in lastNames:
    print "Processing "+lastName
    url = 'http://www.atpworldtour.com/~/media/tennis/players/gladiator/vibrant/'+lastName+'-full15.png'
    response = requests.get(url, stream=True)
    if response.ok == False:
        del response
        url = 'http://www.atpworldtour.com/~/media/tennis/players/gladiator/2016/'+lastName+'_full_16.png'
        response = requests.get(url, stream=True)
    with open('Pictures/'+lastName+'.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response



