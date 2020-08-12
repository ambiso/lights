import threading
import time

from rpi_ws281x import PixelStrip, ws, Color
import numpy as np

from src import app
from src import animations

from src.helpers import clear, getPixels
from .star_light import sparkle
from .trains import trains
from .vstrip import VStrip

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
curr_animations = [sparkle, trains]
generators = []

def run():
	prev_animation = None
	prev_brightness = None
	strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	strip.begin()

	threading.Thread(target=app.run).start()
	print('Press Ctrl-C to quit.')
	len_animations = None
	try:
		while True:
			if len(curr_animations) != len_animations:
				len_animations = len(curr_animations)
				clear(strip)

				generators = []
				for animation in curr_animations:
					generators.append(animation(VStrip(strip)))
			
			if curr_brightness != prev_brightness:
				strip.setBrightness(curr_brightness)
				prev_brightness = curr_brightness
				
			vstrips = []
			for gen in generators:
				vstrips.append(next(gen))
				# vstrip.reverse()

			for pos in strip.numPixels():
				col = np.array([0, 0, 0])
				transparency = 1
				for v in vstrips:
					cur_col = np.array(v.getPixelColor(pos))
					col += cur_col[:3] * transparency
					transparency *= cur_col[3]

				col = np.minimum(col, 255)
				strip.setPixelColor(Color(*col.tolist()))
			
			strip.show()
	
	except KeyboardInterrupt:
		clear(strip)


		
