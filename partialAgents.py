# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
from operator import sub, add

class PartialAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up!"
        name = "Pacman"

    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like I just died!"

    # For now I just move randomly
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# # # # #
#  Helper Functions
# # # # #
def manhattanDist(t1,t2):
  return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])

def getClosestFoodPosition(curPos,foodPosList):
    closestFoodPos = foodPosList[0]
    temp = manhattanDist(curPos,foodPosList[0])

    for foodPos in foodPosList:                         
        if manhattanDist(curPos,foodPos) < temp:
            temp = manhattanDist(curPos,foodPos)
            closestFoodPos = foodPos
    
    return closestFoodPos

# get corners that we can actually travel to
def getTravelableCorners(state):
    corners = api.corners(state)
    travelableCorners = []   
    

    offsets = [(1,1), (-1,1), (1,-1), (-1,-1)]
    for i in range(len(corners)):
        travelableCorners.append(tuple(map(add, corners[i], offsets[i])))
    
    return travelableCorners





class CornerSeekingAgent(Agent):    

    ## Create a variable to hold the last position and visited corners
    def __init__(self):
         self.lastPos = (9,1)
         self.visitedCorners = []         
    
    def getAction(self, state):
        
        curPos = api.whereAmI(state)                                     
        legal = api.legalActions(state)   
        corners = getTravelableCorners(state)  
        #do not include corners we have visited before
        corners = list(set(self.visitedCorners) ^ set(corners))
        print(corners)            
                
        ## Get nodes near pacman        
        nodesDict = {} # key is position, value is direction

        for a in legal:                        
            if a == "West":
                newNode = tuple(map(sub, curPos, (1,0)))                
                nodesDict[newNode] = "West"
            elif a == "East":
                newNode = tuple(map(add, curPos, (1,0)))                
                nodesDict[newNode] = "East"
            elif a == "North":
                newNode = tuple(map(add, curPos, (0,1)))                
                nodesDict[newNode] = "North"
            elif a == "South":
                newNode = tuple(map(sub, curPos, (0,1)))
                nodesDict[newNode] = "South"
        
        ## Remove previous position
        nodesDict.pop(self.lastPos, None)
        
        ## Find node with the smallest heuristic (node closest to destination)
        destPos = (9,1)                
        if len(corners) != 0:
            destPos = corners.pop()
        heuristic = 0
        direction = "Stop"               

        if destPos != curPos:                        
            if len(nodesDict) != 0:
                
                # use the first key in dictionary as base heuristic
                pos = list(nodesDict.keys())[0]
                heuristic = manhattanDist(pos,destPos)
                direction = nodesDict[pos]

                # make sure we get the node which has the smallest heuristic
                for pos in nodesDict:                        
                    if manhattanDist(pos,destPos) < heuristic:
                        heuristic = manhattanDist(pos,destPos) 
                        direction = nodesDict[pos]                                    

                    # print("node: " + str(pos) + ", heuristic: " + str(manhattanDist(pos,destPos))) 
        else:
            self.visitedCorners.append(destPos)
            direction = "Stop"      

        
        # Move in a direction
        self.lastPos = curPos

        # print("\t Go " + direction)                                
                      
        return api.makeMove(direction, legal)



        
