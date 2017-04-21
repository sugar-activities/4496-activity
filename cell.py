import sys, pygame

from level import *
from mount import *

#
# The Cell class describes one cell of a game level.
#

class Cell(object) :
	
	def __init__(self) :
		# Items that will be set by the level factory
		# when it loads the cell
		self._imageFilename = ''
		# Path to the iamge
		self._imagePath = ''
		# The image to display
		self.image = None
		# True if this is a border image (not navigable)
		self._border = False
		# Any voiceover to play when we enter the cell
		self.voiceOnce = ''
		# Flag indicating the cell has food
		self._hasFood = False
		# The lists of mount points by name. Each mount point
		# is an item in the list of type Mount
		self._mounts = dict()
		self._mounts['bad'] = []
		self._mounts['good'] = []
		self._mounts['fixed'] = []
		self._visitCount = 0
		self._stuckDir = [True, True, True, True]
		
		# Other attributes
		# Indicates if the image has been mirrored
		self._imageReversed = False
		self._activeMounts = []
		self._badMount = None
		self._inspected = False
		
		
		# This keeps track of when a cell was viewed
		self.viewCount = 0
		
	#
	# Properties
	#
	def GetBorder(self) : return self._border
	def SetBorder(self, border) : self._border = border
	def GetHasFood(self) : return self._hasFood
	def SetHasFood(self, hf) : self._hasFood = hf
	def GetInspected(self) : return self._inspected
	def SetInspected(self, flag) : self._inspected = flag
	def GetVisited(self) : return self._visitCount > 0
	def GetStuckDir(self) : return self._stuckDir
	def SetStuckDir(self, value) : self._stuckDir = value
	def GetVisitCount(self) : return self._visitCount
	def SetVisitCount(self, value) :self._visitCount = value
	
	
	Visited = property(GetVisited)
	VisitCount = property(GetVisitCount, SetVisitCount)
	Border = property(GetBorder, SetBorder)
	HasFood = property(GetHasFood, SetHasFood)
	Inspected = property(GetInspected, SetInspected)
	StuckDir = property(GetStuckDir, SetStuckDir)
	
	def IsBad(self) : return self._badMount != None
	
	def BadMountSide(self):
		if self.IsBad():
			if self._badMount.Position[0] < 600:
				return "Right"
			else:
				return "Left"
		else: return "None"
	
	def Test(self) :
		if len(self._mounts['bad']) == 0 :
			return
		
		print 'cell'
		self.TestMounts('bad')
		self.TestMounts('good')
		self.TestMounts('fixed')
		
	
	def TestMounts(self, type) :
		if len(self._mounts[type]) == 0 :
			return
		
		print 'Mount type ', type
		for mount in self._mounts[type] :
			mount.Test()

	# Set the image to use for the cell
	# Called by the cell factory
	def SetImage(self, filename, path) :
		self._imageFilename = filename
		self._imagePath = path
		self.image = None  # pygame.image.load(self._imagePath).convert()
		self._imageReversed = False

	# Prepare a cell for use. This includes setting
	# the position of any mounted images.
	def Prepare(self) :
		# We build a list of all active mounts
		self._activeMounts = []
		self.viewCount = 0
		
		# add any fixed mounts to the list
		for mount in self._mounts['fixed'] :
			self._activeMounts.append(mount)
		
		# Do we have any randomly placed bads?
		self._badMount = self.RandomMount(self._mounts['bad'])
		if self._badMount != None :
			self._activeMounts.append(self._badMount)
			
		self._goodMount = self.RandomMount(self._mounts['good'])
		if self._goodMount != None :
			self._activeMounts.append(self._goodMount)
		
		# Prepare each of the mounts for use
		for mount in self._activeMounts :
			mount.Prepare()
	
	# Select and return a random mount of a list of mounts
	# Returns None if the list is empty
	def RandomMount(self, list) :
		if len(list) == 0 :
			return None
		
		return list[random.randint(0, len(list) - 1)]

	# Prepare the view, reversing the image if necessary
	# to be appropriate for a direction I am looking.
	def PrepareView(self, dir) :
		if self.image == None :
			self.image = pygame.image.load(self._imagePath).convert()
			self._imageReversed = False
		needReverse = dir == Level.SOUTH or dir == Level.WEST
		width = self.image.get_width()
		if needReverse != self._imageReversed :
			self.image = pygame.transform.flip(self.image, True, False)
			self._imageReversed = not self._imageReversed
			
		# Prepare any mounted images
		for mount in self._activeMounts :
			mount.PrepareView(dir, width)

	def ReleaseImage(self) :
		self.image = None
		
	def Draw(self, display, rect) :
		if rect.width == 0 or rect.height == 0 :
			return
		for mount in self._activeMounts :
			mount.Draw(display, rect)
	
	def DrawCircle(self, display, rect):
		if self.IsBad():
			self._badMount.DrawCircle(display, rect)
		
	def MountString(self):
		mountstring = ""
		for mount in self._activeMounts:
			mountstring = mountstring + " " + mount.Key
		return mountstring

	# Add a mount object to this cell for a given type
	def AddMount(self, mount, type) :
		self._mounts[type].append(mount)

