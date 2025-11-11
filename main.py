import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

IMAGE_PATH = "C:/Users/Pigeon/Pictures/cat.jpg"

try:
    img = Image.open(IMAGE_PATH)
except:
    IMAGE_PATH = input("Enter image path: ").strip().strip('"')
    img = Image.open(IMAGE_PATH)

if img.mode != 'RGB':
    img = img.convert('RGB')

img.thumbnail((150, 150), Image.Resampling.LANCZOS)
img_data = np.array(img) / 255.0
img_data = img_data[::2, ::2]
h, w = img_data.shape[:2]

fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.set_axis_off()

size = max(w, h) / 100
aspect = w / h

if aspect > 1:
    x = np.linspace(-size, size, w)
    y = np.linspace(-size/aspect, size/aspect, h)
else:
    x = np.linspace(-size*aspect, size*aspect, w)
    y = np.linspace(-size, size, h)

X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

angle = 0

def animate(frame):
    global angle
    ax.clear()
    ax.set_xlim([-size*1.5, size*1.5])
    ax.set_ylim([-size*1.5, size*1.5])
    ax.set_zlim([-size*1.5, size*1.5])
    ax.set_box_aspect([1, 1, 1])
    ax.set_axis_off()
    ax.set_facecolor('black')
    
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    X_rot = X * cos_a + Z * sin_a
    Z_rot = -X * sin_a + Z * cos_a
    
    stride = max(2, min(w, h) // 20)
    ax.plot_surface(X_rot, Y, Z_rot, facecolors=img_data, 
                    rstride=stride, cstride=stride, linewidth=0, antialiased=False)
    angle += 0.05

animate(0)
ani = FuncAnimation(fig, animate, frames=180, interval=50, blit=False, repeat=True)
plt.show()
