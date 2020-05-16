import matplotlib.pyplot as plt
import numpy as np

PATH = "sun3d-{}"

img = plt.imread(PATH.format("rgb.jpg"))
print (img.shape, img.min(), img.max(), img.dtype)
depth1 = plt.imread(PATH.format("depth-raw.png"))
print (depth1.shape, depth1.min(), depth1.max(), depth1.dtype)

depth2 = plt.imread(PATH.format("depth-normal.png"))
print (depth2.shape, depth2.min(), depth2.max(), depth2.dtype)

fig, axs = plt.subplots(3, 3)

axs[0,0].imshow(img)
axs[0,0].set_title('RGB')
axs[0,0].set_axis_off()

axs[0,1].imshow(depth1)
axs[0,1].set_title('Depth "raw"')
axs[0,1].set_axis_off()

axs[0,2].imshow(depth2)
axs[0,2].set_title('Depth "normal"')
axs[0,2].set_axis_off()

# axs[0,0].imshow(img)
# axs[0,0].set_title('RGB')
# axs[0,0].set_axis_off()

row = depth1[5,:]
x = np.arange(len(row))
axs[1,1].plot(x,row)
axs[1,1].set_title('Depth "raw"\nhorizontal wall slice')
# axs[1,1].set_axis_off()

row = depth2[5,:]
x = np.arange(len(row))
axs[1,2].plot(x,row)
axs[1,2].set_title('Depth "normal"\nhorizontal wall slice')
# axs[1,2].set_axis_off()

col = depth1[:,-1]
x = np.arange(len(col))
axs[2,1].plot(x,col)
axs[2,1].set_title('Depth "raw"\nvertical bed slice')
# axs[2,1].set_axis_off()

col = depth2[:,-1]
x = np.arange(len(col))
axs[2,2].plot(x,col)
axs[2,2].set_title('Depth "normal"\nvertical bed slice')
# axs[2,2].set_axis_off()

axs[1,0].set_axis_off()
axs[2,0].set_axis_off()

plt.tight_layout()
plt.show()
