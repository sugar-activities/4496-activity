import pygame, sys
from os import path

from background import *

#
# This is the base class for any game screen
#

class GameScreen(object) :
	def __init__(self, game, background):
		self.game = game					# GameUxo object
		self.version = game.version			# Version object
		self.imageFolder = game.version.ImageFolder
		self.imageManger = game.ImageManager
		self.size = game.Display.get_size()	# Screen size
		self.background = Background(self)
		
		if background != "" :
			img = pygame.image.load(path.join(self.imageFolder , background))
			img = pygame.transform.scale(img, self.size).convert()
			self.background.Transition(img, Background.NONE)
	
	#
	# Properties
	#
	
	def GetDirtyRects(self) :
		return self.game.DirtyRects
	
	def GetImageManager(self) :
		return self.game.ImageManager
	
	def GetSoundManager(self) :
		return self.game.SoundManager
	
	def GetDisplay(self) :
		return self.game.Display
	
	DirtyRects = property(GetDirtyRects)
	ImageManager = property(GetImageManager)
	SoundManager = property(GetSoundManager)
	Display = property(GetDisplay)
	
	# Indicate a screen is now needed
	def Prepare(self) :
		pass
	
	# Indicate a screen is no longer needed
	def Unprepare(self):
		pass
	
	# Update the screen. Delta is elapsed time in milliseconds
	def Update(self, delta):
		self.background.Update(delta)
		
	# Draw the screen. Use the values from GetDrawRects or GetDrawAll
	# to detemine what part of the screen to draw.
	def Draw(self):
		self.background.Draw(self.GetDrawRects())
		
	# Handle keypresses
	def KeyHandler(self, event):
		pass

	# Force a redraw of the whole screen
	# Should be called in Update, not Draw
	def RedrawAll(self) :
		self.game.DirtyRects.RedrawAll()
	
	# Force a redraw of part of the screen
	# Should be called in Update, not Draw
	def Redraw(self, rect) :
		self.game.DirtyRects.Redraw(rect)

	# Returns a list of rectangles that need to be drawn
	def GetDrawRects(self) :
		return self.game.DirtyRects.Get()
		
	# Returns true if all of the screen needs to be drawns
	def GetDrawAll(self) :
		return self.game.DirtyRects.GetAll()
