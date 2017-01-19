# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Beam():

	def __init__(self, position, color, screenWidth, screenHeight, image): #Work on this
		
		self.x = position
		self.y = 0
		self.color = color

		self.screenHeight = screenHeight
		self.screenWidth = screenWidth
		
		# This needs tweaking, should be 5.5
		self.visited = False
		
		self.image = image
			
		self.beam = self.image.get_rect()
		self.beam.move_ip(self.x + self.screenWidth/15, self.y)
		
	def getVisited(self):
		return self.visited
		
	def setVisited(self, bool):
		self.visited = bool
		
	def getPosition(self):
		return self.x
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color

	def draw(self, surface):		
		surface.blit(self.image,(self.x,self.y))

	def getBeam(self):
		#returns this Beam object's Rect defined in self.beam
		return self.beam

		
	def moveBeam(self, speed, surface):
		self.beam.move_ip(speed, 0)	# change the object's internal position
		self.x += speed
		self.draw(surface)    # redraw the obstacle at its new position on the display