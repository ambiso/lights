import numpy as np

def sparkle_brightness(t):
    def _f(t):
        # e^{-\frac{\left(x-10\right)}{17}^{2}}
        return exp(-((t-10)/17)**2)
    def _g(t):
        # \frac{1}{1+e^{-\left(2\cdot x-17\right)}}
        return 1/(1+exp(-(2*t-17)))
    return _f(t) * _g(t)

sparkle_cache = np.array([
        sparkle_brightness(t)
        for t in np.arange(0, 50, 1/5)
    ])

# sparkle_cache = 4**sparkle_cache

sparkle_cache /= max(sparkle_cache)

min_sparkle = 15/255
sparkle_cache += min_sparkle
sparkle_cache[-1] = min_sparkle
sparkle_cache = min(sparkle_cache) + (sparkle_cache - min(sparkle_cache))/(max(sparkle_cache) - min(sparkle_cache)) * (255/255 - min(sparkle_cache))

sparkle_cache = [
    Color(*np.array(np.array([50, 50, 255]) * brightness, dtype=np.int).tolist())
    for brightness in sparkle_cache
]

def sparkle(strip):
    sparkles = [] # (pos, time)

    fill(strip, sparkle_cache[-1])

    while True:
        if len(sparkles) < 75 and random.random() < 0.3:
            pos = random.randint(0, strip.numPixels())
            sparkle = [pos, 0]
            if not any(map(lambda x: x[0] == pos, sparkles)):
                sparkles.append(sparkle)

        for a in sparkles:
            strip.setPixelColor(a[0], sparkle_cache[a[1]])
            a[1] += 1
        strip.show()
        sparkles = [[pos, time] for pos, time in sparkles if time < len(sparkle_cache)]