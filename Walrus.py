#-------------------------------------------------------------------------------
# Name: Walrus.py
# Purpose: Walrus Hero II
# Authors: Raymond, Thomas, & Donny
# Created: In progress
# Copyright: (c) Walrus Hero Group 2014
#-------------------------------------------------------------------------------



def drawBorders():
    leftBorder = pygame.Rect(0,0,160,480) #draws the black border rectangle
    rightBorder = pygame.Rect(640,0,160,480)
    pygame.draw.rect(displaysurf,(0,0,0), leftBorder) #draws the black borders
    pygame.draw.rect(displaysurf,(0,0,0), rightBorder)
    displaysurf.blit(pauseImage,[160,0]) #draws the pause button
    message = "Score:" + str(score)
    label = scoreFont.render(message, 1, (0,0,0)) #displays the score, and high score
    messageX = 640 - (len(message)*10)
    displaysurf.blit(label, (messageX, 10))
    message2 = "Highscore:" + str(highscore)
    label2 = scoreFont.render(message2, 1, (0,0,0))
    message2X = 650 - (len(message2)*10)
    displaysurf.blit(label2, (message2X, 30))

def sound():
    #Initializes music
    try:#loads the android mixer for pygame
        import pygame.mixer as mixer
    except ImportError:
        import android.mixer as mixer
    global presskey
    mixer.init(44100, -16, 2, 4096)
    music = mixer.Sound('song.ogg')
    music.play(-1,0,0)
    #sets the music to play, and mute key is not pressed
    play = True
    pressedkey = False
    mutebox = pygame.Rect(640,400,50,50) #creates a box where the thing is mutable
    while True:
        if paused == True:
            pygame.event.get()
            if mutebox.collidepoint(pygame.mouse.get_pos()) == True:
                if pygame.mouse.get_pressed()[0] == True or androidChecker == True:
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

def savehighscore(): #writes the high score
    with open('highscore.txt', 'w') as file:
        file.write(str(max(score,highscore)))

def quit(): #quits the game
    savehighscore()
    pygame.quit()
    sys.exit()

try: #check if the game is on android
    import android
    androidChecker = True
except ImportError:
    android = None
    androidChecker = False

#Importing libraries
import pygame, sys, os.path, threading, math, time, random
from pygame.locals import *

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
pauseMenu = pygame.image.load('pause.fw.png')
pauseImage = pygame.image.load('pauseButton.png')
background = pygame.image.load('backrond.gif')



class platform(): #a self contained classes for the platform



    def move(self,shift): #move the platform
        for counter in range(0,self.boxnum):
            self.platformrect[counter] = self.platformrect[counter].move(shift,0)
        self.origin += shift
        if self.origin<= 0: #checks if the platform is too far to the right
            for counter in range(0,self.boxnum):
                self.platformrect[counter] = self.platformrect[counter].move(6400,0) #moves it to the left
            self.origin += 6400
##            self.load(self.filename,self.picturename, self.framenum, random.randint(1,3),3)

    def view(self): #view the platform,
        for counter in range(0,self.boxnum):
                displaysurf.blit(self.platformimage[0], [self.platformrect[counter].left, self.platformrect[counter].top]) #loads the corner of the platform
                displaysurf.blit(self.platformimage[2], [self.platformrect[counter].right-20, self.platformrect[counter].top])
                displaysurf.blit(self.platformimage[6], [self.platformrect[counter].left, self.platformrect[counter].bottom-10])
                displaysurf.blit(self.platformimage[8], [self.platformrect[counter].right-20, self.platformrect[counter].bottom-10])
                for rowCounter in range(1, int(self.platformrect[counter].height/10)+1):
                    if rowCounter == 1: #draws the borders
                        for columnCounter in range(2, int(self.platformrect[counter].width/10)-2):
                            displaysurf.blit(self.platformimage[1], [self.platformrect[counter].left+(columnCounter*10), self.platformrect[counter].top])
                    elif rowCounter == int(self.platformrect[counter].height/10):
                        for columnCounter in range(2, int(self.platformrect[counter].width/10)-2): #draws the side
                            displaysurf.blit(self.platformimage[7], [self.platformrect[counter].left+(columnCounter*10), self.platformrect[counter].bottom-10])
                    else:
                        for columnCounter in range(0, int(self.platformrect[counter].width/10)): #draws the middle
                            if columnCounter == 0:
                                displaysurf.blit(self.platformimage[3], [self.platformrect[counter].left, self.platformrect[counter].bottom-(rowCounter*10)])
                            elif columnCounter == int(self.platformrect[counter].width/10)-1:
                                displaysurf.blit(self.platformimage[5], [self.platformrect[counter].left+(columnCounter*10), self.platformrect[counter].bottom-(rowCounter*10)])
                            else:
                                displaysurf.blit(self.platformimage[4], [self.platformrect[counter].left+(columnCounter*10), self.platformrect[counter].bottom-(rowCounter*10)])

    def _colliderectnum_(self,pizza): #outputs the number box the walrus collides with, pizza is the walrus
        for counter in range (0,self.boxnum):
            if self.platformrect[counter].colliderect(pizza.move(0,(pizza.height+self.platformrect[counter].height - 10)))== True and self.platformrect[counter].colliderect(pizza.move(0,3))== True:
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
        if os.path.isfile(filename+ '_'+str(levelnum)+ ".txt") == True: #opens the files
            with open(filename+ '_'+str(levelnum)+ ".txt", 'r') as file:
                self.boxnum = int(file.readline()) #checks the number of platform to draw
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
        self.origin = 1200*(levelnum)+250 #counts down the boxes before moving the platform to the right
        self.move(1600*(levelnum-1)+160)
##        self.filename = filename
##        self.picturename = picturename
##        self.framenum = framenum


class spikeplatform(platform): #changes to adapt to
    def _colliderectnum_(self,pizza): #outputs the number box the walrus collides with, pizza is the walrus
        for counter in range (0,self.boxnum):
            if self.platformrect[counter].colliderect(pizza)== True:
                return counter
        return -1 #returns a null number (the official null number is -1)

    def view(self): #view the platform
            for counter in range(0,self.boxnum):
                displaysurf.blit(self.platformimage[score%self.framenum],[self.platformrect[counter].left,self.platformrect[counter].top])


#Initializes change in motion, walrus, background, and borders
walrus  = pygame.Rect(255,270,50,50) #Changed the rectangle size
pausebox = pygame.Rect(160,0,50,50) #pause button
score = 0
scoreFont = pygame.font.SysFont("helvetica", 20)
walrusFrame = 0
jump = False
highscore = readhighscore() #reads the high score
ground = False
count = 0
safebox, hitbox = [],[]
for counter in range (0,4):
    safebox.append(platform())
    safebox[counter].load('level','platformPart',9,counter+1) #loads the safe box
    hitbox.append(spikeplatform())
    hitbox[counter].load('hitbox','spike',1,counter+1) #loads the hitboxes



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
        elif (event.type == MOUSEBUTTONDOWN or androidChecker == True) and pausebox.collidepoint(pygame.mouse.get_pos()) == True: #checks if the pause button has been clicked
            displaysurf.blit(pauseMenu,[0,0])
            pygame.display.update()
            paused = not paused
    if pygame.mouse.get_pressed()[0] == True or androidChecker == True : #checks if the walrus needs to jump
        if pausebox.collidepoint(pygame.mouse.get_pos()) != True and ground == True:
            jump = True
            ground = False
            count = 0
    else:
        jump = False
        count = 0

    if paused == True:
        continue

    if score%4 == 0:
        walrusFrame += 1
        speed = int(-math.log(score+100)) #adjusts the speed of the platform
    if walrusFrame == 14:
        walrusFrame = 0

    score += 1
    for counter in range (0,4):
        safebox[counter].move(speed)
        hitbox[counter].move(speed)
    displaysurf.blit(background,[160,0])
    displaysurf.blit(walrusImage[walrusFrame],[walrus.left,walrus.top])
    for counter in range (0,4):
        safebox[counter].view()
        hitbox[counter].view()


    #Detects hits
    for counter in range (0,3):
        if hitbox[counter].collidecheck(walrus) == True: #see if the walrus collides with the hitbox
            highscore = max([highscore,score])
            score = 0

    if walrus.top >= 480: #if the warlus falls off the top of the map, it resets the walrus
        highscore = max([highscore,score])
        score = 0
        walrus = walrus.move(0,100-walrus.bottom)


    drawBorders() #Draws borders

    pygame.display.update() #Draws everything
    time.sleep(0.008) #Pause to ensure the game isn't going to fast

    if jump == False:
        ground = False

    if jump == False:
        for counter in range(0,4):
            if safebox[counter].collidecheck(walrus) == True:
                walrus = walrus.move(*safebox[counter].walrusadjust(walrus))
                ground = True

    if ground == False and jump == False:
        falling()

    if jump == True:
        jumping()

