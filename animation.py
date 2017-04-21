import sys, pygame
import xml.dom.minidom
from os import path
from util import *


class Animation(object):
	
	def __init__(self, folder, animationName) :
		self._path = path.join(path.join(folder, animationName))
		self._running = False
		self._frametime = .5 #default value
		self._currentFrametime = 0.0
		self._currentFrame = 0
		self._frames = []
		self.Finished = False
		self._norepeat = False
		
		
	def GetRunning(self): return running
	Running = property(GetRunning)
	
	def GetImage(self):
		return self._frames[self._currentFrame]
	Image = property(GetImage)
	
	def GetReverseImage(self):
		if self._mirror:
			return pygame.transform.flip(self._frames[self._currentFrame], True, False)
		return self._frames[self._currentFrame]
	ReverseImage = property(GetReverseImage)
	
	
	"""
	Load a xml file in the format
	<Animation>
		<Frame file = "filename.png"/>
	</Animation>
	"""
	def Load(self):
		xmlDoc = xml.dom.minidom.parse(path.join(self._path, "anim.xml"))
		root = xmlDoc.documentElement
		self._frameCount = 0
		self._frametime = float(root.getAttribute('frametime'))
		self._mirror = bool(root.getAttribute('mirror'))
		self._norepeat = bool(root.getAttribute('norepeat'))
		for node in root.childNodes :
			if node.nodeName == "frame":
				image = self.LoadFrame(node)
				self._frames.append(image)
				self._frameCount = self._frameCount + 1
		xmlDoc.unlink()
	
	def LoadFrame(self, xmlNode):
		filename = xmlNode.getAttribute('img')
		return pygame.image.load(path.join(self._path, filename))
		
	def Update(self, delta):
		self._currentFrametime = self._currentFrametime + .001 * delta
		#check for need to update to next frame
		if (self._currentFrametime > self._frametime):
			if not self._norepeat:
				self._currentFrame = (self._currentFrame + 1) % self._frameCount
			else:
				if self._currentFrame == self._frameCount - 1:
					self.Finished = True
				self._currentFrame = min(self._currentFrame + 1 , self._frameCount - 1)
			self._currentFrametime  = 0.0
	def Reset(self):
		self._currentFrame = 0
		self._currentFrameTime = 0
		self.Finished = False
		
