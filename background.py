import pygame, sys
from pygame.locals import *
import random

#
# class Background
# Manages a background image and transitions that occur on that background image
class Background(object) :
	NONE = 0
	LEFT = 1
	RIGHT = 2
	FORWARD = 3
	BACK = 4
	
	# Contructor
	# screen: GameScreen object using this background
	def __init__(self, screen):
		# Default transition time
		self._transitionTime = 0.5
		self._screen = screen
		
		# Initialize other variables here
		self._running = False   # Currently not running
		self._image = None	  # Current image

	#
	# Properties
	#
	
	def GetTranTime(self) :
		return self._transitionTime
	
	def SetTranTime(self, value) :
		self._transitionTime = value
		
	def GetRunning(self) :
		return self._running
	
	def GetDisplay(self) :
		return self._screen.Display
	
	# The transition time in seconds
	TransitionTime = property(GetTranTime, SetTranTime)
	Running = property(GetRunning)
	Display = property(GetDisplay)
	
	
	# Begin a transition
	def Transition(self, nextImage, type):
		if type == Background.NONE :
			self._image = nextImage
			self._running = False
			self._screen.RedrawAll()
			return
		
		self._type = type
		self._nextImage = nextImage
		self._seam = 0
		self._running = True

		
	#performs the update step
	def Update(self, delta):
		# If not running, we are done
		if not self._running:
			return
		
		# Retain previous seam and update current seam
		self._prevSeam = self._seam
		self._seam += (0.001 * delta) / self._transitionTime
		
		# We don't let a seam exceed 1 and when both are 1
		# we are done.
		if self._seam > 1 :
			self._seam = 1.0
			if self._prevSeam >= 1 :
				self.prevSeam = 1.0
				self._running = False
				self._image = self._nextImage
				# Whenever we end the transition, we redraw everything
				self._screen.DirtyRects.RedrawAll()
				return
		
		width = self._screen.Display.get_width()
		height = self._screen.Display.get_height()
		
		if self._type == Background.LEFT :
			# Left to right transition
			prevSeam = int(self._prevSeam * width)
			seam = int(self._seam * width)
			self.prevRectL = Rect(seam, 0, width - seam, height)
			self.prevRectR = Rect(0, 0, 0, 0)
			self.newRect = Rect(0, 0, seam, height)
			self.dirtyRect = Rect(prevSeam, 0, seam - prevSeam, height)
			if self.dirtyRect.width > 0 :
				self._screen.DirtyRects.Redraw(self.dirtyRect)
		elif self._type == Background.RIGHT :
			# Left to right transition
			prevSeam = int((1-self._prevSeam) * width)
			seam = int((1-self._seam) * width)
			self.prevRectL = Rect(0, 0, seam, height)
			self.prevRectR = Rect(0, 0, 0, 0)
			self.newRect = Rect(seam, 0, width - seam, height)
			dirtyRect = Rect(seam, 0, prevSeam - seam, height)
			self._screen.DirtyRects.Redraw(dirtyRect)
		elif self._type == Background.FORWARD :
			prevSeamL = int((0.5 - self._prevSeam / 2) * width)
			prevSeamR = int((0.5 + self._prevSeam / 2) * width)
			seamL = int((0.5 - self._seam / 2) * width)
			seamR = int((0.5 + self._seam / 2) * width)
			self.prevRectL = Rect(0, 0, seamL, height)
			self.prevRectR = Rect(seamR, 0, width - seamR, height)
			self.newRect = Rect(seamL, 0, seamR - seamL, height)
			dirtyRect = Rect(seamL, 0, prevSeamL - seamL, height)
			self._screen.DirtyRects.Redraw(dirtyRect)
			dirtyRect = Rect(prevSeamR, 0, seamR - prevSeamR, height)
			self._screen.DirtyRects.Redraw(dirtyRect)
		elif self._type == Background.BACK:
			prevSeam = int((1 - self._prevSeam) * height)
			seam = int((1 - self._seam)*height)
			self.prevRectL = Rect(0, 0, width, seam)
			self.prevRectR = Rect(0,0,0,0)
			self.newRect = Rect(0, seam, width, height - seam)
			dirtyRect = Rect(0, prevSeam, width, prevSeam-seam)
			self._screen.DirtyRects.Redraw(dirtyRect)
			#dirtyRect = Rect(prevSeamR, 0, seamR - prevSeamR, height)
			self._screen.DirtyRects.Redraw(dirtyRect)
			
		
	#draw the screen 
	def Draw(self, rects):
		# If not running, we just draw the background
		if not self._running:
			for rect in rects :
				self.Display.blit(self._image, rect, rect)
			return
		
		for rect in rects :
			prevRectL = rect.clip(self.prevRectL)
			prevRectR = rect.clip(self.prevRectR)
			newRect = rect.clip(self.newRect)
			if prevRectL.width > 0 :
				self.Display.blit(self._image, prevRectL, prevRectL)
			if prevRectR.width > 0 :
				self.Display.blit(self._image, prevRectR, prevRectR)
			if newRect.width > 0 :
				self.Display.blit(self._nextImage, newRect, newRect)
			
		#screen.blit(self._nextImage, rect, rect)
		#updateRects.append(rect)
		#py	.display.update(rect)

