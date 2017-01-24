import threading
import time
import pygame
from label import MenuLabel

class loadMenuLabels(threading.Thread):

	## init takes in height
	def __init__(self, text, fontColor, fontSize, (x,y), state):
		threading.Thread.__init__(self)
		
		self.fontSize = fontSize
		self.fontColor = fontColor
		self.text = text
		self.x = x
		self.y = y
		self.state = state

	def run(self) :
		self.label = MenuLabel(self.text, self.fontColor, self.fontSize, (self.x,self.y), self.state)
		
	def getLabel(self) :
		return self.label

