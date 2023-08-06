
# imports
from syst3m.v1.classes.config import *
from syst3m.v1.classes.color import color

# the loader object class.
class Loader(threading.Thread):
	def __init__(self, message, autostart=True):
		threading.Thread.__init__(self)
		self.message = message
		if self.message[-len(" ..."):] == " ...": self.message = self.message[:-4]
		if self.message[-len("."):] == ".": self.message = self.message[:-1]
		if self.message[0].upper() != self.message[0]: self.message = self.message[1:]+self.message[0].upper()+self.message[1:]
		if autostart: self.start()
	def run(self):
		self.running = True
		while self.running:
			for i in ["|", "/", "-", "\\"]:
				print(f"{self.message} ... {i}", end="\r")
				if not self.running: break
				time.sleep(0.33)
		self.running = "stopped"
	def stop(self, message=None, success=True, response=None):
		if response == None:
			if message == None: message = self.message
		else:
			if response["error"] == None:
				message = response["message"]
			else:
				success = False
				message = "Error: "+response["error"]
		self.running = False
		for i in range(120):
			if self.running == "stopped": break
			time.sleep(0.5)
		if self.running != "stopped": raise ValueError(f"Unable to stop loader [{self.message}].")
		if success:
			print(f"{message} ... done")
		else:
			print(f"{message} ... {color.red}failed{color.end}")

# the loader object class.
class ProgessLoader(threading.Thread):
	def __init__(self, message, index=0, max=10):
		threading.Thread.__init__(self)
		self.message = message
		if self.message[-len(" ..."):] == " ...": self.message = self.message[:-4]
		if self.message[-len("."):] == ".": self.message = self.message[:-1]
		if self.message[0].upper() != self.message[0]: self.message = self.message[1:]+self.message[0].upper()+self.message[1:]
		self.index = index
		self.max = max
		self.progress = None
	def next(self, count=1):
		self.index += count
		p = round((self.index / self.max) * 100, 2)
		if p != self.progress:
			self.progress = p
			print(f"{self.message} ... {self.p}", end="\r")
	def stop(self, message=None, success=True, response=None):
		if response == None:
			if message == None: message = self.message
		else:
			if response["error"] == None:
				message = response["message"]
			else:
				success = False
				message = "Error: "+response["error"]
		if success:
			print(f"{message} ... done")
		else:
			print(f"{message} ... {color.red}failed{color.end}")
