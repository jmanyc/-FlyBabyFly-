# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Obstacle():

	def __init__(self, position, color, width, height, image, textLabel):
		
		#tuple that stores the position of the obstacle in the following format: (xpos,ypos)
		self.position = position

		#stores the x-position of the obstacle object
		self.x = self.position[0]
		self.label.x = self.x

		#stores the y-position of the obstacle object
		self.y = self.position[1]
		if type(label) is MenuLabel:
			self.hasLabel = True
			self.label.y = self.y
		else:
			self.hasLabel = False
		#stores the color of the obstacle object
		self.color = color

		#store the height and width of the obstacle object
		self.height = height
		self.width = width

		#boolean marker for the state of the object. If set to true, then it is skipped over in main.py while cheking for 
		#collisions. Mainly for optimization purposes
		self.visited = False

		#stores the image for the obstacle
		self.image = image
		
		#stores the Rect corresponding to the obstacle object
		self.obstacle = self.image.get_rect()

		#moves the Rect of the obstacle to the obstacle's initial position
		self.obstacle.move_ip(self.x,self.y)
		
		self.label = label
		
	def setPosition(self, position):
		#sets the obstacle's position field to the tuple <position>
		self.position = position
		
	def getXPosition(self):
		#returns the obstacle's x-position
		return self.x
		
	def setColor(self, color):
		#sets this object's color field to the given color
		self.color = color
		
	def getColor(self):
		#returns this object's color field
		return self.color
		
	def draw(self, surface):
		#blits the object's image onto the given surface at its stored position
		surface.blit(self.image,(self.x,self.y))
		self.label.update(surface)
		if self.hasLabel:
			self.label.update(surface)
		
	def getObstacle(self):
		#returns the Rect object associated with this obstacle's image
		return self.obstacle

	def getVisited(self):
		#returns a boolean representing the visited state of the obstacle
		return self.visited

	def setVisited(self, state):
		#sets the visited state of the object to the given boolean <state>
		self.visited = state
				
	def moveObs(self, speed, surface):
		#changes the position of the Rect object associated with this obstacle's image
		self.obstacle.move_ip(speed, 0)	
		self.x += speed
		self.label.x += speed
		if self.hasLabel:
			self.label.x += speed