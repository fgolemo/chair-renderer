import cv2
import numpy as np
import matplotlib.pyplot as plt

from chair_renderer.assets import TEXTURES, get_tex
from chair_renderer.box import floor, right, left, back
from chair_renderer.camera import Camera
from chair_renderer.objects import Obj, Scene
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import SHADER_FACENORMALS

width = 512
height = 512
near = .001
far = 3.62
fov = 60

renderer = Renderer(SHADER_FACENORMALS, width, height)
camera = Camera(width, height, [0, 1, 0], near, far, fov)

scene = Scene(renderer.ctx)

chair = Obj()
chair.load_from_file("chair2.obj")
# chair.add_texture(get_tex(0))
chair.add_color()
chair.rotate(-90, -90, 0)

minima = chair.vertices.min(axis=0)
min_diff = minima[2] - (-.5)

chair.translate(0, 0, -min_diff)
print(chair.vertices)
print(chair.vertices.min(axis=0))

scene.add_obj(chair)

scene.add_obj(floor)
scene.add_obj(right)
scene.add_obj(left)
scene.add_obj(back)

steps = 100
step = np.pi / 100
distance = 1.5
angle = 0

for i in range(steps):
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    angle += step
    camera.eye = [x, y, 0]

    img, depth = renderer.render(scene, camera, light=(1, 5, 10))

    # depth = (depth * 255).astype(np.uint8)
    print(depth.shape, depth.min(), depth.max(), depth.dtype)
    d = np.copy(depth)
    d -= 0.9991234
    d /= (1 - 0.9991234)
    cv2.imshow("rgb", img[:, :, ::-1])
    cv2.imshow("depth", d)
    cv2.waitKey(1)

# fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
#
# ax1.imshow(img)
# ax1.set_title('RGB')
# ax1.set_axis_off()
#
# ax2.imshow(depth)
# ax2.set_title('Depth')
# ax2.set_axis_off()
#
# col = depth[:, 256]
# x = np.arange(0, len(col))
# ax3.plot(col[::-1], x)
# ax3.set_title('Depth slice')
# ax3.set_axis_off()
# plt.show()
