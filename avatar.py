# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17
import pygame

class Avatar():

	def __init__(self, position, yVelocity, color, x1, y1, x2, y2):
		self.position = position
		self.vy = yVelocity
		self.color = color
		flyer = pygame.Rect((x1, y1), (x2, y2))
		
	def setPosition(self, position):
		self.position = position
		
	def getPosition(self):
		return self.position
		
	def setYvel(self, yVelocity):
		self.vy = yVelocity
		
	def getYvel(self):
		return self.vy
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color
