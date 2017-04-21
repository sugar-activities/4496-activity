#!/usr/bin/env python

import math
from animation import *
import xml.dom.minidom
import sys, pygame
from os import path
from util import *
from pygame.locals import *

#
# class Avatar
# This class manages the display and movement of the
# avatar. It is a simpler version of the pet class basically
#

class Avatar(object) :
	def __init__(self, game) :
		self._game = game
		self._folder = game.Version.AvatarFolder
		# The current level.
		self._level = None
		# Current location for the avatar. The location is
		# actually computed in Update, but may change to
		# relative position changes later.
		self._loc = ((50), (824-260))
		self._currentAnimation = None
		self._idleAnim = None
		self._runAnim = None   
		self._rectBef = Rect((0,0),(0,0))
		self._mirrored = False
		
	# Set the level that uses this avatar. The level changes over time.
	def SetLevel(self, level) :
		self._level = level
		
	def Load(self, flag):
		if flag == True:
			self._avatarIdle = Animation(self._folder, "AvatarIdle")
			self._avatarRun = Animation(self._folder, "AvatarRun")
			self._avatarForward = Animation(self._folder, "AvatarForward")
			self._avatarRight = Animation(self._folder, "AvatarRight")
		else:
			self._avatarIdle = Animation(self._folder, "AvatarIdleGirl")
			self._avatarRun = Animation(self._folder, "AvatarRunGirl")
			self._avatarForward = Animation(self._folder, "AvatarForwardGirl")
			self._avatarRight = Animation(self._folder, "AvatarRightGirl")
		self._avatarIdle.Load()
		self._avatarRun.Load()
		self._avatarForward.Load()
		self._avatarRight.Load()

		self._currentAnimation = self._avatarIdle
			
	def Update(self, delta):
		self._currentAnimation.Update(delta)
		rect = Rect(self._loc, self._currentAnimation.Image.get_size())
		currentRect = rect
		rect.union_ip(self._rectBef)
		self._level.Redraw(rect)
		self._rectBef = currentRect
		if self._currentAnimation.Finished:
			self._currentAnimation.Reset()
			self._currentAnimation = self._avatarIdle
		
		
	def Explode(self):
		self._currentAnimation.Reset()
		self._currentAnimation = self._avatarRun
		
	def StopExplode(self):
		if self._currentAnimation != None:
			self._currentAnimation.Reset()
		self._currentAnimation = self._avatarIdle
		
	def MoveForward(self):
		self._currentAnimation.Reset()
		self._currentAnimation = self._avatarForward
		
	def MoveTurn(self, right):
		self._mirrored = right
		self._currentAnimation.Reset()
		self._currentAnimation = self._avatarRight
		
		
	def Draw(self, rects) :
		for rect in rects :
			rectLoc = rect.move(-self._loc[0], -self._loc[1])
			if self._mirrored:
				self._level.Display.blit(self._currentAnimation.Image, rect, rectLoc)
			else:
				self._level.Display.blit(self._currentAnimation.ReverseImage, rect, rectLoc)
	
