import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from chair_renderer.assets import TEXTURES, get_tex
from chair_renderer.box import floor, right, left, back
from chair_renderer.camera import Camera
from chair_renderer.objects import Obj, Scene
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import SHADER_FACENORMALS

width = 512
height = 512
# near = .86655 # best possible near for x=y=1024
near = .001
far = 3.62
fov = 60
CV2_SHOW = False
CV2_SAVE = True
PLT_SHOW = False

renderer = Renderer(SHADER_FACENORMALS, width, height, msaa=8)
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
# print(chair.vertices)
# print(chair.vertices.min(axis=0))

scene.add_obj(chair)

floor.add_texture(get_tex(0))
scene.add_obj(floor)
right.add_texture(get_tex(2))
scene.add_obj(right)
left.add_texture(get_tex(4))
scene.add_obj(left)
back.add_texture(get_tex(5))
scene.add_obj(back)

steps = 5
step = np.pi / steps
distance = 1.5
angle = 0
depth_min = 0.99912244
# depth_min = np.inf

for i in trange(steps):
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    angle += step
    camera.eye = [x, y, 0]

    img, depth = renderer.render(scene, camera, light=(1, 5, 10))

    d = np.copy(depth)
    d -= depth_min
    d /= (1 - depth_min)

    if CV2_SHOW:
        cv2.imshow("rgb", img[:, :, ::-1])
        cv2.imshow("depth", d)
        cv2.waitKey(1)

    if CV2_SAVE:
        # print (img.min(), img.max(), img.dtype)
        # print (d.min(), d.max(), d.dtype)
        cv2.imwrite(f"chair/{i:04}-rgb.png", (img[:, :, ::-1]*255).astype(np.uint8))
        cv2.imwrite(f"chair/{i:04}-depth.png", (d*255).astype(np.uint8))


    if PLT_SHOW:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

        ax1.imshow(img)
        ax1.set_title('RGB')
        ax1.set_axis_off()

        ax2.imshow(d)
        ax2.set_title('Depth')
        ax2.set_axis_off()

        col = d[:, int(round(width/2))]
        x = np.arange(0, len(col))
        ax3.plot(col[::-1], x)
        ax3.set_title('Depth slice')
        ax3.set_axis_off()
        plt.show()

print (depth_min)