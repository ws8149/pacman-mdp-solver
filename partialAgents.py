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
  
# # # # #
#  Helper Functions
# # # # #

def manhattanDist(t1,t2):
  return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])

# get corners that we can actually travel to
def getTravelableCorners(state):
    corners = api.corners(state)
    travelableCorners = []   
    

    offsets = [(1,1), (-1,1), (1,-1), (-1,-1)]
    for i in range(len(corners)):
        travelableCorners.append(tuple(map(add, corners[i], offsets[i])))
    
    return travelableCorners


#get corners that have not been visited
def getUnvisitedCorners(corners,visitedCorners):
  return [c for c in corners if c not in visitedCorners]
    

#Creates nodes based on current legal actions and position
def initializeNodesDict(legal,curPos):
    nodesDict = {}
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
    return nodesDict

#Creates nodes based on current legal actions, position and ghost position
def initializeSurvivalMoves(legal,curPos,ghosts):
    moves = {}

    westIsSafe = True
    eastIsSafe = True
    northIsSafe = True
    southIsSafe = True

    ## determine ghost's direction from current position
    offset = tuple(map(sub, curPos, ghosts[0]))
    #print("offset: " + str(offset))             
            
    if offset[0] > 0:
        #print("ghost to the west")
        westIsSafe = False
    elif offset[0] < 0:
        #print("ghost to the east")
        eastIsSafe = False    
    if offset[1] > 0:
        #print("ghost to the south")
        southIsSafe = False
    elif offset[1] < 0:
        #print("ghost to the north")
        northIsSafe = False

    for a in legal:                        
        if a == "West" and westIsSafe:
            pos = tuple(map(sub, curPos, (1,0)))                
            moves[pos] = "West"
        elif a == "East" and eastIsSafe:
            pos = tuple(map(add, curPos, (1,0)))                
            moves[pos] = "East"
        elif a == "North" and northIsSafe:
            pos = tuple(map(add, curPos, (0,1)))                
            moves[pos] = "North"
        elif a == "South" and southIsSafe:
            pos = tuple(map(sub, curPos, (0,1)))
            moves[pos] = "South"
    return moves





class PartialAgent(Agent):    

    ## Create a variable to hold the last position and visited corners
    def __init__(self):
         self.lastPos = (9,1)         
         self.survive = False # If true, pacman will run from ghosts
         self.corner = (1,1)
         self.visitedCorners = []
                   
    def getAction(self, state):
        
        ##Get pacman's surrounding data
        curPos = api.whereAmI(state)                                     
        legal = api.legalActions(state)     
                             
        food = api.food(state)
        capsules = api.capsules(state)       
        if len(capsules) != 0:
            food.append(capsules[0])                               
                
        ghosts = api.ghosts(state)          
        if len(ghosts) != 0:            
            self.survive = True
        else:
            self.survive = False
        
        # each node is a key-value pair where key is position
        # and value is the direction pacman needs to move to get to that position         
        nodesDict = initializeNodesDict(legal,curPos)

        ## Run from ghosts
        if self.survive:
            
            #print("Pacman: " + str(curPos))
            #print("Ghosts: " + str(ghosts))            
            nodesDict = initializeSurvivalMoves(legal,curPos,ghosts)            
            try:
                direction = nodesDict.values()[0]
            except:
                direction = Directions.STOP
            self.lastPos = curPos
            #print("Run from ghost: " + direction)             
            return api.makeMove(direction, legal)
        

        
        ## Remove last position from nodesDict and update the last position  
        nodesDict.pop(self.lastPos, None)               
        self.lastPos = curPos  

        ## Search for food        
        destPos = (0,0)                                       
        
        # Head towards food nearby
        if len(food) != 0:
            destPos = food.pop()
        # Go to corners and look for food
        else:                        
            if (curPos == self.corner):
                self.corner = getTravelableCorners(state)[1]                
                #print("corner reached, switching to next corner" + str(self.corner))
            #print("no food, going to corner: " + str(self.corner))            
            destPos = self.corner 
        
        direction = Directions.STOP
        

        ## Find the closest node to destination by comparing their manhattan distances
        if len(nodesDict) != 0:                
            # use the first key in dictionary as base heuristic
            pos = list(nodesDict.keys())[0]
            heuristic = manhattanDist(pos,destPos)
            direction = nodesDict[pos]

            # get the node with the smallest heuristic (closest to destination)
            for pos in nodesDict:                        
                if manhattanDist(pos,destPos) < heuristic:
                    heuristic = manhattanDist(pos,destPos) 
                    direction = nodesDict[pos]                                    

                # print("node: " + str(pos) + ", heuristic: " + str(manhattanDist(pos,destPos))) 
               
                                            
        return api.makeMove(direction, legal)


