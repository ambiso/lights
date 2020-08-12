import threading
import time

from rpi_ws281x import PixelStrip, ws, Color

from src import app
from src import animations

from src.helpers import clear, getPixels

# LED strip configuration:
LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 10      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.WS2811_STRIP_GRB
#LED_STRIP      = ws.SK6812W_STRIP


curr_brightness = int(0.05 * 255)
curr_animation = 'sparkle'
def run():
	prev_animation = None
	prev_brightness = None
	strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	strip.begin()
	for i in range(LED_COUNT):
		strip.setPixelColor(i, Color(0, 0, 255))
		if i > 0:
			strip.setPixelColor(i, Color(0, 0, 0))
		strip.show()


	threading.Thread(target=app.run).start()
	print('Press Ctrl-C to quit.')
	try:
		while True:

			if curr_animation != prev_animation:
				fn = animations[curr_animation]
				print('animation changed {} with function {}'.format(prev_animation, curr_animation))
				prev_animation = curr_animation
				clear(strip)
				gen = fn(strip)
			if curr_brightness != prev_brightness:
				strip.setBrightness(curr_brightness)
				prev_brightness = curr_brightness
				
			
			next(gen)
			
			t0 = time.perf_counter()
			pixels = getPixels(strip)
			# print(round(time.perf_counter() - t0, 4))
			# print(pixels)
	except KeyboardInterrupt:
		clear(strip)


		
