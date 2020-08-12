from dataclasses import dataclass

class VStrip:
	def __init__(self, strip):
		self.strip = [(0, 0, 0, 0) for _ in range(strip.numPixels())]

	def setPixelColor(self, i, color):
		self.strip[i] = color

	def numPixels(self):
		return len(self.strip)

	def getPixelColor(self, i):
		return self.strip[i]

	def show(self):
		pass

