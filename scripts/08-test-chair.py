import cv2
import numpy as np
import matplotlib.pyplot as plt

from chair_renderer.assets import TEXTURES, get_tex
from chair_renderer.box import floor, right, left, back
from chair_renderer.camera import Camera
from chair_renderer.objects import Obj, Scene
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import SHADER_TEXTURED, SHADER_PHONG, SHADER_MESHLAB, SHADER_FACENORMALS

width = 512
height = 512
near = .1
far = 2
fov = 60

renderer = Renderer(SHADER_FACENORMALS, width, height)
camera = Camera(width,height,[0,1,.5], near, far, fov)

scene = Scene(renderer.ctx)

chair = Obj()
chair.load_from_file("chair2.obj")
# chair.add_texture(get_tex(0))
chair.add_color()
chair.rotate(-90,0,0)
scene.add_obj(chair)

steps = 100
step = np.pi/100
distance = 1
angle = 3*np.pi/2

for i in range(steps):
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    angle += step
    camera.eye = [x,y,.5]

    img, depth = renderer.render(scene, camera, light=(1,5,10))

    # depth = (depth * 255).astype(np.uint8)
    # print (depth.shape, depth.min(), depth.max(), depth.dtype)

    cv2.imshow("rgb", img[:,:,::-1])
    # cv2.imshow("depth", depth)
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
