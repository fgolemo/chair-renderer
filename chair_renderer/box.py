from chair_renderer.objects import Obj

vertices = [
    [-1.5, -1.5, -.5],
    [-1.5, 2, -.5],
    [1.5, -1.5, -.5],
    [1.5, 2, -.5],
]

faces = [
    [0, 1, 2],
    [3, 1, 2]
]

normals = [
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1]
]

textures = [
    [0, 0, 0],
    [0, 2, 0],
    [2, 0, 0],
    [2, 2, 0]
]

floor = Obj()
floor.load_from_lists(vertices, faces, normals, textures)
floor.add_texture("face.jpg")


vertices = [
    [-1.5, -1.5, -.5],
    [-1.5, -1.5, 2],
    [-1.5, 2, -.5],
    [-1.5, 2, 2],
]

faces = [
    [0, 1, 2],
    [3, 1, 2]
]

normals = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0]
]

textures = [
    [2, 2, 0],
    [2, 0, 0],
    [0, 2, 0],
    [0, 0, 0]
]

right = Obj()
right.load_from_lists(vertices, faces, normals, textures)
right.add_texture("face.jpg")



vertices = [
    [1.5, -1.5, -.5],
    [1.5, -1.5, 2],
    [1.5, 2, -.5],
    [1.5, 2, 2],
]

faces = [
    [0, 1, 2],
    [3, 1, 2]
]

normals = [
    [-1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0]
]

textures = [
    [0, 2, 0],
    [0, 0, 0],
    [2, 2, 0],
    [2, 0, 0]
]

left = Obj()
left.load_from_lists(vertices, faces, normals, textures)
left.add_texture("face.jpg")


vertices = [
    [1.5, -1.5, -.5],
    [1.5, -1.5, 2],
    [-1.5, -1.5, -.5],
    [-1.5, -1.5, 2],
]

faces = [
    [0, 1, 2],
    [3, 1, 2]
]

normals = [
    [-1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0]
]

textures = [
    [2, 2, 0],
    [2, 0, 0],
    [0, 2, 0],
    [0, 0, 0]
]

back = Obj()
back.load_from_lists(vertices, faces, normals, textures)
back.add_texture("face.jpg")


