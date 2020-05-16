import colorsys
import numpy as np

def brith_color():
    h = np.random.random()  # this is the color
    s = 0.5 + np.random.random() / 2.0  # saturation - we want that to be a minimum of 50%
    l = 0.4 + np.random.random() / 5.0  # lightness - not black, not white but nicely in the middle
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

    return r, g, b