# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys, random
from obstacles import Obstacle

class Wall(Obstacle):
	
	
	def __init__(self, lastBeamColor, xPos, screenHeight, colors):
		self.top = screenHeight*3/16

		#All 3 or whatever number of obstacles must equal roughly 3/4 of the screen
		self.obstacleHeight = screenHeight/4
		
		self.width = xPos/28
		#Creating the list to pick the 3 colors from, with the needed color
		self.colorList = [lastBeamColor]
		self.colorList.append(random.choice(colors))# randomly pull some colors to look nice
		self.colorList.append(random.choice(colors))
		random.shuffle(self.colorList) # Now we shuffle the list and then assign them to the following obstacles


		#here we define each of the three wall sections
		self.section1 = Obstacle((xPos, self.top), self.colorList[0], self.width, self.obstacleHeight)
		self.section2 = Obstacle((xPos, self.top + self.obstacleHeight), self.colorList[1], self.width, self.obstacleHeight)
		self.section3 = Obstacle((xPos, self.top + self.obstacleHeight * 2), self.colorList[2], self.width, self.obstacleHeight)
		
		#wallSections is the list that stores each of the sections defined above (the sections are Obstacle objects)
		self.wallSections = []
		self.wallSections.extend([self.section1, self.section2, self.section3])
		
		
		
	def moveWall(self, speed, surface):
		for section in self.wallSections:
			section.moveObs(speed, surface)
			section.draw(surface)
	def getX(self):
		#returns the x-position of the top-left corner of the first obstacle in the wallSections list
		#this is essentially the xposition of the wall's left side
		return self.wallSections[0].getXPosition()
	
	def getWallSections(self):
		#returns the list of Obstacle objects that make up this Wall object
		return self.wallSections

			