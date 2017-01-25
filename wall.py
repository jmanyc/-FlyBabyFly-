# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys, random
from obstacles import Obstacle

class Wall(Obstacle):
	
	
	def __init__(self, lastBeamColor, xPos, screenHeight, colors, preLoaded, label = [0,0,0,0,0,0,0]):
	

		#stores the vertical position of the top edge of the wall object
		self.top = screenHeight*3/32
		self.numObs = preLoaded[7]
		#the sum of the heights of whatever number of obstacles must equal roughly 
		#13/16 of the screen
		self.obstacleHeight = screenHeight * 27/32 /self.numObs
		
		#sotres the width of the wall object (currently set to 1/28th of the wall's 
		#initial x-position, which is the width of the whole screen)
		self.width = xPos/28

		#List containing all of the colors that the obstacles making up the wall could have
		self.colors = list(colors)

		#list storing the color of the last beam encountered in the screen
		self.colorList = [lastBeamColor] 

		#remove the color of the last beam encountered from the color list.
		self.colors.remove(lastBeamColor)

		#list containing the obstacles that make up the wall object
		self.wallSections = []

		#tuple storing the width and height of each obstacle
		self.imageScale = (self.width, self.obstacleHeight)
		
		self.preLoaded = preLoaded
		
		#this loops one time less than the number of obstacles and randomly picks colors from self.colors and appends them to colorList
		#(which is where our last beam color was stored in the first place). This ensures that colorList will be a list of colors of length 
		#equal to the number of obstacles in the wall and that it will include the color of the las beam encountered. 
		for x in range(1, self.numObs): 
			tempColor = random.choice(self.colors)
			self.colors.remove(tempColor)
			self.colorList.append(tempColor)
			
		#next we shuffle colorList	
		random.shuffle(self.colorList) 


		#and now we assign each color list to an obstacle object and append 
		#the obstacle object to the wallSections list
		for x in range(0, self.numObs):
		
			if self.colorList[x] == (255,0,0): #Red
				self.image = self.preLoaded[0]
				self.label = label[0]
				
			elif self.colorList[x] == (0,0,255): #Blue
				self.image = self.preLoaded[1]
<<<<<<< HEAD
				self.label = label[1]				
=======
				self.label = label[1]
>>>>>>> origin/master
				
			elif self.colorList[x] == (0,255,0): #Green
				self.image = self.preLoaded[2]
				self.label = label[2]
<<<<<<< HEAD
				
			elif self.colorList[x] == (255,0,255): #Purple
				self.image = self.preLoaded[3]
				self.label = label[3]
				
			elif self.colorList[x] == (255,255,0): #Yellow
				self.image = self.preLoaded[4]
				self.label = label[4]
				
			elif self.colorList[x] == (0,255,255): #Cyan
				self.image = self.preLoaded[5]
				self.label = label[5]
				
			elif self.colorList[x] == (255,99,71): #Orange
				self.image = self.preLoaded[6]
				self.label = label[6]
				
=======
			elif self.colorList[x] == (255,0,255): #Purple
				self.image = self.preLoaded[3]
				self.label = label[3]
			elif self.colorList[x] == (255,255,0): #Yellow
				self.image = self.preLoaded[4]
				self.label = label[4]
			elif self.colorList[x] == (0,255,255): #Cyan
				self.image = self.preLoaded[5]
				self.label = label[5]
			elif self.colorList[x] == (255,99,71): #Orange
				self.image = self.preLoaded[6]
				self.label = label[6]
>>>>>>> origin/master
			self.section = Obstacle((xPos, self.top + self.obstacleHeight * x), self.colorList[x], self.width, self.obstacleHeight, self.image, self.label)
			
			self.wallSections.append(self.section)
		
	def moveWall(self, speed, surface):
		
		#for each obstacle in the wall, we call that obstacle's move method
		for section in self.wallSections:
			section.moveObs(speed, surface)

		#next, we redraw each obstacle.
		for section in self.wallSections:
			section.draw(surface)
			
	def getX(self):
		#returns the x-position of the top-left corner of the first obstacle in the wallSections list
		#this is essentially the xposition of the wall's left side
		return self.wallSections[0].getXPosition()
	
	def getWallSections(self):
		#returns the list of Obstacle objects that make up this Wall object
		return self.wallSections
		