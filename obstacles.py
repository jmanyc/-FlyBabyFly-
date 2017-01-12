# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Obstacle():

	def __init__(self, position, color, width, height):
	
		self.position = position
		self.x = self.position[0]
		self.y = self.position[1]
		self.color = color
		self.height = height
		self.width = width
		self.obstacle = pygame.Rect((self.x,self.y), (self.width, self.height))
		self.visited = False
		
	def setPosition(self, position):
		self.position = position
		
	def getXPosition(self):
		return self.x
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.obstacle)
		
	def getObstacle(self):
		return self.obstacle

	def getVisited(self):
		return self.visited

	def setVisited(self, state):
		self.visited = state
				
	def moveObs(self, speed, surface):

		#surface.fill((255, 255, 255), self.obstacle)	# fill a surface with the obstacle on a white background
		#pygame.draw.rect(surface, (255, 255, 255), self.obstacle)
		self.obstacle.move_ip(speed, 0)	# change the object's internal position
		self.x += speed
		#self.draw(surface)    # redraw the obstacle at its new position on the display