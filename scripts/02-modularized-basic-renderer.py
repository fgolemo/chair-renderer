# apt-get install xvfb
# alias xpy='xvfb-run -s "-screen 0 1x1x24" python'
# xpy -m ModernGL

import numpy as np
import matplotlib.pyplot as plt

from chair_renderer.camera import Camera
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import SIMPLE_VERTEX_SHADER, FLAT_FRAGMENT_SHADER

vertices = np.array([
    -1, -1, 0,
    1.0, 0, 0,
    -1, 1, 0,
    0, 1, 0,
    1, -1, 0,
    0, 0, 1,

    1, 1, 0,
    1, 1, 0,
    -1, 1, 0,
    0, 1, 0,
    1, -1, 0,
    0, 0, 1,
], dtype='f4')

width = 512
height = 512
near = 1.4
far = 4
fov = 60

renderer = Renderer(SIMPLE_VERTEX_SHADER, FLAT_FRAGMENT_SHADER, width, height)
camera = Camera(width,height,[0,2,1], near, far, fov)

img, depth = renderer.render(vertices, camera)
print(img.shape, img.min(), img.max(), img.dtype)
print(depth.shape, depth.min(), depth.max(), depth.dtype)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img)
ax1.set_title('RGB Plane')
ax1.set_axis_off()

ax2.imshow(depth)
ax2.set_title('Depth')
ax2.set_axis_off()

col = depth[:,128]
x = np.arange(0,len(col))
ax3.plot(col[::-1],x)
ax3.set_title('Depth slice')
ax3.set_axis_off()
plt.show()

