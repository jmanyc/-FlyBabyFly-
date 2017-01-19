# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/10/17

import pygame, os, sys

class Beam():

	def __init__(self, position, color, screenWidth, screenHeight, image): #Work on this
		
		#initialize the beam's xposition to the <position argument>
		self.x = position

		#initialize its y-position to 0
		self.y = 0

		#initialize the beam's color to <color>
		self.color = color

		#store the screen height and width
		self.screenHeight = screenHeight
		self.screenWidth = screenWidth
		
		# This needs tweaking, should be 5.5
		self.visited = False
		
		#stores the image associated with the beam (originally the paint cans)
		self.image = image
			
		#stores the Rect object associated with the beams image
		self.beam = self.image.get_rect()
		
		#moves the Rect object to the beam's image's initial position
		self.beam.move_ip(self.x + self.screenWidth/15, self.y)

	def getVisited(self):\
		#returns the object's visited state
		return self.visited
		
	def setVisited(self, bool):
		#sets the beams visited state to the given boolean <bool>
		self.visited = bool
		
	def getPosition(self):
		#returns the x-position of the beam
		return self.x
		
	def setColor(self, color):
		#sets the color field of the beam to the given color <color>
		self.color = color
		
	def getColor(self):
		#returns the beam object's color field
		return self.color

	def draw(self, surface):		
		#blitst the beam's image onto the given <surface> at the beam's (x,y) position
		surface.blit(self.image,(self.x,self.y))

	def getBeam(self):
		#returns this Beam object's Rect defined in self.beam
		return self.beam

		
	def moveBeam(self, speed, surface):
		#change the position of this beam's imgage's Rect object
		self.beam.move_ip(speed, 0)

		#move the beam (distance determined by <speed> argument)
		self.x += speed
		
		#redraw the beam at its new position on the display
		self.draw(surface)    