import math
import random
import pygame as pg

class Apple():
    def __init__(self):
        self.pos = [0,0]

    def setPos(self):
        from snake import width, height, scale, test
        cols = math.floor(width/scale)
        rows = math.floor(height/scale)

        while True:
            found = False
            posX = math.floor(random.randrange(cols))*scale
            posY = math.floor(random.randrange(rows))*scale

            headPos = test.getPosition()
            tailPos = test.getTailPosition()

            if((posX == headPos[0] and posY == headPos[1]) or (posX == tailPos[0] and posY == tailPos[1])):
                continue
            for i in range(len(test.tail)-1):
                if(posX == test.tail[i][0] and posY == test.tail[i][1]):
                    found = True
                    break
            if(found == True):
                continue
            else:
                break

        self.pos[0] = posX
        self.pos[1] = posY




    def show(self):
        from snake import win, width, height, scale
        pg.draw.rect(win, (255, 0, 0),(self.pos[0], self.pos[1], scale, scale))

    def getPos(self):
        return self.pos