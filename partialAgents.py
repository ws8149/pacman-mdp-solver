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


class PathfinderAgent(Agent):

    # Create a variable to hold the last position
    def __init__(self):
         self.lastPos = (9,1)

    def getAction(self, state):
        
        curPos = api.whereAmI(state)                                     
        legal = api.legalActions(state) 

        
        
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
        
        ## Find path to destination
        destPos = (18,9)
        heuristic = 0
        direction = "Stop"       
        
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

                print("node: " + str(pos) + ", heuristic: " + str(manhattanDist(pos,destPos)))       

        
        # Move in a direction
        self.lastPos = curPos

        print("\t Go " + direction)                
        
        if destPos == curPos:
            direction = "Stop"

        
        
        ## Stop
        #return api.makeMove(Directions.STOP, legal)
        
        ## GoWest
        # if Directions.WEST not in legal:
        #     return api.makeMove("Stop", legal)
        # else:
        #     print(api.whereAmI(state))
        #     return api.makeMove("West", legal)        
        
        return api.makeMove(direction, legal)