#! /usr/bin/env python

import olpcgames, pygame, logging

pygame.init()

from gameuxo import *
from gameversion import *
from distutils import dir_util
from os import path

#__FRAMERATE__ = FRAMERATE_
#__FONTSIZE__ = 24
#__FONTX__ = 20
#__FONTY__ = 20
#__MOVE_COUNT__ = 20

log = logging.getLogger( '%(name)s run' )
log.setLevel( logging.DEBUG )



def main():
	"""The mainloop which is specified in the activity.py file
	
	"main" is the assumed function name
	"""
	
	#Copy all log files to any external drives on OLPC
	if os.path.exists("/media/") and os.path.exists("/home/olpc/Documents/UXOLOG/"):
		drives = os.listdir("/media/")
		for drive in drives:
			try:
				dir_util.copy_tree("/home/olpc/Documents/UXOLOG/", path.join("/media/", drive))
			except:
				print "Copy failed"


		
	
	#
	# Create the game object
	#
	
	game = GameUxo()
	
	#
	# Attach the game version information
	#
	
	game.version = GameVersion()
	
	#
	# Pass control to the game object
	#
	
	game.Go()
	
	#
	# Shutdown
	#
	
	pygame.display.quit()
	raise SystemExit

if __name__ == "__main__":
	logging.basicConfig()
	main()


