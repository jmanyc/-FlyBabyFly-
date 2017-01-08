# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/5/17

class Avatar():

	def __init__(self, position, yVelocity, color):
		self.position = position
		self.vy = yVelocity
		self.color = color
		
	def setPosition(self, position):
		self.position = position
		
	def getPosition(self):
		return self.position
		
	def setYvel(self, yVelocity):
		self.vy = yVelocity
		
	def getYvel(self):
		return self.vy
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color