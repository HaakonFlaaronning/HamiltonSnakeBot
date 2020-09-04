import math
import numpy as np
import random
import pygame as pg
from theSnake import *
from apple import Apple
from node import Node
from myHamilton import MyHamilton



#-----------------------------------------------------------------------------------------------------------------------
scale = 20

# Start game
width = 340
height = 360

rows = int(height/scale)
cols = int(width/scale)


#Create the nodes
num = 0
nodes = [[None for x in range(cols)] for y in range(rows)]
for y in range(rows):
    for x in range(cols):
        node = Node()
        node.pos = [x*scale, y*scale]
        node.nodeNumber = num
        nodes[y][x] = node
        num = num + 1

# Array representation of node matrix
nodeArray = []
for y in range(rows):
    for x in range (cols):
        nodeArray.append(nodes[y][x])

# Adjacency matrix stuff
numberOfElements = 1
for dim in np.shape(nodes): numberOfElements *= dim

adjMatrix = np.zeros((numberOfElements,numberOfElements))
for node in range(numberOfElements):
    if(node-1 >= 0 and node%cols != 0):
        adjMatrix[node][node-1] = 1
    if(node+1 < numberOfElements and (node+1)%cols != 0):
        adjMatrix[node][node+1] = 1
    if(node-cols >= 0):
        adjMatrix[node][node-cols] = 1
    if(node+cols < numberOfElements):
        adjMatrix[node][node+cols] = 1

# NodeNumber + HamiltonIndex getters and setters
def getNodeNumberFromPosition(position):
    for node in nodeArray:
        if(node.pos == position):
            return node.nodeNumber

def getAdjNodes(nodeNumber):
    adjacentNodes = []
    for index in range(0, numberOfElements):
        if(adjMatrix[nodeNumber][index] == 1):
            for node in nodeArray:
                if(node.nodeNumber == index):
                    adjacentNodes.append(node)
    return adjacentNodes

def setHamiltonIndex(node):
    index = 0
    for num in hamilton.path:
        if(num == node.nodeNumber):
            node.hamiltonIndex = index
        else:
            index += 1

def getHamiltonIndexFromNodeNumber(nodeNumber):
    index = 0
    for num in hamilton.path:
        if(num == nodeNumber):
            return index
        else:
            index += 1

def getNodeFromIndex(index):
    for node in nodeArray:
        if(node.hamiltonIndex == index):
            return node

# Reset temporary hamilton indexes
def resetIndexes(nodes):
    for node in nodes:
        node.tempIndex = -2

# Distance between indexes in hamilton cycle - With wrap around
def path_distance(a,b):
    if(a<b):
        return a-b-1
    else:
        return b-a-1+len(nodeArray)

hamilton = MyHamilton()
hamilton.makeHamiltonPath(rows,cols,nodes)
hamilton.path = list(dict.fromkeys(hamilton.path))
hamIndexes = []
nodeNumbers = []

for node in nodeArray:
    setHamiltonIndex(node)
    nodeNumbers.append(node.nodeNumber)
    hamIndexes.append(node.hamiltonIndex)

#Create the snake and apple
pg.init()
win = pg.display.set_mode((width,height))
pg.display.set_caption("Snake")
test = SnakeObj()
apple = Apple()
apple.setPos()
applePosition = apple.getPos()
clock = pg.time.Clock()

#-----------------------------------------------------------------------------------------------------------------------
run = True
dead = False
while run:
#TODO: for hvert steg, bestem hvilken av de nærliggende rutene den skal gå til basert på korteste avstand og at hodet aldri overtar halen i hamilton sykelen
    resetIndexes(nodeArray)
    #Head
    currentNodeNumber = getNodeNumberFromPosition(test.getPosition())
    currentNodeIndex = getHamiltonIndexFromNodeNumber(currentNodeNumber)
    #Adjacent
    adjacentNodes = getAdjNodes(currentNodeNumber)
    #Tail
    tailPosition = test.getTailPosition()
    tailNodeNumber = getNodeNumberFromPosition(tailPosition)
    tailIndex = getHamiltonIndexFromNodeNumber(tailNodeNumber)
    #Apple
    appleNodeNumber = getNodeNumberFromPosition(apple.pos)
    if(currentNodeIndex > getHamiltonIndexFromNodeNumber(appleNodeNumber)):
        appleIndex = getHamiltonIndexFromNodeNumber(appleNodeNumber) + len(hamilton.path)
    else:
        appleIndex = getHamiltonIndexFromNodeNumber(appleNodeNumber)


    # Remove adjacent nodes that are inbetween head and tail (invalid shortcut)
    tempIndexes = []
    for i in range(len(adjacentNodes)-1,-1,-1):
        node = adjacentNodes[i]
        if (currentNodeIndex > node.hamiltonIndex):
            node.tempIndex = node.hamiltonIndex + len(hamilton.path)
        else:
            node.tempIndex = node.hamiltonIndex
        tempIndexes.append(node.tempIndex)
        # Removing
        if (currentNodeIndex > tailIndex):
            if(node.hamiltonIndex <= currentNodeIndex and node.hamiltonIndex > tailIndex-1):
                del (adjacentNodes[i])
        elif(currentNodeIndex < tailIndex):
            if (node.hamiltonIndex <= currentNodeIndex or node.hamiltonIndex > tailIndex-1):
                del (adjacentNodes[i])


# Find node that is closest to the apple
    adjacentIndexes = []
    currentLargest = -999
    if(currentNodeIndex == len(nodeArray)-1):
        nextIndex = 0
    else:
        nextIndex = currentNodeIndex+1
    selectedNode = getNodeFromIndex(nextIndex)

    # Maximum cutting:
    maxCut = path_distance(currentNodeIndex,tailIndex)- test.tailIncrease - 3 # Buffer
    for node in adjacentNodes:
        adjacentIndexes.append(node.hamiltonIndex)
        if(node.tempIndex <= appleIndex):
            tempLargest = node.tempIndex
            if(tempLargest >= currentLargest and abs(node.tempIndex-currentNodeIndex) <= maxCut):
                currentLargest = tempLargest
                selectedNode = node

    #print("CurrentIndex: ", currentNodeIndex, "TailIndex: ", tailIndex, "TempIndexes: ", tempIndexes,"AppleIndex: ", appleIndex,"Adjacent indexes: ",adjacentIndexes, "Selected index: ",selectedNode.hamiltonIndex)
    while test.pos != selectedNode.pos and run:
        test.goToPosition(selectedNode.pos)
        test.update()

        for event in pg.event.get():  # This will loop through a list of any keyboard or mouse events.
            if event.type == pg.QUIT:  # Checks if the red button in the corner of the window is clicked
                run = False  # Ends the game loop

        win.fill((0, 0, 0))

        x = 0
        while x <= width:
            pg.draw.line(win, (255, 255, 255), (x, 0), (x, height))
            x = x + scale

        y = 0
        while y <= height:
            pg.draw.line(win, (255, 255, 255), (0, y), (width, y))
            y = y + scale

        if(test.hitApple(apple.pos[0], apple.pos[1])):
            apple.setPos()
            applePosition = apple.getPos()

        if(test.isDead()):
            test.setPos(0,0)
            dead = True
            break

        test.show()
        apple.show()

        pg.display.update()
        clock.tick(150)
pg.quit()





'''keys = pg.key.get_pressed()
if keys[pg.K_LEFT]:
    if not(test.direction == [1,0]):
        test.direction = [-1,0]
if keys[pg.K_RIGHT]:
    if not(test.direction == [-1,0]):
        test.direction = [1,0]

if keys[pg.K_UP]:
    if not(test.direction == [0,1]):
        test.direction = [0,-1]

if keys[pg.K_DOWN]:
    if not(test.direction == [0,-1]):
        test.direction = [0,1]'''
