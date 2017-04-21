import os, datetime
from os import path
#from olpcgames import camera

class Datalogger:
	def __init__(self):
		if os.path.exists("/home/olpc/Documents"):
			if not os.path.exists("/home/olpc/Documents/UXOLOG"):
				os.mkdir("/home/olpc/Documents/UXOLOG")
			#directory should exist now
			timestamp = datetime.datetime.now()
			fileName = timestamp.strftime("%y-%m-%d-%H-%M-%S")
			self.file = open(path.join("/home/olpc/Documents/UXOLOG/",fileName), "w")
			
			

		else:
			self.file = None
			
	def WriteLine(self, string):
		if self.file != None:
			timestamp = datetime.datetime.now()
			self.file.write(timestamp.strftime("%H:%M-%S;"))
			self.file.write(string)
			self.file.write("\n")
			self.file.flush()

			
	
	def Snap(self):
		pass
		#self.camera.snap_async()
		

