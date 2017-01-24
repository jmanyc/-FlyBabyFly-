import pygame, os, sys

class Window():
	
	def __init__(self, screenWidth, screenHeight, image):
		self.xPos = screenWidth
		self.yPos = screenHeight*5/16
		self.image = image
		
	def draw(self, surface):
		surface.blit(self.image,(self.xPos,self.yPos))
		
	def move(self, speed, surface):
		self.xPos += speed
		self.draw(surface)
		
	def getX(self):
		return self.xPos