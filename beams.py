# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Beam():

	def __init__(self, position, color, screenWidth, screenHeight): #Work on this
		
		self.x = position
		self.y = 0
		self.color = color

		self.screenHeight = screenHeight
		self.screenWidth = screenWidth
		
		self.imageScale = (screenWidth/6, screenHeight) # This needs tweaking, should be 5.5
		
		if self.color == (255,0,0): #Red
			self.image = pygame.transform.scale(pygame.image.load( "Assets/img/RedPaint.png" ).convert_alpha(), self.imageScale)
		elif self.color == (0,0,255): #Blue
			self.image = pygame.transform.scale(pygame.image.load( "Assets/img/BluePaint.png" ).convert_alpha(), self.imageScale)
		elif self.color == (0,255,0): #Green
			self.image = pygame.transform.scale(pygame.image.load( "Assets/img/GreenPaint.png" ).convert_alpha(), self.imageScale)
		self.beam = self.image.get_rect()
		
		
	def getPosition(self):
		return self.x
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color
        
	def draw(self, surface):
		#pygame.draw.rect(surface, self.color, self.beam)
		surface.blit(self.image,(self.x,self.y))

	def getBeam(self):
		#returns this Beam object's Rect defined in self.beam
		return self.beam

		
	def moveBeam(self, speed, surface):
		self.beam.move_ip(speed, 0)	# change the object's internal position
		self.x += speed
		self.draw(surface)    # redraw the obstacle at its new position on the display
		
		
# ------------- Test code ----------------------------------------------------------------
'''
pygame.init()
screen = pygame.display.set_mode((800, 600))


# color options 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

myBeam = Beam([500, 300], BLUE, 40, 800, -5)	# create the obstacle object

clock = pygame.time.Clock()	# initialize pygame's internal clock
screen.fill((255,255,255))	# fill the screen with a white background


myBeam.draw(screen)	# draw the obstacle to the screen
print "entering main loop"

while 1: #Main loop
	print clock.get_fps()
	myBeam.moveBeam(-5, screen)	# move the obstacle leftwards
	
	#pygame.display.update([myBeam.beam]) # update the location of the obstacle on the screen
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print "terminating"
			sys.exit()
			break
	clock.tick(60) # 60 fps
'''