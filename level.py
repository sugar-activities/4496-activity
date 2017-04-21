import sys, pygame
import xml.dom.minidom
from gamescreen import *
from util import *
from pygame.locals import *
from background import *
from animation import *

#
# The Level class manages a level in the game. A level consists of
# an array of cells. A level is also a game screen, but dynamically
# assigns the background images based on the current cell.
#

class Level(GameScreen) :
	NORTH = 0
	EAST = 1
	SOUTH = 2
	WEST = 3
	
	StuckCount = 4
	
	VoiceDelay = 200
	
	ExplosionTime = 3000
	#InspectorTime = 4000
	CircleTime = 7000
	FoodTime = 7000
	
	# Locations for the arrow graphics
	LEFT = (-10, -(412-92))
	RIGHT = (-(1200-10-127), -(412-92))
	UP = (-(600-92), -10)
	INSPECTOR_BUTTON = (-(40), 0)
	
	EXPLOSION_LOCATION = (-(600-400), -(412-300))
	RIGHT_INSPECTOR_LOCATION = (-(800-72), -(412-200))
	LEFT_INSPECTOR_LOCATION = (-(400-72), -(412-200))

	
	def __init__(self, game) :
		GameScreen.__init__(self, game, "")
		# The size of the level - Overwritten by factory
		self.size = (3, 3)
		# Starting location in the level - Overwritten by factory
		self.start = (1, 1)
		# Starting direction
		self.startdir = self.NORTH
		# The level cells - Set by factory
		self.cells = []
		# Music for the level - Set by factory
		self.music = ""
		#the "home" cell
		self.homecell = None
		self._home = True
		
		self._inspectorLoc = Level.RIGHT_INSPECTOR_LOCATION
				
		# Initialization
		self.loc = self.start
		
		# The current cell is the cell we are located in
		self.currCell = None
		
		# The view cell is the cell that we are looking at
		self.viewCell = None
		
		# The preview cell is the cell we were looking at
		# last before we look at this cell
		self._prevCell = None
		
		# The direction we are looking
		self.dir = self.NORTH
		self._map = None
		self._pet = game.Pet
		self._pet.SetLevel(self)
		self._avatar = game.Avatar
		self._avatar.SetLevel(self)
		self._cellTime = 0
		self._inspector = game.Inspector
		self.FoodLocation = (1,1)

		self._state = "None"
		self._stateTime = 0
		
		# The view counter is incremented each time we
		# view a new cell
		self._viewCount = 0

		
	#
	# Properties
	#
	
	def GetMap(self) : return self._map
	def SetMap(self, map) : self._map = map
	def GetDir(self) : return self.dir
	def GetAngle(self) :
		if self.dir == self.NORTH : return 0
		if self.dir == self.EAST : return 90
		if self.dir == self.SOUTH : return 180
		return 270
	def GetLocation(self) : return self.loc
   
	
	Location = property(GetLocation)	
	Map = property(GetMap, SetMap)
	Dir = property(GetDir)
	Angle = property(GetAngle)
	
	# The screen is about to be displayed. Prepare the level
	# for display.
	def Prepare(self) :
		# Set the staring point
		self.dir = self.startdir
		self.SetLoc(self.start, Background.NONE)
		
		# Handle placement of any of the mounts in
		# the cells.
		for row in self.cells :
			for cell in row :
				cell.Prepare()
		# Start the music
		self.SoundManager.SelectMusic(self.music)
	
	# Set the current location (cell)
	def SetLoc(self, loc, transition) :
		self.loc = loc
		self.cellTime = 0
		self.currCell = self.CurrentCell()
		self.currCell.VisitCount += 1
		self.SetView(transition)
		
	# Set the view based on the current cell and direction
	# Sets self.viewCell to the cell we are viewing
	def SetView(self, transition) :
		# Determine where we are looking, the new view cell
		newViewCell = self.ForwardCell()
		if newViewCell != self.viewCell :
			# We are looking at a new cell, save what we
			# were looking at as the previous cell
			self._prevCell = self.viewCell
			self._viewCount = self._viewCount + 1
		self.viewCell = newViewCell
		self.backCell = self.BackCell()
		#Write to log file: Location, Direction, Mounts
		if self._home:
			self.game.logger.WriteLine("Home")
		else:
			self.game.logger.WriteLine(str(self.loc) + ";" + str(self.DirectionVector())+";"+self.viewCell.MountString())
		self.viewCell.viewCount = self._viewCount
		self.viewCell.PrepareView(self.dir)
		if self.viewCell.BadMountSide() == "Left":
			self._inspectorLoc = Level.LEFT_INSPECTOR_LOCATION
		else:
			self._inspectorLoc = Level.RIGHT_INSPECTOR_LOCATION
		self.background.Transition(self.viewCell.image, transition)
		self.ClearMemory()
	
	# This function releases memory allocated to images that have not been viewed
	# in a while.
	def ClearMemory(self) :
		for row in self.cells :
			for cell in row :
				if cell.viewCount < self._viewCount - 5 :
					cell.ReleaseImage()

		#self.RedrawAll()
	
	def Unprepare(self) :
		self._map = None
		self._pet = None

	# Update, advancing the management of the level by a defined period
	def Update(self, delta) :
		GameScreen.Update(self, delta)
		self._map.Update(delta)
		self._pet.Update(delta)
		self._avatar.Update(delta)
		self._cellTime = self._cellTime + delta
		self._stateTime = self._stateTime + delta

		if self.background.Running:
			return
		elif self._state == "Food":
			if self._stateTime > Level.FoodTime:
				self.game.AdvanceState()
		elif self._state == "Inspector":
			self._inspector.Update(delta)
			if self._inspector.Finished:
				self._inspector.Reset()
				self.AdvanceState("None")
		elif self._state == "Explosion":
			if self._stateTime > Level.ExplosionTime:
				self.AdvanceState("Circle")
		elif self._state == "Circle":
			self._inspector.Update(delta)
			if self._stateTime > 2000 and self._stateTime - delta < 2000: 
				self.SoundManager.PlayVoice("19.ogg")
			if self._inspector.Finished:
				self._inspector.Reset()
				self.AdvanceState("Home")
			
		if self._cellTime > Level.VoiceDelay and self.viewCell.voiceOnce != '' :
			#print 'Playing %s' % self.viewCell.voiceOnce
			self.SoundManager.PlayVoice(self.viewCell.voiceOnce)
			self.viewCell.voiceOnce = ''

			
	   			
	
	# Draw the game screen
	def Draw(self) :
		# Base class version handles the background
		GameScreen.Draw(self)
		cell = self.viewCell

		if not self.background.Running :
			# Normal case, just draw the cell content
			for rect in self.GetDrawRects() :
				cell.Draw(self.Display, rect)
		else :
			# When we are transitioning the background,
			# we only draw the rectagles that intersect
			# with the next background we are drawing.
			for rectClip in self.GetDrawRects() :
				rectNew = rectClip.clip(self.background.newRect)
				cell.Draw(self.Display, rectNew)
				if self._prevCell != None :
					rect = rectClip.clip(self.background.prevRectL)
					self._prevCell.Draw(self.Display, rect)
					rect = rectClip.clip(self.background.prevRectR)
					self._prevCell.Draw(self.Display, rect)
	
			
		# Draw the controls on the screen if needed
		if not self.background.Running and self._state == "None":
			self.DrawInterface()
		elif self._state == "Explosion":
			for rect in self.GetDrawRects():
				rectExp = rect.move(Level.EXPLOSION_LOCATION)
				self.Display.blit(self.ImageManager.explosion, rect, rectExp)	
		elif self._state == "Circle":
			cell.DrawCircle(self.Display, rect)
			for rect in self.GetDrawRects():
				rectIns = rect.move(self._inspectorLoc)
				self.Display.blit(self._inspector.Image, rect, rectIns)
		elif self._state == "Inspector":
			cell.DrawCircle(self.Display, rect)
			for rect in self.GetDrawRects():
				rectIns = rect.move(self._inspectorLoc)
				self.Display.blit(self._inspector.Image, rect, rectIns)
		self._map.Draw(self.GetDrawRects())
		self._pet.Draw(self.GetDrawRects())
		self._avatar.Draw(self.GetDrawRects())

	#Draw all needed user controls
	def DrawInterface(self):
		for rect in self.GetDrawRects() :
			rectLeft = rect.move(Level.LEFT)
			self.Display.blit(self.ImageManager.left, rect, rectLeft)

			if not self._home:
				rectRight = rect.move(Level.RIGHT)
				self.Display.blit(self.ImageManager.right, rect, rectRight)	 					
				if (self.CanMoveForward()) :
					rectUp = rect.move(Level.UP)
					self.Display.blit(self.ImageManager.up, rect, rectUp)
				if not self.viewCell.Inspected:
					rectInsp = rect.move(Level.INSPECTOR_BUTTON)
					self.Display.blit(self.ImageManager.inspectorbutton, rect, rectInsp)

	def KeyHandler(self, event):
		# No keystroke handling during transitions
		if self.background.Running or self._state != "None":
			return
		if event.key == K_a or event.key == K_KP4 or event.key == K_LEFT :
			if self.LeaveHome():
				return
			# Left
			self.Turn(False)
		elif event.key == K_d or event.key == K_KP6 or event.key == K_RIGHT :
			# Right
			self.Turn(True)
		elif event.key == K_w or event.key == K_KP8 or event.key == K_UP:
			# Forward, move into the view cell if it is navigable
			self.MoveForward()
		elif event.key == K_s or event.key == K_KP2 or event.key == K_DOWN:
			self.MoveBack()
		elif event.key == K_k or event.key == K_KP1:
			if self._home or self.viewCell.Inspected:
				return
			self.AdvanceState("Inspector")
		elif event.key == K_m:
			self.OutputStuff()
		elif event.key == K_1 :
			self.game.AdvanceState()
			
	def OutputStuff(self):
		print "Location:", self.loc, "Direction:", self.dir
			
		
			
	
	# Handle a turn in place
	def Turn(self, right) :
		if right :
			if self._home:
				return
			self.dir = self.dir + 1
			if self.dir > 3 : self.dir = 0
			self.SetView(Background.RIGHT)
			self._avatar.MoveTurn(True)
		else :
			if self.LeaveHome():
				self._avatar.MoveTurn(False)
				return
			self.dir = self.dir - 1
			if self.dir < 0 : self.dir = 3
			self.SetView(Background.LEFT)
			self._avatar.MoveTurn(False)
	
	def CanMoveForward(self):
		if self.viewCell.Border or self._home or self.viewCell.Inspected:
			return False
		if (not self.currCell.StuckDir[self.dir]) and self.currCell.VisitCount > Level.StuckCount:
			return False
		return True
	
	# Handle a request to move forward
	def MoveForward(self) :
		if not self.CanMoveForward():
			return
		elif self.viewCell.IsBad():
			self.AdvanceState("Explosion")
		elif self.viewCell.HasFood:
			self.AdvanceState("Food")
		else:
			dirvec = self.DirectionVector()
			self.SetLoc(AddTuples(self.loc, dirvec), Background.FORWARD)
			self._avatar.MoveForward()
			
	
	def MoveBack(self) :
		if self._home: 
			return
		if not self.BackCell().VisitCount > 0:
			return
		if self.currCell.VisitCount > Level.StuckCount and not (self.currCell.StuckDir[(self.dir + 2) % 4]):
			return
		self.SetLoc(SubTuples(self.loc, self.DirectionVector()), Background.BACK)
			

	# Returns the current cell we are in
	def CurrentCell(self) :
		return self.cells[self.loc[0]][self.loc[1]]
	
	# Returns the cell we see if we look forward from our
	# current position.
	def ForwardCell(self) :
		if self._home:
			return self.homecell
		dirvec = self.DirectionVector()
		forward = AddTuples(self.loc, dirvec)
		return self.cells[forward[0]][forward[1]]
	
	def BackCell(self) :
		dirvec = self.DirectionVector()
		back = SubTuples(self.loc, dirvec)
		#print "Loc:", self.loc, "Dir:", self.DirectionVector(), "Back", back
		return self.cells[back[0]][back[1]]
	
	def DirectionVector(self) :
		if self.dir == self.NORTH : return (-1, 0)
		if self.dir == self.SOUTH : return (1, 0)
		if self.dir == self.EAST : return (0, 1)
		if self.dir == self.WEST : return (0, -1)
	
	def LeaveHome(self):
		if not self._home:
			return False
		self._home = False
		self.SetLoc(self.start, Background.FORWARD)
		return True
		
	#Does actions needed on state change	
	def AdvanceState(self, state):

		self._stateTime = 0
		self._state = state
		self.RedrawAll()
		if state == "Explosion":
			#explode
			self.game.logger.WriteLine("Explode")
			self._pet.Explode()	
			self._avatar.Explode()
			self.SoundManager.PlayVoice("explosion.ogg")
		elif state == "Food":
			#Food has been found, evolve pet, advance level
			self.game.logger.WriteLine("Got Food")
			self._pet.Feed()
			self.SoundManager.FadeMusic(100)
			self.SoundManager.SelectMusic("upbeat1.ogg")
		elif state == "Circle":
			self.SoundManager.PlayVoice("alarm.ogg")
		elif state == "Inspector":
			if self.viewCell.IsBad():
				self.SoundManager.PlayVoice("10.ogg")
				self.viewCell.Inspected = True
				self._pet.MakeHappy()
			else:
				self.SoundManager.PlayVoice("11.ogg")
				self._pet.MakeSad()
		elif state == "Home":
			self._state = "None"
			if self.homecell != None:
   				self._home = True
   				self.dir = self.startdir
   				self.SetLoc(self.start, Background.NONE)
			elif self.homecell == None:
				#no home cell behavior?
				self.dir = self.startdir
				self.SetLoc(self.start, Background.FORWARD)
				
		
