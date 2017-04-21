import pygame
from gamescreen import *
from pygame.locals import *

#
# The splash screens class. Displays first and second
#

class SplashScreen(GameScreen) :
	
		
	def __init__(self, game, name, mintimeout, maxtimeout):
		GameScreen.__init__(self, game, name)
		self._delay = maxtimeout
		self._holdtime = mintimeout
		
	def Update(self, delta) :
		GameScreen.Update(self, delta)
		self._delay -= delta
		self._holdtime -= delta
		if self._delay <= 0 :
			self.game.AdvanceState()


	def KeyHandler(self, event):
		if event.key == K_SPACE and self._holdtime <= 0:
			self.game.AdvanceState()
