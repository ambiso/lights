#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import threading
import json

from neopixel import *

import colorsys
import numpy as np
import random
from math import sin, pi, exp, floor, ceil
from datetime import datetime

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




def broadcast(strip, color_provider, wait_ms=10):
  if not isinstance(wait_ms, list):
    wait_ms = [wait_ms]
  while True:
    for col, wait_time in itertools.zip_longest(color_provider, wait_ms, fillvalue=0):
      for i in range(strip.numPixels()):
        strip.setPixelColor(i, col)
      strip.show()
      time.sleep(wait_time/1000.0)


if __name__ == '__main__':
    from flask import Flask, request, send_from_directory
    app = Flask(__name__)
    current_brightness = 1.

    @app.route('/brightness/<brightness>', methods=['POST'])
    def set_brightness(brightness):
        global current_brightness
        b = float(brightness)
        if 0. < b < 1.:
            current_brightness = b
            return json.dumps({"sucess": True, "brightness": b}, separators=(",", ":"))
        else:
            return json.dumps({"sucess": False})

    @app.route('/')
    def home():
        return send_from_directory('static', "index.html")

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    def run():
        app.run(host="0.0.0.0", port=1337)

    threading.Thread(target=run).start()
    print('Press Ctrl-C to quit.')
    try:
        sparkle(strip, get_current_brightness=lambda: current_brightness)
    except KeyboardInterrupt:
        clear(strip)
