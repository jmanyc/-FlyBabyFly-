# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17
import pygame
from wall import Wall
from powerups import Powerup

def enum(**enums):
		return type('Enum', (), enums)
Colors = enum(RED = (255,0,0), GREEN = (0,255,0), BLUE = (0,0,255), WHITE = (255,255,255))

class Avatar(): 
	def __init__(self, screenWidth, screenHeight, soundToggle):
		
		self.soundToggle = soundToggle
		self.crashSound = pygame.mixer.Sound( "Assets/sound/hit_obstacle.wav" )
		self.hitGround = pygame.mixer.Sound( "Assets/sound/hit_ground.wav" )
		self.paintSound = pygame.mixer.Sound( "Assets/sound/paintsplash_sound16.wav" )
		self.x = screenWidth/12 # initial spawn of the image
		self.y = screenHeight/4
		self.startingPos = (self.x,self.y)
		
		### Starts with white Image ###
		self.imageScale = (screenHeight/9, screenHeight/9)
		
		self.flierState = 0

		#Preloading the different colors of the squirrel
		self.whiteImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhitePlane.png" ).convert_alpha(), self.imageScale)
		self.redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRedPlane.png" ).convert_alpha(), self.imageScale)
		self.blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelBluePlane.png" ).convert_alpha(), self.imageScale)
		self.greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelGreenPlane.png" ).convert_alpha(), self.imageScale)
		self.purpleImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelPurplePlane.png" ).convert_alpha(), self.imageScale)
		
		self.image = self.whiteImage
		self.tempImage = self.image
		#for testing collision
		self.image_c = self.image.get_rect()
		
		### Setting the upper and lower limits so it stays on screen ###
		self.topLimit = screenHeight*3/32 - self.image.get_height()*2/7 #Adjusting for squirrel hitbox
		self.bottomLimit = screenHeight*15/16 - self.image.get_height()*5/7
		self.curSpeed = 0 #current speed of the avatar
		self.gravity = 0.09 #the gravity setting on the avatar, remember this number is added to the speed every tick, so 60 times a second
		self.alive = True #Used to control the gameState
		self.color = Colors.WHITE #Will be used to check collision, and change avatar image to correct color
		self.crashing = False #Used to animate the crashing of the avatar

	def keyPressed(self):
		### if a key is pressed we check if it's the up or space bar and add to the speed, double the gravity value ###
		if self.y > self.topLimit and self.crashing == False:
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]:
				self.curSpeed += self.gravity*2.5
		else:
			if self.crashing == False: #The squirrel bonks his head on the gutter and falls
				if self.soundToggle == True:
					self.crashSound.play()
				self.crash()
				
	def restart(self):
		self.x = self.startingPos[0]
		self.y = self.startingPos[1]
		self.alive = True #Used to control the gameState
		self.color = Colors.WHITE #Will be used to check collision, and change avatar image to correct color
		self.crashing = False #Used to animate the crashing of the avatar
		self.image = self.whiteImage
		self.tempImage = self.image
		
	def crash(self):
		self.curSpeed = 0
		self.crashing = True
		
	def applyGravity(self):
		### This line of code should be run in the main loop as every tick it moves the position of the avatar ###
		if self.y < self.bottomLimit:
			self.curSpeed -= self.gravity
			self.y -= self.curSpeed
		else:
			if self.soundToggle == True:#If the squirrel hits the ground
				#dust animation
				self.crash()
				self.hitGround.play()
			self.alive = False
			
	def setColor(self, color):
		### Sets the variable color of the avatar, once we have images we can also make this change the image to the correct color ###
		self.color = color
		
	def getColor(self) :
		return self.color

	def getAlive(self):
		### Returns the state of the avatar ###
		return self.alive
		
	def setCrashing(self, bool):
		### For use in collision, so after colliding with a block the flier falls, then dies ###
		self.crashing == True
		
	def setAlive(self, bool):### Note to team, make sure if we add restarts to set avatar alive again ###
		### Sets the alive state of the avatar ###
		self.alive = bool

	def update(self, surface):
		### Draws the avatar at the selected area ###
		surface.blit(self.image,(self.x,self.y))
		self.image = self.tempImage
		self.image_c = self.image.get_rect()
		self.image_c.move_ip(self.x,self.y)
		self.image_c.inflate_ip(self.image.get_width()*-2,self.image.get_height()*-2/7)

	def applyRotation(self):
		angle = self.curSpeed*3.5
		orig_rect = self.image.get_rect()
		rotated_image = pygame.transform.rotate(self.image, angle)
		rotated_rect = orig_rect.copy()
		rotated_rect.center = rotated_image.get_rect().center #Makes sure our new image is centered after rotation
		self.image = rotated_image.subsurface(rotated_rect).copy()
		

	def getPosition(self):
		return self.x + screenWidth/12 # Talk to austin about this
		
	###def setAvatar(self, image):	  Idea for later
	
	def wallCollision(self, activeWalls, soundToggle):
	### Returns true for correct collision, false for incorrect ###
		for wall in activeWalls:
			for obst in wall.getWallSections():
				if obst.getVisited() == False:
					if self.image_c.colliderect(obst.getObstacle()) == True:
						obst.setVisited(True)
						if self.color != obst.getColor():
							self.crashing = True
							self.crash()
							if self.soundToggle == True:
								self.crashSound.play()
							return False
						else:
							return True



	def beamCollision(self,activeBeams, soundToggle):					
		for beam in activeBeams:
			if beam.getVisited() == False:
				if self.image_c.colliderect(beam.getBeam()) == True:
					self.color = beam.getColor()
					if soundToggle == True:
						self.paintSound.play()
					beam.setVisited(True)
					if self.color == (255,0,0): #Red
						self.image = self.redImage
					elif self.color == (0,0,255): #Blue
						self.image = self.blueImage
					elif self.color == (0,255,0): #Green
						self.image = self.greenImage
					elif self.color == (255,0,255): #Purple
						self.image = self.purpleImage
					self.tempImage = self.image
					self.applyRotation()
 						
	def applyRainbow(self):
		return
	
	
	def applyGravitySwitch(self):
		return
		
		
	def powerUpCollision(self, powerUp):	# powerUpCollision checked in gameState 1 loop, calls
		type = powerUp.getType()			# \ appropriate power up method from powerups file

		#if self.image_c.colliderect(beam.getBeam()) == True:
		
		if type == 'rainbow':
			self.applyRainbow()
		elif type == 'gravity Switch':
			self.applyGravitySwitch()
