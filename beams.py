class Beams():

	def __init__(self, position, color, height, width, speed):
		self.position = position
		self.x = position[0]
		self.y = position[1]
		self.color = color
		self.speed = speed
		self.height = height
		self.width = width
		self.beam = pygame.Rect((self.x-self.width/2,self.y-self.height/2), (self.width, self.height))

		
	def setPosition(self, position):
		self.position = position
		
	def getPosition(self):
		return self.position
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color
	
# this update method will work if we use an image for the beam, otherwise, we need a differetn update method
#     def update(self, surface):
#         ### Draws the beam at the selected area ###
#         surface.blit(self.beam,(self.x,self.y))

# moveObs is incomplete
	
    	def moveObs(self, speed):
    		def moveObs(self, speed, surface):

		self.x += self.speed
		self.obstacle.move(self.x, 0)
		#self.obstacle.draw(surface)
		#pygame.draw.(surface)
		self.draw(surface)
