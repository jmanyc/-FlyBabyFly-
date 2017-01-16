import pygame, os, sys

class Grass():
	
	def __init__(self, screenWidth, screenHeight, speed):
		self.xPos = screenWidth
		self.yPos = screenHeight*15/16
		self.imageScale = (self.xPos, self.yPos/15)
		self.speed = speed
		self.image = pygame.transform.scale(pygame.image.load( "Assets/img/grass.png" ).convert(), self.imageScale)
		
	def draw(self, surface):
		surface.blit(self.image,(self.xPos,self.yPos))
		
	def updateGrass(self, surface):
		self.xPos += self.speed
		self.draw(surface)