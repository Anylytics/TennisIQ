# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 17:00:11 2016

@author: guiltyspark
"""
"""
Data Structure:
    0: Date
    1: Tournament ID
    2: Server ID
    3: Returner ID
    4: WonPoint?
    5: Game Score 1
    6: Game Score 2
    7: Number of Games Played
    8: Number of Sets Played
    9: WinnerID
"""     


import numpy as np
import matplotlib.pyplot as plt

tennisScores = [0, 15, 30, 40, 50]

#Generate point distribution spreads
pointsWon = matchMatrix[matchMatrix[:,4]==1]
#scoreCount = np.array(map(lambda x:int(str(x[0])+str(x[1])), pointsWon[:,5:7]))
scoreCountWin = np.array(map(lambda x: x[0]*1000+x[1], pointsWon[:,5:7]))
scoreCountAll = np.array(map(lambda x: x[0]*1000+x[1], matchMatrix[:,5:7]))
#Exclude TieBreaks
#scoreCount = scoreCount[scoreCount < 100100]
#Transform the score double into a score single
scoreCountWin = np.bincount(scoreCountWin)
scoreCountAll = np.bincount(scoreCountAll)
#Plot the number of points won at each score situation
scoreDistVals = np.zeros((5,5))
for idx, score1 in enumerate(tennisScores):
    for idy,score2 in enumerate(tennisScores):
        if scoreCountAll[score1*1000+score2] > 0:
            scoreDistVals[idx,idy] = float(scoreCountWin[score1*1000+score2])/scoreCountAll[score1*1000+score2]
        else:
            scoreDistVals[idx,idy] = np.nan
plt.imshow(scoreDistVals, interpolation='none', cmap='summer')
plt.colorbar()


#if 'matchMatrix' not in locals():
#    #Load the data back in
#    matchMatrix = np.genfromtxt('Processed/points.csv', delimiter=',', skip_header=1, dtype=np.int8)

#P(WinPt | Opponent)

#Plot 1: Roger Federer in different point configurations when serving
rgIndex = allPlayers.index('Roger Federer')
rgMatches = matchMatrix[matchMatrix[:,2]==rgIndex,:]

#Prior -- Overall Percentage of Points won P(winpt)
percentPointsWon = float(np.sum(rgMatches[:,4]))/rgMatches.shape[0]

#Liklihood Function - P(Opponent | Win Pt) = P(Opponent * WinPt) / P(WinPt)
opponentMatrix = np.zeros((len(allPlayers),len(allPlayers)), dtype=np.float)
rgPointsWon = rgMatches[rgMatches[:,4] == 1]
rgPointsWonOpponents = rgPointsWon[:,3]

#Number of times he beat each opponent
opponentMatrix[rgIndex,:] = np.bincount(rgPointsWonOpponents,minlength=opponentMatrix.shape[1])
#Number of times he played each opponent
opponentMatrix[rgIndex,:] = opponentMatrix[rgIndex,:]/np.sum(np.sum(opponentMatrix[rgIndex,:]))

plt.figure(1)
plt.plot(opponentMatrix[rgIndex,:])

#Liklihood Function - P(Score | WinPt)

rgPointsWonScore = rgPointsWon[:,5:7]

