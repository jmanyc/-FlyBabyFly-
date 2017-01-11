# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Beam():

	def __init__(self, position, color, width, height, speed):
	
		self.position = position
		self.x = self.position[0]
		self.y = self.position[1]
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
        
	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.beam)
		
	def moveBeam(self, speed, surface):

		surface.fill((255, 255, 255), self.beam)	# fill a surface with the obstacle on a white background
		self.beam.move_ip(self.speed, 0)	# change the object's internal position

		self.draw(surface)    # redraw the obstacle at its new position on the display
		
		
# ------------- Test code ----------------------------------------------------------------
		
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

	myBeam.moveBeam(-5, screen)	# move the obstacle leftwards
	
	pygame.display.update([myBeam.beam]) # update the location of the obstacle on the screen
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print "terminating"
			sys.exit()
			break
	clock.tick(60) # 60 fps
