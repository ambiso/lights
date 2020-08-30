import random
from rpi_ws281x import Color
import math

def fireworks(strip):
	while True:
		for pos in range(strip.numPixels()):
			r = random.uniform(0., 100.)
			r = int(r * r / 100)
			g = random.uniform(0., 100.)
			g = int(g * g / 100)
			b = random.uniform(0., 100.)
			b = int(b * b / 100)
			#r = int(math.sqrt(r * 100) * 2.55)

			strip.setPixelColor(pos, Color(r, g, b))
		strip.show()
		yield
