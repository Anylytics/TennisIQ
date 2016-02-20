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
from datetime import datetime
import re

pp = pprint.PrettyPrinter(indent=4)

matchData = []

# Read The Data 

with open('Data/pbp_matches_atp_main_current.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        matchData.append(row)

#Step 1, create a lookup table of all the players
player1 = set([row[4] for row in matchData[1:]])
player2 = set([row[5] for row in matchData[1:]])
allPlayers = list(player1.union(player2))
np.savetxt("Processed/players.csv", allPlayers, delimiter=",", fmt='%s')

#Step 2, create a lookup table for all tournaments
touraments = list(set([row[1] for row in matchData[1:]]))
np.savetxt("Processed/tournaments.csv", allPlayers, delimiter=",", fmt='%s')

tourIds = map(lambda x: touraments.index(x[1]), matchData[1:])
player1Ids = map(lambda x: allPlayers.index(x[4]), matchData[1:])
player2Ids = map(lambda x: allPlayers.index(x[5]), matchData[1:])
dates = map(lambda x: datetime.strptime(x[0], '%d %b %y'), matchData[1:])


#Step 2: Go through row by row and 
#for idx, row in enumerate(matchData[1:]):
#    if idx>0:
#        break
    
#row = matchData[1]

scoreConversion = {0: 0, 1:15, 2:30, 3:40}
def scoreConverter(currentScore):
    if currentScore[0,0] < 3 or currentScore[0,1] <3:
        return [scoreConversion[currentScore[0,0]],scoreConversion[currentScore[0,1]]]
    if currentScore[0,0] == currentScore[0,1]:
        return [40, 40]
    if currentScore[0,0]-1 == currentScore[0,1]:
        return [50,40]
    if currentScore[0,0] == currentScore[0,1]-1:
        return [40,50]
    else:
        assert('Score is Busted')
matchMatrix = np.empty((0,8), np.int)
for idz, row in enumerate(matchData[1:]):
    print idz
    scoreLine = row[7]
    

    players = [player1Ids[idz], player2Ids[idz]]
    scoreLine = scoreLine.replace('.', ';')
    gameLines = scoreLine.split(';')
    server = 0
    skippedTb = 0
    for idy, game in enumerate(gameLines):
        if '/' in game:
            skippedTb += 1
            continue
        gameMatrix = np.zeros((len(game),8), np.int)
        gameMatrix[:,0] = dates[idz].strftime('%Y%m%d')
        gameMatrix[:,1] = tourIds[idz]
    
        gameMatrix[:,2] = players[server%2]
        gameMatrix[:,3] = players[(server+1)%2]
        gameMatrix[:,7] = idy + skippedTb
        pointLookup = {'S': 1, 
        'A': 1, 
        'R': 0, 
        'D': 0}
    
        currentScore = np.zeros((1,2), np.int)
        for idx,point in enumerate(game):
            gameMatrix[idx,4] = pointLookup[point]
            gameMatrix[idx,5:7] = scoreConverter(currentScore)
            #Increment Score
            currentScore[0,1-pointLookup[point]]+=1
        
        server += 1
        matchMatrix = np.concatenate((matchMatrix,gameMatrix))


np.savetxt("Processed/points.csv", matchMatrix, delimiter=",", fmt='%s', header="Date, TournamentID, ServerID, ReturnerID, WonPt, GameScore1, GameScore2, NumGamesPlayed")

    
