import pygame
from random import randint
import math

class Player():

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.xAcc = 0
        self.yAcc = -2
        self.w = w
        self.h = h
        self.moveSpeed = 5
        self.jumpSpeed = 15
        self.grounded = False
        self.lastX = x
        self.lastY = y
        self.onGreen = False
        self.alternater = 0
        self.onAnObject = False

    def update(self, objectList, level):
        resetLevel = False
        self.onGreen = False
        self.onAnObject = False
        self.lastY = self.y
        self.y -= self.yVel
        self.yVel += self.yAcc
        if(self.yVel < -16):
            self.yVel = -16

        for i in range(0, len(objectList)):

            if(self.x + self.w > objectList[i].x and self.x < objectList[i].x + objectList[i].w):
                if((self.y + self.h > objectList[i].y and self.yVel < 0 and self.lastY + self.h <= objectList[i].y) or (self.onAnObject and self.y + self.h == objectList[i].y)):
                    self.y = objectList[i].y - self.h
                    self.yVel = 0
                    self.grounded = True
                    self.onAnObject = True

                    if(objectList[i].type == 1):
                        pass
                    elif(objectList[i].type == 2):
                        self.onGreen = True
                    elif(objectList[i].type == 3):
                        objectList[i].counting = True
                    elif(objectList[i].type == 4):
                        resetLevel = True
                    elif(objectList[i].type == 5):
                        self.onGreen = True
                        objectList[i].counting = True
                    if(self.onGreen):
                        self.jumpSpeed = 30
                    else:
                        self.jumpSpeed = 15
                elif(self.y < objectList[i].y + objectList[i].h and self.yVel > 0 and self.lastY >= objectList[i].y + objectList[i].h):
                    self.y = objectList[i].y + objectList[i].h
                    self.yVel = 0
                    if(objectList[i].type == 4):
                        resetLevel = True
            if(objectList[i].counting):
                objectList[i].count -= 1
                if(objectList[i].count == 0):
                    objectList.pop(i)
                    i -= 1
                    objectList[i].count = 8
                    objectList.insert(i, Box(-20, -20, 1))

        self.lastX = self.x
        self.x += self.xVel
        self.xVel += self.xAcc

        for i in range(0, len(objectList)):

            if(self.y + self.h > objectList[i].y and self.y < objectList[i].y + objectList[i].h):
                if(self.x + self.w > objectList[i].x and self.xVel > 0 and self.lastX + self.w <= objectList[i].x):
                    self.x = objectList[i].x - self.w
                    self.xVel = 0
                    if(objectList[i].type == 4):
                        resetLevel = True
                elif(self.x < objectList[i].x + objectList[i].w and self.xVel < 0 and self.lastX >= objectList[i].x + objectList[i].w):
                    self.x = objectList[i].x + objectList[i].w
                    self.xVel = 0
                    if(objectList[i].type == 4):
                        resetLevel = True

        if(self.x > 980):
            level += 1
            resetLevel = True
        elif(self.x < 0):
            self.x = 0

        return (objectList, level, resetLevel)


class Box():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.w = 20
        self.h = 20
        self.type = type
        self.counting = False
        self.count = 8
