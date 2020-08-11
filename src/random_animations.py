from rpi_ws281x import Color

from .helpers import clear, fill

def rojava(strip):
	while True:
		for i in range(50):
			strip.setPixelColor(i, Color(255,255,0))
		for i in range(50, 100):
			strip.setPixelColor(i, Color(255,0,0))
		for i in range(100, 150):
			strip.setPixelColor(i, Color(0,255,0))

		for i in range(150, 200):
			strip.setPixelColor(i, Color(0,255,0))
		for i in range(200, 250):
			strip.setPixelColor(i, Color(255,0,0))
		for i in range(250, 300):
			strip.setPixelColor(i, Color(255,255,0))
		strip.show()

def strobe(strip):
	while True:
		fill(strip, Color(255,255,255))
		fill(strip, Color(0,0,0))
		time.sleep(1/11)
		#time.sleep(1/(((sin(i/10) + 1)/2 * 3) + 4))
		#time.sleep((sin(i/10) + 1)/2 * 0.2)
		yield
		
def stack(strip, color_provider, wait_ms=10):
	clear(strip)
	for i in range(strip.numPixels()):
		color = next(color_provider)
		for j in range(strip.numPixels() - i):
			strip.setPixelColor(j, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			strip.setPixelColor(j, 0)
		strip.setPixelColor(strip.numPixels() - i - 1, color)

def rainbowCycle(strip, wait_ms=20):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	steps = 256
	color_map = gen_color_map(strip.numPixels(), steps)
	while True:
		for j in range(steps):
			for i in range(strip.numPixels()):
				col = color_map[j%steps*strip.numPixels()+i]
				strip.setPixelColor(i, Color(*col))
			strip.show()
			time.sleep(wait_ms/1000.0)