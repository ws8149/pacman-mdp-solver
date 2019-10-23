# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
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

def getPossibleMoves(direction):
    if (direction == Directions.WEST ):
        return ['West', 'South', 'North']


def buildMap(walls, food):    
    myMap = walls
    for i in range(myMap.width):
        for j in range(myMap.height):
            #mark wall as "-1", empty space as "0"
            if myMap[i][j] == True:
                myMap[i][j] = -1
            else:
                myMap[i][j] = 0

                
    #mark food as "9"
    for f in food:
        myMap[f[0]][f[1]] = 5
    return myMap

#Get food value from map, returns current position food value wall is detected
def getFoodValue(myMap, pos, curPos,):
    if myMap[pos[0]][pos[1]] == -1:
        return myMap[curPos[0]][curPos[1]]
    else:
        return myMap[pos[0]][pos[1]]
        

def buildMoves(curPos, myMap):
    
    moves = {}
    directions = ['West','East','North','South']
    for a in directions:  
        
        if a == "West":
            pos = tuple(map(sub, curPos, (1,0)))                            
            foodValue = getFoodValue(myMap,pos,curPos)
            moves["West"] = foodValue

        elif a == "East":            
            pos = tuple(map(add, curPos, (1,0))) 
            foodValue = getFoodValue(myMap,pos,curPos)
            moves["East"] = foodValue  

        elif a == "North":           
            pos = tuple(map(add, curPos, (0,1)))  
            foodValue = getFoodValue(myMap,pos,curPos)
            moves["North"] = foodValue  

        elif a == "South":                        
            pos = tuple(map(sub, curPos, (0,1)))        
            foodValue = getFoodValue(myMap,pos,curPos)
            moves["South"] = foodValue  
    
    return moves      

  
        

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
       
    
    def final(self, state):
        print "Looks like the game just ended!"

    
    def getAction(self, state):
        
        print("----------------------------")         

        #build moves              
        legal = api.legalActions(state)
        curPos = api.whereAmI(state)                                 

        #build map
        food = api.food(state)
        walls = state.getWalls()
        myMap = buildMap(walls,food)              

        moves = buildMoves(curPos,myMap) 

        
        #find expected values
        expectedValues = {}
        possibleMoves = ['West','East','North','South']
        for m in possibleMoves:
            if m == 'West':
                expectedValues['West'] = 0.8 * moves['West'] + 0.1 * moves['North'] + 0.1 * moves['South']
            elif m == 'East': 
                expectedValues['East'] = 0.8 * moves['East'] + 0.1 * moves['North'] + 0.1 * moves['South']
            elif m == 'North': 
                expectedValues['North'] = 0.8 * moves['North'] + 0.1 * moves['West'] + 0.1 * moves['East']
            elif m == "South":
                expectedValues['South'] = 0.8 * moves['South'] + 0.1 * moves['West'] + 0.1 * moves['East']
                                                   
        meu = max(expectedValues.items(), key=lambda k: k[1])[0]

        print("moves:")
        print(moves)
        print("expectedValues: ")
        print(expectedValues)    
        print("meu:" + meu)                
                
        ##c = raw_input("Continue? ")
        return api.makeMove(meu, legal)





