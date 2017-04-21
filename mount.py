#!/usr/bin/env python

import sys, pygame, random  

from level import *

#
# The Cell class describes the mounting of an image
# within a cell. The mount can be a box or a point.  A
# point is just a box of size zero as far as this code is
# concerned. Each mount point has an associated image
# from the imagemanager and a scale factor.  Scale factors
# are over a range from the maximum to the minimum Y values
#

class Mount(object) :
	def __init__(self) :
		# Attributes
		# Position of mount or top left corner of box
		self._boxUL = (0, 0)
		# Size of box or 0,0 for a mount
		self._boxSize = (0, 0)
		# The name of the image
		self._key = ''
		# The actual image from the imagemanager
		self._imageRaw = None
		# Minimum scale
		self._scaleMin = 1.0
		# Maximum scale
		self._scaleMax = 1.0
		# Position
		self._position = (0, 0)
		# No Mirroring option
		self._noMirror = False
		
		# Other attributes
		# The actual image we will display (scaled)
		self._image = None
		# Indicates if the image has been mirrored
		self._imageReversed = False
	
	#
	# Properties
	#
	def GetBoxUL(self) : return self._boxUL
	def SetBoxUL(self, pos) : self._boxUL = pos
	def GetBoxSize(self) : return self._boxSize
	def SetBoxSize(self, size) : self._boxSize = size
	def GetPosition(self) : return self._position
	def GetNoMirror(self) : return self._noMirror
	def SetNoMirror(self, nm) : self._noMirror = nm
	def GetKey(self) : return self._key
	def GetPosition(self): return self._position
	
	BoxUL = property(GetBoxUL, SetBoxUL)
	BoxSize = property(GetBoxSize, SetBoxSize)
	Position = property(GetPosition)
	NoMirror = property(GetNoMirror, SetNoMirror)
	Key = property(GetKey)
	Position = property(GetPosition)
	
	# Set the scale for the image
	def SetScales(self, min, max) :
		self._scaleMin = min
		self._scaleMax = max
	
	# Set the reference to the image we will
	# display for this mount from the image manager
	def SetImage(self, key, image) :
		self._key = key
		self._imageRaw = image
		
	# Prepare a mount for use. This is only called for mounts
	# that will actually be displayed.
	def Prepare(self) :
		# Select a random location for the image within the box
		dx = random.randint(0, self.BoxSize[0])
		dy = random.randint(0, self.BoxSize[1])
		self._position = (dx + self.BoxUL[0], dy + self.BoxUL[1])
		
		# Determine the scale
		if self.BoxSize[1] > 0 :
			scale = self._scaleMin + float(dy) / float(self.BoxSize[1]) * (self._scaleMax - self._scaleMin)
		else :
			scale = self._scaleMin
		
		# Create the scaled local copy of the image
		self._image = pygame.transform.scale(self._imageRaw, (int(self._imageRaw.get_width() * scale), int(self._imageRaw.get_height() * scale)))
		self._imageReversed = False
		
	# Prepare the image for display in a given view direction
	def PrepareView(self, dir, width) :
		needReverse = dir == Level.SOUTH or dir == Level.WEST
		if needReverse != self._imageReversed :
			if not self._noMirror :
				self._image = pygame.transform.flip(self._image, True, False)
			self._imageReversed = not self._imageReversed
			self._position = (width - self._position[0], self._position[1])

	def Draw(self, display, rect) :
		# What is the actual x,y location to draw this image?
		drawLoc = (-(self._position[0]- self._image.get_width() / 2), -(self._position[1] - self._image.get_height() / 2))
		rectLeft = rect.move(drawLoc)
		display.blit(self._image, rect, rectLeft)
		
	def DrawCircle(self, display, rect):
		drawLoc = ((self._position[0] - self._image.get_width() / 2) -5 , (self._position[1] - self._image.get_height() /2)-5)
		drawRect = Rect(drawLoc[0], drawLoc[1], self._image.get_size()[0]+10, self._image.get_size()[1]+10)
		#print drawRect
		display.DrawEllipse((255,0,0), drawRect, 6)		



	def Test(self) :
		print 'BoxUL: ', self._boxUL
		print 'BoxSize: ', self._boxSize
		print 'Key: ', self._key
		print 'Scales: ', self._scaleMin, ' to ', self._scaleMax
