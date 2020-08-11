import time
import threading

from rpi_ws281x import *

import random
from math import sin, pi, exp, floor, ceil
from datetime import datetime

from src import app
from src.star_light import sparkle
from src.helpers import *
from src import animations


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


current_brightness = 1.
curr_animation = 'trains'
def run():
	prev_animation = None
	prev_brightness = None
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	strip.begin()

	threading.Thread(target=app.run).start()
	print('Press Ctrl-C to quit.')
	try:
		while True:

			if curr_animation != prev_animation:
				fn = animations[curr_animation]['fn']
				print('animation changed {} with function {}'.format(prev_animation, curr_animation))
				prev_animation = curr_animation
				clear(strip)
				gen = fn(strip)
			if current_brightness != prev_brightness:
				strip.setBrightness(int(255 * current_brightness))
				prev_brightness = current_brightness
				
			next(gen)
		# sparkle(strip, get_current_brightness=lambda: current_brightness)
	except KeyboardInterrupt:
		clear(strip)
