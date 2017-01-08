class Beams():

	def __init__(self, position, color, x1, y1, x2, y2):
		self.position = position
		self.color = color
		beam = pygame.Rect((x1, y1), (x2, y2))
		
	def setPosition(self, position):
		self.position = position
		
	def getPosition(self):
		return self.position
		
	def setColor(self, color):
		self.color = color
		
	def getColor(self):
		return self.color
