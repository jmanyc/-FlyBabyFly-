def getHighScores(playerscore = -1):	
	fp = file('HighScoreFile.txt') #reads the file
	lines = fp.readlines() #reads lines and creates an array of lines
	fp.close() #closes the file
	scorelist = [] #list of scores that is returned
	for line in lines: 
		words = line.split()
		scorelist.append( int(words[0]) ) #converts to int and adds to the scorelist
		
	if playerscore != -1: #adds the player score if one is passed in
		scorelist.append(playerscore)
		scorelist.sort(reverse = True) #sorts it in descending order
	
	writeString = '' #creates the string for writing to the file
	for score in scorelist:
		writeString += str(score) + '\n'		
	
	fp = file( 'HighScoreFile.txt', 'w') #writes over the old file, adding the player score
	fp.write(writeString)
	fp.close()	
	
	return scorelist[:10]

if __name__ == "__main__":
	print getHighScores() #add an argument here to add it to the high score list
