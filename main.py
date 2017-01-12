# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17


### This is going to be part of the Main Loop file, not it's own class ###
import pygame
import sys
import avatar
from wall import Wall
from label import MenuLabel
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
title = MenuLabel("Fly Baby, Fly", "Comic Sans MS", (100,100,100),(255,105,180),42,(300,100),100)
start = MenuLabel("Start Game", "Comic Sans MS", (100,100,100),(255,255,0),26,(300,200),1)
instruction = MenuLabel("Instructions", "Comic Sans MS", (100,100,100),(255,153,0),26,(300,280),2)
options = MenuLabel("Options", "Comic Sans MS", (100,100,100),(0,0,0),26,(300,360),6)
mainQuit = MenuLabel("Quit", "Comic Sans MS", (100,100,100),(0,0,0),26,(300,440),4)
mainMenu = [start, mainQuit, instruction, options] #Main Menu Labels

#Credits
Producer = MenuLabel("He's a People Person (Producer): Chris Marcello", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8), 100)
Designer = MenuLabel("Man with Vision (Designer): James Lindberg", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 70), 100)
Programmer = MenuLabel("Hackerman (Lead Programmer): Lucas DeGraw", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 140), 100)
Artist = MenuLabel("Frida Kahlo + GIMP (Lead Artist): Riley Karp", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 210), 100)
Sound = MenuLabel("Mariachi (Lead Sound Design): Jerry Diaz ", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 280), 100)
Gamer = MenuLabel("Gamer (Quality Assurance): Austin Nantkees", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 350), 100)
Knife = MenuLabel("Swiss Army Knife (Multirole): Jon", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 420), 100)
DJ = MenuLabel("DJ (Art Assistance): Dean", "Comic Sans MS", (100,100,100),(0,0,0), 26, (screenWidth/2, screenHeight/8 + 490), 100)
Bruce = MenuLabel("Special Thanks to: Bruce (Totally Not CIA) Maxwell","Comic Sans MS",(100,100,100),(0,0,0),26,(screenWidth/2, screenHeight/8 + 560),100)

lossBack = MenuLabel("Back", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth*8/9,screenHeight/15),5)
creditsMenu = [Producer, Designer, Programmer, Artist, Sound, Gamer, Knife, DJ, Bruce, lossBack]

#Instructions
paint = MenuLabel("Paint streams will change your plane's color", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth/2,screenHeight*2/7),100)
help = MenuLabel("Go through the color block that matches your plane", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth/2,screenHeight*3/7),100)
controls = MenuLabel("Press Spacebar to increase your upward speed!", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth/2,screenHeight*4/7),100)
mainBack = MenuLabel("Back", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth*6/7,screenHeight/15),0)

#Options Menu
musicToggled = MenuLabel("Background Music On/Off", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth/2,screenHeight*2/7),42)
soundToggled = MenuLabel("Sound Effects On/Off", "Comic Sans MS", (100,100,100),(0,0,0),24,(screenWidth/2,screenHeight*3/7), 43)
optionsList = [mainBack, musicToggled, soundToggled]

#Loss Screen
credits = MenuLabel("Credits", "Comic Sans MS", (100,100,100),(0,0,0),26,(300,260),3)
restart = MenuLabel("Retry!", "Comic Sans MS", (100,100,100),(0,0,0),26,(300,100),1)
main = MenuLabel("Main Menu", "Comic Sans MS", (100,100,100),(0,0,0),26,(300,180),0)
lossQuit = MenuLabel("Quit", "Comic Sans MS", (100,100,100),(0,0,0),26,(300,340),4)
lossMenu = [restart, credits, lossQuit, main]

### Initializing Main Loop variables and images ###
squirrel = pygame.image.load( "Assets/img/squirrelPilot.png" ).convert_alpha()
imageBkg = pygame.transform.scale(pygame.image.load( "Assets/img/HouseNoGrass.png" ).convert(),(screenWidth,screenHeight))
grass = pygame.transform.scale(pygame.image.load("Assets/img/Grass.png").convert_alpha(),(screenWidth/3,screenHeight))
### Check if it's the right grass file ###

justClicked = False #Boolean so we can't double click options in the menu
counter = 0
objectList = []
grassList = []

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
###colors = [RED,BLUE,GREEN]


while 1:#Main loop
	if gameState == 0: #Start Menu
		# handle every event since the last frame.
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
		screen.blit(squirrel,(500,50))
		title.update(screen)
		for item in mainMenu:
			if item.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
			
				# If hovering over the item, and a button is clicked, go to the state the button is linked to.
				if soundToggle == True:
					clickSound.play()
				gameState = item.getState()
				
				if gameState == 1: #If you add anything to this if statement, add it to the retry menu too
					pygame.mixer.music.set_volume(0.4)
					# Reseting the avatar game, had to call it flier because naming it avatar, along with the avatar file was messy
					counter = 0
					flier = avatar.Avatar(screenWidth, screenHeight,soundToggle)
				break
			
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
			
	
	elif gameState == 1: #The actual game looping part
		pygame.mouse.set_visible(False)
		screen.blit(imageBkg,(0,0))
		#screen.blit(grass,(0,0))
		counter+=1
		tempList = []
		
		if counter % 200 == 0:
			myWall = Wall(BLUE, screenWidth, screenHeight, colors)	# create the Wall object
			#bottomGrass = grass
			objectList.append(myWall)
			#grassList.append(bottomGrass)
			
		flier.keyPressed() # handles pressing keys, now if we need to speed up our program work on this
		flier.applyGravity() # calls the simulated gravity function of avatar
		#screen.fill((255,255,255))# white background on the screen
		
		#Create an iterator here to move each object, and stop drawing the ones that go off-screen
		for item in objectList:# This will just be a wall list, since it calls moveWall.
			item.moveWall(-4, screen)
			if item.getX() > -screenWidth/28:
				tempList.append(item)
				### If performance becomes an issue, check into forcing all update at once, instead of staggered
		
		#for item in grassList:
			#item.move_ip(-4,0)
		objectList = tempList
		
		flier.update(screen)
	
		if flier.getAlive() == False: #if the flier is dead
			pygame.mixer.music.set_volume(1.0)
			objectList = []
			pygame.mouse.set_visible(True)
			gameState = 5 #goto loss screen 
		#print clock.get_fps() #Prints out the fps during the game for testing
			
	
	elif gameState == 2: #Instructions
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		help.update(screen)
		controls.update(screen)
		mainBack.update(screen)
		paint.update(screen)
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (mainBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			if soundToggle == True:
				clickSound.play()
			gameState = 0
			
			
	elif gameState == 3: #Credits
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		
		for item in creditsMenu:
			item.update(screen)
			
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE] or (lossBack.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0]):
			#If back button is clicked, go back to loss screen
			if soundToggle == True:
				clickSound.play()
			gameState = 5
			screen.fill((40,80,160))
			
	elif gameState == 4: #Quit state
		pygame.quit()
		sys.exit()
		
	elif gameState == 5: #Loss Screen
		
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
		for item in lossMenu:
			if item.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
				if soundToggle == True:
					clickSound.play()
				gameState = item.getState()
				
				if gameState == 1:
					pygame.mixer.music.set_volume(0.4)
					# Reseting the avatar game, had to call it flier because naming it avatar, along with the avatar file was messy
					counter = 0
					flier = avatar.Avatar(screenWidth, screenHeight,soundToggle)
				justClicked = pygame.mouse.get_pressed()[0]
				
				break
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		
	if gameState == 6: #Options menu
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos()
		for item in optionsList:
			if item.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
				
				clickedState = item.getState()
				
				if clickedState == 42: #Music Toggle
					if musicToggle == True:
						pygame.mixer.music.pause()
						musicToggle = False
					else:
						pygame.mixer.music.unpause()
						musicToggle = True
				elif clickedState == 43: #Sound Toggle
					if soundToggle == True:
						soundToggle = False
					else:
						soundToggle = True
				elif clickedState == 0:
					gameState = 0
				if soundToggle == True:
					clickSound.play()
			item.isHover = False
			item.update(screen)
		if musicToggle == True:
			musicToggled.isHover = True
			musicToggled.update(screen)
		if soundToggle == True:
			soundToggled.isHover = True
			soundToggled.update(screen)
			
		justClicked = pygame.mouse.get_pressed()[0]
		
	for event in pygame.event.get(): ##### Find out why removing this crashes the program #####
			if event.type == pygame.QUIT:
				pygame.quit() # quit the screen
				sys.exit()
				break
				
	pygame.display.update() # update the screen

	clock.tick(60) # 60 fps
