#!/usr/bin/env python

import pygame

#
# The DirtyRectsManager class manages the dirty regions on the screen.
#
class DirtyRectsManager :
	def __init__(self, screen) :
		self._size = screen.get_size()
		self._all = True
		self._rects = []
		self._screen = [pygame.Rect(0, 0, self._size[0], self._size[1])]
	
	# Return true if all of the screen is dirty and needs to be updated
	def GetAll(self) :
		return self._all
	
	# Return a list of rectangles that are dirty. 
	def Get(self) :
		if self._all :
			return self._screen
		else :
			return self._rects
	
	# Force a redraw of the entire screen
	def RedrawAll(self) :
		self._all = True
		self._rects = []
		
	# Force a redraw of one rectangle on the screen
	def Redraw(self, rect) :
		if rect.size > 0 :
			self._rects.append(rect)
	
	# Update the screen based on the current dirty
	# rectangles list, clearing the list when done
	def Update(self) :
		if self._all :
			pygame.display.update()
			self._all = False
		elif self._rects.count :
			pygame.display.update(self._rects)

		self._rects = []

