# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Obstacle():

	def __init__(self, position, color, width, height, image):
	
		self.position = position
		self.x = self.position[0]
		self.y = self.position[1]
		self.color = color
		self.height = height
		self.width = width
		self.visited = False
		self.image = image
		
		self.obstacle = self.image.get_rect()
		self.obstacle.move_ip(self.x,self.y)
		
	def setPosition(self, position):
		self.position = position
		
	def getXPosition(self):
		return self.x
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color
		
	def draw(self, surface):
		surface.blit(self.image,(self.x,self.y))
		#pygame.draw.rect(surface, self.color, self.obstacle)
		
	def getObstacle(self):
		return self.obstacle

	def getVisited(self):
		return self.visited

	def setVisited(self, state):
		self.visited = state
				
	def moveObs(self, speed, surface):
		self.obstacle.move_ip(speed, 0)	# change the object's internal position
		self.x += speed