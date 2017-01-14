#MenuLabel class for adding labels to a pygame menu, useful for changing gamestates
#Checks for hovering over a button
#Don't set background color over 235

import pygame

class MenuLabel():
	def __init__(self, text, bkgColor, fontColor, fontSize, (x,y), state):
		### Storing all the important text information ###
		self.hoverSound = pygame.mixer.Sound( "Assets/sound/click.wav" )
		#Text Part#
		self.fontSize = fontSize
		self.cFont = pygame.font.Font("Assets/font/dizzyedge.otf",fontSize)
		self.fontColor = fontColor
		
		self.text = text
		self.cText = self.cFont.render( self.text, True, self.fontColor)
		
		#Height and width of the text
		self.width = self.cText.get_rect().width
		self.height = self.cText.get_rect().height
		
		#Color of the rectangle, and dealing with hover/state
		self.bkgColor = bkgColor
		self.tempColor = bkgColor #Backup color for when we change it on hover
		self.x = x - self.width/2
		self.y = y
		self.hoverOnce = False
		self.isHover = False
		self.state = state #Right now, a number giving a gamestate variable
		
	def hover(self, (x,y),soundToggle):
		### Used to tell if the cursor is hovering over a button ###
		if (x>=self.x - self.width/8 and x <= self.x + self.width*9/8) and (y >= self.y -self.height/4 and y <= self.y + self.height*5/4):
            ### Creates a box that checks if the inputted coords are inside this box's space ###
			if self.hoverOnce == False:#So sound and bkgColor are only changed once per hover
				self.hoverOnce = True
				if soundToggle == True:
					self.hoverSound.play()
				self.bkgColor = (self.bkgColor[0]+20,self.bkgColor[1]+20,self.bkgColor[2]+20)
                # Yes, this can cause issues if you pick any color above 235... So don't do that, less operations this way
			self.isHover = True
			return True
		self.isHover = False
		self.hoverOnce = False
		self.bkgColor = self.tempColor
		return False
		
	def updateText(self, text):
		self.cText = self.cFont.render( text, True, self.fontColor)
		self.width = self.cText.get_rect().width
		self.height = self.cText.get_rect().height
		
	def getState(self):
		### Returns the gameState the button points to ###
		return self.state
	
	def update(self, screen):
		### Draws the shadow, then the rectangle, then the text onto the screen ###
		if self.isHover == True:
			pygame.draw.rect( screen, (255,255,255), pygame.Rect( (self.x - self.width/8 + 7, self.y-self.height/4 + 7), (self.width*10/8, self.height*6/4) ) ) #box-Shadow
		else:
			pygame.draw.rect( screen, (0,0,0), pygame.Rect( (self.x - self.width/8 + 7, self.y-self.height/4 + 7), (self.width*10/8, self.height*6/4) ) ) #box-Shadow
		pygame.draw.rect( screen, self.bkgColor, pygame.Rect( (self.x - self.width/8, self.y-self.height/4), (self.width*10/8, self.height*6/4) ) )
		screen.blit( self.cText, (self.x, self.y) )