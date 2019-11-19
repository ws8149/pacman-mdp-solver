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

#variable initializations
foodValue = 5
ghostValue = -8
reward = 0.7
discount = 0.7
numberOfIterations = 10

#grid used in practicals
class Grid:

	# Adapted from Lab Solutions 5 (Parsons, 2017)
	# Draws a grid - where an array has one position for each element on the grid
	# Not used for any function in the map other than printing a pretty grid

	def __init__(self, width, height):
		self.width = width
		self.height = height
		subgrid = []
		for i in range(self.height):
			row = []
			for j in range(self.width):
				row.append(0)
			subgrid.append(row)

		self.grid = subgrid

	def setValue(self, x, y, value):
		self.grid[y][x] = value

	def getValue(self, x, y):
		return self.grid[y][x]

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	#Print grid
	def display(self):
		for i in range(self.height):
			for j in range(self.width):
				# print grid elements with no newline
				print self.grid[i][j],
			print
		print

	def prettyDisplay(self):
		for i in range(self.height):
			for j in range(self.width):
				# print grid elements with no newline
				print self.grid[self.height - (i + 1)][j],
			print
		print

  

def buildMap(walls, food, ghosts):            
    myMap = Grid(walls.width,walls.height)    
    
    #mark wall as "###", empty space as "0"
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):                        
            if walls[i][j] == True:
                myMap.setValue(i,j,"###")
            else:
                myMap.setValue(i,j, 0.0)                

    
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):
            val = myMap.getValue(i,j)       
            if val == ghostValue or val == foodValue:
                myMap.setValue(i,j, 0.0)

    #mark food as "5"
    for f in food:        
        myMap.setValue(f[0],f[1], foodValue)

    #mark ghosts as "-8"        
    for g in ghosts:               
        myMap.setValue(int(g[0]),int(g[1]), ghostValue)

    
    return myMap


#Get utility from position in map, returns current position utility if wall or out of bounds is detected
def getUtility(myMap, pos, curPos):
    
    #check for out of bounds
    if pos[0] < 0 or pos[0] > myMap.getWidth() - 1 :
        return myMap.getValue(curPos[0],curPos[1])        
    
    if pos[1] < 0 or pos[1] > myMap.getHeight() - 1:
        return myMap.getValue(curPos[0],curPos[1])
    
    if myMap.getValue(pos[0],pos[1]) == "###":    
        return myMap.getValue(curPos[0],curPos[1])
    else:
        return myMap.getValue(pos[0],pos[1])
        
#Builds the possible moves of a position
def buildMoves(curPos, myMap):
    
    moves = {}
    directions = ['West','East','North','South']
    for a in directions:  
        
        if a == "West":
            pos = tuple(map(sub, curPos, (1,0)))                            
            utility = getUtility(myMap,pos,curPos)
            moves["West"] = utility

        elif a == "East":            
            pos = tuple(map(add, curPos, (1,0))) 
            utility = getUtility(myMap,pos,curPos)
            moves["East"] = utility

        elif a == "North":           
            pos = tuple(map(add, curPos, (0,1)))  
            utility = getUtility(myMap,pos,curPos)
            moves["North"] = utility

        elif a == "South":                        
            pos = tuple(map(sub, curPos, (0,1)))        
            utility = getUtility(myMap,pos,curPos)
            moves["South"] = utility
    
    return moves      

#gets the maximum expected value in key-value pair form eg: ['North', 7.2]
#Calculates expected value by summing up the probabilities multiplied by the utility
def getMaxExpectedValue(moves):
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
    # return the highest value from expectedValues
    return max(expectedValues.items(), key=lambda k: k[1])


#do value iteration, updating every position in the map
def valueIteration(myMap):    
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):
            val = myMap.getValue(i,j)            
            if val != "###" and val != foodValue and val != ghostValue:                
                moves = buildMoves((i,j),myMap)                 
                #apply bellman equation
                u = reward + discount * getMaxExpectedValue(moves)[1]
                myMap.setValue(i,j,u)
                
                

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"
        self.myMap = Grid(0,0)

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)
       
    
    def final(self, state):        
        print "Looks like the game just ended!"

    
    def getAction(self, state):
        
        #print("----------------------------")         
         
        legal = api.legalActions(state)
        curPos = api.whereAmI(state)                                 

        #build map 
        food = api.food(state)
        walls = state.getWalls()
        ghosts = api.ghosts(state)                            
        self.myMap = buildMap(walls,food,ghosts)                                                
                
          
        #do value iteration on map
        for i in range(numberOfIterations):
            valueIteration(self.myMap)
        
        #self.myMap.prettyDisplay()

        #get best move
        moves = buildMoves(curPos,self.myMap) 
        direction = getMaxExpectedValue(moves)[0]                                 
                
        #c = raw_input("Continue? ")        
        return api.makeMove(direction, legal)





