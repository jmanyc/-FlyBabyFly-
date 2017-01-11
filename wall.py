# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys
from obstacles import Obstacle


class Wall(Obstacle):
	
	
	def __init__(self, lastBeamColor, xPos, screenHeight, speed = None):
		self.top = screenHeight/8
		self.obstacleHeight = screenHeight/4
		self.width = 50 # width hardcoded because it should always be the same
		self.speed = speed
		self.RED = (255,0,0)
		self.BLUE = (0,0,255)
		self.GREEN = (0,255,0)
		if self.speed != None:
			self.section1 = Obstacle((xPos, self.top), self.RED, self.width, self.obstacleHeight, self.speed)
			self.section2 = Obstacle((xPos, self.top + self.obstacleHeight), self.BLUE, self.width, self.obstacleHeight, self.speed)
			self.section3 = Obstacle((xPos, self.top + self.obstacleHeight * 2), self.GREEN, self.width, self.obstacleHeight, self.speed)
		else:
			self.section1 = Obstacle((xPos, self.top), self.RED, self.width, self.obstacleHeight)
			self.section2 = Obstacle((xPos, self.top + self.obstacleHeight), self.BLUE, self.width, self.obstacleHeight)
			self.section3 = Obstacle((xPos, self.top + self.obstacleHeight * 2), self.GREEN, self.width, self.obstacleHeight)
		
<<<<<<< HEAD
		#self.sub_wallSections = [] #edit this to do all in one line
=======
		#self.sub_wallSections = []
>>>>>>> origin/master
		#self.sub_wallSections.extend([self.section1.obstacle, self.section2.obstacle, self.section3.obstacle])
		
		self.wallSections = []
		self.wallSections.extend([self.section1, self.section2, self.section3])
		
		#self.lastBeamColor = lastBeamColor
		
		#self.sectionColors = []
		#self.sectionColors.extend([self.section1color, self.section2color, self.section3color])
		
<<<<<<< HEAD
	"""def setSection1color(self, color):
=======
# 	def getRectColor(self, current_rect):
# 		return current
		
	def setSection1color(self, color):
>>>>>>> origin/master
		self.section1color = color
		
	def getSection1color(self):
		return self.section1color
		
	def setSection2color(self, color):
		self.section2color = color
		
	def getSection2color(self):
		return self.section2color
		
	def setSection3color(self, color):
		self.section3color = color
		
	def getSection3color(self):
		return self.section3color"""
		
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
<<<<<<< HEAD
		return self.sub_wallSections
=======
		return self.wallSections
>>>>>>> origin/master
