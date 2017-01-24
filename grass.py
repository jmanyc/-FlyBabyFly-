import pygame, os, sys

class Grass():
	
	def __init__(self, xPos, screenHeight, image):
		self.xPos = xPos
		self.yPos = screenHeight*17/18
		
		self.image = image
		
	def draw(self, surface):
		surface.blit(self.image,(self.xPos,self.yPos))
		
	def move(self,speed, surface):
		self.xPos += speed
		self.draw(surface)
		
	def getX(self):
		return self.xPos