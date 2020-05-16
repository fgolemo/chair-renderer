# apt-get install xvfb
# alias xpy='xvfb-run -s "-screen 0 1x1x24" python'
# xpy -m ModernGL


import numpy as np
import matplotlib.pyplot as plt

from chair_renderer.assets import TEXTURES, get_tex
from chair_renderer.box import floor, right, left, back
from chair_renderer.camera import Camera
from chair_renderer.objects import Obj, Scene
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import SHADER_TEXTURED

width = 512
height = 512
near = 1.4
far = 10
fov = 60

renderer = Renderer(SHADER_TEXTURED, width, height)
camera = Camera(width,height,[0,4,2], near, far, fov)

scene = Scene(renderer.ctx)

floor.add_texture(get_tex(0))
scene.add_obj(floor)

left.add_texture(get_tex(2))
scene.add_obj(left)

right.add_texture(get_tex(4))
scene.add_obj(right)

back.add_texture(get_tex(5))
scene.add_obj(back)

img, depth = renderer.render(scene, camera)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img)
ax1.set_title('RGB Plane')
ax1.set_axis_off()

ax2.imshow(depth)
ax2.set_title('Depth')
ax2.set_axis_off()
col = depth[:, 256]

x = np.arange(0, len(col))
ax3.plot(col[::-1], x)
ax3.set_title('Depth slice')
ax3.set_axis_off()
plt.show()
