# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, sys, avatar, socket, HighScoreReader, quoteReader, random, copy
from beams import Beam
from wall import Wall
from label import MenuLabel
from grass import Grass
from window import Window
import mainfuncs as m
from powerups import Powerup
from loadObstacles import *
from loadMenuLabels import *


###Reading in settings###
fp = file('Settings.txt') #reads the file
lines = fp.readlines() #reads lines and creates an array of lines
fp.close() #closes the file
settings = [] #list of scores that is returned
for line in lines: 
	words = line.split()
	settings.append( int(words[0]) )
	
'''
Settings File: 0: off, 1: on
Line 0: Low Resolution Mode
Line 1: Background Music
Line 2: Sound Effects Toggle
Line 3: Colorblind Mode
'''
	
fp = file('Store.txt') #reads the file
lines = fp.readlines() #reads lines and creates an array of lines
fp.close() #closes the file
itemsBought = [] #list of scores that is returned
for line in lines: 
	words = line.split()
	itemsBought.append( int(words[0]) )
	
	


### Initializing all needed Pygame stuff ###
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()
infoObject = pygame.display.Info()

if settings[0] == 0:
	lowRes = False
	screenWidth = infoObject.current_w
	screenHeight = infoObject.current_h
else:
	lowRes = True
	screenWidth = 1024
	screenHeight = 768

displayFlags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE #using hardware acceleration
screen = pygame.display.set_mode((screenWidth, screenHeight), displayFlags) #Screen size fits all screens

clock = pygame.time.Clock()

### Displays main background while the rest loads ###
mainBackground = pygame.transform.scale(pygame.image.load( "Assets/img/StartScreenFinal.png" ).convert(),(screenWidth,screenHeight))
fan = pygame.transform.scale(pygame.image.load( "Assets/img/Fan.png" ).convert_alpha(),(screenHeight*2/11,screenHeight*2/11))
storebackground = pygame.transform.scale(pygame.image.load( "Assets/img/Store.png" ).convert(),(screenWidth,screenHeight))
introWidth = screenWidth*4
introHeight = screenHeight*4
introXPos = screenWidth*7/12*4
introYPos = screenHeight/6*3
intro = pygame.transform.scale(pygame.image.load( "Assets/img/startimage.png" ).convert(),(introWidth,introHeight))
screen.fill((0,0,0))#Loading
pygame.display.update()

preLoaded1 = loadObstacles(screenWidth, screenHeight, 1) 
preLoaded1.start()
preLoaded2 = loadObstacles(screenWidth, screenHeight, 2) 
preLoaded2.start()
preLoaded3 = loadObstacles(screenWidth, screenHeight, 3) 
preLoaded3.start()
preLoaded4 = loadObstacles(screenWidth, screenHeight, 4)
preLoaded4.start()


### Game Sound ###
hoverSound = pygame.mixer.Sound( "Assets/sound/click.wav" )
clickSound = pygame.mixer.Sound( "Assets/sound/pop.wav" )
pointSound = pygame.mixer.Sound( "Assets/sound/blip.wav" )
rainbowSound = pygame.mixer.Sound( "Assets/sound/rainbowsound.ogg" )
errorSound = pygame.mixer.Sound( "Assets/sound/beep.wav" )
fanSound = pygame.mixer.Sound( "Assets/sound/fan.ogg" )
kachingSound = pygame.mixer.Sound( "Assets/sound/KACHING.wav" )
antiGravity = pygame.mixer.Sound( "Assets/sound/antigravitysong.ogg" )
pygame.mixer.music.load("Assets/sound/soundtrack2.ogg")

pygame.mixer.music.play(-1)
if settings[1] == 1:
	musicToggle = True
else:
	pygame.mixer.music.pause()
	musicToggle = False
if settings[2] == 1:
	soundToggle = True
else:
	soundToggle = False

### Gamestate variables ###
gameState = 9
'''
	0 = menu loop
	1 = go to game
	2 = Instructions
	3 = Credits
	4 = Quit Game
	5 = Loss Screen
	6 = Options screen
'''

''' Flier States:

	0 = default
	1 = rainbow
	2 = reverse gravity
'''
			
### Menu Items/Labels ###
# varName = MenuLable("Text", "Font-Style", BkgColor of Box, Text Color, fontSize, Position, gamestate it points to)

#Main Menu
title = MenuLabel("Fly Baby, Fly",(255,105,180),screenWidth/32,(screenWidth*9/16,screenHeight/10),100)
start = MenuLabel("Start Game",(255,153,0),screenWidth/53,(screenWidth*9/16,screenHeight/14*3),1)
instruction = MenuLabel("Instructions",(255,153,0),screenWidth/53,(screenWidth*9/16,screenHeight/14*4),2)
options = MenuLabel("Options",(255,153,0),screenWidth/53,(screenWidth*9/16,screenHeight/14*5),6)
mainQuit = MenuLabel("Quit",(255,153,0),screenWidth/53,(screenWidth*9/16,screenHeight/14*6),4)
mainMenu = [start, mainQuit, instruction, options] #Main Menu Labels

#Credits
Producer = loadMenuLabels("He's a People Person (Producer): Chris Marcello",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11), 100)
Designer = loadMenuLabels("Man with Vision (Designer): James Lindberg", (0,0,0), screenWidth/53, (screenWidth/2, screenHeight*2/11), 100)
Programmer = loadMenuLabels("Hackerman (Lead Programmer): Lucas DeGraw",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*3), 100)
Artist = loadMenuLabels("Frida Kahlo + GIMP (Lead Artist): Riley Karp",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*4), 100)
Sound = loadMenuLabels("Mariachi (Lead Sound Design): Jerry Diaz ", (0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*5), 100)
Gamer = loadMenuLabels("Gamer (Quality Assurance): Austin Nantkes",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*6), 100)
Knife = loadMenuLabels("Swiss Army Knife (Multirole): Jonathan Stempel",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*7), 100)
DJ = loadMenuLabels("DJ (Art Assistance): Dean Weiner",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*8), 100)
MusicGuy = loadMenuLabels("Most soundtracks from here: http://www.bensound.com/royalty-free-music",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/11*10), 100)
Bruce = loadMenuLabels("Special Thanks to: Bruce (Totally Not CIA) Maxwell",(0,0,0),screenWidth/53,(screenWidth/2, screenHeight/11*9),100)

lossBack = loadMenuLabels("Back",(0,0,0), screenWidth/57,(screenWidth*8/9,screenHeight/15),5)
creditsMenu = [Producer, Designer, Programmer, Artist, Sound, Gamer, Knife, DJ, Bruce, MusicGuy, lossBack]

for label in creditsMenu :
	label.start()
	
#Colorblind Mode Labels
planeLabel = MenuLabel("Color: White",(0,0,0), screenWidth/70, (screenWidth/9,screenHeight*2/9), 100)

imageScale = (screenHeight/10, screenHeight/15)

redLabelImage = pygame.transform.scale(pygame.image.load( "Assets/img/RedLabel.png" ).convert_alpha(), imageScale)
blueLabelImage = pygame.transform.scale(pygame.image.load( "Assets/img/BlueLabel.png" ).convert_alpha(), imageScale)
greenLabelImage = pygame.transform.scale(pygame.image.load( "Assets/img/GreenLabel.png" ).convert_alpha(), imageScale)
purpleLabelImage = pygame.transform.scale(pygame.image.load( "Assets/img/PurpleLabel.png" ).convert_alpha(), imageScale)
yellowLabelImage = pygame.transform.scale(pygame.image.load( "Assets/img/YellowLabel.png" ).convert_alpha(), imageScale)
cyanLabelImage = pygame.transform.scale(pygame.image.load( "Assets/img/CyanLabel.png" ).convert_alpha(), imageScale)
orangeLabelImage =  pygame.transform.scale(pygame.image.load( "Assets/img/OrangeLabel.png" ).convert_alpha(), imageScale)

cbImageLabels = [redLabelImage, blueLabelImage, greenLabelImage, purpleLabelImage, yellowLabelImage, cyanLabelImage, orangeLabelImage]



#Instructions (Original screenWidth/57)
paint = MenuLabel("Paint streams will change your plane's color!",(255,105,180),screenWidth/57,(screenWidth*2/7,screenHeight*1/14),100)
help = MenuLabel("Go through the color block that matches your plane!",(255,105,180),screenWidth/57,(screenWidth*2/7,screenHeight*3/14),100)
help2 = MenuLabel("Don't fly above or below the paint beams!",(255,105,180),screenWidth/57,(screenWidth*2/7,screenHeight*5/14),100)
controls = MenuLabel("Press Spacebar, 'w' or the up arrow to increase your upward speed!",(255,105,180),screenWidth/57,(screenWidth*9/28,screenHeight*7/14),100)
controls2 = MenuLabel("Press spacebar to restart the game!", (255,105,180),screenWidth/57,(screenWidth*2/7,screenHeight*9/14),100)
controls3 = MenuLabel("Press 'p' to pause and unpause the game!", (255,105,180),screenWidth/57,(screenWidth*2/7,screenHeight*11/14),100)
powerUps = MenuLabel("Use Powerups to increase your chances!",(255,105,180),screenWidth/57,(screenWidth*2/7,screenHeight*13/14),100)
gravityLabel = MenuLabel("Swaps gravity",(255,105,180),screenWidth/57,(screenWidth*6/7,screenHeight*10/14),100)
rainbowLabel = MenuLabel("Go through any barrier",(255,105,180),screenWidth/57,(screenWidth*6/7,screenHeight*6/14),100)
mainBack = MenuLabel("Back", (0,0,0),screenWidth/57,(screenWidth*6/7,screenHeight/15),0)
instructions = [help, help2, controls, controls2, controls3, powerUps, gravityLabel, rainbowLabel, mainBack, paint]



#Options Menu
lowResolution = MenuLabel("Slow Game Mode",(191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*5/8),41)
resInfo = MenuLabel("Turn on Slow Game Mode and restart game if it runs poorly",(191, 255, 0),screenWidth/68,(screenWidth/2,screenHeight*6/8),100)
musicToggled = MenuLabel("Background Music On/Off", (191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*2/8),42)
soundToggled = MenuLabel("Sound Effects On/Off",(191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*3/8), 43)
colorBlindLabel = MenuLabel("Colorblind Mode On/Off",(191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*4/8), 48)
optionsList = [mainBack, musicToggled, soundToggled,lowResolution, colorBlindLabel]

#Loss Screen
credits = loadMenuLabels("Credits",(0,0,0),screenWidth/53,(screenWidth/5,screenHeight*5/10),3)
restart = loadMenuLabels("Retry!",(0,0,0),screenWidth/53,(screenWidth/5,screenHeight*2/10),1)
main = loadMenuLabels("Main Menu",(0,0,0),screenWidth/53,(screenWidth/5,screenHeight*3/10),0)
supply = loadMenuLabels("Supply Stash",(0,0,0),screenWidth/53,(screenWidth/5,screenHeight*4/10),8)
lossQuit = loadMenuLabels("Quit",(0,0,0),screenWidth/53,(screenWidth/5,screenHeight*6/10),4)
lossMenu = [restart, credits, lossQuit,supply, main]

for label in lossMenu :
	label.start()

#Store state 8
storeTitle = MenuLabel("Squirrel Supply Stash",(0, 0, 0),screenWidth/40,(screenWidth/2,screenHeight/9),100)
planeSkins = MenuLabel("Plane Types",(0, 0, 0),screenWidth/40,(screenWidth/3,screenHeight*2/9),100)
paperBomber = MenuLabel("Paper Bomber",(0, 0, 0),screenWidth/57,(screenWidth/3,screenHeight*3/9),81)
paperFlyboy = MenuLabel("Paper Flyboy",(0, 0, 0),screenWidth/57,(screenWidth/3,screenHeight*4/9),82)
biBomber = MenuLabel("Biplane Bomber",(0, 0, 0),screenWidth/57,(screenWidth/3,screenHeight*5/9),83)
biFlyboy = MenuLabel("Biplane Flyboy",(0, 0, 0),screenWidth/57,(screenWidth/3,screenHeight*6/9),84)
bubble = MenuLabel("Bubble Bomber",(0, 0, 0),screenWidth/57,(screenWidth/3,screenHeight*7/9),85)
bubbleBoy = MenuLabel("Bubble Flyboy",(0, 0, 0),screenWidth/57,(screenWidth/3,screenHeight*8/9),80)

#Plane images for each plane in the store
paper_bomber = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhitePlane.png" ).convert_alpha(), (screenHeight/9, screenHeight/9))
paper_flyboy = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesWhitePlane.png" ).convert_alpha(), (screenHeight/9, screenHeight/9))
biplane_bomber = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhiteBP.png" ).convert_alpha(), (screenHeight/9, screenHeight/9))
biplane_flyboy = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesWhiteBP.png" ).convert_alpha(), (screenHeight/9, screenHeight/9))
bubble_bomber = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhiteBubble.png" ).convert_alpha(), (screenHeight/9, screenHeight/9))
bubble_flyboy = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesWhiteBubble.png" ).convert_alpha(), (screenHeight/9, screenHeight/9))

#-----------------------------------------------------------------------------------------

lossBack = MenuLabel("Back",(0,0,0), screenWidth/57,(screenWidth*8/9,screenHeight/15),5)
totalLabel = MenuLabel("Total Score: "+str(itemsBought[-1]),(0,0,0), screenWidth/52,(screenWidth*2/3,screenHeight*2/9),100)
storeTitles = [paperBomber, paperFlyboy, biBomber, biFlyboy ,bubble, bubbleBoy, lossBack]

#Cost boxes in store
cost = MenuLabel("Cost",(0, 0, 0),screenWidth/40,(screenWidth/2,screenHeight*2/9),100)
cost25 = MenuLabel(" 50 ",(0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*4/9),100)
cost50 = MenuLabel(" 100 ",(0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*5/9),100)
cost75 = MenuLabel(" 150 ",(0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*6/9),100)
cost100 = MenuLabel(" 200 ",(0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*7/9),100)
cost125 = MenuLabel(" 250 ",(0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*8/9),100)
storeCost = [cost, cost25, cost50, cost75, cost100, cost125]

#Default flyer type (before others are bought)
currentType = 'paperBomber'

#Buy buttons for each plane in the store
paperFlyboyBuy = MenuLabel("Buy",(0, 0, 0),screenWidth/57,(screenWidth*2/3,screenHeight*4/9),86)
biBomberBuy = MenuLabel("Buy",(0, 0, 0),screenWidth/57,(screenWidth*2/3,screenHeight*5/9),87)
biFlyboyBuy = MenuLabel("Buy",(0, 0, 0),screenWidth/57,(screenWidth*2/3,screenHeight*6/9),88)
bubbleBuy = MenuLabel("Buy",(0, 0, 0),screenWidth/57,(screenWidth*2/3,screenHeight*7/9),89)
bubbleBoyBuy = MenuLabel("Buy",(0, 0, 0),screenWidth/57,(screenWidth*2/3,screenHeight*8/9),90)
storeBuy = [paperFlyboyBuy, biBomberBuy, biFlyboyBuy, bubbleBuy, bubbleBoyBuy]


#In-Game
scoreLabel = MenuLabel("Score: 0",(0, 0, 0),screenWidth/57,(screenWidth/9,screenHeight/9),100)
quoteLabel = MenuLabel(quoteReader.getQuote(), (0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*11/12),100)
pauseLabel = MenuLabel("Game Paused",(0,0,0),screenWidth/50,(screenWidth/2,screenHeight/2),100)
### Initializing Main Loop variables and images ###
imageBkg = pygame.transform.scale(pygame.image.load( "Assets/img/HouseNoGrass.png" ).convert(),(screenWidth,screenHeight))

### Powerup images ###

rainbow_powerup = pygame.transform.scale(pygame.image.load( "Assets/img/Rainbow.png" ).convert_alpha(), (screenHeight/7, screenHeight/7))
gravityFlip = pygame.transform.scale(pygame.image.load( "Assets/img/GravitySwap.png" ).convert_alpha(), (screenHeight/7, screenHeight/7))

###Base squirrel###
imageScale = (screenHeight/9, screenHeight/9)
whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhitePlane.png" ).convert_alpha(), imageScale)
redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRedPlane.png" ).convert_alpha(), imageScale)
blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelBluePlane.png" ).convert_alpha(), imageScale)
greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelGreenPlane.png" ).convert_alpha(), imageScale)
purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelPurplePlane.png" ).convert_alpha(), imageScale)
yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelYellowPlane.png" ).convert_alpha(), imageScale)
cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelCyanPlane.png" ).convert_alpha(), imageScale)
orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelOrangePlane.png" ).convert_alpha(), imageScale)
rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRainbowPlane.png" ).convert_alpha(), imageScale)
imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]


isSpacebar = False
justClicked = False #Boolean so we can't double click options in the menu
isPassing = False #Boolean so score isn't counted twice, nor sound played twice
paused = False
if settings[3] == 1:
	colorBlind = True
else:
	colorBlind = False
counter = 0
score = 0
wallSpeed = -3
nextWall = random.randint(145, 170)
nextBeam = 60
nextPowerUp = 850
low = 100
high = 140
angle = 0

rainbowYvel = 3 # we could make it proportional to the wall speed, but idk if James wants
				# \ to keep the vertical powerup velocity constant or not

obstacleList = preLoaded1

activeWalls = []
activeBeams = []
activePowerUps = []
grassList = []
windowList = []
scoreLabels = []

fpsTest = []
fpsSum = 0

#Color list
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
ORANGE = (255,99,71)

baseColors = [RED,BLUE,GREEN,PURPLE,CYAN,ORANGE,YELLOW]

### load all paint beam images ###

imageScale = (screenHeight/5, screenHeight*15/16)
redPaint = pygame.transform.scale(pygame.image.load( "Assets/img/RedPaint.png" ).convert_alpha(), imageScale)
bluePaint = pygame.transform.scale(pygame.image.load( "Assets/img/BluePaint.png" ).convert_alpha(), imageScale)
greenPaint = pygame.transform.scale(pygame.image.load( "Assets/img/GreenPaint.png" ).convert_alpha(), imageScale)
purplePaint = pygame.transform.scale(pygame.image.load( "Assets/img/PurplePaint.png" ).convert_alpha(), imageScale)
yellowPaint = pygame.transform.scale(pygame.image.load( "Assets/img/YellowPaint.png" ).convert_alpha(), imageScale)
orangePaint = pygame.transform.scale(pygame.image.load( "Assets/img/OrangePaint.png" ).convert_alpha(), imageScale)
cyanPaint = pygame.transform.scale(pygame.image.load( "Assets/img/CyanPaint.png" ).convert_alpha(), imageScale)

windowImage = pygame.transform.scale(pygame.image.load( "Assets/img/Window.png" ).convert(), (screenWidth/6, screenWidth/6))
grassImage = pygame.transform.scale(pygame.image.load( "Assets/img/grass.png" ).convert(), (screenWidth, screenHeight/16))

#m.importLists(avatarParams, creditsMenu, optionsList, lossMenu, instructions)	# call mainfunc's importLists function to return local lists
avatarParams = [screenWidth, screenHeight, soundToggle, currentType]

flier = avatar.Avatar(avatarParams[0], avatarParams[1], avatarParams[2], imageList)

preLoaded1.join()
preLoaded2.join()
preLoaded3.join()
preLoaded4.join()

obstacleList = preLoaded1.getObstacles()

### Server Params ###
host = '137.146.141.168';
port = 8888;

def serverConnect(host, port, score):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.1)
	try:
		s.connect((host , port))
		data = str(score)
		s.sendall(data)
		reply = s.recv(4096)
		s.close()
		serverHighScores = reply.split()
	except socket.error:
		print 'Failed to connect to server'
		serverHighScores = ["Couldn't Connect to Server"]
		
	localHighScores = HighScoreReader.getHighScores(score)
	
	return localHighScores, serverHighScores

while 1:#Main loop
	if gameState == 0: #Start Menu
		# handle every event since the last frame.
		screen.blit(mainBackground,(0,0))
		
		
		angle -= 3 #Slow speed
		if angle < -360:
			angle = 0
		temp_image = fan
		orig_rect = fan.get_rect()
		rotated_image = pygame.transform.rotate(fan, angle)
		rotated_rect = orig_rect.copy()
		rotated_rect.center = rotated_image.get_rect().center #Makes sure our new image is centered after rotation
		fan = rotated_image.subsurface(rotated_rect).copy()
		screen.blit(fan,(screenWidth*29/128,screenHeight*8/30))
		fan = temp_image
		
		
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
		quoteLabel.update(screen)
		title.update(screen)	# relocated code to mainButtonsClicked function
		
		bools = [musicToggle, musicToggled, soundToggled, justClicked, lowRes, lowResolution,colorBlind]
		avatarParams = [screenWidth, screenHeight, soundToggle, currentType]
		gameState, score, counter = m.mainButtonsClicked(gameState, score, counter, bools, mainMenu, mouse, screen, clickSound, scoreLabel, avatarParams)	# relocated code to checkMainItems function


		justClicked = pygame.mouse.get_pressed()[0]
			
# -----------------------------------------------------------------------------------------

	
	elif gameState == 1: #The actual game looping part
		pygame.mouse.set_visible(False)
		
		counter += 1
		
		screen.blit(imageBkg,(0,0))
		
		tempList = []
		
		if grassList != []:
			if grassList[-1].getX() < screenWidth/10:
				newGrass = Grass(screenWidth, screenHeight, grassImage)
				grassList.append(newGrass)
		else:
			newGrass = Grass(0, screenHeight, grassImage)
			grassList.append(newGrass)
		
		for item in grassList:
			item.move(wallSpeed, screen)
			if item.getX() > -screenWidth*1.2:
				tempList.append(item)
		grassList = list(tempList)
		
		tempList = []
		if counter % 750 == 0:
			newWindow = Window(screenWidth,screenHeight, windowImage)
			windowList.append(newWindow)
			
		for item in windowList:
			item.move(wallSpeed, screen)
			if item.getX() > -screenWidth/2:
				tempList.append(item)
				
		windowList = list(tempList)
		
		tempList = []
		if counter == nextBeam:
			
			if abs(nextBeam - nextWall) > 50: #So they don't spawn on top of each other
				tempColors = list(baseColors)
				tempColors.remove(flier.getColor())
				difColor = random.choice(tempColors)

				if colorBlind:
					if difColor == RED:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, redPaint, copy.copy(redLabelImage))
					elif difColor == GREEN:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, greenPaint, copy.copy(greenLabelImage))
					elif difColor == BLUE:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, bluePaint, copy.copy(blueLabelImage))
					elif difColor == PURPLE:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, purplePaint, copy.copy(purpleLabelImage))
					elif difColor == ORANGE:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, orangePaint, copy.copy(orangeLabelImage))
					elif difColor == YELLOW:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, yellowPaint, copy.copy(yellowLabelImage))
					elif difColor == CYAN:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, cyanPaint, copy.copy(cyanLabelImage))
				else:
					if difColor == RED:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, redPaint)
					elif difColor == GREEN:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, greenPaint)
					elif difColor == BLUE:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, bluePaint)
					elif difColor == PURPLE:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, purplePaint)
					elif difColor == ORANGE:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, orangePaint)
					elif difColor == YELLOW:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, yellowPaint)
					elif difColor == CYAN:
						myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, cyanPaint)
					
				if activeBeams != []:
					if myBeam.getColor() != activeBeams[-1].getColor() and myBeam.getColor() != flier.getColor():
						activeBeams.append(myBeam)
				else:
					if myBeam.getColor() != flier.getColor():
						activeBeams.append(myBeam)
			nextBeam = random.randint(low + 150, high + 180) + counter
			
		if counter == nextWall:
			if activeBeams != []:
				if colorBlind:
					myWall = Wall(activeBeams[-1].getColor(), screenWidth, screenHeight, baseColors, obstacleList, cbImageLabels)	# create the Wall object with a certain number of obstacles
				else:
					myWall = Wall(activeBeams[-1].getColor(), screenWidth, screenHeight, baseColors, obstacleList)
			else:
				if colorBlind:
					myWall = Wall(flier.getColor(), screenWidth, screenHeight, baseColors, obstacleList, cbImageLabels)	# create the Wall object with a certain number of obstacles
				else:
					myWall = Wall(flier.getColor(), screenWidth, screenHeight, baseColors, obstacleList)

			nextWall = random.randint(low + 145, high + 170) + counter
			activeWalls.append(myWall)
			
		
		m.updateFlier(flier) #Calls movement, gravity and rotation of avatar
		
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE]:
			isSpacebar = True
		else:
			isSpacebar = False
		### Iteration of objects on screen ###
		for item in activeWalls:#Create an iterator here to move each object, and stop drawing the ones that go off-screen
			item.moveWall(wallSpeed, screen)
			if item.getX() > -screenWidth/28:
				tempList.append(item)
				### If performance becomes an issue, check into forcing all update at once, instead of staggered

		activeWalls = list(tempList)
		tempList = []
		
		for item in activeBeams:
			item.moveBeam(wallSpeed, screen)
			if item.getPosition() > -screenWidth/5:
				tempList.append(item)
				
		activeBeams = list(tempList)
		if flier.beamCollision(activeBeams[:1]):
			rainbowSound.stop()
			antiGravity.stop()
			pygame.mixer.music.set_volume(0.75)
			planeLabel.updateText("Color: "+flier.string)
		
		if flier.wallCollision(activeWalls[:1]) == True: #If passing through the wall is true
			if isPassing == False:												 # added gameState argument for rainbow testing
				m.playSound(pointSound, soundToggle)
				score += 1
				scoreLabel.updateText("Score: "+str(score))
				isPassing = True #So score is calculated once per wall
				
				### Changing the difficulty ###
				if score % 2 == 0:
					if low > 0:
						low -= 7
					if high > 0:
						high -= 7
				if score == 1:
					obstacleList = preLoaded2.getObstacles()
				elif score == 3:
					wallSpeed = -4
				elif score == 6:
					obstacleList = preLoaded3.getObstacles()
				elif score == 10:
					wallSpeed = -5
				elif score == 16:
					obstacleList = preLoaded4.getObstacles()
				elif score == 18:
					obstacleList = preLoaded3.getObstacles()
				elif score == 20:
					obstacleList = preLoaded4.getObstacles()
				elif score == 24:
					wallSpeed = -6
				elif score == 35:
					wallSpeed = -7
				elif score == 50:
					wallSpeed = -8
		else:
			isPassing = False
		
		# Powerup collision handling, created one powerup for testing purposes, still need
		# \ to implement spawning

		if counter == nextPowerUp and flier.flierState != 1:
			if random.randint(0,1) == 0:
				power_up = Powerup([screenWidth,screenHeight/2], rainbow_powerup, 'rainbow')
			else:
				power_up = Powerup([screenWidth,screenHeight/2], gravityFlip, 'gravitySwitch')
			
			activePowerUps.append(power_up)
			nextPowerUp = counter + random.randint(1200,1800)
		tempList = []
		
		for item in activePowerUps:
			rainbowYvel = item.movePowerUp([wallSpeed,rainbowYvel], screen)
			if item.x  > -screenWidth/2:
				tempList.append(item)
				
		activePowerUps = list(tempList)
		
		if flier.powerUpCollision(activePowerUps, soundToggle):	# Does the avatar collide with a powerup?
			activePowerUps = []
			
			if flier.flierState == 1: 
				
				
				if colorBlind:
					flier.string = 'Rainbow'
					planeLabel.updateText("Color: "+flier.string)
					planeLabel.update(screen)
				activeBeams = []
				nextBeam = random.randint(low + 220, high + 260) + counter
				rainbowSound.play()
				pygame.mixer.music.set_volume(0.0)
			if flier.flierState == 2:
				antiGravity.play()
				pygame.mixer.music.set_volume(0.0)
			#inputs the current score, then returns a list of all scores cut off at top 10
		scoreLabel.update(screen)
		if colorBlind:
			planeLabel.x = flier.x
			planeLabel.y = flier.y + flier.image.get_height()
			planeLabel.update(screen)
		fpsTest.append( clock.get_fps() )
		
		flier.update(screen) #It's a start.
		if flier.getAlive() == False: #if the flier is dead
			
			pygame.mixer.music.set_volume(1.0)
			quoteLabel.updateText(quoteReader.getQuote())
			counter = 0
			tempList = []
			activeWalls = []
			activeBeams = []
			activePowerUps = []
			windowList = []
			grassList = []
			
			nextPowerUp = 850
			wallSpeed = -3
			gameState = 5 #goto loss screen
			flier.restart(soundToggle)
			planeLabel.updateText("Color: "+flier.string)
			nextWall = random.randint(145, 170)
			nextBeam = 60
			low = 80
			high = 120
			obstacleList = preLoaded1.getObstacles()

			localHighScores, serverHighScores = serverConnect(host, port, score)

			for x in fpsTest:
				fpsSum+=x
				
			print fpsSum/len(fpsTest)
			fpsTest = []
			fpsSum = 0
			
			fp = file('Store.txt') #reads the file
			lines = fp.readlines() #reads lines and creates an array of lines
			fp.close() #closes the file
			itemsBought = [] #list of scores that is returned
			for line in lines: 
				words = line.split()
				itemsBought.append( int(words[0]) )
				
			itemsBought[-1] += score
			totalLabel.updateText("Total Score: "+str(itemsBought[-1]))
			writeString = '' #creates the string for writing to the file
			for num in itemsBought:
				writeString += str(num) + '\n'		
			
			fp = file( 'Store.txt', 'w') #writes over the old file, adding the player score
			fp.write(writeString)
			fp.close()	
			
			
			
			loadedScore = MenuLabel("Local High Scores",(0, 0, 0),screenWidth/53,(screenWidth*3/5,screenHeight/15 + screenHeight/10),100)
			scoreLabels.append(loadedScore)
			
			for x in range(2,len(localHighScores) +2):
			
				loadedScore = MenuLabel("Score: " +str(localHighScores[x-2]), (0, 0, 0),screenWidth/57,(screenWidth*3/5,screenHeight/15*x + screenHeight/10),100)
				scoreLabels.append(loadedScore)
				
			loadedScore = MenuLabel("Server High Scores",(0, 0, 0),screenWidth/53,(screenWidth*4/5,screenHeight/15 + screenHeight/10),100)
			scoreLabels.append(loadedScore)
			
			if serverHighScores[0] == "Couldn't Connect to Server":
				loadedScore = MenuLabel(str(serverHighScores[0]),(0, 0, 0),screenWidth/57,(screenWidth*4/5,screenHeight/15*2 + screenHeight/10),100)
				scoreLabels.append(loadedScore)
				
			else:
				for x in range(2,len(serverHighScores)+2):
					loadedScore = MenuLabel("Score: " +str(serverHighScores[x-2]),(0, 0, 0),screenWidth/57,(screenWidth*4/5,screenHeight/15*x + screenHeight/10),100)
					scoreLabels.append(loadedScore)
					
			pygame.mouse.set_visible(True)
			
		else:
			
			key = pygame.key.get_pressed()
			if key[pygame.K_p] == True:
				if paused == False:
					gameState = 7
					paused = True
			else:
				paused = False
# -----------------------------------------------------------------------------------------

		
		
	elif gameState == 2: #Instructions
		if type(instructions[0]) is loadMenuLabels :
			tempList = []
			for item in instructions :
				item.join()
				tempList.append(item.getLabel())
			instructions = list(tempList)
			
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		m.State2Update(screen, instructions, Powerup([screenWidth*4/5,screenHeight/2], gravityFlip, 'gravitySwitch'), Powerup([screenWidth*4/5,screenHeight/4], rainbow_powerup, 'rainbow'))	# relocated code to State2Update function
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (mainBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			m.playSound(clickSound,soundToggle)
			gameState = 0
			
# ----------------------------------------------------------------------------------------

			
	elif gameState == 3: #Credits
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		if type(creditsMenu[0]) is loadMenuLabels :
			tempList = []
			for item in creditsMenu :
				item.join()
				tempList.append(item.getLabel())
			creditsMenu = list(tempList)
			
		for item in creditsMenu:
			item.update(screen)
			
		lossBack = creditsMenu[10]
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (lossBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			#If back button is clicked, go back to loss screen
			m.playSound(clickSound,soundToggle)
			gameState = 5
			screen.fill((40,80,160))
			
# -----------------------------------------------------------------------------------------

			
	elif gameState == 4: #Quit state
		pygame.quit()
		sys.exit()
		
# -----------------------------------------------------------------------------------------
		
		
	elif gameState == 5: #Loss Screen
		
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] == True and isSpacebar == False:
			gameState = 1
			### Call this to restart the game and scores ###
			score = 0
			scoreLabel.updateText("Score: "+str(score))
			pygame.mixer.music.set_volume(0.75)
			counter = 0
		mouse = pygame.mouse.get_pos()
		isSpacebar = key[pygame.K_SPACE]
		
		if type(lossMenu[0]) is loadMenuLabels:
			tempList = []
			for item in lossMenu :
				item.join()
				tempList.append(item.getLabel())
			lossMenu = list(tempList)
			
		for item in scoreLabels:
			item.update(screen)
			
		for item in lossMenu:
			quoteLabel.update(screen)
			
			if item.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
				m.playSound(clickSound,soundToggle)
				gameState = item.getState()
				
				if gameState == 1:

					### Call this to restart the game and scores ###
					flier, score = m.restartGame(score, scoreLabel, flier)	# relocated code to restartGame function

				elif gameState == 0:
				
					if musicToggle == True:
						pygame.mixer.music.load("Assets/sound/soundtrack2.ogg")
						pygame.mixer.music.play(-1)
						
					quoteLabel.updateText(quoteReader.getQuote())
				justClicked = pygame.mouse.get_pressed()[0]
				
				break
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		
# -----------------------------------------------------------------------------------------

		
	if gameState == 6: #Options menu
		screen.fill((40,80,160)) #Blue screen
		avatarParams = [screenWidth, screenHeight, soundToggle, currentType]
		mouse = pygame.mouse.get_pos()
		bools = [musicToggle, musicToggled, soundToggled, justClicked, lowRes, lowResolution, colorBlind]
		musicToggle, soundToggle, gameState, lowRes, colorBlind = m.updateSoundOptions(bools, gameState, optionsList, mouse, screen, avatarParams, clickSound)
		# relocated code to updateSoundOptions function
		resInfo.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		flier.restart(soundToggle) #Restart all the fields of the flier
		
# -----------------------------------------------------------------------------------------
		
	
	
	if gameState == 7:#Pause game state, press p to unpause
		pauseLabel.update(screen)
		key = pygame.key.get_pressed()
		if key[pygame.K_p] == True:
			if paused == False:
				gameState = 1
				paused = True
		else:
			paused = False
			
			
# -----------------------------------------------------------------------------------------------------------------


	if gameState == 8: #Store page
		screen.blit(storebackground,(0,0))
		storeTitle.update(screen)
		planeSkins.update(screen)
		totalLabel.update(screen)
		
		# Blit all of the different plane images to the screen
		screen.blit(paper_bomber, (screenWidth*1/6,screenHeight*5/18))
		screen.blit(paper_flyboy, (screenWidth*1/6,screenHeight*7/18))
		screen.blit(biplane_bomber, (screenWidth*1/6,screenHeight*9/18))
		screen.blit(biplane_flyboy, (screenWidth*1/6,screenHeight*11/18))
		screen.blit(bubble_bomber, (screenWidth*1/6,screenHeight*13/18))
		screen.blit(bubble_flyboy, (screenWidth*1/6,screenHeight*15/18))
		
		#Checking if the items have been bought already
		if itemsBought[0] == 1:
			if storeBuy[0].text != "Bought":
				storeBuy[0].updateText("Bought")
		if itemsBought[1] == 1:
			if storeBuy[1].text != "Bought":
				storeBuy[1].updateText("Bought")
		if itemsBought[2] == 1:	
			if storeBuy[2].text != "Bought":
				storeBuy[2].updateText("Bought")
		if itemsBought[3] == 1:
			if storeBuy[3].text != "Bought":
				storeBuy[3].updateText("Bought")
		if itemsBought[4] == 1:
			if storeBuy[4].text != "Bought":
				storeBuy[4].updateText("Bought")
				
		mouse = pygame.mouse.get_pos()
		
		for item in storeCost: #Display cost
			item.update(screen)
			
		for item in storeBuy: #Display and allow buying of planes
			if item.hover((mouse[0],mouse[1]),avatarParams[2]) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				clickedState = item.getState()
				
				if clickedState == 86 and itemsBought[0] == 0:#paper with shades
					if itemsBought[-1] >= 50:
						itemsBought[-1] -= 50
						itemsBought[0] = 1
						m.playSound(kachingSound, soundToggle)
					else:
						errorSound.play()
				if clickedState == 87 and itemsBought[1] == 0:#biplane with hat
					if itemsBought[-1] >= 100:
						itemsBought[-1] -= 100
						itemsBought[1] = 1
						m.playSound(kachingSound, soundToggle)
					else:
						errorSound.play()
				if clickedState == 88 and itemsBought[2] == 0:#biplane with hat
					if itemsBought[-1] >= 150:
						itemsBought[-1] -= 150
						itemsBought[2] = 1
						m.playSound(kachingSound, soundToggle)
					else:
						errorSound.play()
				if clickedState == 89 and itemsBought[3] == 0:#biplane with hat
					if itemsBought[-1] >= 200:
						itemsBought[-1] -= 200
						itemsBought[3] = 1
						m.playSound(kachingSound, soundToggle)
					else:
						errorSound.play()
				if clickedState == 90 and itemsBought[4] == 0:#biplane with hat
					if itemsBought[-1] >= 250:
						itemsBought[-1] -= 250
						itemsBought[4] = 1
						m.playSound(kachingSound, soundToggle)
					else:
						errorSound.play()
						
				writeString = '' #creates the string for writing to the file
				for num in itemsBought:
					writeString += str(num) + '\n'		
				
				fp = file( 'Store.txt', 'w') #writes over the old file
				fp.write(writeString)
				fp.close()	
				totalLabel.updateText("Total Score: "+str(itemsBought[-1]))
					
			item.isHover = False
			item.update(screen)
			
		for item in storeTitles: #Display and allowing selection of planes you own
		
			if item.hover((mouse[0],mouse[1]),avatarParams[2]) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				m.playSound(clickSound,soundToggle)
				clickedState = item.getState()
				item.isHover = False
				if clickedState == 81:
					currentType = 'paperBomber'
					whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhitePlane.png" ).convert_alpha(), imageScale)
					redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRedPlane.png" ).convert_alpha(), imageScale)
					blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelBluePlane.png" ).convert_alpha(), imageScale)
					greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelGreenPlane.png" ).convert_alpha(), imageScale)
					purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelPurplePlane.png" ).convert_alpha(), imageScale)
					yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelYellowPlane.png" ).convert_alpha(), imageScale)
					cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelCyanPlane.png" ).convert_alpha(), imageScale)
					orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelOrangePlane.png" ).convert_alpha(), imageScale)
					rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRainbowPlane.png" ).convert_alpha(), imageScale)
					imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]
					flier.load(imageList)
					pygame.mixer.music.load("Assets/sound/background.ogg")
					pygame.mixer.music.play(-1)
					
				elif clickedState == 82 and itemsBought[0] == 1:
					currentType = 'paperFlyboy'
					imageScale = (screenHeight/9, screenHeight/9)
					whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesWhitePlane.png" ).convert_alpha(), imageScale)
					redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesRedPlane.png" ).convert_alpha(), imageScale)
					blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesBluePlane.png" ).convert_alpha(), imageScale)
					greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesGreenPlane.png" ).convert_alpha(), imageScale)
					purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesPurplePlane.png" ).convert_alpha(), imageScale)
					yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesYellowPlane.png" ).convert_alpha(), imageScale)
					cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesCyanPlane.png" ).convert_alpha(), imageScale)
					orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesOrangePlane.png" ).convert_alpha(), imageScale)
					rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesRainbowPlane.png" ).convert_alpha(), imageScale)
					imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]
					flier.load(imageList)
					pygame.mixer.music.load("Assets/sound/background.ogg")
					pygame.mixer.music.play(-1)
					
					
				elif clickedState == 83 and itemsBought[1] == 1:
					currentType = 'biBomber'
					imageScale = (screenHeight/9, screenHeight/9)
					whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhiteBP.png" ).convert_alpha(), imageScale)
					redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRedBP.png" ).convert_alpha(), imageScale)
					blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelBlueBP.png" ).convert_alpha(), imageScale)
					greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelGreenBP.png" ).convert_alpha(), imageScale)
					purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelPurpleBP.png" ).convert_alpha(), imageScale)
					yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelYellowBP.png" ).convert_alpha(), imageScale)
					cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelCyanBP.png" ).convert_alpha(), imageScale)
					orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelOrangeBP.png" ).convert_alpha(), imageScale)
					rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRainbowBP.png" ).convert_alpha(), imageScale)
					imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]
					flier.load(imageList)
					pygame.mixer.music.load("Assets/sound/Original_Soundtrack.ogg")
					pygame.mixer.music.play(-1)
					
				elif clickedState == 84 and itemsBought[2] == 1:
					currentType = 'biFlyboy'
					imageScale = (screenHeight/9, screenHeight/9)
					whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesWhiteBP.png" ).convert_alpha(), imageScale)
					redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesRedBP.png" ).convert_alpha(), imageScale)
					blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesBlueBP.png" ).convert_alpha(), imageScale)
					greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesGreenBP.png" ).convert_alpha(), imageScale)
					purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesPurpleBP.png" ).convert_alpha(), imageScale)
					yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesYellowBP.png" ).convert_alpha(), imageScale)
					cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesCyanBP.png" ).convert_alpha(), imageScale)
					orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesOrangeBP.png" ).convert_alpha(), imageScale)
					rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesRainbowBP.png" ).convert_alpha(), imageScale)
					imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]
					flier.load(imageList)
					pygame.mixer.music.load("Assets/sound/Original_Soundtrack.ogg")
					pygame.mixer.music.play(-1)
					
				elif clickedState == 85 and itemsBought[3] == 1:
					currentType = 'bubbleBomber'
					imageScale = (screenHeight/9, screenHeight/9)
					whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhiteBubble.png" ).convert_alpha(), imageScale)
					redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRedBubble.png" ).convert_alpha(), imageScale)
					blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelBlueBubble.png" ).convert_alpha(), imageScale)
					greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelGreenBubble.png" ).convert_alpha(), imageScale)
					purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelPurpleBubble.png" ).convert_alpha(), imageScale)
					yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelYellowBubble.png" ).convert_alpha(), imageScale)
					cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelCyanBubble.png" ).convert_alpha(), imageScale)
					orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelOrangeBubble.png" ).convert_alpha(), imageScale)
					rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRainbowBubble.png" ).convert_alpha(), imageScale)
					imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]
					flier.load(imageList)
					pygame.mixer.music.load("Assets/sound/soundtrack3.ogg")
					pygame.mixer.music.play(-1)
					
				elif clickedState == 80 and itemsBought[4] == 1:
					currentType = 'bubbleFlyboy'
					imageScale = (screenHeight/9, screenHeight/9)
					whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesWhiteBubble.png" ).convert_alpha(), imageScale)
					redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesRedBubble.png" ).convert_alpha(), imageScale)
					blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesBlueBubble.png" ).convert_alpha(), imageScale)
					greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesGreenBubble.png" ).convert_alpha(), imageScale)
					purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesPurpleBubble.png" ).convert_alpha(), imageScale)
					yellowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesYellowBubble.png" ).convert_alpha(), imageScale)
					cyanImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesCyanBubble.png" ).convert_alpha(), imageScale)
					orangeImage =  pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesOrangeBubble.png" ).convert_alpha(), imageScale)
					rainbowImage = pygame.transform.scale(pygame.image.load( "Assets/img/SunglassesRainbowBubble.png" ).convert_alpha(), imageScale)
					imageList = [whiteImage, redImage, blueImage, greenImage, purpleImage, yellowImage, cyanImage, orangeImage, rainbowImage]
					flier.load(imageList)
					pygame.mixer.music.load("Assets/sound/soundtrack3.ogg")
					pygame.mixer.music.play(-1)
					
				elif clickedState == 5: #Back to the loss screen!
					screen.fill((40,80,160))
					gameState = 5
					flier.restart(soundToggle)
					break
			item.isHover = False
			item.update(screen)
			if currentType == 'paperBomber':
				paperBomber.isHover = True
				paperBomber.update(screen)
			elif currentType == 'paperFlyboy':
				paperFlyboy.isHover = True
				paperFlyboy.update(screen)
			elif currentType == 'biBomber':
				biBomber.isHover = True
				biBomber.update(screen)
			elif currentType == 'biFlyboy':
				biFlyboy.isHover = True
				biFlyboy.update(screen)
			elif currentType == 'bubbleBomber':
				bubble.isHover = True
				bubble.update(screen)
			elif currentType == 'bubbleFlyboy':
				bubbleBoy.isHover = True
				bubbleBoy.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]	
		
		
# ------------------------------------------------------------------------------------------------------
	#Intro animation
	if gameState == 9:
		pygame.mouse.set_visible(False)
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE]:
			gameState = 0
			
		if introXPos < screenWidth*8/12*2:
			counter +=1
			
		else:
			introXPos -= 4
			introYPos += 4
			screen.blit(intro,(0,0),(introXPos, introYPos, introWidth, introHeight))
			intro = pygame.transform.scale(intro,(introWidth,introHeight))
			
		if counter >= 70:
			if counter == 75:
				fanSound.play()
			screen.blit(mainBackground,(0,0))
			angle -= 3 #Slow speed
			if angle < -360:
				angle = 0
			temp_image = fan
			orig_rect = fan.get_rect()
			rotated_image = pygame.transform.rotate(fan, angle)
			rotated_rect = orig_rect.copy()
			rotated_rect.center = rotated_image.get_rect().center #Makes sure our new image is centered after rotation
			fan = rotated_image.subsurface(rotated_rect).copy()
			screen.blit(fan,(screenWidth*29/128,screenHeight*8/30))
			fan = temp_image
			counter += 1
			
		if counter >= 230:
			pygame.mouse.set_visible(True)
			counter = 0
			gameState = 0
			
	for event in pygame.event.get(): ##### Find out why removing this crashes the program #####
		if event.type == pygame.QUIT:
			pygame.quit() # quit the screen
			sys.exit()				
			break
		
	pygame.display.update() # update the screen

	clock.tick(65) # 65 fps
