# apt-get install xvfb
# alias xpy='xvfb-run -s "-screen 0 1x1x24" python'
# xpy -m ModernGL


import moderngl
import numpy as np
from pyrr import Matrix44
from PIL import Image
from chair_renderer.shaders import TEXTURED_FRAGMENT_SHADER, TEXTURED_VERTEX_SHADER
import cv2

ctx = moderngl.create_standalone_context()

prog = ctx.program(vertex_shader=TEXTURED_VERTEX_SHADER,
                   fragment_shader=TEXTURED_FRAGMENT_SHADER)

# little square made from 2 triangle faces
vertices = np.array([
    # face 1 (3 vertices)
    -1, -1, 0, # coords A
    0, 0, 1, # normal A
    0, 0, 0, # texture A
    -1, 1, 0, # coords B
    0, 0, 1, # normal B
    0, 2, 0, # texture B
    1, -1, 0, # coords C
    0, 0, 1, # ... and so on
    2, 0, 0,

    # face 2 (3 vertices)
    1, 1, 0,
    0, 0, 1,
    2, 2, 0,
    -1, 1, 0,
    0, 0, 1,
    0, 2, 0,
    1, -1, 0,
    0, 0, 1,
    2, 0, 0,
], dtype='f4')

vbo = ctx.buffer(vertices)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_norm', 'in_text')

texture_image = Image.open('face.jpg')

width = 512
height = 512
size = (height, width)

ctx.enable(moderngl.DEPTH_TEST)
cbo = ctx.texture(size, 4)
dbo = ctx.depth_texture(size, alignment=1)
fbo = ctx.framebuffer(color_attachments=[cbo], depth_attachment=dbo)
fbo.use()

fbo.use()
ctx.clear()

near = 1.4
far = 4

proj = Matrix44.perspective_projection(60, width / height, near, far)
lookat = Matrix44.look_at(
    (0, 2, 1),  # eye / camera position
    (0.0, 0.0, 0.0),  # lookat
    (0.0, 0.0, 1.0),  # camera up vector
)
prog['model'].write((proj * lookat).astype('f4').tobytes())
prog['Light'].value = (-140.0, -300.0, 350.0)
prog['Color'].value = (1.0, 1.0, 1.0, 0.25)

texture = ctx.texture(texture_image.size, 3, texture_image.tobytes())
texture.build_mipmaps()
texture.use()

vao.render(moderngl.TRIANGLES)
raw = fbo.read(components=4, dtype='f4')  # RGBA, floats
img = np.frombuffer(raw, dtype='f4').reshape((height, width, 4))
img = img[::-1, :, :3]
print(img.shape)
cv2.imwrite("mgl-test-rgb.png", (img*255).astype(np.uint8))
import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img)
ax1.set_title('RGB Plane')
ax1.set_axis_off()

depth = np.frombuffer(dbo.read(alignment=1), dtype=np.dtype('f4')).reshape(size[::-1])
depth = depth[::-1, :]
cv2.imwrite("mgl-test-depth.png", (depth*255).astype(np.uint8))
print(depth.shape, depth.min(), depth.max())

ax2.imshow(depth)
ax2.set_title('Depth')
ax2.set_axis_off()
col = depth[:,128]


x = np.arange(0,len(col))
ax3.plot(col[::-1],x)
ax3.set_title('Depth slice')
ax3.set_axis_off()
plt.show()

