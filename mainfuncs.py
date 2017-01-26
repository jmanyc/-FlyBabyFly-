# Fly Baby Fly
# Jan Plan 2017
# CS269
# 1/16/17

import pygame
import sys
import avatar
import HighScoreReader
import quoteReader
import random
from beams import Beam
from wall import Wall
from label import *
from grass import Grass
from powerups import Powerup

### All of these functions are called in the main loop; they manage transition of game 
# \ states and update the appropriate buttons, objects and sounds within the game.

# importLists is called in main to return local lists of those from main here in mainfunc

def importLists(avatarParams, creditsMenu, optionsList, lossMenu, instructions):
	return avatarParams, creditsMenu, optionsList, lossMenu, instructions
	
# 

def updateScreen(screen, rect, refresh):
	print "Haha, this isn't done yet, and hopefully won't have to be"
'''
	Crop out the background at the rect
	blit it over the current rect
	move the rect
	append it to refresh
	
	Later run refresh through update
'''

def updateFlier(flier):
	flier.keyPressed() # handles pressing keys, now if we need to speed up our program work on this
	flier.applyGravity() # calls the simulated gravity function of avatar
	flier.applyRotation() # Applies rotation to the image

def playSound(sound, toggle):
	### Made this to reduce the size of main.py ###
	### Plays a sound if the toggle is on ###
	if toggle == True:
		sound.play()
		
# If the user has has clicked on Instructions button from the main menu, then, call the 
# \ four buttons' update methods; their update methods check if the mouse is hovering over
# \ them and has been clicked, and route the 
	
def State2Update(screen, instructions, gravity, rainbow):	# main consolidation
	
	help, controls, powerUps, gravityLabel, rainbowLabel, mainBack, paint = instructions
	help.update(screen)		
	controls.update(screen)
	powerUps.update(screen)
	gravityLabel.update(screen)
	rainbowLabel.update(screen)
	gravity.draw(screen)
	rainbow.draw(screen)
	mainBack.update(screen)
	paint.update(screen)

# If the user is on the sound options screen, if the mouse is hovering over one of the 
# \ three buttons and clicks on it, then it toggles the appropriate option (background
# \ music or sound effects) or returns to the main screen. It returns the updated sound
# \ settings as well as the current game state.
	#bools = [musicToggle, musicToggled, soundToggled,justClicked]
def updateSoundOptions(bools, gameState, optionsList, mouse, screen, avatarParams, clickSound):	# main consolidation
	for item in optionsList:
		if item.hover((mouse[0],mouse[1]),avatarParams[2]) == True and pygame.mouse.get_pressed()[0] and bools[3] == False:
			# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
			clickedState = item.getState()
			
			if clickedState == 42: #Music Toggle
				if bools[0] == True:
					pygame.mixer.music.pause()
					bools[0] = False
				else:
					pygame.mixer.music.unpause()
					bools[0] = True
					
			elif clickedState == 43: #Sound Toggle
				if avatarParams[2] == True:
					avatarParams[2] = False
				else:
					avatarParams[2] = True
					
			elif clickedState == 41: #LowRes Toggle
				if bools[4] == True:
					bools[4] = False
				else:
					bools[4] = True
			elif clickedState == 48:
				if bools[6] == True:
					bools[6] = False
				else:
					bools[6] = True
			elif clickedState == 0:
				gameState = 0
				settings = [bools[4], bools[0], avatarParams[2], bools[6]]
				writeString = ''
				for set in settings:
					if set == True:
						writeString += str(1) + '\n'
					else:
						writeString += str(0) + '\n'
	
				fp = file( 'Settings.txt', 'w') #writes over the old file, adding the player score
				fp.write(writeString)
				fp.close()	
			playSound(clickSound,avatarParams[2])
		item.isHover = False
		item.update(screen)
	if bools[0] == True:
		bools[1].isHover = True
		bools[1].update(screen)
	if avatarParams[2] == True:
		bools[2].isHover = True
		bools[2].update(screen)
	if bools[4] == True:
		bools[5].isHover = True
		bools[5].update(screen)
	if bools[6] == True:
		optionsList[4].isHover = True
		optionsList[4].update(screen)
	return [bools[0], avatarParams[2], gameState, bools[4], bools[6]]
	
# If the user is at the main menu, mainButtonsClicked is called to check if the mouse is
# \ hovering over a button and clicks it. If so, it routes the user to the appropriate screen.

def mainButtonsClicked(gameState, score, counter, bools, mainMenu, mouse, screen, clickSound, scoreLabel, avatarParams):	# main consolidation
	for item in mainMenu:
			if item.hover((mouse[0],mouse[1]),avatarParams[2]) == True and pygame.mouse.get_pressed()[0] and bools[3] == False:
				
				# If hovering over the item, and a button is clicked, go to the state the button is linked to.
				playSound(clickSound,avatarParams[2])
				gameState = item.getState()
				
				if gameState == 1: #If you add anything to this if statement, add it to the retry menu too
					### Call this to restart the game and scores ###
					if bools[0] == True:
						if avatarParams[3] == 'paperBomber' or avatarParams[3] == 'paperFlyboy':
							pygame.mixer.music.load("Assets/sound/background.ogg")
						elif avatarParams[3] == 'biBomber' or avatarParams[3] == 'biFlyboy':
							pygame.mixer.music.load("Assets/sound/Original_Soundtrack.ogg")
						elif avatarParams[3] == 'bubbleBomber' or avatarParams[3] == 'bubbleFlyboy':
							pygame.mixer.music.load("Assets/sound/soundtrack3.ogg")
						pygame.mixer.music.play(-1)
					score = 0
					scoreLabel.updateText("Score: "+str(score))
					pygame.mixer.music.set_volume(0.75)
					counter = 0
				break
			
			item.update(screen)
	return [gameState, score, counter]
	
# If you're at the loss screen and click Retry to play the game again (as checked in the 
# \ main loop), then restartGame is called to restart the game for the user (line 286 in main).
	
def restartGame(score, scoreLabel, flier):	# main consolidation
	score = 0
	scoreLabel.updateText("Score: "+str(score))
	pygame.mixer.music.set_volume(0.75)
	return flier, score
