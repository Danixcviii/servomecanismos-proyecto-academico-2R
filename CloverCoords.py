import numpy as np
import matplotlib.pyplot as plt

def clover(theta,scl,lfs,rot):
  r = (scl)*(-np.cos(lfs*(theta - rot))+(2*(np.sin(lfs*(theta - rot)))**2) + 7.875)
  return r

points = 200
x = 0  
y = 0
xc = []
yc = []
x0 = 14.5 # Clover center X
y0 = 14.5 # Clover center Y
lfs = 4 # leafs of the clover
rot = np.pi/4 # rotation of the clover
scl = 1.2 # scale of the clover
r = 0
theta = 0

with open("Coords.txt", "w") as txt_file:
  for i in range(points):
    theta = (i*2*np.pi)/(points)
    r = clover(theta,scl,lfs,rot)
    x = r*np.cos(theta) + x0
    y = r*np.sin(theta) + y0
    txt_file.write(str(x) + ";" + str(y) + "\n")
    xc.append(x)
    yc.append(y)

xpoints = np.array(xc)
ypoints = np.array(yc)

fig1, ax = plt.subplots()
plt.plot(xpoints, ypoints,'.', markersize = 1)
plt.grid()
plt.xlim((0,40))
plt.ylim((0,40))
ax.set_box_aspect(1)
plt.show()
