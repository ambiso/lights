import random
from math import exp
import colorsys

import numpy as np
from rpi_ws281x import Color

from .helpers import *


def sparkle_brightness(t):
    def _f(t):
        # e^{-\frac{\left(x-10\right)}{17}^{2}}
        return exp(-((t-10)/17)**2)
    def _g(t):
        # \frac{1}{1+e^{-\left(2\cdot x-17\right)}}
        return 1/(1+exp(-(2*t-17)))
    return _f(t) * _g(t)

def make_sparkle_cache(n):
    def _sparkle(base_color):
        sparkle_cache = np.array([
                sparkle_brightness(t)
                for t in np.arange(0, 50, 1/5)
            ])

        # sparkle_cache = 4**sparkle_cache

        sparkle_cache /= max(sparkle_cache)

        min_sparkle = 10/255
        sparkle_cache += min_sparkle
        sparkle_cache[-1] = min_sparkle
        sparkle_cache = min(sparkle_cache) + (sparkle_cache - min(sparkle_cache))/(max(sparkle_cache) - min(sparkle_cache)) * (1. - min(sparkle_cache))

        sparkle_cache = [
            Color(*np.array(np.array(base_color), dtype=np.int).tolist())
            for brightness in sparkle_cache
        ]
        return sparkle_cache
    return [_sparkle(
            np.array(colorsys.hsv_to_rgb(i / (n-1), 1, 1)) * 255
    ) for i in range(n)]

def sparkle(strip):
    sparkles = [] # (pos, time)

    n = 100
    slowness = 1000
    sparkle_cache = make_sparkle_cache(n)
    t = 0
    fill(strip, sparkle_cache[t // slowness][-1])

    def _rst():
        non_sparkles = set(range(strip.numPixels())) - set(a[0] for a in sparkles)
        for pos in non_sparkles:
            strip.setPixelColor(pos, sparkle_cache[t // slowness][-1])

    while True:

        if len(sparkles) < 200 and random.random() < 0.9:
            pos = random.randint(0, strip.numPixels())
            sparkle = [pos, 0]
            if not any(map(lambda x: x[0] == pos, sparkles)):
                sparkles.append(sparkle)

        if n % slowness == 0:
            _rst()

        for a in sparkles:
            strip.setPixelColor(a[0], sparkle_cache[t // slowness][a[1]])
            a[1] += 1
        strip.show()

        yield
        sparkles = [[pos, time] for pos, time in sparkles if time < len(sparkle_cache[t // slowness])]
        t += 1
        t %= n * slowness