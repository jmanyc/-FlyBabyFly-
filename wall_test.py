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

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
MAROON = (128,0,0)
OLIVE = (128,128,0)
colors = [RED, BLUE, GREEN, YELLOW, PURPLE, CYAN, MAROON, OLIVE] ### For current game, only BLUE RED GREEN

heights = []	# put the heights of the three blocks in a list (in the main loop the section
heights.extend([150, 150, 150]) # \ heights will vary while the wall sections remain adjacent)
myWall = Wall(BLUE, 800, 600, colors)	# create the Wall object

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