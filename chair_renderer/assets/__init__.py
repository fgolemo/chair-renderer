import os

ASSET_DIR = os.path.dirname(os.path.realpath(__file__))
TEXTURES = [x for x in os.listdir(f"{ASSET_DIR}/textures") if ".jpg" in x[-4:]]
TEXTURES.sort()

def get_tex(id):
    return f"{ASSET_DIR}/textures/{TEXTURES[id]}"