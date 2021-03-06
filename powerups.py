# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/18/17

import pygame, os, sys


class Powerup():
	def __init__(self, position, image, type):
		self.image = image
		self.position = position
		self.x = position[0]
		self.y = position[1]
		
		self.visited = False
		
		self.image = image
			
		self.powerUp = self.image.get_rect()
		self.powerUp.move_ip(self.x, self.y)
		
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
		surface.blit(self.image,(self.x, self.y))
	
	def getPower(self):
		return self.powerUpType
	
	def getPowerUp(self):
		#returns this power up object's Rect defined in self.powerUp
		return self.powerUp
		
	def movePowerUp(self, speed, surface):
		
 		self.powerUp.move_ip(speed[0], speed[1])	# change the object's internal position
		self.x += speed[0]
		self.y += speed[1]
		self.draw(surface) # redraw the obstacle at its new position on the display
 		if self.y <= 100 and speed[1] < 0 or self.y >= 650 and speed[1] > 0:
 			speed[1] = -speed[1]
 			
		return speed[1]	# the speed is returned to rainbowYvel (hardcoded value, could be changed
						#  so that it is proportional to the wall speed) in main so that it passes in 
						# \ the new reversed y velocity every time that it calls movePowerUp