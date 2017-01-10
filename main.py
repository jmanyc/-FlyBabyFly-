# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17


### This is going to be part of the Main Loop file, not it's own class ###
import pygame
import sys
import avatar
from time import sleep

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
#Call the mixer_init and mixer.pre_init before pygame every time

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
hoverSound = pygame.mixer.Sound( "click.wav" )
clickSound = pygame.mixer.Sound( "pop.wav" )
gameState = 0
class MenuLabel():
	def __init__(self, text, font, bkgColor, fontColor, fontSize, (x,y), state):
		### Storing all the important text information ###
		
		#Text Part#
		self.fontSize = fontSize
		self.font = font
		self.cFont = pygame.font.SysFont( self.font, self.fontSize, bold=True )
		
		self.text = text
		self.cText = self.cFont.render( self.text, True, fontColor )
		
		#Height and width of the text
		self.width = self.cText.get_rect().width
		self.height = self.cText.get_rect().height
		
		#Color of the rectangle
		self.bkgColor = bkgColor
		self.tempColor = bkgColor #Backup color for when we change it on hover
		self.x = x - self.width/2
		self.y = y
		self.hoverOnce = False
		self.state = state #Right now, a number giving a gamestate variable
		
	def hover(self, (x,y)):
		### Used to tell if the cursor is hovering over a button ###
		if (x>=self.x - self.width/6 and x <= self.x + self.width*7/6) and (y >= self.y -self.height/4 and y <= self.y + self.height*5/4):
            ### Creates a box that checks if the inputted coords are inside this box's space ###
			if self.hoverOnce == False: # So we
				self.hoverOnce = True
				hoverSound.play()
				self.bkgColor = (self.bkgColor[0]+20,self.bkgColor[1]+20,self.bkgColor[2]+20)
                # Yes, this can cause issues if you pick any color above 235... So don't do that, less operations this way
			return True
		self.hoverOnce = False
		self.bkgColor = self.tempColor
		return False
		
	def getState(self):
		return self.state
	
	def update(self, screen):
		pygame.draw.rect( screen, (0,0,0), pygame.Rect( (self.x - self.width/8, self.y-self.height/8), (self.width*8/6, self.height*6/4) ) )
		pygame.draw.rect( screen, self.bkgColor, pygame.Rect( (self.x - self.width/6, self.y-self.height/4), (self.width*8/6, self.height*6/4) ) )
		screen.blit( self.cText, (self.x, self.y) )
			
			### 0 = menu loop
			### 1 = go to game
			### 2 = Instructions
			### 3 = Credits
			### 4 = Quit Game
		
screen.fill((40,80,160)) #BKG

### Menu Items/Labels ###
# varName = MenuLable("Text", "Font-Style", BkgColor of Box, Text Color, fontSize, Position, gamestate it points to)

#Main Menu
start = MenuLabel("Start Game", "Helvetica", (100,100,100),(0,0,0),32,(300,100),1)
instruction = MenuLabel("Instructions", "Helvetica", (100,100,100),(0,0,0),32,(300,180),2)
credits = MenuLabel("Credits", "Helvetica", (100,100,100),(0,0,0),32,(300,260),3)
quit = MenuLabel("Quit", "Helvetica", (100,100,100),(0,0,0),32,(300,340),4)
mainMenu = [start, credits, quit, instruction] #Main Menu Labels

#Credits
cast = MenuLabel("THE CREW", "Helvetica", (100,100,100),(0,0,0),48,(300,180),100)

#Instructions
help = MenuLabel("Press Spacebar to increase your upward speed!", "Helvetica", (100,100,100),(0,0,0),24,(320,180),100)
back = MenuLabel("Backspace to go back", "Helvetica", (100,100,100),(0,0,0),24,(400,80),100)

#Loss Screen
restart = MenuLabel("Retry!", "Helvetica", (100,100,100),(0,0,0),32,(300,100),1)
main = MenuLabel("Main Menu", "Helvetica", (100,100,100),(0,0,0),32,(300,180),0)
lossMenu = [restart, credits, quit, main]


justClicked = False #Boolean so we can't double click options in the menu
flier = avatar.Avatar()
while 1:#Main loop
	if gameState == 0: #Start Menu
		# handle every event since the last frame.
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
		
		for item in mainMenu:
			if item.hover((mouse[0],mouse[1])) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
				clickSound.play()
				gameState = item.getState()
				if gameState == 1:
					# Reseting the avatar game, had to call it flier because naming it avatar, along with the avatar file was messy
					flier = avatar.Avatar()
				break
			
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
			
	
	elif gameState == 1: #The actual game looping part

		flier.keyPressed() # handles pressing keys, now if we need to speed up our program work on this
		flier.applyGravity() # calls the simulated gravity function of avatar
		screen.fill((255,255,255))# white background on the screen
		#Create an iterator here to move each object/obstacle
		
		flier.update(screen) # updates the position of the avatar on the screen
	
		if flier.getAlive() == False:
			print "You Crashed!"
			gameState = 5 #goto loss screen 
			
	
	elif gameState == 2: #Instructions
		screen.fill((40,80,160))
		help.update(screen)
		back.update(screen)
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE]:
			clickSound.play()
			gameState = 0
			
	elif gameState == 3: #Credits
		screen.fill((40,80,160))
		cast.update(screen)
		back.update(screen)
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE]:
			clickSound.play()
			gameState = 0
			
	elif gameState == 4: #Quit
		pygame.quit()
		sys.exit()
		
	elif gameState == 5: #Loss Screen
		screen.fill((40,80,160))
		mouse = pygame.mouse.get_pos() # Position of the mouse, gets refreshed every tick
		for item in lossMenu:
			if item.hover((mouse[0],mouse[1])) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
				clickSound.play()
				gameState = item.getState()
				if gameState == 1:
					# Reseting the avatar game, had to call it flier because naming it avatar, along with the avatar file was messy
					flier = avatar.Avatar()
				justClicked = pygame.mouse.get_pressed()[0]
				
				break
			item.update(screen)
		justClicked = pygame.mouse.get_pressed()[0]
		
	for event in pygame.event.get(): ##### Find out why removing this crashes the program #####
			if event.type == pygame.QUIT:
				pygame.quit() # quit the screen
				sys.exit()
				break
				
	pygame.display.update() # update the screen

	clock.tick(60) # 60 fps
