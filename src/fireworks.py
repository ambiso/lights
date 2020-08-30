import random
from rpi_ws281x import Color
import math

def fireworks(strip):
	t = 0.1
	while True:
		for pos in range(strip.numPixels()):
			v = (math.sin(t) + 1) / 2 / t * 10
			v = int(v)
			strip.setPixelColor(pos, Color(v, v, v))
		strip.show()
		yield
		t += 0.1
