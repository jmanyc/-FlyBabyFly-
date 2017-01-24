# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, sys, avatar, socket, HighScoreReader, quoteReader, random
from beams import Beam
from wall import Wall
from label import MenuLabel
#from grass import Grass
import mainfuncs as m
from powerups import Powerup
from loadObstacles import *

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
'''

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
screen.blit(mainBackground,(0,0))
screen.blit(fan,(screenWidth*29/128,screenHeight*8/30))
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
rainbowSound = pygame.mixer.Sound( "Assets/sound/paintsplash_sound16.wav" )

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
Producer = MenuLabel("He's a People Person (Producer): Chris Marcello",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8), 100)
Designer = MenuLabel("Man with Vision (Designer): James Lindberg", (0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 70), 100)
Programmer = MenuLabel("Hackerman (Lead Programmer): Lucas DeGraw",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 140), 100)
Artist = MenuLabel("Frida Kahlo + GIMP (Lead Artist): Riley Karp",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 210), 100)
Sound = MenuLabel("Mariachi (Lead Sound Design): Jerry Diaz ", (0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 280), 100)
Gamer = MenuLabel("Gamer (Quality Assurance): Austin Nantkes",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 350), 100)
Knife = MenuLabel("Swiss Army Knife (Multirole): Jon",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 420), 100)
DJ = MenuLabel("DJ (Art Assistance): Dean",(0,0,0), screenWidth/53, (screenWidth/2, screenHeight/8 + 490), 100)

Bruce = MenuLabel("Special Thanks to: Bruce (Totally Not CIA) Maxwell",(0,0,0),screenWidth/53,(screenWidth/2, screenHeight/8 + 560),100)

lossBack = MenuLabel("Back",(0,0,0), screenWidth/57,(screenWidth*8/9,screenHeight/15),5)
creditsMenu = [Producer, Designer, Programmer, Artist, Sound, Gamer, Knife, DJ, Bruce, lossBack]

#Instructions
paint = MenuLabel("Paint streams will change your plane's color",(255,105,180),screenWidth/57,(screenWidth/2,screenHeight*2/7),100)
help = MenuLabel("Go through the color block that matches your plane",(255,105,180),screenWidth/57,(screenWidth/2,screenHeight*3/7),100)
controls = MenuLabel("Press Spacebar to increase your upward speed!",(255,105,180),screenWidth/57,(screenWidth/2,screenHeight*4/7),100)
mainBack = MenuLabel("Back", (0,0,0),screenWidth/57,(screenWidth*6/7,screenHeight/15),0)
instructions = [paint, help, controls, mainBack]

#Options Menu
lowResolution = MenuLabel("Slow Game Mode",(191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*4/7),41)
resInfo = MenuLabel("Turn on Slow Game Mode and restart game if it runs poorly",(191, 255, 0),screenWidth/68,(screenWidth/2,screenHeight*5/7),100)
musicToggled = MenuLabel("Background Music On/Off", (191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*2/7),42)
soundToggled = MenuLabel("Sound Effects On/Off",(191, 255, 0),screenWidth/57,(screenWidth/2,screenHeight*3/7), 43)
optionsList = [mainBack, musicToggled, soundToggled,lowResolution]

#Loss Screen
credits = MenuLabel("Credits",(0,0,0),screenWidth/53,(300,260),3)
restart = MenuLabel("Retry!",(0,0,0),screenWidth/53,(300,100),1)
main = MenuLabel("Main Menu",(0,0,0),screenWidth/53,(300,180),0)
lossQuit = MenuLabel("Quit",(0,0,0),screenWidth/53,(300,340),4)
lossMenu = [restart, credits, lossQuit, main]

#In-Game
scoreLabel = MenuLabel("Score: 0",(0, 0, 0),screenWidth/57,(screenWidth/9,screenHeight/9),100)
quoteLabel = MenuLabel(quoteReader.getQuote(), (0, 0, 0),screenWidth/57,(screenWidth/2,screenHeight*11/12),100)

### Initializing Main Loop variables and images ###
imageBkg = pygame.transform.scale(pygame.image.load( "Assets/img/HouseWGrass.png" ).convert(),(screenWidth,screenHeight))

### Powerup images ###

rainbow_powerup = pygame.transform.scale(pygame.image.load( "Assets/img/Rainbow.png" ).convert_alpha(), (screenHeight/7, screenHeight/7))

### Need to load and convert power up images ###



#testGrass = Grass(screenWidth, screenHeight, -4)

justClicked = False #Boolean so we can't double click options in the menu
isPassing = False #Boolean so score isn't counted twice, nor sound played twice
spacePress = False #So game doesn't restart if you're holding down space and die
paused = False

counter = 0
score = 0
wallSpeed = -3
nextWall = random.randint(130, 160)
nextBeam = 60
low = 80
high = 120
angle = 0

rainbowYvel = 3 # we could make it proportional to the wall speed, but idk if James wants
				# \ to keep the vertical powerup velocity constant or not

obstacleList = preLoaded1

activeWalls = []
activeBeams = []
activePowerUps = []
grassList = []
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
colors = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN, ORANGE] ### For current game, only BLUE RED GREEN
baseColors = [RED,BLUE,GREEN,PURPLE]

imageScale = (screenHeight/5, screenHeight*15/16)
redPaint = pygame.transform.scale(pygame.image.load( "Assets/img/RedPaint.png" ).convert_alpha(), imageScale)
bluePaint = pygame.transform.scale(pygame.image.load( "Assets/img/BluePaint.png" ).convert_alpha(), imageScale)
greenPaint = pygame.transform.scale(pygame.image.load( "Assets/img/GreenPaint.png" ).convert_alpha(), imageScale)
purplePaint = pygame.transform.scale(pygame.image.load( "Assets/img/PurplePaint.png" ).convert_alpha(), imageScale)


#m.importLists(avatarParams, creditsMenu, optionsList, lossMenu, instructions)	# call mainfunc's importLists function to return local lists
avatarParams = [screenWidth, screenHeight, soundToggle]

flier = avatar.Avatar(avatarParams[0], avatarParams[1], avatarParams[2])

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
		
		bools = [musicToggle, musicToggled, soundToggled, justClicked, lowRes, lowResolution]
		avatarParams = [screenWidth, screenHeight, soundToggle]
		gameState, score, counter = m.mainButtonsClicked(gameState, score, counter, bools, mainMenu, mouse, screen, clickSound, scoreLabel, avatarParams)	# relocated code to checkMainItems function


		justClicked = pygame.mouse.get_pressed()[0]
			
# -----------------------------------------------------------------------------------------

	
	elif gameState == 1: #The actual game looping part
		pygame.mouse.set_visible(False)
		
		screen.blit(imageBkg,(0,0))

		#screen.blit(grass,(0,0))
		counter += 1
		
		tempList = []
		if counter == nextBeam:
			rainbowSound.stop()
			if abs(nextBeam - nextWall) > 35: #So they don't spawn on top of each other
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
				'''
				elif difColor == ORANGE:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, orangePaint)
				elif difColor == YELLOW:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, yellowPaint)
				elif difColor == CYAN:
					myBeam = Beam(screenWidth, difColor , screenWidth, screenHeight, cyanPaint)
					'''
				if activeBeams != []:
					if myBeam.getColor() != activeBeams[-1].getColor() and myBeam.getColor() != flier.getColor():
						activeBeams.append(myBeam)
				else:
					if myBeam.getColor() != flier.getColor():
						activeBeams.append(myBeam)
			nextBeam = random.randint(low + 150, high + 180) + counter
			
		if counter == nextWall:
			if activeBeams != []:
				myWall = Wall(activeBeams[-1].getColor(), screenWidth, screenHeight, colors, obstacleList)	# create the Wall object with a certain number of obstacles
				#Last beam in the list is the closest one to the wall being created
			else:
				myWall = Wall(flier.getColor(), screenWidth, screenHeight, baseColors, obstacleList)
				
			nextWall = random.randint(low + 130, high + 160) + counter
			activeWalls.append(myWall)
			
		
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
			if item.getPosition() > -screenWidth/5:
				tempList.append(item)
				
		activeBeams = list(tempList)
		flier.beamCollision(activeBeams[:1])
		
		if flier.wallCollision(activeWalls[:1]) == True: #If passing through the wall is true
			if isPassing == False:												 # added gameState argument for rainbow testing
				m.playSound(pointSound, soundToggle)
				score += 1
				scoreLabel.updateText("Score: "+str(score))
				isPassing = True #So score is calculated once per wall
				### Changing the difficulty ###
				if score % 2 == 0:
					if low > 0:
						low -= 8
					if high > 0:
						high -= 8
				if score == 1:
					#obstacleList = preLoaded2
					obstacleList = preLoaded2.getObstacles()
				elif score == 3:
					wallSpeed = -4
				elif score == 6:
					#obstacleList = preLoaded3
					obstacleList = preLoaded3.getObstacles()

				elif score == 10:
					wallSpeed = -5
				elif score == 16:
					#obstacleList = preLoaded4
					obstacleList = preLoaded4.getObstacles()

		else:
			isPassing = False
			
# ----------------------------------------------- powerups ------------------------------------

		
		# Powerup collision handling, created one powerup for testing purposes, still need
		# \ to implement spawning

		if counter == 150:
			power_up = Powerup([screenWidth,screenHeight/2], rainbow_powerup, 'rainbow')
			activePowerUps.append(power_up)
		for item in activePowerUps:
			rainbowYvel = item.movePowerUp([wallSpeed,rainbowYvel], screen)
			if item.x < -40:
				activePowerUps.remove(item)
		
		if flier.powerUpCollision(activePowerUps, soundToggle):	# Does the avatar collide with a powerup?
			if flier.flierState == 1: 
				flier.applyRainbow()
				activeBeams = []
				nextBeam = random.randint(low + 170, high + 230) + counter
				#Play rainbow Sound
					
# ----------------------------------------------- powerups ------------------------------------

			#inputs the current score, then returns a list of all scores cut off at top 10
		scoreLabel.update(screen)
		
		fpsTest.append( clock.get_fps() )
		
		flier.update(screen) #It's a start.
		if flier.getAlive() == False: #if the flier is dead
			pygame.mixer.music.set_volume(1.0)
			quoteLabel.updateText(quoteReader.getQuote())
			activeWalls = []
			activeBeams = []
			
			wallSpeed = -3
			gameState = 5 #goto loss screen
			flier.restart(soundToggle)
			nextWall = random.randint(130, 160)
			nextBeam = 80
			low = 80
			high = 120
			obstacleList = preLoaded1.getObstacles()

			localHighScores, serverHighScores = serverConnect(host, port, score)

			for x in fpsTest:
				fpsSum+=x
				
			print fpsSum/len(fpsTest)
			fpsTest = []
			fpsSum = 0
			
			
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
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		m.State2Update(screen, instructions)	# relocated code to State2Update function
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (mainBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			m.playSound(clickSound,soundToggle)
			gameState = 0
			
# ----------------------------------------------------------------------------------------

			
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
			
# -----------------------------------------------------------------------------------------

			
	elif gameState == 4: #Quit state
		pygame.quit()
		sys.exit()
		
# -----------------------------------------------------------------------------------------
		
		
	elif gameState == 5: #Loss Screen

		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] == True:
			gameState = 1
			### Call this to restart the game and scores ###
			score = 0
			scoreLabel.updateText("Score: "+str(score))
			pygame.mixer.music.set_volume(0.4)
			counter = 0
		mouse = pygame.mouse.get_pos()
		
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
					counter, flier, score = m.restartGame(counter, score, scoreLabel, flier)	# relocated code to restartGame function

				elif gameState == 0:
				
					if musicToggle == True:
						pygame.mixer.music.load("Assets/sound/soundtrack3.mp3")
						pygame.mixer.music.play(-1)
						
					quoteLabel.updateText(quoteReader.getQuote())
				justClicked = pygame.mouse.get_pressed()[0]
				
				break
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		
# -----------------------------------------------------------------------------------------

		
	if gameState == 6: #Options menu
		screen.fill((40,80,160))
		avatarParams = [screenWidth, screenHeight, soundToggle]
		mouse = pygame.mouse.get_pos()
		bools = [musicToggle, musicToggled, soundToggled, justClicked, lowRes, lowResolution]
		avatarParams = [screenWidth, screenHeight, soundToggle]
		musicToggle, soundToggle, gameState, lowRes = m.updateSoundOptions(bools, gameState, optionsList, mouse, screen, avatarParams, clickSound)
		# relocated code to updateSoundOptions function
		resInfo.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		flier.restart(soundToggle)
	
	if gameState == 7:
		key = pygame.key.get_pressed()
		if key[pygame.K_p] == True:
			if paused == False:
				gameState = 1
				paused = True
		else:
			paused = False
			
	for event in pygame.event.get(): ##### Find out why removing this crashes the program #####
			if event.type == pygame.QUIT:
				pygame.quit() # quit the screen
				sys.exit()
				break
		
	pygame.display.update() # update the screen

	clock.tick(65) # 60 fps
