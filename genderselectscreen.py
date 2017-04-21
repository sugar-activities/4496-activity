import pygame
from gamescreen import *
from pygame.locals import *

#
# The gender selection screen
#

class GenderSelectScreen(GameScreen):
	def __init__(self, game) :
		GameScreen.__init__(self, game, "genderselect.jpg")
		self._draw = True
		self._time = 0
		self._voiceActive = False
		
	def Unprepare(self) :
		self.SoundManager.FadeVoice(1000)

	def Update(self, delta) :
		GameScreen.Update(self, delta)
		self._time += delta
		if not self._voiceActive and self._time > 1000 :
			self._voiceActive = True
			self.SoundManager.PlayVoice('01.ogg')

	def KeyHandler(self, event):
		if event.key == K_j or event.key == K_KP7 or event.key == K_SPACE  :
			print "Selected Boy"
			self.game.SetBoy(True)
			self.game.AdvanceState()
		elif event.key == K_l or event.key == K_KP1 :
			print "Selected Girl"
			self.game.SetBoy(False)
			self.game.AdvanceState()
