from pyrr import Matrix44


class Camera(object):
    def __init__(self, width, height, eye, near=0.001, far=10, fov=60, lookat=(0, 0, 0), up=(0, 0, 1)):
        super().__init__()
        self.width = width
        self.height = height
        self.near = near
        self.far = far
        self.fov = fov
        self.eye = eye
        self.lookat = lookat
        self.up = up

    def get_view_model(self):
        proj = Matrix44.perspective_projection(self.fov, self.width / self.height, self.near, self.far)
        lookat = Matrix44.look_at(
            self.eye,  # eye / camera position
            self.lookat,  # lookat
            self.up,  # camera up vector
        )
        return proj, lookat

    def size(self):
        return (self.height, self.width)