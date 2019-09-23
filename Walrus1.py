#-------------------------------------------------------------------------------
# Name: Walrus.py
# Purpose: Walrus Hero II
# Authors: Raymond, Thomas, & Donny
# Created: In progress
# Copyright: (c) Walrus Hero Group 2014
#-------------------------------------------------------------------------------


#Draws background
def drawBackground(x,y):
    background = pygame.Rect(160,0,480,480)
    displaysurf.blit(background,[160,0])
    displaysurf.blit(backgroundGroundImage[0],[x,320])
    displaysurf.blit(backgroundGroundImage[1],[y,320])


def drawBorders():
    global score, highscore
    leftBorder = pygame.Rect(0,0,160,480)
    rightBorder = pygame.Rect(640,0,160,480)
    pygame.draw.rect(displaysurf,black, leftBorder)
    pygame.draw.rect(displaysurf,black, rightBorder)
    displaysurf.blit(pauseImage,[160,0])
    message = "Score:" + str(score)
    label = scoreFont.render(message, 1, (0,0,0))
    messageX = 640 - (len(message)*10)
    displaysurf.blit(label, (messageX, 10))
    message2 = "Highscore:" + str(highscore)
    label2 = scoreFont.render(message2, 1, (0,0,0))
    message2X = 650 - (len(message2)*10)
    displaysurf.blit(label2, (message2X, 30))

def sound():
    #Initializes music
    global presskey
    pygame.mixer.init(44100, -16, 2, 4096)
    music = pygame.mixer.Sound('song.ogg')
    music.play(-1,0,0)
    #sets the music to play, and mute key is not pressed
    play = True
    pressedkey = False
    mutebox = pygame.Rect(640,400,50,50)
    while True:
        if paused == True:
            pygame.event.get()
            if mutebox.collidepoint(pygame.mouse.get_pos()) == True and pygame.mouse.get_pressed()[0] == True:
                if pressedkey == False: #checks if the space key is already pressed
                    if play == True:
                        pygame.mixer.pause() #stops the music
                        play = False
                    else:
                        pygame.mixer.unpause()
                        play = True
                pressedkey = True #to make sure that the switch
            else:
                pressedkey = False #make the player free to mute it again
        time.sleep(0.05)

def readhighscore():
    #opens (or creates if necessary) the highscore file and puts out the high score
    if os.path.isfile('highscore.txt') == True:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    else:
        with open('highscore.txt', 'w') as file:
            return 0

def savehighscore():
    with open('highscore.txt', 'w') as file:
        file.write(str(max(score,highscore)))

def quit():
    savehighscore()
    pygame.quit()
    sys.exit()

try:
    import android
    androidChecker = True
except ImportError:
    android = None
    androidChecker = False

#Importing libraries
import pygame, sys, time, os.path, threading, math
from colourtable import *
from pygame.locals import *
from operator import add


#Initializes pygame
pygame.init()

#Initializes screen
displaysurf = pygame.display.set_mode((800,480))
pygame.display.set_caption('Walrus Hero II')
displaysurf.blit(pygame.image.load('walrus.jpg'),[0,0])
pygame.display.update()
time.sleep(1)

#makes a thread that plays music independantly
paused = False
threading.Thread(target=sound).start()

#Loads Images
walrusImage = []
for x in range(1,15):
    picture = "Walrus_jump_" + str(x) + ".png"
    walrusImage.append(pygame.image.load(picture))
backgroundGroundImage = []
for x in range(1,3):
    picture = "backgroundGround_" + str(x) + ".png"
    backgroundGroundImage.append(pygame.image.load(picture))
pauseMenu = pygame.image.load('pause.fw.png')
pauseImage = pygame.image.load('pauseButton.png')
background = pygame.image.load('backrond.png')



class platform(): #a self condained



    def move(self,shift): #move the platform
        for counter in range(0,self.boxnum):
            self.platformrect[counter] = self.platformrect[counter].move(shift,0)
        self.origin += shift
        if self.origin<=160:
            for counter in range(0,self.boxnum):
                self.platformrect[counter] = self.platformrect[counter].move((1600*2),0)
            self.origin += (1600*2)

    def view(self): #view the platform
        for counter in range(0,self.boxnum):
            displaysurf.blit(self.platformimage[score%self.framenum],[self.platformrect[counter].left,self.platformrect[counter].top])

    def _colliderectnum_(self,pizza): #outputs the number box the walrus collides with, pizza is the walrus
        for counter in range (0,self.boxnum):
            if self.platformrect[counter].colliderect(pizza.move(0,2))== True:
                return counter
        return -1 #returns a null number

    def collidecheck(self, pizza): #checks if the walrus had collided with the platform
        if self._colliderectnum_(pizza) == -1:
            return False
        else:
            return True

    def walrusadjust(self, pizza): #adjusts the walrus if it hits a platform
        return [0,self.platformrect[self._colliderectnum_(pizza)].top - walrus.bottom]

    def load(self,filename,picturename,framenum, levelnum):#This uses the .png file, do not use with jpg, bmp, etc.
                                            #Leave out the file extension when using it
        self.platformimage, self.platformrect = [],[]
        if os.path.isfile(filename+ '_'+str(levelnum)+ ".txt") == True:
            with open(filename+ '_'+str(levelnum)+ ".txt", 'r') as file:
                self.boxnum = int(file.readline())
                file.readline()
                for boxcounter in range(0,self.boxnum):
                    templist = []
                    for boxparametercounter in range(0,4):
                        templist.append(int(file.readline()))
                    file.readline()
                    self.platformrect.append(pygame.Rect(*templist))
            for counter in range (1,framenum+1):
                self.platformimage.append(pygame.image.load(picturename+'_'+str(counter)+'.png'))
        self.framenum = framenum
        self.origin = 1600*(levelnum) #counts down the boxes before resetting
        self.move(1600*(levelnum-1))

class background(platform):

    moveback = 960

    def move(self,speed):
        if self.location.left <= -320: #makes the background move back to the right part of the screen to keep going left
            self.location = self.location(moveback,0)
        else:
            self.location = self.location(moveback,speed)

#Initializes change in motion, walrus, background, and borders
change = [0,0]
walrus  = pygame.Rect(255,270,50,50) #Changed the rectangle size
pausebox = pygame.Rect(160,0,50,50) #pause button
score = 0
scoreFont = pygame.font.SysFont("helvetica", 20)
walrusFrame = 0
ground1 = 160
ground2 = 640
jump = False
highscore = readhighscore() #reads the high score
ground = False
count = 0
speed = 0
safebox, hitbox = [],[]
for counter in range (0,2):
    safebox.append(platform())
    safebox[counter].load('level','platform',1,counter+1) #loads the safe box
    hitbox.append(platform())
    hitbox[counter].load('hitbox','spikey',1,counter+1) #loads the hitboxes



def jumping():
    global walrus, count, jump
    walrus = walrus.move(0,-12)
    count += 1
    if count >= 13: #tells the walrus to stop rising
        jump = False
        count = 0

def falling(): #makes the walrus fall
    global walrus
    walrus = walrus.move(0,8)



while True: #Main loop

    for event in pygame.event.get():
        if event.type == QUIT: #quits the program
            quit()
        elif event.type == KEYDOWN: #this part pauses the game
            if event.key == K_p:
                displaysurf.blit(pauseMenu,[0,0])
                paused = not paused
        elif event.type == MOUSEBUTTONDOWN: #checks if the pause button
            if pausebox.collidepoint(pygame.mouse.get_pos()) == True:
                displaysurf.blit(pauseMenu,[0,0])
                pygame.display.update()
                paused = not paused
            elif ground == True:
                jump = True
                count = 0
        else:
            jump = False
            count = 0

    if paused == True:
        continue

    if score%4 == 0:
        walrusFrame += 1
        speed = int(-math.log(score+2)) #adjusts the speed of the platform
    if walrusFrame == 14:
        walrusFrame = 0

    score += 1
    for counter in range (0,2):
        safebox[counter].move(speed)
        hitbox[counter].move(speed)
    change [0] = 0 #Resets change in motion
    ground1, ground2 = ground1 + speed, ground2 + speed
    if ground1 <= -320:
        ground1 += 960
    if ground2 <= -320:
        ground2 += 960
    drawBackground(ground1,ground2)
    displaysurf.blit(walrusImage[walrusFrame],[walrus.left,walrus.top])
    for counter in range (0,2):
        safebox[counter].view()
        hitbox[counter].view()


    #Detects hits
    for counter in range (0,2):
        if hitbox[counter].collidecheck(walrus) == True: #see if the walrus collides with the hitbox
            highscore = max([highscore,score])
            score = 0

    drawBorders() #Draws borders

    pygame.display.update() #Draws everything
    time.sleep(0.005) #Pause to ensure the game isn't going to fast

    if jump == False:
        ground = False

    if walrus.bottom >= 320:
        ground = True

    for counter in range(0,2):
        if safebox[counter].collidecheck(walrus) == True:
            walrus = walrus.move(*safebox[counter].walrusadjust(walrus))
            ground = True

    if ground == False and jump == False:
        falling()

    if jump == True:
        jumping()

