import itertools
import numpy as np
import colorsys

from rpi_ws281x import Color, PixelStrip

def fill(strip, color):
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
  strip.show()

def show_n(n):
  while True:
    for i in range(n):
      strip.setPixelColor(i, Color(255,255,255))
    strip.show()


def sin_cycle(speed):
  for i in itertools.count():
    yield sin(i*speed/(2*pi))/2+0.5

def linear_diminish(value, steps):
  yield value
  for i in range(0, steps):
    yield value * (steps - i - 1) / steps


def clear(strip):
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, 0)
  strip.show()
  print('Cleared')

def wheel(steps):
  while True:
    yield from np.arange(0, 1, 1/steps)

def random_color():
  while True:
    yield Color(int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))


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

def const(value):
  while True:
    yield value


def getPixels(strip: PixelStrip):
  num_pixels = strip.numPixels()
  all_pixels = []
  for i in range(num_pixels):
    color = strip.getPixelColorRGB(i)
    all_pixels.append(color)

  return all_pixels
