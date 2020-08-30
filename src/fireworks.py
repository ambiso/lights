import random
from rpi_ws281x import Color
import math

def fireworks(strip):
	t = 0.1
	rem = 1
	while True:
		for pos in range(strip.numPixels()):
			v = (math.sin(t) + 1) / 2
			v *= rem
			v = int(v * 255)
			strip.setPixelColor(pos, Color(v, v, v))
		strip.show()
		yield
		t += 1.6
		rem -= 0.01
		rem = max(rem, 0)
