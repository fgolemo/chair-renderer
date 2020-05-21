import matplotlib.pyplot as plt
import numpy as np

# PATH = "mgl-test-{}.png"
# OUT = "mgl-test.csv"
PATH = "chair/0004-{}.png"
OUT = "chair-test.csv"

img = plt.imread(PATH.format("rgb"))
print (img.shape, img.min(), img.max(), img.dtype)
# img = (img*255).astype(np.uint8)
# print (img.min(), img.max())
depth = plt.imread(PATH.format("depth"))
print (depth.shape, depth.min(), depth.max(), depth.dtype)

out = []

for y in range(512):
    for x in range(512):
        z = depth[x,y]
        r = img[x,y,0]
        g = img[x,y,1]
        b = img[x,y,2]
        out.append(f"{x},{y},{z},{r},{g},{b}\n")

with open(OUT, "w") as f:
    f.writelines(out)

