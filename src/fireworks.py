import random
from rpi_ws281x import Color
import math

def fireworks(strip):
	while True:
		for pos in range(strip.numPixels()):
			r = random.uniform(0., 100.)
			r = int(r * r / 100)

			strip.setPixelColor(pos, Color(r, r, r))
		strip.show()
		yield
