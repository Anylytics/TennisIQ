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

#if 'matchMatrix' not in locals():
#    #Load the data back in
#    matchMatrix = np.genfromtxt('Processed/points.csv', delimiter=',', skip_header=1, dtype=np.int8)


#Plot 1: Roger Federer in different point configurations when serving
rgIndex = allPlayers.index('Roger Federer')
rgMatches = matchMatrix[matchMatrix[:,2]==rgIndex,:]

#Prior -- Overall Percentage of Points won
percentPointsWon = float(np.sum(rgMatches[:,4]))/rgMatches.shape[0]

#Liklihood Function - P(Opponent | Win Pt)
opponentMatrix = np.zeros((len(allPlayers),len(allPlayers)), dtype=np.float)
rgPointsWon = rgMatches[rgMatches[:,4] == 1]
rgPointsWonOpponents = rgPointsWon[:,3]

opponentMatrix[rgIndex,:] = np.bincount(rgPointsWonOpponents,minlength=opponentMatrix.shape[1])/np.sum(np.sum(opponentMatrix[rgIndex,:]))

plt.figure(1)
plt.plot(opponentMatrix[rgIndex,:])

#Liklihood Function - P(Score | WinPt)

rgPointsWonScore = rgPointsWon[:,5:7]

