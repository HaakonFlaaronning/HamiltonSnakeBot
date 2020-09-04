import math
import random
import pygame as pg


scale = 20

class SnakeObj(object):

    def __init__(self):
        self.pos = [0,0]
        self.direction = [1,0]
        self.sizeIndex = 0
        self.tailIncrease = 2
        self.tail= []
        self.tailPosition = [0,0]

    def setPos(self, x, y):
        self.pos = [x,y]

    def show(self):
        from snake import win, width, height
        for t in self.tail:
            pg.draw.rect(win, (0, 255, 0), (t[0],t[1], scale, scale))

        pg.draw.rect(win, (0, 0, 255),(self.pos[0]-1, self.pos[1]-1, scale+2, scale+2)) #add this for border around head
        pg.draw.rect(win, (0, 255, 0),(self.pos[0], self.pos[1], scale, scale))

    def update(self):
        if (self.sizeIndex > 0):
            if (self.sizeIndex == len(self.tail)):
                self.tail.pop(0)
            self.tail.append([self.pos[0], self.pos[1]])

        self.pos[0] += self.direction[0]*scale
        self.pos[1] += self.direction[1]*scale

        if (len(self.tail) > 0):
            self.tailPosition = self.tail[0]
        else:
            self.tailPosition = self.pos

    def isDead(self):
        from snake import win, width, height
        if (self.pos[0] < 0 or self.pos[1] < 0 or self.pos[0] > width - scale or self.pos[1] > height - scale):
            self.sizeIndex = 0
            self.tail.clear()
            return True

        for i in range(len(self.tail)):
            if (self.pos[0] == self.tail[i][0] and self.pos[1] == self.tail[i][1]):
                self.sizeIndex = 0
                self.tail.clear()
                return True
        return False

    def hitApple(self, x, y):
        if(self.pos == [x,y]):
            self.sizeIndex += self.tailIncrease
            return True
        return False

    def getPosition(self):
        return self.pos

    def getTailPosition(self):
        return self.tailPosition

    def goToPosition(self,goalPos):
        if (self.pos[1] < goalPos[1]):
            self.direction = [0, 1]
        elif (self.pos[1] > goalPos[1]):
            self.direction = [0, -1]
        elif(self.pos[0] > goalPos[0]):
            self.direction = [-1,0]
        elif(self.pos[0] < goalPos[0]):
            self.direction = [1, 0]




