import random
from math import exp
import colorsys

import numpy as np
from neopixel import Color

from .helpers import *


def sparkle_brightness(t):
    def _f(t):
        # e^{-\frac{\left(x-10\right)}{17}^{2}}
        return exp(-((t-10)/17)**2)
    def _g(t):
        # \frac{1}{1+e^{-\left(2\cdot x-17\right)}}
        return 1/(1+exp(-(2*t-17)))
    return _f(t) * _g(t)

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

def make_sparkle_cache(n, brightness: float):
    def _sparkle(base_color):
        sparkle_cache = np.array([
                sparkle_brightness(t)
                for t in np.arange(0, 50, 1/5)
            ])

        # sparkle_cache = 4**sparkle_cache

        sparkle_cache /= max(sparkle_cache)

        min_sparkle = brightness * 0.1
        sparkle_cache += min_sparkle
        sparkle_cache[-1] = min_sparkle
        sparkle_cache = min(sparkle_cache) + (sparkle_cache - min(sparkle_cache))/(max(sparkle_cache) - min(sparkle_cache)) * (brightness - min(sparkle_cache))

        sparkle_cache = [
            Color(*np.array(np.array(base_color) * brightness, dtype=np.int).tolist())
            for brightness in sparkle_cache
        ]
        return sparkle_cache
    return [_sparkle(
            np.array(colorsys.hsv_to_rgb(i / (n-1), 1, 1)) * 255
    ) for i in range(n)]

def sparkle(strip, get_current_brightness = lambda: 1.):
    sparkles = [] # (pos, time)

    n = 100
    slowness = 10
    last_brightness = get_current_brightness()
    sparkle_cache = make_sparkle_cache(n, last_brightness)
    t = 0
    fill(strip, sparkle_cache[t // slowness][-1])

    def _rst():
        non_sparkles = set(range(strip.numPixels())) - set(a[0] for a in sparkles)
        for pos in non_sparkles:
            strip.setPixelColor(pos, sparkle_cache[t // slowness][-1])

    while True:
        new_brightness = get_current_brightness()

        if len(sparkles) < 75 and random.random() < 0.3:
            pos = random.randint(0, strip.numPixels())
            sparkle = [pos, 0]
            if not any(map(lambda x: x[0] == pos, sparkles)):
                sparkles.append(sparkle)

        if new_brightness != last_brightness:
            last_brightness = new_brightness
            sparkle_cache = make_sparkle_cache(n, new_brightness)
        _rst()

        for a in sparkles:
            strip.setPixelColor(a[0], sparkle_cache[t // slowness][a[1]])
            a[1] += 1
        strip.show()
        sparkles = [[pos, time] for pos, time in sparkles if time < len(sparkle_cache[t // slowness])]
        t += 1
        t %= n * slowness