#!/usr/bin/env python

from level import *
import math

#
# The Map class manages the map for a level
#

class Map(object) :
	SIZE = (256, 256)
	LOCATION = (-(1200-256-20), -(20))
	ICONSIZE = (32, 32)
	
	def __init__(self, level) :
		self._image = None
		self._rotatedImage = None
		self._level = level
		self._playerIcon = None
		self._foodIcon = None
		
		# Bottom left and top right points for the level in this image
		self.tl = (0, 0)
		self.br = (100, 100)
		
		# Current angle in degress
		self._dir = 0
		
		# Rotation speed in degrees per second
		self._speed = 180
		self._moveSpeed = 10
		
		self._foodGridLocation = (1,1)
		self._foodLocation = (0,0) #Do not change, detects for initial calculations
		self._playerGridLocation = (0,0)
		self._playerLocation = (0,0)
		self._moveToLocation = self._playerLocation

		
	#
	# Properties
	#
	
	def GetTL(self) : return self.tl
	def GetBR(self) : return self.br
	def GetImage(self) : return self._image
	def SetImage(self, image) :
		self._image = image
		self._rotatedImage = image
		self._dir = Level.NORTH
	def GetFoodIcon(self) : return self._foodIcon
	def SetFoodIcon(self, image) :
		self._foodIcon = image 
		self._rotatedFoodIcon = image
	def GetPlayerIcon(self) : return self._playerIcon
	def SetPlayerIcon(self, image) : 
		self._playerIcon = image
	def GetFoodLocation(self) : return (self._foodGridLocation[1], self._foodGridLocation[0])
	def SetFoodLocation(self, location) : 
		self._foodGridLocation = (location[1], location[0])
	
	
	TL = property(GetTL)
	BR = property(GetBR)
	Image = property(GetImage, SetImage)
	FoodIcon = property(GetFoodIcon, SetFoodIcon)
	PlayerIcon = property(GetPlayerIcon, SetPlayerIcon)
	FoodLocation = property
	
	def SetBounds(self, tl, br) :
		self.tl = tl
		self.br = br
		
	def Update(self, delta) :
		if self._foodLocation == (0,0):
			self._foodLocation =  SubTuples(self.GridToLocation(self._level.FoodLocation), (16, 16))
		desired = self._level.Angle
		if self._dir != desired :
			# The direction has changed. We need to rotate the map
			# Make _dir be in the shortest direction
			diff = desired - self._dir
			if diff < -180 :
				diff = diff + 360
			elif diff > 180 :
				diff = diff - 360
				
			if diff > 0 :
				# Clockwise rotation
				deltaAngle = delta * 0.001 * self._speed
				if deltaAngle > diff :
					self._dir = desired
				else :
					self._dir = self._dir + deltaAngle
			else :
				# Counter-clockwise rotation
				deltaAngle = -delta * 0.001 * self._speed
				if deltaAngle < diff :
					self._dir = desired
				else :
					self._dir = self._dir + deltaAngle
					
			self._rotatedImage = pygame.transform.rotate(self._image, self._dir)
			self._rotatedFoodIcon = pygame.transform.rotate(self._foodIcon, self._dir)
			foodSize = self._rotatedFoodIcon.get_size()
			#Get food location on rotated map
			self._foodLocation =  SubTuples(self.GridToLocation(self._level.FoodLocation), (foodSize[0]/2, foodSize[1]/2))
			self._playerLocation = SubTuples(self.GridToLocation(self._playerGridLocation), (Map.ICONSIZE[0]/2, Map.ICONSIZE[1]/2))
			rect = Rect(-Map.LOCATION[0], -Map.LOCATION[1], Map.SIZE[0], Map.SIZE[1])
			self._level.Redraw(rect)
		if self._playerGridLocation != self._level.Location:
			self.MoveToLocation((self._level.Location[1], self._level.Location[0]))


			
		
	
	def Draw(self, rects) :
		# We will need to offset the image by how much it grew in size
		deltaSize = SubTuples(self._rotatedImage.get_size(), Map.SIZE)
		offset = AddTuples(Map.LOCATION, (deltaSize[0]/2, deltaSize[1]/2))
		for rect in rects :
			rectLoc = rect.move(offset)
			self._level.Display.blit(self._rotatedImage, rect, rectLoc)
			self._level.Display.blit(self._rotatedFoodIcon, self._foodLocation)
			self._level.Display.blit(self._playerIcon, self._playerLocation)
		
		
	
	def GridToLocation(self, GridLocation) :
		#print "Level Size:", self._level.size
		#print "Getting Grid Location:", GridLocation
		unrotatedX = GridLocation[0] * ((self.br[0]-self.tl[0])/(self._level.size[1]-1))+self.tl[0]
		unrotatedY = GridLocation[1] * ((self.br[1]-self.tl[1])/(self._level.size[0]-1))+self.tl[1]
		#print "Unrotated Location:", (unrotatedX, unrotatedY)
		
		angle = math.radians(self._dir)
		localX = unrotatedX - Map.SIZE[0]/2	#need to rotate around map center
		localY = unrotatedY - Map.SIZE[1]/2

		localXRotated = localX * math.cos(angle) + localY * math.sin(angle)
		localYRotated = -localX * math.sin(angle) + localY * math.cos(angle)

		
		rotatedX = localXRotated + Map.SIZE[0]/2 - Map.LOCATION[0]#change back to global location
		rotatedY = localYRotated + Map.SIZE[1]/2 - Map.LOCATION[1]

		return (rotatedX, rotatedY)
		
	def MoveToLocation(self, GridLocation) :
		self._playerGridLocation = GridLocation
		self._playerLocation = SubTuples(self.GridToLocation(self._playerGridLocation), (Map.ICONSIZE[0]/2, Map.ICONSIZE[1]/2))
		rect = Rect(-self._playerLocation[0], -self._playerLocation[1], Map.ICONSIZE[0], Map.ICONSIZE[1])
		self._level.Redraw(rect)
		
	
