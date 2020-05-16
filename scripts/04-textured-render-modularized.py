# apt-get install xvfb
# alias xpy='xvfb-run -s "-screen 0 1x1x24" python'
# xpy -m ModernGL


import numpy as np
import matplotlib.pyplot as plt

from chair_renderer.camera import Camera
from chair_renderer.objects import Obj, Scene
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import TEXTURED_VERTEX_SHADER, TEXTURED_FRAGMENT_SHADER, SHADER_TEXTURED

vertices = [
    [-1, -1, 0],
    [-1, 1, 0],
    [1, -1, 0],
    [1, 1, 0],
]

faces = [
    [0, 1, 2],
    [3, 1, 2]
]

normals = [
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1]
]

textures = [
    [0, 0, 0],
    [0, 2, 0],
    [2, 0, 0],
    [2, 2, 0]
]

width = 512
height = 512
near = 1.4
far = 4
fov = 60

renderer = Renderer(SHADER_TEXTURED, width, height)
camera = Camera(width,height,[0,2,1], near, far, fov)

obj = Obj()
obj.load_from_lists(vertices, faces, normals, textures)
obj.add_texture("face.jpg")

scene = Scene(renderer.ctx)
scene.add_obj(obj)

img, depth = renderer.render(scene, camera)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img)
ax1.set_title('RGB Plane')
ax1.set_axis_off()

ax2.imshow(depth)
ax2.set_title('Depth')
ax2.set_axis_off()
col = depth[:, 128]

x = np.arange(0, len(col))
ax3.plot(col[::-1], x)
ax3.set_title('Depth slice')
ax3.set_axis_off()
plt.show()
