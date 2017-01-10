# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17


### This is going to be part of the Main Loop file, not it's own class ###
import pygame
import sys
import avatar
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
		if (x>=self.x - self.width/6 and x <= self.x + self.width*8/6) and (y >= self.y -self.height/4 and y <= self.y + self.height*6/4):
			if self.hoverOnce == False: # So we
				self.hoverOnce = True
				hoverSound.play()
				self.bkgColor = (self.bkgColor[0]+20,self.bkgColor[1]+20,self.bkgColor[2]+20)
			return True
		self.hoverOnce = False
		self.bkgColor = self.tempColor
		return False
		
	def getState(self):
		return self.state
	
	def update(self, screen):
		pygame.draw.rect( screen, self.bkgColor, pygame.Rect( (self.x - self.width/6, self.y-self.height/4), (self.width*8/6, self.height*6/4) ) )
		screen.blit( self.cText, (self.x, self.y) )
			
			### 0 = menu loop
			### 1 = go to game
			### 2 = Instructions
			### 3 = Credits
			### 4 = Quit Game
		
screen.fill((40,80,160)) #BKG

### Menu Items/Labels
start = MenuLabel("Start Game", "Helvetica", (100,100,100),(0,0,0),32,(300,100),1)
instruction = MenuLabel("Instructions", "Helvetica", (100,100,100),(0,0,0),32,(300,180),2)
credits = MenuLabel("Credits", "Helvetica", (100,100,100),(0,0,0),32,(300,260),3)
quit = MenuLabel("Quit", "Helvetica", (100,100,100),(0,0,0),32,(300,340),4)
list = [start, credits, quit, instruction] #Main Menu Labels

credits = MenuLabel("THE CREW", "Helvetica", (100,100,100),(0,0,0),48,(300,180),100)

#Instructions
help = MenuLabel("Press Spacebar to increase your upward speed!", "Helvetica", (100,100,100),(0,0,0),24,(300,180),100)


flier = avatar.Avatar()
while 1:#Main loop
	if gameState == 0: #Start Menu
		# handle every event since the last frame.
		screen.fill((40,80,160))
		for item in list:
			mouse = pygame.mouse.get_pos()
			if item.hover((mouse[0],mouse[1])) == True and pygame.mouse.get_pressed()[0]:
				clickSound.play()
				gameState = item.getState()
				if gameState == 1:
					flier = avatar.Avatar()
				break
			
			item.update(screen)
			
	
	elif gameState == 1: #The actual "main loop" looping part

		flier.keyPressed() # handle the keys
		flier.applyGravity() # calls the simulated gravity function of avatar
		screen.fill((255,255,255))# white background on the screen
		#Create an iterator here to move each object/obstacle
		
		flier.update(screen) # updates the position of the avatar on the screen
	
		if flier.getAlive() == False:
			print "You Crashed!"
			gameState = 0
			
	
	elif gameState == 2:
		screen.fill((40,80,160))
		help.update(screen)
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE]:
			gameState = 0
			
	elif gameState == 3:
		screen.fill((40,80,160))
		credits.update(screen)
		key = pygame.key.get_pressed()
		if key[pygame.K_BACKSPACE]:
			gameState = 0
			
	elif gameState == 4:
		pygame.quit()
		sys.exit()
		
	for event in pygame.event.get(): ##### Find out why removing this crashes the program #####
			if event.type == pygame.QUIT:
				pygame.quit() # quit the screen
				sys.exit()
				break
				
	pygame.display.update() # update the screen

	clock.tick(60) # 60 fps
