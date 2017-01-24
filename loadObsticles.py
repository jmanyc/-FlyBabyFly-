import threading
import time
import pygame

class loadObsticles(threading.Thread):

	## init takes in height
	def __init__(self, screenWidth, screenHeight, height):
		threading.Thread.__init__(self)
		
		self.height = height
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight

	def run(self) :
		imageScale = (self.screenWidth/28, self.screenHeight * 27/32 / self.height) # For 1 tall walls
		redObs = pygame.transform.scale(pygame.image.load( "Assets/img/RedObstacle.png" ).convert(), imageScale)
		blueObs = pygame.transform.scale(pygame.image.load( "Assets/img/BlueObstacle.png" ).convert(), imageScale)
		greenObs = pygame.transform.scale(pygame.image.load( "Assets/img/GreenObstacle.png" ).convert(), imageScale)
		purpleObs = pygame.transform.scale(pygame.image.load( "Assets/img/PurpleObstacle.png" ).convert(), imageScale)
		self.preloaded = [redObs, blueObs, greenObs, purpleObs]
	def getObsticles(self) :
		return self.preloaded
