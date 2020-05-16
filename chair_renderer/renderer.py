import moderngl
import numpy as np


class Renderer(object):

    def __init__(self, shader, width, height):
        super().__init__()
        self.shader = shader

        self.size = (width, height)
        self.ctx = moderngl.create_standalone_context()
        self.prog = self.ctx.program(vertex_shader=shader["vertex"],
                                     fragment_shader=shader["frag"])

        self.ctx.enable(moderngl.DEPTH_TEST)
        cbo = self.ctx.texture(self.size, 4)
        self.dbo = self.ctx.depth_texture(self.size, alignment=1)
        self.fbo = self.ctx.framebuffer(color_attachments=[cbo], depth_attachment=self.dbo)
        self.fbo.use()

    def render(self, scene, camera):
        self.ctx.clear()

        # create a C-style binary buffer for the scene data
        vbo = self.ctx.buffer(scene.pack())

        # merge the textures and load them into a buffer
        scene.pack_textures()

        # load the scene data (vertices, colors, etc.) into the renderer
        vao = self.ctx.simple_vertex_array(self.prog, vbo, *self.shader["params"])

        # get the camera parameters and feed them into the renderer
        proj, lookat = camera.get_view_model()
        self.prog['model'].write((proj * lookat).astype('f4').tobytes())

        # render out the current
        vao.render(moderngl.TRIANGLES)

        # get the RGB data and convert to numpy array
        raw = self.fbo.read(components=4, dtype='f4')  # RGBA, floats
        img = np.frombuffer(raw, dtype='f4').reshape((camera.height, camera.width, 4))

        # the y axis is flipped during rendering, so we have to unflip this.
        # and the image has 4 channels: RGB+Alpha, but we don't care about alpha.
        # note that the image will be numpy.float32 in range [0,1]
        img = img[::-1, :, :3]

        # get the depth buffer and conver to numpy
        depth = np.frombuffer(self.dbo.read(alignment=1), dtype=np.dtype('f4')).reshape(camera.size())
        # similar to the RGB, the dept is flipped upside-down as well so we need to unflip.
        depth = depth[::-1, :]

        return img, depth
