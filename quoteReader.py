import random

def getQuote(): 
	fp = file('Quotes.txt') #reads the file
	lines = fp.readlines() #reads lines and creates an array of lines
	fp.close() 
	quoteslist = [] #creates the quotes list
	for line in lines: #adds the quotes to the list
		if line != '':
			quoteslist.append(line)
			
	quote = random.choice(quoteslist) #chooses a random one	
	return quote #returns it
	
if __name__ == "__main__":
	print getQuote()