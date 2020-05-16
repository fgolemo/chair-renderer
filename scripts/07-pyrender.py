# Render offscreen -- make sure to set the PyOpenGL platform
import os
# os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = '/lib:/usr/lib:/usr/bin/lib:/'
# os.environ["PYOPENGL_PLATFORM"] = "egl"
# os.environ["PYOPENGL_PLATFORM"] = "osmesa"

import numpy as np
import trimesh
import pyrender

# Load the FUZE bottle trimesh and put it in a scene
fuze_trimesh = trimesh.load('teapot-versmol.obj')
mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
scene = pyrender.Scene()
scene.add(mesh)

# Set up the camera -- z-axis away from the scene, x-axis right, y-axis up

camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
s = np.sqrt(2)/2
camera_pose = np.array([
       [0.0, -s,   s,   0.3],
       [1.0,  0.0, 0.0, 0.0],
       [0.0,  s,   s,   0.35],
       [0.0,  0.0, 0.0, 1.0],
    ])
scene.add(camera, pose=camera_pose)

# Set up the light -- a single spot light in the same spot as the camera
light = pyrender.SpotLight(color=np.ones(3), intensity=3.0,
                           innerConeAngle=np.pi / 16.0)
scene.add(light, pose=camera_pose)

# Render the scene
r = pyrender.OffscreenRenderer(640, 480)
color, depth = r.render(scene)

# Show the images
import matplotlib.pyplot as plt

plt.figure()
plt.subplot(1, 2, 1)
plt.axis('off')
plt.imshow(color)
plt.subplot(1, 2, 2)
plt.axis('off')
plt.imshow(depth, cmap=plt.cm.gray_r)
plt.show()
