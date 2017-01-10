# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys
from wall import Wall

# ------------- Wall Test Code -----------------------------------------------------------
		
pygame.init()
screen = pygame.display.set_mode((800, 600))

# color options 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

heights = []
heights.extend([150, 150, 150])
myWall = Wall(BLUE, [500, 125], [500, 275], [500,425], RED, GREEN, BLUE, heights, -5)	# create the Wall object

clock = pygame.time.Clock()	# initialize pygame's internal clock
screen.fill((255,255,255))	# fill the screen with a white background


myWall.draw(screen)	# draw the obstacle to the screen
print "entering main loop"

while 1: #Main loop

	myWall.moveWall(-10, screen)	# move the obstacle leftwards
	
#	pygame.display.update([myObstacle.obstacle]) # update the location of the obstacle on the screen
	#myWall.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print "terminating"
			sys.exit()
			break
	clock.tick(60) # 60 fps