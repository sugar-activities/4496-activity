import sys, pygame
import xml.dom.minidom
from gamescreen import *
from cellfactory import *
from level import *
from cell import *
from util import *
from map import *
from animation import *

#
# The Level class manages a level in the game. A level consists of
# an array of cells. A level is also a game screen, but dynamically
# assigns the background images based on the current cell.
#
# This is the factory class that creates a level.
#

class LevelFactory :


	def __init__(self, game) :
		self._game = game
		self._cellFactory = CellFactory(game)
		
	# Load the level from an XML file
	#<level size="4, 5" start="2,2" startdir="1">
	# <row>
	#	  <cell/>
	#	  <cell xml="1/0-1.xml"/>
	#	  <cell xml="1/0-2.xml"/>
	#	  <cell xml="1/0-3.xml"/>
	#	  <cell/>
	# </row>
	# </level>

	def Create(self, filename) :
		#
		# Create the level object
		#
		level = Level(self._game)

		

		#
		# Load the XML level description
		#
		xmlDoc = xml.dom.minidom.parse(path.join(self._game.version.LevelsFolder, filename))
		root = xmlDoc.documentElement
		level.size = ScanPair(root.getAttribute('size'))
		level.start = ScanPair(root.getAttribute('start'))
		level.startdir = int(root.getAttribute('startdir'))
		level.music = root.getAttribute('music')
		
		for node in root.childNodes :
			if node.nodeName == 'row' :
				self.LoadRow(level, node)
			elif node.nodeName == 'map' :
				self.LoadMap(level, node)
			elif node.nodeName == 'home' :
				self.LoadHome(level, node)

		#
		# Set the border cells
		#
		for i in range(0, level.size[0]) :
			level.cells[i][0].Border = True
			level.cells[i][level.size[1]-1].Border = True
			
		for i in range(0, level.size[1]) :
			level.cells[0][i].Border = True
			level.cells[level.size[0]-1][i].Border = True
		
		return level
	
	# Load the contents of an xml <row> tag. This is
	# one row of a level.
	def LoadRow(self, level, node) :
		row = []
		for child in node.childNodes :
			if child.nodeName == 'cell' :
				# We have a cell
				cell = self.LoadCell(child)
				if cell.HasFood:
					level.FoodLocation = (len(row),len(level.cells))
				row.append(cell)

				
		level.cells.append(row)

	# Load the contents of an xml <cell> tag. This is
	# one cell in a row.
	def LoadCell(self, node) :
		cellxml = node.getAttribute('xml')
		return self._cellFactory.Load(cellxml)
		
	def LoadHome(self, level, node):
		cellxml = node.getAttribute('xml')
		level.homecell = self._cellFactory.Load(cellxml)
	

		

	# Load the xml that describes the map
	# <map img="map1.png" tl="38, 38" br="217,217" foodIcon="foodIcon.png" playerIcon="playerArrow.png"/>
	def LoadMap(self, level, node) :
		# Create map object and attach to level
		map = Map(level)
		level.Map = map
		# Get the attributes
		imgFilename = node.getAttribute('img')
		tl = ScanPair(node.getAttribute('tl'))
		br = ScanPair(node.getAttribute('br'))
		foodIconName = node.getAttribute('foodIcon')
		foodIcon = pygame.image.load(path.join(self._game.version.ImageFolder, foodIconName))
		map.FoodIcon = foodIcon
		playerIconName = node.getAttribute('playerIcon')
		playerIcon = pygame.image.load(path.join(self._game.version.ImageFolder, playerIconName))
		map.PlayerIcon = playerIcon
		map.SetBounds(tl, br)
		# Get the image
		img = pygame.image.load(path.join(self._game.version.LevelsFolder, imgFilename))
		map.Image = img

	

		
