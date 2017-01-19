import threading
import time
import socket
import HighScoreReader
class Client(threading.Thread):
	def __init__(self, ip, port, score) :
		threading.Thread.__init__(self)
		
		self.score = score
		self.ip = ip
		self.port = port

	def run(self) :
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5)
		try:
			s.connect((self.ip , self.port))
			#print "hahaha"
			#Send some data to remote server
			message = str(self.score)
			s.sendall(message)

			reply = s.recv(4096)
			s.close()
			self.highScores = reply.split()
		except socket.error:
			print 'Failed to connect to server'
			self.highScores = HighScoreReader.getHighScores(self.score)
	def getHighScores(self) :
		return self.highScores
