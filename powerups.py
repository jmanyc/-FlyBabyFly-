# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/18/17

import pygame, os, sys


class Powerup():
	def __init__(self, position, screenWidth, screenHeight, image, type):
		self.image = image
		self.position 
		self.x = position[0]
		self.y = position[1]
		self.color = color

		self.screenHeight = screenHeight
		self.screenWidth = screenWidth
		
		self.visited = False
		
		self.image = image
			
		self.powerUp = self.image.get_rect()
		self.powerUp.move_ip(self.x, self.y)
		#self.powerUp.inflate(self.image.get_width()*-1,0)
		
		self.powerUpType = type
		
	def getType(self):
		return self.powerUpType
		
	def getVisited(self):
		return self.visited
		
	def setVisited(self, bool):
		self.visited = bool
		
	def getPosition(self):
		return self.position

	def draw(self, surface):		
		surface.blit(self.image,(self.position))

	def getPowerUp(self):
		#returns this power up object's Rect defined in self.powerUp
		return self.powerUp
		
	def movePowerUp(self, speed, surface):
		self.powerUp.move_ip(speed[0], speed[1])	# change the object's internal position
		self.x += speed
		self.draw(surface)    # redraw the obstacle at its new position on the display