# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys
from wall import Wall

# ------------- Wall Test Code -----------------------------------------------------------
		
pygame.init()	# initialize pygame
screen = pygame.display.set_mode((800, 600))	# initialize the display surface

# set color options 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)

heights = []	# put the heights of the three blocks in a list (in the main loop the section
heights.extend([150, 150, 150]) # \ heights will vary while the wall sections remain adjacent)
myWall = Wall(BLUE, [500, 125], [500, 275], [500,425], RED, GREEN, BLUE, heights)	# create the Wall object

clock = pygame.time.Clock()	# initialize pygame's internal clock
screen.fill((255,255,255))	# fill the screen with a white background
#pygame.display.update()


#myWall.draw(screen)	# draw the obstacle to the screen
print "entering main loop"

while 1: #Main loop

	myWall.moveWall(-5, screen)	# move the obstacle leftwards
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print "terminating"
			sys.exit()
			break
	clock.tick(60) # 60 fps