# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17
import pygame
from wall import Wall
def enum(**enums):
		return type('Enum', (), enums)
Colors = enum(RED = (255,0,0), GREEN = (0,255,0), BLUE = (0,0,255))

class Avatar(): 
	def __init__(self, screenWidth, screenHeight, soundToggle):
		self.infoObject = pygame.display.Info()
		self.soundToggle = soundToggle
		self.crashSound = pygame.mixer.Sound( "Assets/sound/hit_obstacle.wav" )


		### Starts with Red Image ###
		self.imageScale = (screenWidth/17, screenHeight/10)
		self.image = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelWhitePlane.png" ).convert_alpha(), self.imageScale)
		self.tempImage = self.image
		#for testing collision
		self.image_c = self.image.get_rect()

		self.redImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelRedPlane.png" ).convert_alpha(), self.imageScale)
		self.blueImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelBluePlane.png" ).convert_alpha(), self.imageScale)
		self.greenImage = pygame.transform.scale(pygame.image.load( "Assets/img/SquirrelGreenPlane.png" ).convert_alpha(), self.imageScale)
		
		self.image_c = self.image.get_rect()	#
		self.x = screenWidth/12 # initial spawn of the image
		self.y = screenHeight/4
		
		### Setting the upper and lower limits so it stays on screen ###
		self.topLimit = screenHeight*3/32 - self.image.get_height()*2/7
		self.bottomLimit = screenHeight*15/16 - self.image.get_height()*5/7
		self.curSpeed = 0 #current speed of the avatar
		self.gravity = 0.19 #the gravity setting on the avatar, remember this number is added to the speed every tick, so 60 times a second
		self.alive = True #Used to control the gameState
		self.color = Colors.RED #Will be used to check collision, and change avatar image to correct color
		self.crashing = False #Used to animate the crashing of the avatar

	def keyPressed(self):
		### if a key is pressed we check if it's the up or space bar and add to the speed, double the gravity value ###
		if self.y > self.topLimit and self.crashing == False:
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]:
				self.curSpeed += self.gravity*2.5
			### Color of Avatar changed depending on arrow key pressed & image swapped out ###
			if key[pygame.K_1] :
				self.color = Colors.RED
				self.image = self.redImage
			if key[pygame.K_2] :
				self.color = Colors.GREEN
				self.image = self.greenImage
			if key[pygame.K_3] :
				self.color = Colors.BLUE
				self.image = self.blueImage
			self.tempImage = self.image
		else:
			if self.crashing == False: #As we haven't changed it yet, this way we do it only once and the falling is smooth
				if self.soundToggle == True:
					self.crashSound.play()
				self.curSpeed = 0
			self.crashing = True
		
	def applyGravity(self):
		### This line of code should be run in the main loop as every tick it moves the position of the avatar ###
		if self.y < self.bottomLimit:
			self.curSpeed -= self.gravity
			self.y -= self.curSpeed
		else:
			if self.soundToggle == True:
				self.crashSound.play()
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

	def applyRotation(self):
		angle = self.curSpeed*3.5
		orig_rect = self.image.get_rect()
		rot_image = pygame.transform.rotate(self.image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		self.image = rot_image.subsurface(rot_rect).copy()
		

	def getPosition(self):
		return self.x + screenWidth/12 # Talk to austin about this
		
	###def setAvatar(self, image):	  Idea for later
	
 	def checkCollision(self, activeWalls, activeBeams = None):
 		'''
 			method for collision detection. Takes in 2 lists: activeObstacles and 
 		'''
 		for wall in activeWalls:
 			
 			for obst in wall.getWallSections():
 				if obst.getVisited() == False:
 					if self.image_c.colliderect(obst.getObstacle()) == True:
 						print "COLLISION"
 						if self.color != obst.getColor():
 							self.crashing =True
 						else:
 							obst.setVisited(True)
 							return True
 						return False
 						
 					

 		
 				
 
 		
		
				
		
		
##### Test code, copied and edited from source #####
if __name__ == "__main__":




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



	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	avatar = Avatar(800,600,True)

	heights = []	# put the heights of the three blocks in a list (in the main loop the section
	heights.extend([150, 150, 150]) # \ heights will vary while the wall sections remain adjacent)
	myWall = Wall(BLUE, screen.get_width(), screen.get_height(),colors)	# create the Wall object
	activeWalls = []
	activeWalls.append(myWall)
	print len(activeWalls)
	clock = pygame.time.Clock()

	while 1:#Main loop
		# handle every event since the last frame.
		avatar.keyPressed() # handle the keys
		avatar.applyGravity() # calls the simulated gravity function of avatar
		
		screen.fill((255,255,255))# white background on the screen
		myWall.moveWall(-5, screen)	# move the obstacle leftwards
		avatar.checkCollision(activeWalls)


		avatar.update(screen) # updates the position of the avatar on the screen
		pygame.display.update() # update the screen
		
		if avatar.getAlive() == False:
			print "You Crashed!"
			pygame.quit()#Quit the game
			break
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()#Quit the game
				break
		clock.tick(60) # 60 fps
