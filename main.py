import time
import threading

from neopixel import *

import colorsys
import numpy as np
import random
from math import sin, pi, exp, floor, ceil
from datetime import datetime

from app import run
from src.star_light import sparkle
from src.helpers import *


# LED strip configuration:
LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 10      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 127     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.WS2811_STRIP_GRB
#LED_STRIP      = ws.SK6812W_STRIP




if __name__ == '__main__':
    current_brightness = 1.


    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    threading.Thread(target=run).start()
    print('Press Ctrl-C to quit.')
    try:
        sparkle(strip, get_current_brightness=lambda: current_brightness)
    except KeyboardInterrupt:
        clear(strip)
