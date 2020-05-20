from PIL import Image
import numpy as np
from moderngl.ext import obj
import colorsys
from scipy.spatial.transform import Rotation as R
from chair_renderer.utils import brith_color, normalize_v3

MAX_TEX_TILING = 2


class Scene(object):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.has_textures = False
        self.objs = []

    def add_obj(self, obj):
        self.objs.append(obj)
        if obj.has_texture:
            self.has_textures = True

    def pack(self):
        for o in self.objs:
            o.pack()

        output_vertices = []
        output_normals = []
        output_textures = []

        for idx, obj in enumerate(self.objs):
            for face in obj.faces:
                for vertex in face:
                    output_vertices.append(obj.vertices[vertex])
                    if obj.has_normals:
                        output_normals.append(obj.normals[vertex])
                    if obj.has_texture:
                        u, v, w = obj.textures[vertex]
                        if len(self.objs) > 1:
                            v /= MAX_TEX_TILING
                            u_ = idx / len(self.objs)
                            if u > 0:
                                u_ += u / len(self.objs) / MAX_TEX_TILING
                            u = u_
                        output_textures.append([u, v, w])

        if len(output_normals) + len(output_textures) == 0:
            return np.array(output_vertices, dtype='f4').flatten()

        elif len(output_normals) > 0 and len(output_textures) == 0:
            out = list(zip(output_vertices, output_normals))
            return np.array(out, dtype='f4').flatten()

        elif len(output_textures) > 0 and len(output_normals) == 0:
            out = list(zip(output_vertices, output_textures))
            return np.array(out, dtype='f4').flatten()

        elif len(output_textures) > 0 and len(output_normals) > 0:
            out = list(zip(output_vertices, output_normals, output_textures))
            return np.array(out, dtype='f4').flatten()

    def pack_textures(self):
        assert self.has_textures

        if len(self.objs) == 1:
            tex = self.objs[0].texture_image
        else:
            # in this case we're repeating the texture 4 times to allow up to MAX_TEX_TILINGx repetition
            tex = Image.new(
                'RGB',
                (MAX_TEX_TILING * 500 * len(self.objs), 500 * MAX_TEX_TILING))

            for idx in range(len(self.objs)):
                tmp_tex = self.objs[idx].texture_image.resize(
                    (500, 500), resample=Image.BICUBIC)

                # 4 copies because I can't think of a better way to do this without massive effort
                # this only works with MAX_TEX_TILING == 2. If this is larger then you have to loop over the tex.paste()
                tex.paste(tmp_tex, (500 * MAX_TEX_TILING * idx, 0))
                tex.paste(tmp_tex, (500 * MAX_TEX_TILING * idx + 500, 0))
                tex.paste(tmp_tex, (500 * MAX_TEX_TILING * idx, 500))
                tex.paste(tmp_tex, (500 * MAX_TEX_TILING * idx + 500, 500))

        # import matplotlib.pyplot as plt
        # plt.imshow(tex)
        # plt.show()

        texture = self.ctx.texture(tex.size, 3, tex.tobytes())
        texture.build_mipmaps()
        texture.use()


def get_concat_h_resize(im1, im2, resample=Image.BICUBIC,
                        resize_big_image=True):
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize(
            (int(im1.width * im2.height / im1.height), im2.height),
            resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize(
            (int(im2.width * im1.height / im2.height), im1.height),
            resample=resample)
    dst = Image.new('RGB', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    return dst


class Obj(object):
    """ Very important: we're assuming a verbose format where each
    line of vertex UV coordinates or vertex normal has one corresponding line of vertex

    """

    def __init__(self):
        super().__init__()
        self.vertices = []
        self.faces = []
        self.normals = []
        self.textures = []
        self.has_normals = False
        self.has_texture = False
        self.texture_image = None

    def load_from_file(self, path):
        # TODO we have to deal with the fact that vertex normals and vertex texture coordinates might be reused here
        model = obj.Obj.open(path)
        self.vertices = model.vert
        self.faces = [f[0] - 1 for f in model.face
                     ]  # everything is zero-indexed
        self.faces = [
            self.faces[i:i + 3] for i in range(0, len(self.faces), 3)
        ]  # FIXME: this here is the offender
        self.normals = [list(elem) for elem in model.norm]
        if len(self.normals) > 0:
            self.has_normals = True
        self.textures = model.text
        if len(self.textures) > 0:
            self.has_texture = True
        del model

    def load_from_lists(self, vertices, faces, normals=None, textures=None):
        self.vertices = vertices
        self.faces = faces
        if normals is not None:
            assert len(normals) == len(vertices)
            self.normals = normals
            self.has_normals = True
        if textures is not None:
            assert len(textures) == len(vertices)
            self.textures = textures
            self.has_texture = True

    def add_texture(self, path):
        self.texture_image = Image.open(path)
        self.has_texture = True

    def add_color(self, color=None):
        # This is suboptimal, ideally we should use vertex colors
        # but for that I would have to change the shader code and I'm not gonna touch that right now.
        # Instead, we can create a new texture as color and use that.
        # The problem isn't the texture as color but that it's treated like any other color and resized

        if color is None:
            r, g, b = brith_color()
        else:
            assert len(color) == 3
            r, g, b = color
        self.texture_image = Image.new("RGB", (256, 256), (r, g, b))
        self.has_texture = True
        self.textures = [  # bare minimum
            [0, 0, 0],
            [0, 1, 0],
            [1, 0, 0],
        ]
        for _ in range(len(self.vertices) - 3):
            self.textures.append([np.random.rand(), np.random.rand(), 0])

    def pack(self):
        self.vertices = np.array(self.vertices, dtype=np.float16)
        self.faces = np.array(self.faces, dtype=np.uint)

        if self.has_normals:
            self.normals = np.array(self.normals, dtype=np.float16)
        else:
            self.calc_normals()
            self.has_normals = True  # because the shader expects them

        if self.has_texture:
            assert self.texture_image is not None  # need to call `obj.add_texture(path)` first
            self.textures = np.array(self.textures, dtype=np.float16)

        # for x in [self.vertices, self.faces, self.normals, self.textures]:
        #     print (len(x))

    def rotate(self, x, y, z):
        # in degrees
        r = R.from_euler("xyz", (x, y, z), degrees=True)
        self.vertices = np.array(self.vertices)
        self.vertices = np.matmul(self.vertices, r.as_dcm())

    def translate(self, x, y, z):
        print (f"moving obj by {x}x, {y}y, {z}z")
        self.vertices = np.array(self.vertices)
        self.vertices[:, 0] += x
        self.vertices[:, 1] += y
        self.vertices[:, 2] += z

    def calc_normals(self):
        self.normals = np.zeros(self.vertices.shape, dtype=self.vertices.dtype)
        self.faces = np.array(self.faces)
        self.vertices = np.array(self.vertices)
        tris = self.vertices[self.faces]
        # Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle

        n = np.cross(tris[::, 1] - tris[::, 0], tris[::, 2] - tris[::, 0])
        # n is now an array of normals per triangle. The length of each normal is dependent the vertices,
        # we need to normalize these, so that our next step weights each normal equally.
        n = normalize_v3(n)
        # now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
        # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
        # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
        # The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array

        self.normals[self.faces[:, 0]] += n
        self.normals[self.faces[:, 1]] += n
        self.normals[self.faces[:, 2]] += n
        self.normals = normalize_v3(self.normals)
