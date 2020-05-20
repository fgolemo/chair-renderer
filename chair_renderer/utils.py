import colorsys
import numpy as np

def brith_color():
    h = np.random.random()  # this is the color
    s = 0.5 + np.random.random() / 2.0  # saturation - we want that to be a minimum of 50%
    l = 0.4 + np.random.random() / 5.0  # lightness - not black, not white but nicely in the middle
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

    return r, g, b

def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    arr2 = np.copy(arr)
    lens = np.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2) + 0.1
    arr2[:, 0] /= lens
    arr2[:, 1] /= lens
    arr2[:, 2] /= lens
    return arr2
