import pygame
from random import randint
import math
import Entity

class Game():
    def __init__(self, sW, sH, player):
        self.sW = sW
        self.sH = sH
        self.player = player
        self.stop = False
        self.objectList = []
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((sW, sH))

        #pygame.mixer.music.load('music/jump.mp3')
        #pygame.mixer.music.play(-1)

        self.level = 1

    def getInput(self):
        shift = False
        keys = pygame.key.get_pressed()
        self.player.xVel = 0
        if keys[pygame.K_LSHIFT]:
            shift = True
        if keys[pygame.K_a]:
            if shift:
                self.player.xVel = -self.player.moveSpeed * 2
            else:
                self.player.xVel = -self.player.moveSpeed
        if keys[pygame.K_d]:
            if shift:
                self.player.xVel = self.player.moveSpeed * 2
            else:
                self.player.xVel = self.player.moveSpeed
        if keys[pygame.K_r]:
            self.resetLevel()
        if keys[pygame.K_m]:
            pygame.mixer.music.pause()
        if keys[pygame.K_SPACE] and self.player.grounded:
            self.jumpSound.play()
            self.player.yVel = self.player.jumpSpeed
            self.player.grounded = False
            self.player.onGreen = False

    def render(self):
        self.screen.fill(self.BLACK)
        for i in range(0, len(self.objectList)):
            if(self.objectList[i].type == 1):
                pygame.draw.rect(self.screen, self.RED, (self.objectList[i].x, self.objectList[i].y, self.objectList[i].w, self.objectList[i].h))
            elif(self.objectList[i].type == 2):
                pygame.draw.rect(self.screen, self.GREEN, (self.objectList[i].x, self.objectList[i].y, self.objectList[i].w, self.objectList[i].h))
            elif(self.objectList[i].type == 3):
                pygame.draw.rect(self.screen, self.ORANGE, (self.objectList[i].x, self.objectList[i].y, self.objectList[i].w, self.objectList[i].h))
            elif(self.objectList[i].type == 4):
                pygame.draw.rect(self.screen, self.PURPLE, (self.objectList[i].x, self.objectList[i].y, self.objectList[i].w, self.objectList[i].h))
            elif(self.objectList[i].type == 5):
                pygame.draw.rect(self.screen, self.GREEN, (self.objectList[i].x, self.objectList[i].y, self.objectList[i].w / 2, self.objectList[i].h))
                pygame.draw.rect(self.screen, self.ORANGE, (self.objectList[i].x + self.objectList[i].w / 2, self.objectList[i].y, self.objectList[i].w / 2, self.objectList[i].h))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurface = smallText.render(str(self.level), True, self.WHITE)
        TextRect = textSurface.get_rect()
        TextSurf = textSurface
        TextRect.center = (10, 15)
        self.screen.blit(TextSurf, TextRect)


        pygame.draw.rect(self.screen, self.WHITE, (self.player.x, self.player.y, self.player.w, self.player.h))
        pygame.display.flip()

    def update(self):
        self.objectList, self.level, resetLevel = self.player.update(self.objectList, self.level)
        if resetLevel:
            self.resetLevel()

    def resetLevel(self):
        if(self.level == 1):
            self.player.x = 20
        else:
            self.player.x = 0
        self.player.y = 460
        self.objectList = []
        file = open('pages/screen' + str(self.level) + '.txt', 'r')
        fileText = file.readlines()
        for i in range(0, len(fileText)):
            for j in range(0, len(fileText[i])):
                if fileText[i][j] == '.':
                    pass
                elif fileText[i][j] == '1':
                    self.objectList.append(Entity.Box(j * 20, i * 20, 1))
                elif fileText[i][j] == '2':
                    self.objectList.append(Entity.Box(j * 20, i * 20, 2))
                elif fileText[i][j] == '3':
                    self.objectList.append(Entity.Box(j * 20, i * 20, 3))
                elif fileText[i][j] == '4':
                    self.objectList.append(Entity.Box(j * 20, i * 20, 4))
                elif fileText[i][j] == '5':
                    self.objectList.append(Entity.Box(j * 20, i * 20, 5))


    def game_intro(self):
        levelMenu = False
        intro = True
        greenButtXYWH = (self.sW / 3 - 50, 300, 100, 50)
        redButtXYWH = ((self.sW / 3) * 2 - 50, 300, 100, 50)

        while intro:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(self.WHITE)
            largeText = pygame.font.Font('freesansbold.ttf',115)
            textSurface = largeText.render('Kill Me', True, self.BLACK)
            TextRect = textSurface.get_rect()
            TextSurf = textSurface
            TextRect.center = ((self.sW/2),(self.sH/4))
            self.screen.blit(TextSurf, TextRect)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            pygame.draw.rect(self.screen, self.GREEN,greenButtXYWH)
            pygame.draw.rect(self.screen, self.RED,redButtXYWH)

            if(greenButtXYWH[0] <= mouse[0] <= greenButtXYWH[0] + greenButtXYWH[2] and greenButtXYWH[1] <= mouse[1] <= greenButtXYWH[1] + greenButtXYWH[3]):
                pygame.draw.rect(self.screen, self.YELLOW,greenButtXYWH)
                if(click[0] == 1):
                    #print("Start")
                    intro = False
            elif(redButtXYWH[0] <= mouse[0] <= redButtXYWH[0] + redButtXYWH[2] and redButtXYWH[1] <= mouse[1] <= redButtXYWH[1] + redButtXYWH[3]):
                pygame.draw.rect(self.screen, self.PURPLE,redButtXYWH)
                if(click[0] == 1):
                    levelMenu = True

            smallText = pygame.font.Font("freesansbold.ttf",20)
            textSurface = smallText.render('Start', True, self.BLACK)
            TextRect = textSurface.get_rect()
            TextSurf = textSurface
            TextRect.center = (greenButtXYWH[0] + (greenButtXYWH[2] / 2), greenButtXYWH[1] + (greenButtXYWH[3] / 2))
            self.screen.blit(TextSurf, TextRect)

            textSurface = smallText.render('Levels', True, self.BLACK)
            TextRect = textSurface.get_rect()
            TextSurf = textSurface
            TextRect.center = (redButtXYWH[0] + (redButtXYWH[2] / 2), redButtXYWH[1] + (redButtXYWH[3] / 2))
            self.screen.blit(TextSurf, TextRect)

            if(levelMenu):
                pass

            pygame.display.update()
            self.clock.tick(15)



    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (160, 32, 240)
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption('Bouncy Boi')

    jumpSound = pygame.mixer.Sound('music/jump.wav')
    jumpSound.set_volume(.01)
    #pygame.mixer.Sound('music/jump.wav').set_volume(.2)

import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

game = Game(1000, 500, Entity.Player(20, 480, 20, 20))
game.resetLevel()

game.game_intro()
while not game.stop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop = True

    game.getInput()
    game.update()
    game.render()

    game.clock.tick(30)

pygame.quit()
