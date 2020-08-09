#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import thread

from neopixel import *

import colorsys
import numpy as np
import random
from math import sin, pi, exp, floor, ceil
import itertools
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

def gen_color_map(n):
    color_map = []
    for i in range(n):
        brightness_map = []
        for j in range(n):
            col = np.array(colorsys.hsv_to_rgb(i / n, 1, j / n))
            col = np.array(col*255, dtype=np.int).tolist()
            brightness_map.append(col)
        color_map.append(brightness_map)
    return color_map

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


def broadcast(strip, color_provider, wait_ms=10):
    if not isinstance(wait_ms, list):
        wait_ms = [wait_ms]
    while True:
        for col, wait_time in itertools.zip_longest(color_provider, wait_ms, fillvalue=0):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, col)
            strip.show()
            time.sleep(wait_time/1000.0)

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


def nightrider(strip, width, color_provider, wait_ms=10, its=1):
    for i in range(its):
        for way in [
                range(strip.numPixels() - width),
                range(strip.numPixels() - width, 0, -1)
                ]:
            for i in way:
                color = next(color_provider)
                for j in range(width):
                    strip.setPixelColor(i+j, color)
                strip.show()
                strip.setPixelColor(i, 0)
                strip.setPixelColor(i+j+1, 0)
                time.sleep(wait_ms/1000.0)

def reduce_rl(pos):
    return (pos - LEFT) % (RIGHT-LEFT) + LEFT

def ride_cycle(strip, width, color_provider, wait_ms=10):
    while True:
        for i in range(LEFT, RIGHT+1):
            color = next(color_provider)
            for j in range(width):
                strip.setPixelColor(reduce_rl(i + j), color)
            strip.show()
            strip.setPixelColor(i, 0)
            strip.setPixelColor(reduce_rl(i+j+1), 0)
            time.sleep(wait_ms/1000.0)


def cycle_01(x, delta):
    while True:
        x += delta
        x %= 1.
        yield x

def ride_trains(strip, wait_ms=10):

    color_map = gen_color_map(100)

    def gauss(x, mu, sigma):
        return exp(-((x-mu)/sigma)**2/2)

    class Train:
        def __init__(self):
            self.color_provider = cycle_01(random.uniform(0., 1.), random.uniform(0.00001, .0001))
            self.width = random.randint(15, 30)
            if random.uniform(0., 1.) > .5:
                self.speed = random.uniform(.5, 1.7)
            else:
                self.speed = random.uniform(-1.7, -.5)
            self.position = random.randint(0, RIGHT-LEFT)

        def draw(self, vstrip):
            for i in range(floor(self.position), ceil(self.position + self.width)):
                c = next(self.color_provider)
                vstrip[i % len(vstrip)].append((c, gauss(i, self.position + self.width/2, self.width / 5)))
            self.speed += random.uniform(-0.01, 0.01)
            self.speed = min(.9, max(-.9, self.speed))
            self.width += random.uniform(-0.01, 0.01)
            self.width = min(60, max(10, self.width))
            self.position += self.speed
            self.position %= len(vstrip)

    trains = [Train() for _ in range(8)]
    #strobe_counter = datetime.now()
    #interval = 0
    while True:
        vstrip = [ [] for _ in range(RIGHT-LEFT+1) ]
        for train in trains:
            train.draw(vstrip)


        for i, colors in enumerate(vstrip):
            if len(colors) == 0:
                strip.setPixelColor(i + LEFT, Color(0,0,0))
            else:
                col = [color_map[floor(hue * (len(color_map)-1))][floor(val * (len(color_map)-1))] for (hue, val) in colors]
                col = np.sum(col, axis=0) / len(col)
                col = np.array(col, dtype=np.int).tolist()
                color = Color(*col)
                strip.setPixelColor(i + LEFT, color)
        strip.show()

        #if (datetime.now() - strobe_counter).total_seconds() > interval:
        #    interval = random.randint(3, 60)
        #    strobe_counter = datetime.now()
        #    strobe(strip, random.randint(2, 7))
        #for i in range(LEFT, RIGHT+1):
            #color = next(color_provider)
            #for j in range(width):
                #strip.setPixelColor(reduce_rl(i + j), color)
            #strip.show()
            #strip.setPixelColor(i, 0)
            #strip.setPixelColor(reduce_rl(i+j+1), 0)
            #time.sleep(wait_ms/1000.0)

class ColorGen:
    def __init__(self):
        self.hue_provider = const(0)
        self.saturation_provider = const(1)
        self.value_provider = const(1)

    def hue(self, provider):
        self.hue_provider = provider

    def saturation(self, provider):
        self.saturation_provider = provider

    def value(self, provider):
        self.value_provider = provider

    def __iter__(self):
        return self

    def __next__(self):
        col = np.array(colorsys.hsv_to_rgb(
            next(self.hue_provider),
            next(self.saturation_provider),
            next(self.value_provider),
            ))
        col = np.array(col*255, dtype=np.int).tolist()
        return Color(*col)


def const(value):
    while True:
        yield value


def random_color():
    while True:
        yield Color(int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))


def wheel(steps):
    while True:
        yield from np.arange(0, 1, 1/steps)


def clear(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    print('Cleared')


def linear_diminish(value, steps):
    yield value
    for i in range(0, steps):
        yield value * (steps - i - 1) / steps

def sin_cycle(speed):
    for i in itertools.count():
        yield sin(i*speed/(2*pi))/2+0.5


def strobe(strip, n=10):
    for i in range(n):
        fill(strip, Color(255,255,255))
        fill(strip, Color(0,0,0))
        time.sleep(1/11)
        #time.sleep(1/(((sin(i/10) + 1)/2 * 3) + 4))
        #time.sleep((sin(i/10) + 1)/2 * 0.2)



    

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

def show_n(n):
    while True:
        for i in range(n):
            strip.setPixelColor(i, Color(255,255,255))
        strip.show()

LEFT = 44
RIGHT = 249

BRIGHTNESS = 1.

def show_left_right():
    while True:
        strip.setPixelColor(LEFT, Color(255,255,255))
        strip.setPixelColor(RIGHT, Color(255,255,255))
        strip.show()

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    current_brightness = 1.

    @app.route('/')
    def set_brightness(brightness):
        current_brightness = brightness

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    thread.start_new_thread(app.run)
    print('Press Ctrl-C to quit.')
    try:
        #rojava(strip)
        #rainbowCycle(strip, wait_ms=10)
        # left: 46
        #show_left_right()
        # ride_trains(strip, 5)
        #ride_cycle(strip, 9, const(Color(255,255,255)), 5)
        #broadcast(strip, color_wheel(1000), wait_ms=10)
        #broadcast(strip, linear_diminish([255, 0, 0], 255), wait_ms=500)
        #broadcast(strip, sin_value(0, 1/100), wait_ms=0)
        #stack(strip, color_wheel(strip.numPixels()), 0)
        #stack(strip, const(Color(255,255,255)), 0)
        #stack(strip, random_color(), 0)
        #nightrider(strip, 8, const(Color(255,0,0)), 5, 5)
        #cg = ColorGen()
        #cg.hue(const(0.09))
        #cg.value(const(1))
        #cg.saturation(const(0.7))
        #cg.hue(sin_cycle(1/2))
        #cg.value(const(1/5))
        #broadcast(strip, [Color(0,0,0), Color(255, 255, 255)], wait_ms=[200, 10])
        #stack(strip, cg, 0)
        #strobe(strip)
        sparkle(strip, get_current_brightness=lambda: current_brightness)
    except KeyboardInterrupt:
        clear(strip)
