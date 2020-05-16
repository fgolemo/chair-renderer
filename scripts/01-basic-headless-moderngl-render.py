# apt-get install xvfb
# alias xpy='xvfb-run -s "-screen 0 1x1x24" python'
# xpy -m ModernGL


import moderngl
import numpy as np
from pyrr import Matrix44

ctx = moderngl.create_standalone_context()

prog = ctx.program(vertex_shader="""
    #version 330
    uniform mat4 model;
    in vec3 in_vert;
    in vec3 in_color;
    out vec3 color;
    void main() {
        gl_Position = model * vec4(in_vert, 1.0);
        color = in_color;
    }
    """,
                   fragment_shader="""
    #version 330
    in vec3 color;
    out vec4 fragColor;
    void main() {
        fragColor = vec4(color, 1.0);
    }
""")

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

vbo = ctx.buffer(vertices)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')

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

vao.render(moderngl.TRIANGLES)
raw = fbo.read(components=4, dtype='f4')  # RGBA, floats
img = np.frombuffer(raw, dtype='f4').reshape((height, width, 4))
img = img[::-1, :, :3]
print(img.shape)
import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

ax1.imshow(img)
ax1.set_title('RGB Plane')
ax1.set_axis_off()

depth = np.frombuffer(dbo.read(alignment=1), dtype=np.dtype('f4')).reshape(size[::-1])
depth = depth[::-1, :]
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

