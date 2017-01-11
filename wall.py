# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

import pygame, os, sys
from obstacles import Obstacle


class Wall(Obstacle):
	
	def __init__(self, lastBeamColor, pos1, pos2, pos3, color1, color2, color3, heights, speed = None):

		self.width = 40 # width hardcoded because it should always be the same
		self.heights = heights
		self.speed = speed
		if self.speed != None:
			self.section1 = Obstacle(pos1, color1, self.width, self.heights[0], self.speed)
			self.section2 = Obstacle(pos2, color2, self.width, self.heights[1], self.speed)
			self.section3 = Obstacle(pos3, color3, self.width, self.heights[2], self.speed)
		else:
			self.section1 = Obstacle(pos1, color1, self.width, self.heights[0])
			self.section2 = Obstacle(pos2, color2, self.width, self.heights[1])
			self.section3 = Obstacle(pos3, color3, self.width, self.heights[2])
		
		self.sub_wallSections = []
		self.sub_wallSections.extend([self.section1.obstacle, self.section2.obstacle, self.section3.obstacle])
		
		self.wallSections = []
		self.wallSections.extend([self.section1, self.section2, self.section3])
		
		self.section1color = color1
		self.section2color = color2
		self.section3color = color3
		self.lastBeamColor = lastBeamColor
		
		self.sectionColors = []
		self.sectionColors.extend([self.section1color, self.section2color, self.section3color])
		
	def setSection1color(self, color):
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
		return self.section3color
		
# 	def draw(self, surface):
# 		pygame.draw.rect(surface, self.section1color, self.section1.obstacle)
# 		pygame.draw.rect(surface, self.section2color, self.section2.obstacle)
# 		pygame.draw.rect(surface, self.section3color, self.section3.obstacle)
		
	def moveWall(self, speed, surface):
		for section in self.wallSections:
			section.moveObs(speed, surface)
			section.draw(surface)

	#	self.update()
		
	#def update(self):
	#	for section in self.sub_wallSections:
		#	pygame.display.update([section])
			#pygame.display.update()

			
	def sectionList(self):
		return self.sub_wallSections