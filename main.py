# import sys
# from PyQt5.QtWidgets import (QApplication, QWidget,
#   QPushButton, QVBoxLayout, QHBoxLayout,QVBoxLayout,QMainWindow,QLabel,QTextEdit)
# from PyQt5.QtGui import QPixmap, QPalette
# from PyQt5.QtCore import Qt
import math, pygame, sys, os, copy, random
from time import sleep
import pygame.gfxdraw
from pygame.locals import *
from PIL import Image
import random
## Constants##

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 800
TEXTHEIGHT = 20
BUBBLERADIUS = 20
BUBBLEWIDTH = BUBBLERADIUS * 2
STARTX = WINDOWWIDTH / 2
STARTY = WINDOWHEIGHT - 55

RIGHT = 'right'
LEFT = 'left'
BLANK = '.'

## COLORS ##
#            R    G    B
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)       #|0>
GREEN = (50,205,50)   #|1>
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255,215,0)
BLUE=(0, 0, 255)
BGCOLOR = WHITE
COLORLIST = [RED, GREEN, PURPLE,ORANGE,BLUE]

class Bubble(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = STARTX
        self.rect.centery = STARTY
        self.speed = 3
        self.color = color
        self.radius = BUBBLERADIUS
        self.angle = 0

    def update(self):

        if self.angle == 90:
            xmove = 0
            ymove = self.speed * -1
        elif self.angle < 90:
            xmove = self.xcalculate(self.angle)
            ymove = self.ycalculate(self.angle)
        elif self.angle > 90:
            xmove = self.xcalculate(180 - self.angle) * -1
            ymove = self.ycalculate(180 - self.angle)

        self.rect.x += xmove
        self.rect.y += ymove

    def draw(self):
        pygame.gfxdraw.filled_circle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, GRAY)

    def xcalculate(self, angle):
        radians = math.radians(angle)

        xmove = math.cos(radians) * (self.speed)
        return xmove

    def ycalculate(self, angle):
        radians = math.radians(angle)

        ymove = math.sin(radians) * (self.speed) * -1
        return ymove

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        basewidth = 100
        img = Image.open('Arrow.png')
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save('Arrow_size.png')
        pygame.sprite.Sprite.__init__(self)
        self.angle = 90
        arrowImage = pygame.image.load('Arrow_size.png')
        arrowImage.convert_alpha()
        arrowRect = arrowImage.get_rect()
        self.image = arrowImage
        self.transformImage = self.image
        self.rect = arrowRect
        self.rect.centerx = STARTX
        self.rect.centery = STARTY

    def update(self, direction):

        if direction == LEFT and self.angle < 180:
            self.angle += 2
        elif direction == RIGHT and self.angle > 0:
            self.angle -= 2
        #this is hint to transfowm images
        self.transformImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.transformImage.get_rect()
        self.rect.centerx = STARTX
        self.rect.centery = STARTY

    def draw(self):
        DISPLAYSURF.blit(self.transformImage, self.rect)

class Gate(pygame.sprite.Sprite):
    def __init__(self,x,y):
        basewidth = 500
        img = Image.open('H.png')
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save('H_size.png')
        #height = str(img.get_height())
        #width = str(img.get_width())
        pygame.sprite.Sprite.__init__(self)
        gateImage = pygame.image.load('H_size.png')
        gateImage.convert_alpha()
        gateRect = gateImage.get_rect()
        self.image = gateImage
        self.transformImage = self.image
        self.rect = gateRect
        self.rect.centerx = x
        self.rect.centery = y
        #to move around hadamard gate
    # def update(self):
    #     x=[40,40+WINDOWWIDTH-40]
    #     y=[0,0+WINDOWHEIGHT/2]
    #     self.rect.centerx = x
    #     self.rect.centery = y

    def draw(self):
        DISPLAYSURF.blit(self.transformImage,self.rect)
       #Search how to draw on new coordinates
       # DISPLAYSURF.blit(pygame.Surface.rect.centerx,self.rect.centery)

class Button(pygame.sprite.Sprite):

    def __init__(self, position,color):

        self.rect = pygame.Rect(0, 0, 30, 30)
        (self.rect.centerx,self.rect.centery) = position
        self.radius = BUBBLERADIUS
        self.color=color

    def draw(self):
        # draw selected image
        pygame.gfxdraw.filled_circle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, GRAY)

    def event_handler(self, event):
        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN:  # is some button clicked
            if event.button == 1:  # is left button clicked
                if self.rect.collidepoint(event.pos):  # is mouse over button
                    return self.color
                else:
                    return None
            else:
                return None
        else:
            return None

def main():

    global FPSCLOCK, DISPLAYSURF, DISPLAYRECT, MAINFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Hadamard Gate')
    MAINFONT = pygame.font.SysFont('Helvetica', TEXTHEIGHT)
    #need to add key for the two qbits or need to find a way to add text to the bubble
    DISPLAYSURF, DISPLAYRECT = makeDisplay()
    while True:
        col=endScreen()
        runGame(col)


def runGame(color):
    track = 0
    StartFont = pygame.font.SysFont('Titillium Web', 18)
    Message1 = StartFont.render('=|0> qubit',True, BLACK, BGCOLOR)  #Red
    Message2 = StartFont.render('=|1> qubit',True, BLACK, BGCOLOR)  #Green
    Message3 = StartFont.render('=1/√2 (|0> + |1>)', True, BLACK, BGCOLOR)  #Orange
    Message4 = StartFont.render('=1/√2 (|0> - |1>)', True, BLACK, BGCOLOR)  #Blue

    #DISPLAYSURF.fill(BGCOLOR)

    gameColorList = copy.deepcopy(COLORLIST)
    direction = None
    launchBubble = False
    newBubble = None
    arrow = Arrow()
    gate = Gate(STARTX + 30,WINDOWHEIGHT/2)

    #key bubble1 bottom most
    keyBubble1=Bubble(gameColorList[4])
    keyBubble1.rect.left = 5
    keyBubble1.rect.bottom = WINDOWHEIGHT - 5

    #key bubble2
    keyBubble2=Bubble(gameColorList[3])
    keyBubble2.rect.left = 5
    keyBubble2.rect.bottom = WINDOWHEIGHT - 55

    # key bubble3
    keyBubble3 = Bubble(gameColorList[1])
    keyBubble3.rect.left = 5
    keyBubble3.rect.bottom = WINDOWHEIGHT - 105
    # key bubble4 top most
    keyBubble4 = Bubble(gameColorList[0])
    keyBubble4.rect.left = 5
    keyBubble4.rect.bottom = WINDOWHEIGHT - 155

    # startMessage1Rect = startMessage1.get_rect()
    # startMessage2Rect = startMessage2.get_rect()
    Message4Rect = (50,WINDOWHEIGHT - 30)
    Message3Rect = (50,WINDOWHEIGHT - 80)
    Message2Rect = (50, WINDOWHEIGHT - 130)
    Message1Rect = (50, WINDOWHEIGHT - 180)

    #next bubble starts from center arrow position
    #color purple
    nextBubble = Bubble(color)
    nextBubble.rect.centerx = STARTX
    nextBubble.rect.centery = STARTY

    #score = Score()
    count=0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        DISPLAYSURF.blit(Message1, Message1Rect)
        DISPLAYSURF.blit(Message2, Message2Rect)
        DISPLAYSURF.blit(Message3, Message3Rect)
        DISPLAYSURF.blit(Message4, Message4Rect)
        gx= random.randint(50,WINDOWWIDTH-50)
        gy=random.randint(20, WINDOWHEIGHT/2+20)
        #moves Hadamard Gate around
        gate.draw()
        keyBubble1.draw()
        keyBubble2.draw()
        keyBubble3.draw()
        keyBubble4.draw()
        pygame.display.update()
        #take input
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if (event.key == K_LEFT):
                    direction = LEFT
                elif (event.key == K_RIGHT):
                    direction = RIGHT
                elif(event.key==K_SPACE):
                    launchBubble = True

            elif event.type == KEYUP:
                direction = None
                if event.key == K_ESCAPE:
                    return

            elif event.type == QUIT:
                terminate()

        if launchBubble == True:
            # if newBubble == None:
                # newBubble=Bubble(nextBubble.color)
                # newBubble = nextBubble
                nextBubble.angle = arrow.angle
                #r = random.randint(0, 1)
                nextBubble.color = color
                #change color of qubit after going through gate                                                     #130
                if nextBubble.rect.centery<WINDOWHEIGHT/2:
                    if nextBubble.rect.centerx<gate.rect.centerx+50 and nextBubble.rect.centerx+20>gate.rect.centerx-50:
                        #alternates between the two colors
                        nextBubble.angle=90
                        if color==RED:#count%2==0:
                            nextBubble.color = gameColorList[3]

                        elif color==GREEN:
                            nextBubble.color = gameColorList[4]

                        elif color==ORANGE:
                            nextBubble.color=gameColorList[0]

                        elif color==BLUE:
                            nextBubble.color=gameColorList[1]
                nextBubble.update()


        if nextBubble.rect.right >= WINDOWWIDTH - 5:
            nextBubble.angle = 180 - nextBubble.angle
        elif nextBubble.rect.left <= 5:
            nextBubble.angle = 180 - nextBubble.angle


        if nextBubble.rect.y<=0:
            return
            launchBubble=False
            #gate = Gate(gx,WINDOWHEIGHT/2)
            #count = count + 1

        #setting start position for new launch
        if launchBubble == False:
            #gate.update()
            nextBubble = Bubble(color)
            nextBubble.angle = arrow.angle
            nextBubble.rect.centerx = STARTX
            nextBubble.rect.centery = STARTY

        if launchBubble==True:
            coverNextBubble()

        arrow.update(direction)
        arrow.draw()
        nextBubble.update()
        nextBubble.draw()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeDisplay():
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYRECT = DISPLAYSURF.get_rect()
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.convert()
    pygame.display.update()
    return DISPLAYSURF, DISPLAYRECT


def terminate():
    pygame.quit()
    sys.exit()


def coverNextBubble():
    whiteRect = pygame.Rect(0, 0, BUBBLEWIDTH, BUBBLEWIDTH)
    whiteRect.bottom = WINDOWHEIGHT
    whiteRect.right = WINDOWWIDTH
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, whiteRect)


def endScreen():
    endFont = pygame.font.SysFont('Helvetica', 20)
    endMessage1 = endFont.render('Select a Qubit to Start Hadamard Gate Simulation.',
                                 True, BLACK, BGCOLOR)
    endMessage1Rect = endMessage1.get_rect()
    endMessage1Rect.centerx = DISPLAYRECT.centerx
    endMessage1Rect.centery = 100
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(endMessage1, endMessage1Rect)
    Message1 = endFont.render('|0>', True, BLACK, BGCOLOR)
    Message2 = endFont.render('|1>', True, BLACK, BGCOLOR)
    Message3 = endFont.render('1/√2 (|0> + |1>)', True, BLACK, BGCOLOR)
    Message4 = endFont.render('1/√2 (|0> - |1>)', True, BLACK, BGCOLOR)

    #position of label
    Message1Rect = (WINDOWWIDTH/2, 200 + 45)
    Message2Rect = (WINDOWWIDTH/2, 200 + 90)
    Message3Rect = (WINDOWWIDTH / 2, 200 + 140)
    Message4Rect = (WINDOWWIDTH / 2, 200 + 190)

    DISPLAYSURF.blit(Message1, Message1Rect)
    DISPLAYSURF.blit(Message2, Message2Rect)
    DISPLAYSURF.blit(Message3, Message3Rect)
    DISPLAYSURF.blit(Message4, Message4Rect)

    #button creation    x                   ,      y     color
    button1 = Button((WINDOWWIDTH/2-60      , 200 + 50), RED)
    button2 = Button((WINDOWWIDTH/2-60      , 200 + 100), GREEN)
    button3 = Button((WINDOWWIDTH / 2 - 60  , 200 + 150), ORANGE)
    button4 = Button((WINDOWWIDTH / 2 - 60  , 200 + 200), BLUE)

    button1.draw()
    button2.draw()
    button3.draw()
    button4.draw()

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif (button1.event_handler(event)!=None):
                return button1.event_handler(event)

            elif(button2.event_handler(event)!=None):
                return button2.event_handler(event)

            elif(button3.event_handler(event)!=None):
                return button3.event_handler(event)

            elif (button4.event_handler(event) != None):
                return button4.event_handler(event)

            elif event.type == K_ESCAPE:
                terminate()


if __name__ == '__main__':
    main()