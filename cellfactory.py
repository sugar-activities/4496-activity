#!/usr/bin/env python

import sys, pygame
import xml.dom.minidom
from cellfactory import *
from level import *
from cell import *
from util import *

#
# class CellFactory
# Simple factory that creates cell objects.
#

class CellFactory(object) :
	def __init__(self, game) :
		self._game = game
	
	def Load(self, filename) :
		# Create the cell object
		cell = Cell()
		#print filename
		if filename != '' :
			# Load the xml file that describes the cell
			xmlDoc = xml.dom.minidom.parse(path.join(self._game.version.CellsFolder, filename))
			root = xmlDoc.documentElement
			self.LoadCellXml(cell, root)
			xmlDoc.unlink()
			del xmlDoc
		
		return cell

	# Load the the xml that describes a cell.
	# <?xml version="1.0" encoding="UTF-8"?>
	# <cell img="0-1.xml">
	# </cell>
	def LoadCellXml(self, cell, root) :
		# The cell image
		imgFilename = root.getAttribute('img')
		imgPath = path.join(self._game.version.CellsFolder, imgFilename)
		cell.SetImage(imgFilename, imgPath)
		
		stuckEast = root.getAttribute('stuckEast') != "false"
		stuckNorth = root.getAttribute('stuckNorth') != "false"
		stuckWest = root.getAttribute('stuckWest') != "false"
		stuckSouth = root.getAttribute('stuckSouth') != "false"
		cell.StuckDir = [stuckEast, stuckNorth, stuckWest, stuckSouth]
		# Simple attributes
		cell.voiceOnce = root.getAttribute('voiceonce')
		if root.getAttribute('food') == "true" :
			cell.HasFood = True
		
		for node in root.childNodes :
			if node.nodeName == 'bad' :
				self.LoadMounts(cell, node, 'bad')
			elif node.nodeName == 'good' :
				self.LoadMounts(cell, node, 'good')
			elif node.nodeName == 'fix' :
				self.LoadMounts(cell, node, 'fixed')

		# cell.Test()

	# Load the contents of the <bad>, <good>, and <fixed> tags
	# adding them to the cell.
	def LoadMounts(self, cell, root, type) :
		# Iterate over the children, looking for mount or box
		for node in root.childNodes :
			if node.nodeName == 'mount' :
				self.LoadMount(cell, node, type)
	
	# Load a tag of type <mount>
	# <mount key="birds" pos="6,21" dim="738,96" scale="0.01,0.975" />
	def LoadMount(self, cell, node, type) :
		mount = Mount()
		mount.BoxUL = ScanPair(node.getAttribute('pos'))
		dim = node.getAttribute('dim')
		if dim != "" :
			# We have a dimension
			mount.BoxSize = ScanPair(dim)
		
		if node.getAttribute('nomirror') == "true" :
			mount.NoMirror = True
			
		# Get the image key
		key = node.getAttribute('key')
		mount.SetImage(key, self._game.ImageManager.KeyImage(key))
		
		# Get the scale factor (or factors)
		scale = node.getAttribute('scale')
		if scale != "":
			# Get the image scale factors
			sp = scale.split(',')
			if len(sp) > 1 :
				mount.SetScales(float(sp[0]), float(sp[1]))
			else :
				mount.SetScales(float(sp[0]), float(sp[0]))
		else:
			mount.SetScales(1.0, 1.0)
		
		cell.AddMount(mount, type)

