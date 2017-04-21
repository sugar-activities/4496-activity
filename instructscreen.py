import pygame
from gamescreen import *


class InstructScreen(GameScreen):
	def __init__(self, game):
		GameScreen.__init__(self, game, "homescreen.jpg")
		self._draw = True
		self._time = 0
		self._voiceActive = False
		self._state = "Start"
		self._leftLoc = (570,400)
		self._rightLoc = (630,400)
		self._upLoc = (600,370)
		self._downLoc = (600,430)
		self._leftRect = Rect(0,0,0,0)
		self._fullRect = Rect((570,370),(630 + self.ImageManager.right.get_size()[0], 430 + self.ImageManager.down.get_size()[1]))
		
	#def GetDisplay(self) :
	#	return self._screen.Display
	#	
	#Display = property(GetDisplay)
		
	
	def Unprepare(self) :
		self.SoundManager.FadeVoice(1000)

	def Update(self, delta) :
		GameScreen.Update(self, delta)
		self._time += delta
		if self._state == "Start":
			if self._time > 2000:
				self._state = "LeftPress"
				self._time = 0
		if self._state == "LeftMove":
			self._leftLoc = (self._leftLoc[0] - 35 * float(delta) / 100, self._leftLoc[1])
			newRect = Rect(self._leftLoc, self.ImageManager.left.get_size())
			self.DirtyRects.Redraw(self._leftRect.union(newRect))
			self._leftRect = newRect
			if self._leftLoc[0] < 50:
				self._leftLoc = (50, self._leftLoc[1])
				self._state = "LeftOnly"

		self.RedrawAll()

	def KeyHandler(self, event):
		if event.key == K_j or event.key == K_KP7 or event.key == K_SPACE  :
			self.game.AdvanceState()
		if event.key == K_a or event.key == K_KP4 or event.key == K_LEFT:
			if self._state == "LeftPress" or self._state == "Start":
				self._state = "LeftMove"
			if self._state == "LeftOnly":
				self.game.AdvanceState()
			
	def Draw(self):
		GameScreen.Draw(self)
		if self._state == "Start" or self._state == "LeftMove" or self._state == "LeftPress":
			for rect in self.GetDrawRects():
				loc = (-self._leftLoc[0] + self.ImageManager.left.get_width() /2, -self._leftLoc[1] + self.ImageManager.left.get_height()/2)
				rectLeft = rect.move(loc)
				self.Display.blit(self.ImageManager.left, rect, rectLeft)
				loc = (-self._upLoc[0] + self.ImageManager.up.get_width() /2, -self._upLoc[1] + self.ImageManager.up.get_height()/2)
				rectUp = rect.move(loc)
				self.Display.blit(self.ImageManager.up, rect, rectUp)
				loc = (-self._rightLoc[0] + self.ImageManager.right.get_width() /2, -self._rightLoc[1] + self.ImageManager.right.get_height()/2)
				rectRight = rect.move(loc)
				self.Display.blit(self.ImageManager.right, rect, rectRight)
				loc = (-self._downLoc[0] + self.ImageManager.down.get_width() /2, -self._downLoc[1] + self.ImageManager.down.get_height()/2)
				rectDown = rect.move(loc)
				self.Display.blit(self.ImageManager.down, rect, rectDown)
			self.Display.DrawLine((255,255,255), (565,350), (0, 725), 4)
			self.Display.DrawLine((255,255,255), (632,450), (0, 800), 4)
		if self._state == "LeftPress":
			drawLoc = (self._leftLoc[0] - self.ImageManager.left.get_width() /2 -10, self._leftLoc[1] - self.ImageManager.left.get_height()/2 -10)
			drawRect = Rect(drawLoc[0], drawLoc[1], self.ImageManager.left.get_size()[0]+10, self.ImageManager.left.get_size()[1]+10)
			self.Display.DrawEllipse((0,255,0),drawRect, 3)
		if self._state == "LeftOnly":
			for rect in self.GetDrawRects():
				loc = (-self._leftLoc[0] + self.ImageManager.left.get_width() /2, -self._leftLoc[1] + self.ImageManager.left.get_height()/2)
				rectLeft = rect.move(loc)
				self.Display.blit(self.ImageManager.left, rect, rectLeft)

			
				
			
			
		
			
		