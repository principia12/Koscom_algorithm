from scipy.spatial.distance import pdist, squareform
from particlebox import ParticleBox
from forces import gravitational_force, restoring_force

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation




#------------------------------------------------------------
# set up initial state
np.random.seed(0)

NUMBER_OF_PARTICLES = 50
MEAN_VELOCITY = 1
init_state = []

for i in range(NUMBER_OF_PARTICLES):
    # initial position 
    x_init, y_init = np.random.random(), np.random.random()
    x_init = 4 * (x_init - 0.5)
    y_init = 4 * (y_init - 0.5)
    
    # initial velocity
    v_dir_init = np.random.random()
    v_dir_init = 2*np.pi*v_dir_init
    v_x_init = MEAN_VELOCITY * np.cos(v_dir_init)
    v_y_init = MEAN_VELOCITY * np.sin(v_dir_init)
    init_state.append([x_init, y_init, v_x_init, v_y_init])

init_state = -0.5 + np.random.random((NUMBER_OF_PARTICLES, 4))
init_state[:, :2] *= 3.9

'''
box = ParticleBox(init_state = [[1.0,0.0,0.0,0.0], 
                                [-1.0,0.0,0.0,0.0]], 
                  size=0.04, 
                  G = 0, 
                  interaction = restoring_force,)
'''
box = ParticleBox(init_state = init_state, 
                  G = 0.0, 
                  interaction = lambda x,y:(0,0))

dt = 1. / 30 # 30fps


#------------------------------------------------------------
# set up figure and animation
fig = plt.figure()

fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

# particles holds the locations of the particles
particles, = ax.plot([], [], 'bo', ms=6)

# rect is the box edge
rect = plt.Rectangle(box.bounds[::2],
                     box.bounds[1] - box.bounds[0],
                     box.bounds[3] - box.bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(rect)

def init():
    """initialize animation"""
    global box, rect
    particles.set_data([], [])
    rect.set_edgecolor('none')
    return particles, rect

def animate(i):
    """perform animation step"""
    global box, rect, dt, ax, fig
    box.step(dt)

    ms = int(fig.dpi * 2 * box.size * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])
    
    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(box.state[:, 0], box.state[:, 1])
    particles.set_markersize(ms)
    return particles, rect

ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)


# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#ani.save('particle_box.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()