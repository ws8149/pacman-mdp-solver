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
         
    #mark wall as "#", empty space as "0"
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):                        
            if walls[i][j] == True:
                myMap.setValue(i,j,"###")
            else:
                myMap.setValue(i,j, 0.0)                

    ##try 
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):
            val = myMap.getValue(i,j)       
            if val == -8 or val == 5.0:
                myMap.setValue(i,j, 0.0)

    #mark food as "5"
    for f in food:        
        myMap.setValue(f[0],f[1], 5.0)
        
    for g in ghosts:       
        # for some reason the api returns a float ??    
        myMap.setValue(int(g[0]),int(g[1]), -8.0)

    
    return myMap

def updateMap(myMap,food,ghosts):
    #remove prev ghost or food location 
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):
            val = myMap.getValue(i,j)       
            if val == -8 or val == 5.0:
                myMap.setValue(i,j, 0.0)
       
    #mark food as "5"
    for f in food:        
        myMap.setValue(f[0],f[1], 5.0)

    #mark ghost location
    for g in ghosts:       
        # for some reason the api returns a float ??    
        myMap.setValue(int(g[0]),int(g[1]), -8.0)


#Get food value from map, returns current position food value if wall or out of bounds is detected
def getFoodValue(myMap, pos, curPos,):
    
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

#gets the maximum expected value in key-value pair form eg: ['North', 7.2]
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
    return max(expectedValues.items(), key=lambda k: k[1])

#do value iteration, updating every position in the map
def valueIteration(myMap):
    reward = 0
    discount = 1      
    for i in range(myMap.getWidth()):
        for j in range(myMap.getHeight()):
            val = myMap.getValue(i,j)            
            if val != "###" and val != 5 and val != -8:                
                moves = buildMoves((i,j),myMap)                 
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
        
        print("----------------------------")         
         

        #build moves              
        legal = api.legalActions(state)
        curPos = api.whereAmI(state)                                 

        #build map 
        food = api.food(state)
        walls = state.getWalls()
        ghosts = api.ghosts(state)             

        # if (self.myMap.getHeight() == 0):
        #     print("building map..")
        #     self.myMap = buildMap(walls,food,ghosts)            
        # else:    
        #     print("updating map..")    
        #     updateMap(self.myMap,food,ghosts)                    
        self.myMap = buildMap(walls,food,ghosts)            

        moves = buildMoves(curPos,self.myMap)                       
        
        
        self.myMap.prettyDisplay()        
        print "------myMap------"    
        #do x value iterations
        for i in range(10):
            valueIteration(self.myMap)
        self.myMap.prettyDisplay()         
        
                          

        #get best move
        moves = buildMoves(curPos,self.myMap) 
        direction = getMaxExpectedValue(moves)[0]
        print("moves:")
        print(moves)        
        print("Go: " + direction)                         
                
        #c = raw_input("Continue? ")        
        return api.makeMove(direction, legal)





