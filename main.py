#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

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
  # Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
  # Intialize the library (must be called once before other functions).
  strip.begin()
  strip.setPixelColor()

  print ('Press Ctrl-C to quit.')
  try:
    #ride_cycle(strip, 9, const(Color(255,255,255)), 5)
    #broadcast(strip, color_wheel(1000), wait_ms=10)
    #broadcast(strip, linear_diminish([255, 0, 0], 255), wait_ms=500)
    #broadcast(strip, sin_value(0, 1/100), wait_ms=0)
    #broadcast(strip, [Color(0,0,0), Color(255, 255, 255)], wait_ms=[200, 10])
    #stack(strip, color_wheel(strip.numPixels()), 0)
    #stack(strip, const(Color(255,255,255)), 0)
    #stack(strip, random_color(), 0)
    #stack(strip, cg, 0)
    #nightrider(strip, 8, const(Color(255,0,0)), 5, 5)
    #strobe(strip)
    sparkle(strip)
  except KeyboardInterrupt:
    clear(strip)
