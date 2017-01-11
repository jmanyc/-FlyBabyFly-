# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys, random
from obstacles import Obstacle

class Wall(Obstacle):
	
	
	def __init__(self, lastBeamColor, xPos, screenHeight, colors):
		self.top = screenHeight*3/16
		self.obstacleHeight = screenHeight/4 #All 3 or whatever number of obstacles must equal roughly 3/4 of the screen
		self.width = xPos/28

		self.colorList = [lastBeamColor]#Creating the list to pick the 3 colors from, with the needed color
		self.colorList.append(random.choice(colors))# randomly pull some colors to look nice
		self.colorList.append(random.choice(colors))
		random.shuffle(self.colorList) # Now we shuffle the list and then assign them to the following obstacles
		
		self.section1 = Obstacle((xPos, self.top), self.colorList[0], self.width, self.obstacleHeight)
		self.section2 = Obstacle((xPos, self.top + self.obstacleHeight), self.colorList[1], self.width, self.obstacleHeight)
		self.section3 = Obstacle((xPos, self.top + self.obstacleHeight * 2), self.colorList[2], self.width, self.obstacleHeight)
		#self.sub_wallSections = [] #edit this to do all in one line

		#self.sub_wallSections = []

		#self.sub_wallSections.extend([self.section1.obstacle, self.section2.obstacle, self.section3.obstacle])
		
		self.wallSections = []
		self.wallSections.extend([self.section1, self.section2, self.section3])
		
		#self.lastBeamColor = lastBeamColor
		
		#self.sectionColors = []
		#self.sectionColors.extend([self.section1color, self.section2color, self.section3color])
		

# 	"""def setSection1color(self, color):
# # 	def getRectColor(self, current_rect):
# # 		return current
# 		
# 	def setSection1color(self, color):
# 		self.section1color = color
# 		
# 	def getSection1color(self):
# 		return self.section1color
# 		
# 	def setSection2color(self, color):
# 		self.section2color = color
# 		
# 	def getSection2color(self):
# 		return self.section2color
# 		
# 	def setSection3color(self, color):
# 		self.section3color = color
# 		
# 	def getSection3color(self):
# 		return self.section3color"""
		
# 	def draw(self, surface):
# 		pygame.draw.rect(surface, self.section1color, self.section1.obstacle)
# 		pygame.draw.rect(surface, self.section2color, self.section2.obstacle)
# 		pygame.draw.rect(surface, self.section3color, self.section3.obstacle)
		
	def moveWall(self, speed, surface):
		for section in self.wallSections:
			section.moveObs(speed, surface)
			section.draw(surface)
	def getX(self):
		return self.wallSections.getXPosition()
	#	self.update()
		
	#def update(self):
	#	for section in self.sub_wallSections:
		#	pygame.display.update([section])
			#pygame.display.update()

			
	def sectionList(self):
		return self.wallSections