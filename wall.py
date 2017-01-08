import obstacles

class Wall(Obstacle):
	
	def __init__(self, lastBeamColor):
	
		Obstacle.__init__(self, position, color)
		self.b1color = b1color
		self.b2color = b2color
		self.b3color = b3color
		self.lastBeamColor = lastBeamColor
		
	def setb1color(self, color):
		self.b1color = b1color
		
	def getb1color(self):
		return self.b1color
		
	def setb2color(self, color):
		self.b2color = b1color
		
	def getb2color(self):
		return self.b2color
		
	def setb3color(self, color):
		self.b3color = b1color
		
	def getb3color(self):
		return self.b3color