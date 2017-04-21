from datalogger import *

import olpcgames, pygame, logging, gc
from pygame.locals import *

from gameversion import *
from splashscreen import *
from genderselectscreen import *
from instructscreen import *
from level import *
from levelfactory import *
from imagemanager import *
from soundmanager import *
from dirtyrects import *
from pet import *
from avatar import *
from displaymanager import *

#
# This is the main class the defines the game.
#

class GameUxo :
	def __init__(self) :
		self.version = None
		self.currentScreen = None
		self.state = "Start"
		self._newstate = False
		self._imageManager = None
		self._soundManager = None
		self._dirtyRects = None
		self._display = None
		self._pet = None
		self._avatar = None
		self.logger = Datalogger()
		self.logger.WriteLine("Game Start")

		
		
		# True as long as the program is running
		self._running = True
		
		# If true, we need to advance the game screens state machine
		self._pendingAdvance = False
		
		# Until we know otherwise
		self.boy = True
		
	
	#
	# Properties
	#
	
	def GetImageManager(self) :
		return self._imageManager
	
	def GetSoundManager(self) :
		return self._soundManager
	
	def GetDirtyRects(self) :
		return self._dirtyRects
	
	def GetDisplay(self) :
		return self._display
	
	def GetPet(self) :
		return self._pet
		
	def GetAvatar(self):
		return self._avatar
	
	def GetVersion(self) :
		return self.version
		
	def GetBoy(self): 
		return self.boy
		
	def SetBoy(self, flag):
		self.logger.WriteLine("Boy: " + str(flag))
		self._avatar.Load(flag)
		self.boy = flag
		
	def GetInspector(self): 
		return self._inspector
	
	def SetInspector(self, inspector):
		self._inspector = inspector
	
	
	ImageManager = property(GetImageManager)
	SoundManager = property(GetSoundManager)
	DirtyRects = property(GetDirtyRects)
	Display = property(GetDisplay)
	Pet = property(GetPet)
	Avatar = property(GetAvatar)
	Version = property(GetVersion)
	Boy = property(GetBoy, SetBoy)
	Inspector = property(GetInspector, SetInspector)
	
	
	#
	# Main entry point for the game execution
	#
	def Go(self) :  
		#
		# Define and create the screen and clock
		#
		size = self.version.DefaultScreenSize
		self.logger.WriteLine("Voice: " + self.version.VoiceFolder)
		if self.version.PC:
			self._display = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		else:	
			self._display = pygame.display.set_mode(size)	
		pygame.display.set_caption(self.version.Caption)

		self._display = DisplayManager(self._display)
		clock = pygame.time.Clock()
		pygame.mouse.set_visible(False)
		
		#Turn off mouse motion events for preformance
		pygame.event.set_blocked(MOUSEMOTION)

		
		#
		# The dirty rectangle manager
		#
		self._dirtyRects = DirtyRectsManager(self._display)
		
		#
		# Create other objects
		#
		self._imageManager = ImageManager(self.version, self.logger)
		self._soundManager = SoundManager(self.version, self.logger)
		self._pet = Pet(self)
		self._inspector = Animation(self.version.InspectorFolder, 'Stop')
		self._avatar = Avatar(self)
		
		#
		# When the class starts, we are in the "Start" state
		# Advance now to the first valid state.
		#
		
		self.AdvanceStateActual()
		
		#
		# The main game loop
		#
		
		self._running = True
		while self._running:
			# Amount of time that has passed in milliseconds
			delta = clock.tick(30)
			#print "Clock " + str(delta)
			#sys.stdout.flush()
			
			#
			# Handle any events
			#
			events = pygame.event.get()
			if events:
				for event in events:
					if event.type == pygame.KEYDOWN:
						self.currentScreen.KeyHandler(event)
						if event.key == K_ESCAPE :
							self._running = False
					elif event.type == pygame.QUIT:
						print "Recieved quit"
						sys.stdout.flush()
						self._running = False
					elif event.type == pygame.VIDEOEXPOSE or event.type == pygame.VIDEORESIZE:
						self.currentScreen.RedrawAll()

			#
			# Update
			#
			self.currentScreen.Update(delta)
			
			if self.version.PC:
				self._dirtyRects.RedrawAll()
			
			#
			# Draw the current screen.
			#
			self.currentScreen.Draw()
			
			if self.version.PC:
				self._display.Flip()
			
			#
			# Do any updates on the screen screen
			#

			self._dirtyRects.Update()
			
			
			
			sys.stdout.flush()
			#
			# Handle any activities when a state becomes active and
			# has been drawn for the first time. This is where we will
			# do any preloading for other states.
			#
			if self._newstate :
				if self.state == "Splash1" :
					# Do loading during the first splash screen
					self.Splash1Loading()
				elif self.state == "Splash2" :
					self.Splash2Loading()
				   
					
			#
			# End of loop activities
			#
			self._newstate = False
			
			#
			# Handle any pending advance
			#
			if self._pendingAdvance :
				self._pendingAdvance = False
				self.AdvanceStateActual()


	# This function is called while the first splash screen is
	# displayed. It can be used for loading content.
	def Splash1Loading(self) :
		self._imageManager.Load1()
	
	# This function is called while the second slash screen is
	# displayed.
	def Splash2Loading(self) :
		self._pet.Load()
		self._inspector.Load()
		

	#
	# The main game screens state machine
	#
	
	def AdvanceState(self) :
		self._pendingAdvance = True
		
	def AdvanceStateActual(self) :
		#
		# Clear the current state
		#
		self._pendingAdvance = False
		if(self.currentScreen != None) :
			self.currentScreen.Unprepare()
			self.currentScreen = None
			gc.collect()
		
		#
		# Switch to the new state
		#
		
		if self.state == "Start":
			self.SoundManager.SelectMusic(SoundManager.Upbeat)
			self.currentScreen = SplashScreen(self, "credit.jpg", 0, 5000)
			self.state = "Splash1"
		elif self.state == "Splash1" :
			self.currentScreen = SplashScreen(self, "splashscreen.jpg", 0, 5000)
			self.state = "Splash2"
		elif self.state == "Splash2" :
			self.currentScreen = SplashScreen(self, "directionScreen.jpg", 5000, 10000)
			self.state = "Splash3"
		elif self.state == "Splash3" :
			self.currentScreen = GenderSelectScreen(self)
			self.state = "GenderSelect"
		elif self.state == 'GenderSelect':
			self.SoundManager.FadeMusic(1000)
			self.StartLevel('Tutorial', 'tutorial.xml')
	   	elif self.state == "Tutorial":
	   		self.SoundManager.FadeMusic(1000)
	   		self.StartLevel("Level1", "1.xml")
	   	elif self.state == "Level1":
	   		self.SoundManager.FadeMusic(1000)
	   		self.StartLevel("Level2", "2.xml")
	   	elif self.state == "Level2":
			self.SoundManager.FadeMusic(1000)
	   		self.StartLevel("Level3", "3.xml")
	   	elif self.state == "Level3":
			self.SoundManager.FadeMusic(1000)
	   		self.StartLevel("Level4", "4.xml")
	   	elif self.state == "Level4":
	   		self.SoundManager.FadeMusic(1000)
	   		self.StartLevel("Level5", "5.xml")
	   	elif self.state == "Level5":
	   		self.currentScreen = SplashScreen(self, "credit.jpg", 0, 2000)
	   	
		self._newstate = True
		self._dirtyRects.RedrawAll()
	
	
		#
		# Prepare the screen
		#
		
		if self.currentScreen != None :
			self.currentScreen.Prepare()
		else :
			self._running = False
		#print self.state
	
	#
	# Starting levels
	#
	
	def StartLevel(self, level, file) :
		# Clear the screen and display an hourglass
		
		self.logger.WriteLine("Level Start;" + level)
		self.Display.fill((0, 0, 0))
		self.ImageManager.DrawCentered(self.Display, self.ImageManager.hourglass)
		pygame.display.update()
		self.state = level
		factory = LevelFactory(self)
		self.currentScreen = factory.Create(file) 
	

	

	
	
