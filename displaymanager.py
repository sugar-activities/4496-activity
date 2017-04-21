
import pygame
from pygame import Rect

class DisplayManager(object):
	def __init__(self, display):
		self._scale = 825
		self._base = 825
		self._voffset = 0
		self._hoffset = 0
		self._display = display
		self._size = display.get_size()
		
		if self._size == (1200, 825):
			print "No Scale"
			self._scale = 825
			self._voffset = 0
			self._hoffset = 0
			self._viewarea = Rect(0,0,1200,825)
		else:
			self._scale = self._size[1]
			self._hoffset = int((self._size[0] - 1200 * self._scale / self._base)/2)
			if self._hoffset < 0:
				self._base = 1200
				self._scale = self._size[0]
				self._hoffset = 0
				self._voffset = int((self._size[1] - 825*self._scale / self._base)/2)
			self._viewarea = Rect(self._hoffset, self._voffset, 1200 * self._scale / self._base, 825 * self._scale / self._base)
			print "Scale:", self._scale, "V:", self._voffset, "H:", self._hoffset
			
		self._surface = pygame.Surface((1200,825))
		self._surface = pygame.display.get_surface()
		
	def blit(self, source, dest, area=None):
		self._surface.blit(source, dest, area)
			
	def get_width(self):
		return 1200
	
	def get_height(self):
		return 825
		
	def get_size(self):
		return (1200, 825)
		
	def fill(self, arg):
		self._surface.fill(arg)
	
	def Flip(self):
		scaled = pygame.transform.scale(self._surface, self._viewarea.size)
		self._display.blit(scaled, self._viewarea)
		
	
		
	def DrawEllipse(self, color, location, width = 1):
		pygame.draw.ellipse(self._surface, color, location, width)
		
	def DrawLine(self, color, start, end, width = 1):
		pygame.draw.line(self._surface, color, start, end, width)
