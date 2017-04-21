#!/usr/bin/env python

import pygame
from os import path
import os
from gameversion import *
from animation import *

#
# The ImageManager class is in charge of any images that are
# presistent during the game.
#

class ImageManager :
	
	# version: GameVersion
	def __init__(self, version, logger) :
		self._logger = logger
		self.left = None
		self.right = None
		self.up = None
		self.explosion = None
		self.check = None
		self._version = version
		self._imageFolder = version.ImageFolder
		self._keyImageFolder = version.KeyImageFolder
		self._avatarFolder = version.AvatarFolder
		self._keyImages = {}
	
	def Load1(self) :
		self.left = pygame.image.load(path.join(self._imageFolder, "left2.png"))
		self.right = pygame.image.load(path.join(self._imageFolder, "right2.png"))
		self.up = pygame.image.load(path.join(self._imageFolder, "up3.png"))
		self.down = pygame.transform.flip(self.up, False, True)
		self.hourglass = pygame.image.load(path.join(self._imageFolder, "hourglass.png"))
		self.explosion = pygame.image.load(path.join(self._imageFolder, "boom.png"))
		self.inspectorbutton = pygame.image.load(path.join(self._imageFolder, "inspectorbutton.png"))
		#self.check = pygame.image.load(path.join(self._imageFolder, "check.png"))
		self.avatar = pygame.image.load(path.join(self._imageFolder, "child.png"))

		
		
		#
		# Load the "key" images
		#
		for filepath in os.listdir(self._keyImageFolder) :
			filename = os.path.basename(filepath)
			
			# Ignore hidden files/directorys (such as .svn)
			if filename[0] == '.' :
				continue
				
			basename = filename.split(".")[0]
			self._keyImages[basename] = pygame.image.load(path.join(self._keyImageFolder, filename))

	# Draw an image centered on a surface. Returns the destination rectangle
	# the image draws in so we can dirty it if necessary.
	def DrawCentered(self, surface, image) :
		w = image.get_width()
		h = image.get_height()
		rectDest = pygame.Rect((surface.get_width() - w) / 2, (surface.get_height() - h) / 2, w, h)
		rectSrc = pygame.Rect(0, 0, w, h)
		surface.blit(image, rectDest, rectSrc)
		return rectDest
	
	# Returns a key image by name
	def KeyImage(self, name) :
		return self._keyImages[name]
		
	def LoadAvatar(self, flag):
		if flag == True:
			self.avatar = pygame.image.load(path.join(self._imageFolder, "child.png"))
			self.avatarIdle(self._avatarFolder, "AvatarIdle")
			self.avatarRun(self._avatarFolder, "AvatarRun")
		else:
			self.avatar = pygame.image.load(path.join(self._imageFolder, "child_girl.png"))
			#self.avatarIdle(self._avatarFolder, "AvatarIdleGirl")
			#self.avatarRun(self._avatarFolder, "AvatarRunGirl")
		
