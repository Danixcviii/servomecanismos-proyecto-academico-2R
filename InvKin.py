import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

a1 = 21 # link lenth in cm
a2 = 21 # link lenth in cm
x0 = 0.0
y0 = 0.0
sens = 1
coords = []

with open(r"Coords.txt", 'r') as fp:
    points = len(fp.readlines())
    
L1x = np.zeros(points*sens)
L2x = np.zeros(points*sens)
L1y = np.zeros(points*sens)
L2y = np.zeros(points*sens)
Q1 = np.zeros(points*sens)
Q2 = np.zeros(points*sens)
q1s = np.zeros(points)
q2s = np.zeros(points)
q1sig = np.zeros(points*sens)
q2sig = np.zeros(points*sens)
tlin = np.zeros(points*sens)
cnt = int(0)

fig = plt.figure(figsize=(15,10))
spec = fig.add_gridspec(2, 4)
ax1 = fig.add_subplot(spec[0,2:4], xlim=(0,len(tlin)))
ax2 = fig.add_subplot(spec[1,2:4], xlim=(0,len(tlin)))
#ax3 = fig.add_subplot(spec[1,2:4])
ax = fig.add_subplot(spec[0:2,0:2], aspect='equal', autoscale_on=False, xlim=(-5,30), ylim=(-22,30))
ax.grid()
ax1.grid()
ax2.grid()
Link1, = ax.plot([], [], 'o-', lw=2, color='#df1f1f')
Link2, = ax.plot([], [], 'o-', lw=2, color='#1f1fdf')
trace, = ax.plot([], [], '.-', markersize = 1,lw=1 , color='#1fdf1f')
trace2, = ax.plot([], [], '.', lw = 1, markersize = 1, alpha = 0.2, color = "#df1fdf")
Q1angle, = ax1.plot([], [], '-', lw = 2, alpha = 1, color="#1fdfdf")
Q2angle, = ax2.plot([], [], '-', lw = 2, alpha = 1, color="#dfdf1f")

with open("Coords.txt") as file:
  for i in file:
    coords = i.split(";")
    x0 = float(coords[0])
    y0 = float(coords[1])

    q2 = np.arccos((x0**2 + y0**2 - a1**2 - a2**2)/(2* a1 *a2))
    q1 = np.arctan2(y0,x0) - np.arctan2(a2*np.sin(q2),a1 + a2*np.cos(q2))

    q1s[cnt] = q1
    q2s[cnt] = q2

    cnt = cnt + 1
    plt.plot(x0, y0,'.',markersize=2, color = '#000000')

q1s = np.append(q1s, [q1s[0]])
q2s = np.append(q2s, [q2s[0]])

for i in range(cnt):
  for j in range(sens):
    tlin[(i*sens)+j] = (i*sens)+j
    q1 = q1s[i]+(((q1s[i+1] - q1s[i]))*(j))/(sens)
    q2 = q2s[i]+(((q2s[i+1] - q2s[i]))*(j))/(sens)
    Q1[(i*sens)+j] = q1
    Q2[(i*sens)+j] = q2
    q1sig[(i*sens)+j] = q1s[i+1]
    q2sig[(i*sens)+j] = q2s[i+1]
    L1x[(i*sens)+j] = a1*np.cos(q1)
    L1y[(i*sens)+j] = a1*np.sin(q1)
    L2x[(i*sens)+j] = a2*np.cos(q2+q1) + L1x[(i*sens)+j]
    L2y[(i*sens)+j] = a2*np.sin(q2+q1) + L1y[(i*sens)+j]

# initialization function
def init():
    Link1.set_data([], [])
    Link2.set_data([], [])
    trace.set_data([], [])
    trace2.set_data([], [])
    Q1angle.set_data([], [])
    Q2angle.set_data([], [])
    return Link1,Link2,trace,trace2,Q1angle,Q2angle

# animation function
def animate(i):
    Link1.set_data([0, L1x[i]], [0,L1y[i]])
    Link2.set_data([L1x[i], L2x[i]], [L1y[i],L2y[i]])
    trace.set_data(L2x[:i],L2y[:i])
    trace2.set_data(L1x[:i],L1y[:i])
    Q1angle.set_data(tlin[:i], (180/np.pi)*Q1[:i])
    Q2angle.set_data(tlin[:i], (180/np.pi)*Q2[:i])
    return Link1,Link2,trace,trace2,Q1angle,Q2angle

ax1.step(tlin,(180/np.pi)*q1sig, '-' , color='#df1f1f', lw = 1)
ax2.step(tlin,(180/np.pi)*q2sig, '-', color='#1f1fdf', lw = 1)
#ax3.plot((Q2-Q1))

# call the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=cnt*sens, interval=(100)/6, blit=True, repeat=True)

print('start ani')
ani.save('2r_Robot_Animation.gif')
print('saved ani')

# plt.show()