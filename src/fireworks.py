import random

def fireworks(strip):
	while True:
		for pos in range(strip.numPixels()):
			r = random.randint(0, 255)
			strip.setPixelColor(pos, Color(r, r, r))
		strip.show()
		yield
