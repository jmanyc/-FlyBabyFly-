# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys, random
from obstacles import Obstacle

class Wall(Obstacle):
	
	
	def __init__(self, lastBeamColor, xPos, screenHeight, colors, numObs):
		self.top = screenHeight*3/32
		self.obstacleHeight = screenHeight * 27/32 /numObs #All 3 or whatever number of obstacles must equal roughly 13/16 of the screen
		self.width = xPos/28
		self.colors = list(colors)
		self.colorList = [lastBeamColor] #Contains all the colors that are going to be in the wall
		self.wallSections = [] #Contains obstacles
		self.imageScale = (self.width, self.obstacleHeight)
		self.redObs = pygame.transform.scale(pygame.image.load( "Assets/img/RedObstacle.png" ).convert(), self.imageScale)
		self.blueObs = pygame.transform.scale(pygame.image.load( "Assets/img/BlueObstacle.png" ).convert(), self.imageScale)
		self.greenObs = pygame.transform.scale(pygame.image.load( "Assets/img/GreenObstacle.png" ).convert(), self.imageScale)
		self.whiteObs = pygame.transform.scale(pygame.image.load( "Assets/img/WhiteObstacle.png" ).convert(), self.imageScale)
		self.purpleObs = pygame.transform.scale(pygame.image.load( "Assets/img/PurpleObstacle.png" ).convert(), self.imageScale)
		self.preLoaded = [self.redObs, self.blueObs, self.greenObs, self.whiteObs]
		for x in range(1, numObs): #Minus one, because we pass in the needed color already
			tempColor = random.choice(self.colors)
			while tempColor == lastBeamColor:
				tempColor = random.choice(self.colors)
			self.colors.remove(tempColor)
			self.colorList.append(tempColor)
		random.shuffle(self.colorList) # Now we shuffle the list and then assign them to the following obstacles
		
		for x in range(0, numObs):
			self.section = Obstacle((xPos, self.top + self.obstacleHeight * x), self.colorList[x], self.width, self.obstacleHeight, self.preLoaded)
			self.wallSections.append(self.section)
		
	def moveWall(self, speed, surface):
		for section in self.wallSections:
			section.moveObs(speed, surface)
		for section in self.wallSections:
			section.draw(surface)
			
	def getX(self):
		#returns the x-position of the top-left corner of the first obstacle in the wallSections list
		#this is essentially the xposition of the wall's left side
		return self.wallSections[0].getXPosition()
	
	def getWallSections(self):
		#returns the list of Obstacle objects that make up this Wall object
		return self.wallSections
		