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
	
def State2Update(screen):	# main consolidation
		help.update(screen)
		controls.update(screen)
		mainBack.update(screen)
		paint.update(screen)
	
def updateSoundOptions(musicToggle, soundToggle, gameState, optionsList):	# main consolidation
	for item in optionsList:
		if item.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
			# If hovering over the item, and a button is clicked, go to the state the button is linked to. 
			clickedState = item.getState()
			
			if clickedState == 42: #Music Toggle
				if musicToggle == True:
					pygame.mixer.music.pause()
					musicToggle = False
				else:
					pygame.mixer.music.unpause()
					musicToggle = True
			elif clickedState == 43: #Sound Toggle
				if soundToggle == True:
					soundToggle = False
				else:
					soundToggle = True
			elif clickedState == 0:
				gameState = 0
			playSound(clickSound,soundToggle)
		item.isHover = False
		item.update(screen)
	if musicToggle == True:
		musicToggled.isHover = True
		musicToggled.update(screen)
	if soundToggle == True:
		soundToggled.isHover = True
		soundToggled.update(screen)
		
	return [musicToggle, soundToggle, gameState]
	
# 
	
def checkMainItems(mainMenu, gameState, flier):	# main consolidation
	for item in mainMenu:
			if item.hover((mouse[0],mouse[1]),soundToggle) == True and pygame.mouse.get_pressed()[0] and justClicked == False:
				
				# If hovering over the item, and a button is clicked, go to the state the button is linked to.
				playSound(clickSound,soundToggle)
				gameState = item.getState()
				
				if gameState == 1: #If you add anything to this if statement, add it to the retry menu too
					### Call this to restart the game and scores ###
					score = 0
					scoreLabel.updateText("Score: "+str(score))
					pygame.mixer.music.set_volume(0.4)
					counter = 0
					flier = avatar.Avatar(screenWidth, screenHeight, soundToggle)
				break
			
			item.update(screen)
	return [gameState, flier]
	
# If you're at the loss screen and click Retry to play the game again (as checked in the 
# \ main loop), then restartGame is called to restart the game for the user. 
	
def restartGame(counter, flier):	# main consolidation
	score = 0
	scoreLabel.updateText("Score: "+str(score))
	pygame.mixer.music.set_volume(0.4)
	counter = 0
	flier = avatar.Avatar(screenWidth, screenHeight, soundToggle)
	return counter, flier