# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

### This is going to be part of the Main Loop file, not it's own class ###
import pygame
import sys
import avatar
import HighScoreReader
import quoteReader
import random
from beams import *
from wall import Wall
from label import *
from grass import Grass
import mainfuncs as m

### Initializing all needed Pygame stuff ###
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()
infoObject = pygame.display.Info()
screenWidth = infoObject.current_w
screenHeight = infoObject.current_h
displayFlags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE #using hardware acceleration
screen = pygame.display.set_mode((screenWidth, screenHeight), displayFlags) #Screen size fits all screens

clock = pygame.time.Clock()

### Game Sound ###
hoverSound = pygame.mixer.Sound( "Assets/sound/click.wav" )
clickSound = pygame.mixer.Sound( "Assets/sound/pop.wav" )
pointSound = pygame.mixer.Sound( "Assets/sound/blip.wav" )
crashSound = pygame.mixer.Sound( "Assets/sound/hit_obstacle.wav" )

pygame.mixer.music.load("Assets/sound/background.mp3")

pygame.mixer.music.play(-1)
musicToggle = True
soundToggle = True

### Gamestate variables ###
gameState = 0
'''
	0 = menu loop
	1 = go to game
	2 = Instructions
	3 = Credits
	4 = Quit Game
	5 = Loss Screen
	6 = Options screen
'''
			
			
### Menu Items/Labels ###
# varName = MenuLable("Text", "Font-Style", BkgColor of Box, Text Color, fontSize, Position, gamestate it points to)

#Main Menu
title = MenuLabel("Fly Baby, Fly", (100,100,100),(255,105,180),42,(300,100),100)
start = MenuLabel("Start Game", (100,100,100),(255,153,0),26,(300,200),1)
instruction = MenuLabel("Instructions", (100,100,100),(255,153,0),26,(300,280),2)
options = MenuLabel("Options", (100,100,100),(255,153,0),26,(300,360),6)
mainQuit = MenuLabel("Quit", (100,100,100),(255,153,0),26,(300,440),4)
mainMenu = [start, mainQuit, instruction, options] #Main Menu Labels

#Credits
Producer = MenuLabel("He's a People Person (Producer): Chris Marcello", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8), 100)
Designer = MenuLabel("Man with Vision (Designer): James Lindberg", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 70), 100)
Programmer = MenuLabel("Hackerman (Lead Programmer): Lucas DeGraw", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 140), 100)
Artist = MenuLabel("Frida Kahlo + GIMP (Lead Artist): Riley Karp", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 210), 100)
Sound = MenuLabel("Mariachi (Lead Sound Design): Jerry Diaz ", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 280), 100)
Gamer = MenuLabel("Gamer (Quality Assurance): Austin Nantkes", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 350), 100)
Knife = MenuLabel("Swiss Army Knife (Multirole): Jon", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 420), 100)
DJ = MenuLabel("DJ (Art Assistance): Dean", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 490), 100)

Bruce = MenuLabel("Special Thanks to: Bruce (Totally Not CIA) Maxwell",(100,100,100),(0,0,0),26,(screenWidth/2, screenHeight/8 + 560),100)

lossBack = MenuLabel("Back", (100,100,100),(0,0,0),24,(screenWidth*8/9,screenHeight/15),5)
creditsMenu = [Producer, Designer, Programmer, Artist, Sound, Gamer, Knife, DJ, Bruce, lossBack]

#Instructions
paint = MenuLabel("Paint streams will change your plane's color", (100,100,100),(255,105,180),24,(screenWidth/2,screenHeight*2/7),100)
help = MenuLabel("Go through the color block that matches your plane", (100,100,100),(255,105,180),24,(screenWidth/2,screenHeight*3/7),100)
controls = MenuLabel("Press Spacebar to increase your upward speed!", (100,100,100),(255,105,180),24,(screenWidth/2,screenHeight*4/7),100)
mainBack = MenuLabel("Back", (100,100,100),(0,0,0),24,(screenWidth*6/7,screenHeight/15),0)
instructions = [paint, help, controls, mainBack]

#Options Menu
musicToggled = MenuLabel("Background Music On/Off", (100,100,100),(191, 255, 0),24,(screenWidth/2,screenHeight*2/7),42)
soundToggled = MenuLabel("Sound Effects On/Off", (100,100,100),(191, 255, 0),24,(screenWidth/2,screenHeight*3/7), 43)
optionsList = [mainBack, musicToggled, soundToggled]

#Loss Screen
credits = MenuLabel("Credits", (100,100,100),(0,0,0),26,(300,260),3)
restart = MenuLabel("Retry!", (100,100,100),(0,0,0),26,(300,100),1)
main = MenuLabel("Main Menu", (100,100,100),(0,0,0),26,(300,180),0)
lossQuit = MenuLabel("Quit", (100,100,100),(0,0,0),26,(300,340),4)
lossMenu = [restart, credits, lossQuit, main]

#In-Game
scoreLabel = MenuLabel("Score: 0", (100,100,100),(0, 0, 0),24,(screenWidth/9,screenHeight/9),100)
quoteLabel = MenuLabel(quoteReader.getQuote(), (100,100,100),(0, 0, 0),24,(screenWidth/2,screenHeight*11/12),100)

### Initializing Main Loop variables and images ###
squirrel = pygame.image.load( "Assets/img/squirrelPilot.png" ).convert_alpha()
imageBkg = pygame.transform.scale(pygame.image.load( "Assets/img/GrayHouse.png" ).convert(),(screenWidth,screenHeight))
testGrass = Grass(screenWidth, screenHeight, -4)

justClicked = False #Boolean so we can't double click options in the menu
isPassing = False #Boolean so score isn't counted twice, nor sound played twice
spacePress = False #So game doesn't restart if you're holding down space and die

counter = 0
score = 0
wallSpeed = -4
nextWall = random.randint(130, 160)
nextBeam = random.randint(170, 200)

activeWalls = []
activeBeams = []
grassList = []
scoreLabels = []
#Color list
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
MAROON = (128,0,0)
OLIVE = (128,128,0)
colors = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN, MAROON, OLIVE] ### For current game, only BLUE RED GREEN
baseColors = [RED,BLUE,GREEN,PURPLE]

imageScale = (screenHeight/5, screenHeight*15/16)
redPaint = pygame.transform.scale(pygame.image.load( "Assets/img/RedPaint.png" ).convert_alpha(), imageScale)
bluePaint = pygame.transform.scale(pygame.image.load( "Assets/img/BluePaint.png" ).convert_alpha(), imageScale)
greenPaint = pygame.transform.scale(pygame.image.load( "Assets/img/GreenPaint.png" ).convert_alpha(), imageScale)
purplePaint = pygame.transform.scale(pygame.image.load( "Assets/img/PurplePaint.png" ).convert_alpha(), imageScale)

avatarParams = [screenWidth, screenHeight, soundToggle]
#bools = [musicToggle, musicToggled, soundToggled, justClicked]
m.importLists(avatarParams, creditsMenu, optionsList, lossMenu, instructions)	# call mainfunc's importLists function to return local lists
																				# of those from main in mainfunc
flier = avatar.Avatar(avatarParams[0], avatarParams[1], avatarParams[2])
while 1:#Main loop
	if gameState == 0: #Start Menu
		# handle every event since the last frame.
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
		screen.blit(squirrel,(500,50))
		quoteLabel.update(screen)
		title.update(screen)	# relocated code to mainButtonsClicked function
		bools = [musicToggle, musicToggled, soundToggled, justClicked]

		gameState, flier, score, counter = m.mainButtonsClicked(gameState, flier, score, counter, bools, mainMenu, mouse, screen, clickSound, scoreLabel, avatarParams)	# relocated code to checkMainItems function


		justClicked = pygame.mouse.get_pressed()[0]
			
	
	elif gameState == 1: #The actual game looping part
		pygame.mouse.set_visible(False)
		
		screen.blit(imageBkg,(0,0))
		if score == 5:
			wallSpeed = -4

		#screen.blit(grass,(0,0))
		counter += 1
		testGrass.updateGrass(screen)
		
		tempList = []
		if counter == nextBeam:
			if abs(nextBeam - nextWall) > 40: #So they don't spawn on top of each other
				difColor = random.choice(baseColors)
				while difColor == flier.getColor():
					difColor = random.choice(baseColors)
					
				if difColor == RED:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, redPaint)
				elif difColor == GREEN:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, greenPaint)
				elif difColor == BLUE:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, bluePaint)
				elif difColor == PURPLE:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, purplePaint)
				activeBeams.append(myBeam)
			nextBeam = random.randint(170, 200) + counter
			
		if counter == nextWall:
			if len(activeBeams)!= 0:
				myWall = Wall(activeBeams[len(activeBeams)-1].getColor(), screenWidth, screenHeight, colors, 3)	# create the Wall object with a certain number of obstacles
				#Last beam in the list is the closest one to the wall being created
			else:
				myWall = Wall(flier.getColor(), screenWidth, screenHeight, colors, 3)
				
			nextWall = random.randint(130, 160) + counter
			#bottomGrass = grass
			activeWalls.append(myWall)
			#grassList.append(bottomGrass)
			
		m.updateFlier(flier) #Calls movement, gravity and rotation of avatar
		
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
			if item.getPosition() > -screenWidth/4:
				tempList.append(item)
				
		activeBeams = list(tempList)
		
		flier.beamCollision(activeBeams, soundToggle)
		
		if flier.wallCollision(activeWalls[:1], soundToggle) == True: #If passing through the wall is true
			if isPassing == False:
				m.playSound(pointSound, soundToggle)
				score += 1
				scoreLabel.updateText("Score: "+str(score))
				isPassing = True #So score is calculated once per wall
		else:
			isPassing = False
			
		scoreLabel.update(screen)
		flier.update(screen)
	
		if flier.getAlive() == False: #if the flier is dead
			pygame.mixer.music.set_volume(1.0)
			quoteLabel.updateText(quoteReader.getQuote())
			activeWalls = []
			activeBeams = []
			nextWall = random.randint(130, 160)
			nextBeam = random.randint(170, 200)
			pygame.mouse.set_visible(True)
			wallSpeed = -4
			gameState = 5 #goto loss screen 
			highScores = HighScoreReader.getHighScores(score) #inputs the current score, then returns a list of all scores cut off at top 10
			for x in range(0,len(highScores)):
				loadedScore = MenuLabel("Score: " +str(highScores[x]), (100,100,100),(0, 0, 0),24,(screenWidth*3/4,screenHeight/15*x + screenHeight/5),100)
				scoreLabels.append(loadedScore)
		#print clock.get_fps() #Prints out the fps during the game for testing
	
	elif gameState == 2: #Instructions
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		m.State2Update(screen, instructions)	# relocated code to State2Update function
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (mainBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			m.playSound(clickSound,soundToggle)
			gameState = 0
			
	elif gameState == 3: #Credits
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		
		for item in creditsMenu:
			item.update(screen)
			
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (lossBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			#If back button is clicked, go back to loss screen
			m.playSound(clickSound,soundToggle)
			gameState = 5
			screen.fill((40,80,160))
			
	elif gameState == 4: #Quit state
		pygame.quit()
		sys.exit()
		
	elif gameState == 5: #Loss Screen
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] == True:
			gameState = 1
			### Call this to restart the game and scores ###
			score = 0
			scoreLabel.updateText("Score: "+str(score))
			pygame.mixer.music.set_volume(0.4)
			counter = 0
			flier = avatar.Avatar(screenWidth, screenHeight, soundToggle)
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
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
					counter, flier = m.restartGame(counter, score, scoreLabel, flier)	# relocated code to restartGame function

				elif gameState == 0:
					quoteLabel.updateText(quoteReader.getQuote())
				justClicked = pygame.mouse.get_pressed()[0]
				
				break
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		
	if gameState == 6: #Options menu
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		bools = [musicToggle, musicToggled, soundToggled, justClicked]
		musicToggle, soundToggle, gameState = m.updateSoundOptions(bools, gameState, optionsList, mouse, screen, avatarParams, clickSound)
		# relocated code to updateSoundOptions function
		
		justClicked = pygame.mouse.get_pressed()[0]
		
	for event in pygame.event.get(): ##### Find out why removing this crashes the program #####
			if event.type == pygame.QUIT:
				pygame.quit() # quit the screen
				sys.exit()
				break
		
	pygame.display.update() # update the screen
	clock.tick(60) # 60 fps