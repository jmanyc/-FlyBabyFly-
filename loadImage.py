import threading
import time
import pygame

class loadImage(threading.Thread):

	## init takes in height
	def __init__(self, path, imageScale):
		threading.Thread.__init__(self)

		self.imageScale = imageScale
		self.path = path

	def run(self) :
		self.image = pygame.transform.scale(pygame.image.load( self.path ).convert_alpha(), self.imageScale)
		
	def getImage(self) :
		return self.image