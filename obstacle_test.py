# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys
from obstacles import Obstacle

# ------------- Test code ----------------------------------------------------------------
		
pygame.init()
screen = pygame.display.set_mode((800, 600))


# color options 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

myObstacle = Obstacle([500, 500], BLUE, 40, 280, -5)	# create the obstacle object

clock = pygame.time.Clock()	# initialize pygame's internal clock
screen.fill((255,255,255))	# fill the screen with a white background


myObstacle.draw(screen)	# draw the obstacle to the screen
print "entering main loop"

while 1: #Main loop

	myObstacle.moveObs(-5, screen)	# move the obstacle leftwards
	
	pygame.display.update([myObstacle.obstacle]) # update the location of the obstacle on the screen
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print "terminating"
			sys.exit()
			break
	clock.tick(60) # 60 fps