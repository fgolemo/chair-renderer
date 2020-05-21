import moderngl
import numpy as np
import OpenGL.GL as gl
from pympler import tracker


class Renderer(object):

    def __init__(self, shader, width, height, msaa=0):
        super().__init__()
        self.shader = shader
        self.msaa = msaa

        self.size = (width, height)
        self.ctx = moderngl.create_standalone_context()
        self.prog = self.ctx.program(
            vertex_shader=shader["vertex"], fragment_shader=shader["frag"])
        self.ctx.enable(moderngl.DEPTH_TEST)

        if msaa > 0:
            self.cbo_smol = self.ctx.texture(self.size, 4, samples=0)
            self.cbo_biig = self.ctx.texture(self.size, 4, samples=8)
            self.dbo_smol = self.ctx.depth_texture(self.size, alignment=1, samples=0)
            self.dbo_biig = self.ctx.depth_texture(self.size, alignment=1, samples=8)
            self.fbo = self.ctx.framebuffer(color_attachments=[self.cbo_smol], depth_attachment=self.dbo_smol)
            self.fbo_msaa = self.ctx.framebuffer(
                color_attachments=[self.cbo_biig], depth_attachment=self.dbo_biig)
            self.fbo_msaa.use()
        else:
            self.cbo_smol = self.ctx.texture(self.size, 4, samples=0)
            self.dbo = self.ctx.depth_texture(self.size, alignment=1, samples=0)
            self.fbo = self.ctx.framebuffer(
                color_attachments=[self.cbo_smol], depth_attachment=self.dbo)
            self.fbo.use()

    def render(self, scene, camera, light=(1.0, 1.0, 1.0)):
        # tr = tracker.SummaryTracker()

        self.ctx.clear()

        # create a C-style binary buffer for the scene data
        scene_packed = scene.pack()
        vbo = self.ctx.buffer(scene_packed)

        # merge the textures and load them into a buffer
        scene.pack_textures()

        # load the scene data (vertices, colors, etc.) into the renderer
        vao = self.ctx.simple_vertex_array(self.prog, vbo,
                                           *self.shader["params"])

        # get the camera parameters and feed them into the renderer
        proj, lookat = camera.get_view_model()
        self.prog['model'].write((proj * lookat).astype('f4').tobytes())
        self.prog['Light'].value = light
        # prog['Color'].value = (1.0, 1.0, 1.0, 0.25)

        # render out the current
        vao.render(moderngl.TRIANGLES)

        if self.msaa > 0:

            gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self.fbo_msaa.glo)
            gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, self.fbo.glo)
            gl.glBlitFramebuffer(0, 0, self.size[0], self.size[1], 0, 0,
                                 self.size[0], self.size[1],
                                 gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT, gl.GL_NEAREST)

            # gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self.fbo_msaa.glo)
            # gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, self.fbo.glo)
            # gl.glBlitFramebuffer(0, 0, self.size[0], self.size[1], 0, 0,
            #                      self.size[0], self.size[1],
            #                      , gl.GL_LINEAR)

        # get the RGB data and convert to numpy array
        raw = self.fbo.read(components=4, dtype='f4')  # RGBA, floats
        img = np.frombuffer(
            raw, dtype='f4').reshape((camera.height, camera.width, 4))

        # the y axis is flipped during rendering, so we have to unflip this.
        # and the image has 4 channels: RGB+Alpha, but we don't care about alpha.
        # note that the image will be numpy.float32 in range [0,1]
        img = img[::-1, :, :3]

        # get the depth buffer and conver to numpy
        depth = np.frombuffer(
            self.dbo_smol.read(alignment=1),
            dtype=np.dtype('f4')).reshape(camera.size())
        # similar to the RGB, the dept is flipped upside-down as well so we need to unflip.
        depth = depth[::-1, :]

        # tr.print_diff()
        return img, depth
