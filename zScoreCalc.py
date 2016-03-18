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
import cPickle as pickle

pp = pprint.PrettyPrinter(indent=4)

modes = ['Server', 'Returner']

for mode in modes:
    pointData = []
    # Read The Data 
    with open('Analysis_Nitin/heatMap%s.csv' % (mode), 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in csvreader:
            pointData.append(row)
            
    #Calculate the Z-Score for all the players at 0-0 topN = 100
    minPoints = 30        
    topNs = ['5', '10', '20']        
    for topN in topNs:
        possiblescores = ['0-0', '0-15','0-30', '0-40', 
        '15-0', '15-15','15-30', '15-40',
        '30-0', '30-15', '30-30', '30-40',
        '40-0', '40-15', '40-30', '40-40',
        '50-40', '40-50']
        
        for currscore in possiblescores:
            rows = [ind for ind,x in enumerate(pointData) if x[2]==currscore and x[3] == topN and int(x[6])>minPoints]
            scores = np.array(map(lambda x: float(pointData[x][5]), rows))
            zscores = spstats.mstats.zscore(scores)
            max_zscore = max(zscores)
            min_zscore = abs(min(zscores))
            zscore_norm = ((zscores+min_zscore)/(max_zscore+min_zscore))*2
            tmp = map(lambda x,y: pointData[x].append(y), rows, zscore_norm)
            
    tmpCount = 0
    for idx,row in enumerate(pointData):
        if len(row)<8:
            pointData[idx].append(-1)
            tmpCount += 1
            
    print "%d rows of %d not statistically significant" % (tmpCount, len(pointData))
       
    prunedPointData = []
    for row in pointData:
        if row[3] in ['5', '10', '20']:
            prunedPointData.append(row)
    
    np.savetxt("Processed/zscore_heatmap_%s.csv" % (mode), prunedPointData, delimiter=",", fmt='%s')
    fname = "Processed/zscore_headmap_%s.pickle" % (mode)
    with open(fname, 'wb') as handle:
      pickle.dump(prunedPointData, handle)


