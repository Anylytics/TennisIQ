# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 23:25:41 2016

@author: guiltyspark
"""

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

pointData = []

# Read The Data 
with open('Analysis_Nitin/heatMapReturner.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader, None)
    for row in csvreader:
        pointData.append(row)
        
#Calculate the Z-Score for all the players at 0-0 topN = 100
topN = '10'
possiblescores = ['0-0', '0-15','0-30', '0-40', 
'15-0', '15-15','15-30', '15-40',
'30-0', '30-15', '30-30', '30-40',
'40-0', '40-15', '40-30', '40-40',
'50-40', '40-50']

for currscore in possiblescores:
    rows = [ind for ind,x in enumerate(pointData) if x[2]==currscore and x[3] == topN and int(x[6])>50]
    scores = np.array(map(lambda x: float(pointData[x][5]), rows))
    zscores = spstats.mstats.zscore(scores)
    tmp = map(lambda x,y: pointData[x].append(y), rows, zscores)
    

name = 'Roger Federer'
all_zscores = [x[-1] for x in pointData if x[3] == topN and int(x[6])>50]
all_topNpoints = [x for x in pointData if x[3] == topN and int(x[6]) > 50]

rows = [x for x in pointData if x[1] == name and x[3] == topN]
tennisScores = [0, 15, 30, 40, 50]
scoreDistVals = np.zeros((5,5))
for idx, score1 in enumerate(tennisScores):
    for idy,score2 in enumerate(tennisScores):
        theScore = [x for x in rows if x[2]==str(score1)+'-'+str(score2)]
        if len(theScore) == 1 and len(theScore[0]) >= 8:
            theScore = theScore[0]
            scoreDistVals[idx,idy] = theScore[-1]
        else:
            scoreDistVals[idx,idy] = np.nan
plt.figure(3)
plt.clf()
plt.imshow(scoreDistVals, interpolation='none', cmap='jet', vmin=min(all_zscores), vmax=max(all_zscores))
plt.colorbar()
plt.title(name)
plt.xlabel('Server Score')
plt.ylabel('Returner Score')
plt.savefig('FiguresReturner/'+name+'.png')
