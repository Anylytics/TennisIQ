# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 23:05:47 2016

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

def generateScoreDistMatrix(pointData, name, topN):
    rows = [x for x in pointData if x[1] == name and x[3] == topN]
    tennisScores = [0, 15, 30, 40, 50]
    scoreDistVals = np.zeros((5,5))
    for idx, score1 in enumerate(tennisScores):
        for idy,score2 in enumerate(tennisScores):
            theScore = [x for x in rows if x[2]==str(score1)+'-'+str(score2)]
            if len(theScore) == 1 and len(theScore[0]) >= 8 and theScore[0][-2]>=0:
                theScore = theScore[0]
                scoreDistVals[idx,idy] = theScore[-2]
            else:
                scoreDistVals[idx,idy] = np.nan
    return scoreDistVals




fname = "Processed/zscore_headmap_Server.pickle"
with open(fname, 'rb') as handle:
    serverPointData = pickle.load(handle)


#fname = "Processed/zscore_headmap_Returner.pickle"
with open(fname, 'rb') as handle:
    returnerPointData = pickle.load(handle)


rows = [x for x in returnerPointData if x[1] == 'Novak Djokovic' and x[3] == '5' and x[2]=='0-0']

names = ['Novak Djokovic', 'Andy Murray', 'Roger Federer', 'Stanislas Wawrinka', 'Rafael Nadal', 'Kei Nishikori']
#names = ['Novak Djokovic']
topN = '20'

for name in names:

    #all_zscores = [x[-1] for x in pointData if x[3] == topN and int(x[6])>minPoints]
    servingMatrix = generateScoreDistMatrix(serverPointData, name, topN)
    returningMatrix = generateScoreDistMatrix(returnerPointData, name, topN)
    
    
    fig, axes = plt.subplots(nrows=1, ncols=2, sharex=False, sharey = False, figsize=(8, 8), dpi=180)    
    labels = ['Love', '15', '30', '40', 'Adv']
    axes[0].imshow(servingMatrix, interpolation='nearest', cmap='YlGnBu', vmin=0, vmax=2, origin='lower')
    #axes[0].set_xlabel('Server Score')
    axes[0].set_ylabel('Returner Score')
    axes[0].set_xticks([0,1,2,3,4])
    axes[0].set_yticks([0,1,2,3,4])
    axes[0].set_xticklabels(labels)
    axes[0].set_yticklabels(labels)
    axes[0].set_title('%s Serving' % (name))
        
    im = axes[1].imshow(returningMatrix, interpolation='nearest', cmap='YlGnBu', vmin=0, vmax=2, origin='lower')
    #axes[1].set_xlabel('Server Score')
    #axes[1].set_ylabel('Returner Score')
    axes[1].set_xticks([0,1,2,3,4])
    axes[1].set_yticks([])
    axes[1].set_xticklabels(labels)
    #xes[1].set_yticklabels(labels)
    axes[1].set_title('%s Returning' % (name))
    fig.text(0.45, 0.04, 'Server Score', ha='center')
    plt.tight_layout()  
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax, ticks=[0, 1, 2])
    cbar.set_ticklabels(['Worst', 'Average', 'Best'])
  

    plt.show()
    plt.draw()
    
    plt.savefig('Figures/%s_topN_%s.png' % (name, topN),figsize=(12, 12), dpi=180)
