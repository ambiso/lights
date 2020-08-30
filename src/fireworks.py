import random
from rpi_ws281x import Color

def fireworks(strip):
	while True:
		for pos in range(strip.numPixels()):
			r = random.uniform(0., 1.)
			r = int(r * r * r * 255)
			strip.setPixelColor(pos, Color(r, r, r))
		strip.show()
		yield
