import random
from math import sin, pi, exp, floor, ceil

import numpy as np
from rpi_ws281x import *


from .helpers import gen_color_map

LEFT = 44
RIGHT = 249

def cycle_01(x, delta):
  while True:
    x += delta
    x %= 1.
    yield x
    
def ride_trains(strip, null=None):

  color_map = gen_color_map(100)

  def gauss(x, mu, sigma):
    return exp(-((x-mu)/sigma)**2/2)

  class Train:
    def __init__(self):
      self.color_provider = cycle_01(random.uniform(0., 1.), random.uniform(0.00001, .0001))
      self.width = random.randint(15, 30)
      # if random.uniform(0., 1.) > .5:
      self.speed = random.uniform(.5, 1.7)
      # else:
      #   self.speed = random.uniform(-1.7, -.5)
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
        col = np.sum(col, axis=0)
        col = np.array(col, dtype=np.int).tolist()
        for j in range(len(col)):
          col[j] = min(col[j], 255)
        color = Color(*col)
        strip.setPixelColor(i + LEFT, color)
    strip.show()

    yield

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