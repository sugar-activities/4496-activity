#!/usr/bin/env python

import pygame
from os import path
from gameversion import *

#
# Class SoundManager
# Manages the background music and any spoken content.
#

class SoundManager(object) :
	NoMusic = ''
	NoVoice = ''
	Upbeat = 'upbeat1.ogg'
	
	def __init__(self, version, logger) :
		self._version = version
		self._music = SoundManager.NoMusic
		self._musicSound = None
		self._logger = logger
		
		# Currently playing voice
		self._voice = SoundManager.NoVoice
		self._voiceSound = None

	# 
	# Voice playback management
	#
	
	# Load a voice so we can play it later
	# This version just returns the voice file
	# so an application can play it.
	def LoadVoice(self, filename) :
		return pygame.mixer.Sound(path.join(self._version.VoiceFolder, filename))

	# Select a voice message to play. If already playing
	# something else, fade it out and select new voice
	def PlayVoice(self, voice) :
		self._logger.WriteLine("Sound;" + voice)
		# If something playing fade it out
		self.FadeVoice(100)
		# Load the new voice sound
		self._voice = voice
		self._voiceSound = pygame.mixer.Sound(path.join(self._version.VoiceFolder, voice))
		self._voiceSound.play()
		
	def FadeVoice(self, time) :
		# If something playing fade it out
		if self._voiceSound != None :
			self._voiceSound.fadeout(time)
			self._voiceSound = None
			self._voice = ''

	#
	# Background music management
	#
	
	# Select a background music to play. If already playing
	# something else, fade it out and select new music
	def SelectMusic(self, music) :
		# Already selected?
		if music == self._music :
			return
		
		# If something playing fade it out
		self.FadeMusic(100)
			
		# Load the new background sound
		self._music = music
		self._musicSound = pygame.mixer.Sound(path.join(self._version.MusicFolder, music))
		self._musicSound.play(loops = -1)
		
	def FadeMusic(self, time) :
		# If something playing fade it out
		if self._musicSound != None :
			self._musicSound.fadeout(time)
			self._musicSound = None
			self._music = SoundManager.NoMusic
