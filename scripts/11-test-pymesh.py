import cv2
import numpy as np
import matplotlib.pyplot as plt
import pymesh
import trimesh

from chair_renderer.assets import TEXTURES, get_tex
from chair_renderer.box import floor
from chair_renderer.camera import Camera
from chair_renderer.objects import Obj, Scene
from chair_renderer.renderer import Renderer
from chair_renderer.shaders import SHADER_TEXTURED
from chair_renderer.utils import normalize_v3

width = 512
height = 512
near = .1
far = 2
fov = 60

renderer = Renderer(SHADER_TEXTURED, width, height)
camera = Camera(width,height,[0,1,.5], near, far, fov)

scene = Scene(renderer.ctx)

mesh = pymesh.load_mesh("chair2.obj")
mesh.add_attribute("vertex_normal")
normals = mesh.get_attribute("vertex_normal").reshape((len(mesh.vertices),3))

mesh = trimesh.load_mesh('chair2.obj')
print(mesh.vertices.shape)
print(mesh.faces.shape)
obj = Obj()
obj.vertices = mesh.vertices
obj.faces = mesh.faces
obj.normals = normals
obj.has_normals = True

print (obj.normals)
obj.add_color()
scene.add_obj(obj)

steps = 100
step = np.pi/100
distance = 1
angle = 3*np.pi/2

for i in range(steps):
    x = distance * np.cos(angle)
    y = distance * np.sin(angle)
    angle += step
    camera.eye = [x,y,.5]

    img, depth = renderer.render(scene, camera)

    # depth = (depth * 255).astype(np.uint8)
    # print (depth.shape, depth.min(), depth.max(), depth.dtype)

    cv2.imshow("rgb", img[:,:,::-1])
    cv2.imshow("depth", depth)
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
