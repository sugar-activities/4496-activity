#!/usr/bin/env python

import math
from animation import *
import xml.dom.minidom
import sys, pygame
from os import path
from util import *
from pygame.locals import *

#
# class Pet
# This class manages the display and movement of the
# pet. The pet is persistent, one object is allocated
# for the duration of the game.
#

class Pet(object) :
	MaxX = 400 #constant
	MinX = 200 #constant
	StandTime = 1.5
	def __init__(self, game) :
		# Reference to the game that uses this pet
		self._game = game
		# The folder we find pets in 
		self._folder = game.Version.PetFolder
		# The current leve.
		self._level = None
		# Current location for the pet. The location is
		# actually computed in Update, but may change to
		# relative position changes later.
		self._loc = (300.0, 750.0)
		self._time = 0
		self._stateTime = 0.0
		self._animations = {}
		self._mood = "happy"
		self._pettype = "pup"
		#self.action = "idle"
		self._left = False
		self._state = "idle"
		self._rectBef = Rect((0,0),(0,0))
		self._walkspeed = 30
		self._runspeed = 90
		self._currentAnimation = None

		
		
	
	# Set the level that uses this pet. The level changes over time.
	def SetLevel(self, level) :
		self._level = level
		
	# Load content needed for the pet.
	def Load(self) :
		del self._animations
		self._animations = {}
		xmlDoc = xml.dom.minidom.parse(path.join(self._folder, "pet.xml"))
		root = xmlDoc.documentElement
		self._frameCount = 0
		for node in root.childNodes :
			if node.nodeName == "Animation":
				folder = node.getAttribute('folder')
				name = node.getAttribute('name')
				pettype = node.getAttribute('pettype')
				mood = node.getAttribute('mood')
				if pettype == self._pettype:		
					animation = Animation(self._folder, folder)
					animation.Load()
					self._animations[pettype+':'+name+':'+mood] = animation
		self._loadCurrentAnimation()
		
	
	# This function is called prior to Draw. It is responsible for
	# any advance of the animation in time. It is also responsible to
	# calling self._level.Redraw(rect) to indicate rectangles that need
	# to be redrawn. This includes both where the pet was before and where
	# it is now.
	def Update(self, delta) :
		# Where it was before
		
		self._time = self._time + 0.001 * delta
		self._stateTime = self._stateTime + delta * .001
		
		self._currentAnimation.Update(delta)
		
		self._updateState(delta)
		

		
		#self._loc = (800 , 500  )
		rect = Rect(self._loc, self._currentAnimation.Image.get_size())
		currentRect = rect
		rect.union_ip(self._rectBef)
		self._level.Redraw(rect)
		self._rectBef = currentRect
	
	def _updateState(self, delta):
		if self._state == "walkstart":
			if self._currentAnimation.Finished:
				self._state = "walk"
				self._stateTime = 0
				self._loadCurrentAnimation()
		elif self._state == "walk":
			if self._left:
				self._loc = (self._loc[0] - delta * .001 * self._walkspeed, self._loc[1])
				if self._loc[0] < self.MinX:
					self._loc = (self.MinX, self._loc[1])
					self._state = "walkend"
					self._stateTime = 0.0
					self._loadCurrentAnimation()
			else:
				self._loc = (self._loc[0] + delta * .001 * self._walkspeed, self._loc[1])
				if self._loc[0] > self.MaxX:
					self._loc = (self.MaxX, self._loc[1])
					self._state = "walkend"
					self._stateTime = 0.0
					self._loadCurrentAnimation()
		elif self._state == "walkend":
			if self._currentAnimation.Finished:
				self._state = "idle"
				self._stateTime = 0
				self._loadCurrentAnimation()
		elif self._state == "idle":
			if self._stateTime > self.StandTime:
				self._state = "walkstart"
				self._left = not self._left
				self._loadCurrentAnimation()
				self._stateTime = 0
		elif self._state == "fleestart":
			if self._currentAnimation.Finished:
				self._state = "flee"
				self._stateTime = 0
				self._loadCurrentAnimation(True)
		elif self._state == "flee":
			self._loc = (self._loc[0] + delta * .001 * self._runspeed, self._loc[1])
			if self._currentAnimation.Finished:
				self._loc = (300.0, 750.0)
				self._state = "idle"
				self._mood = "sad"
				self._stateTime = 0
				self._loadCurrentAnimation()
		elif self._state == "lick":
			if self._currentAnimation.Finished:
				self._state = "idle"
				if self._pettype == "pup":
					self._pettype = "ado"
					self.Load()
				if self._pettype == "ado":
					self._pettype = "dog"  
					self.Load()
				self._stateTime = 0
				self._loadCurrentAnimation()
		#elif self._state == self._mood:
		#	if self._stateTime > self.StandTime:
		#		self._state = "walk"
		#		self._direction = "side"
		#		self._left = not self._left
		#		self._loadCurrentAnimation()
		#elif self._state == "scared" and self._direction == "forward":
		#	if self._currentAnimation.Finished:
		#		self._direction = "side"
		#		self._loadCurrentAnimation()
		#elif self._state == "scared":
		#	self._loc = (self._loc[0] - delta * .001 * self._runspeed, self._loc[1])
			
			
			
	# This function draws. Only draw withing a rectangle in the list
	# of rectangles on the actual image.
	def Draw(self, rects) :
		for rect in rects :
			rectLoc = rect.move(-self._loc[0] + self._currentAnimation.Image.get_width()/2, -self._loc[1] + self._currentAnimation.Image.get_height()/2)
			if self._left: 
				self._level.Display.blit(self._currentAnimation.ReverseImage, rect, rectLoc)
			else: 
				self._level.Display.blit(self._currentAnimation.Image, rect, rectLoc)
			
	def Feed(self):
		self._state = "lick"
		self._stateTime = 0
		self._loadCurrentAnimation(True)
		
	
	def Explode(self):
		self._state = "fleestart"
		self._stateTime = 0
		self._loadCurrentAnimation(True)
		
	def MakeHappy(self):
		if self._mood == "verysad":
			self._mood = "sad"
		elif self._mood == "happy":
			self._mood = "veryhappy"
		elif self._mood == "sad":
			self._mood = "happy"
		self.stopWalk()
	
	def MakeSad(self):
		if self._mood == "veryhappy":
			self._mood = "happy"
		elif self._mood == "happy":
			self._mood = "sad"
		elif self._mood == "sad":
			self._mood = "verysad"
		self.stopWalk()
		
		
	def _loadCurrentAnimation(self, special = False):
		if self._currentAnimation != None:
			self._currentAnimation.Reset()
		#print "Loading Animation", "\"" + self._pettype+':'+self._direction+':'+self._state + "\""
		if special:
			self._currentAnimation = self._animations[self._pettype+':'+self._state+':'+"special"]
		elif self._state == "idle":
			self._currentAnimation = self._animations[self._pettype+':'+self._state+':'+self._mood]
		elif self._mood == "veryhappy":
			self._currentAnimation = self._animations[self._pettype+':'+self._state+':'+"happy"]
		elif self._mood == "verysad":
			self._currentAnimation = self._animations[self._pettype+':'+self._state+':'+"sad"]
		else:
			self._currentAnimation = self._animations[self._pettype+':'+self._state+':'+self._mood]
			
	

	def stopWalk(self):
		self._state = "idle"
		self._stateTime = 0.0
		self._loadCurrentAnimation()


		
		
			
			
