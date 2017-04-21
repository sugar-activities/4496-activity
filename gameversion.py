import pygame

#
# This class defines a local version of the game, specifying
# the directories and any constants to use.
#

class GameVersion :
	# The default screen size
	DefaultScreenSize = (1200, 825)
		
	# Caption for the window
	Caption = 'uxo'
	
	# Location
	Location = "cambodia"

	# A folder containing basic game images
	ImageFolder = Location + '/image'
	
	# A folder with they key (number) images
	KeyImageFolder = Location + '/keyimage'
	
	# Voice folder
	VoiceFolder = Location + '/KhmerVoice'
	
	# Levels folder
	LevelsFolder = Location + '/levels'
	
	# Cells folder
	CellsFolder = Location + '/cells'
	
	# Pet folder
	PetFolder = Location + '/pet'
	
	# Music folder
	MusicFolder = Location + '/music'
	
	#Avatar folder
	AvatarFolder = Location + '/avatar'
	
	InspectorFolder = Location + '/inspector'
	
	
	try:
		import olpcgames, olpcgames.util
		if not olpcgames.ACTIVITY: raise RuntimeError
		# Do something for the OLPC
		PC = False
	except (RuntimeError,ImportError):
		# do something as you would usually do that something
		#PC Version
		PC = True
	
	#sound_folder = 'sound'
	#button_folder = 'image/Buttons/olpc'
	
	#background_folder = 'image/background'
	#pet_folder = 'image/background'
	#music_folder = 'music'
	#composite_folder = 'CompXML'
	#element_folder = 'ElementXML'
