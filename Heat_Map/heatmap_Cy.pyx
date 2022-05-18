#cython: language_level=3

import numpy as np
cimport numpy as cnp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cython 

# Set the colormap
plt.rcParams['image.cmap'] = 'BrBG'

cdef evolve(cnp.ndarray[cnp.double_t, ndim=2] u, cnp.ndarray[cnp.double_t, ndim=2] u_previous, float a, float dt, float dx2, float dy2):
    """
    Explicit time evolution.
       u:            new temperature field
       u_previous:   previous field
       a:            diffusion constant
       dt:           time step. 
    """

    cdef int n = u.shape[0] 
    cdef int m = u.shape[1]
    
    cdef int i, j

    for i in range(1, n-1):
        for j in range(1, m-1):
            u[i, j] = u_previous[i, j] + a * dt * ( \
             (u_previous[i+1, j] - 2*u_previous[i, j] + \
              u_previous[i-1, j]) / dx2 + \
             (u_previous[i, j+1] - 2*u_previous[i, j] + \
                 u_previous[i, j-1]) / dy2 )
    u_previous[:] = u[:]

cpdef iterate(cnp.ndarray[cnp.double_t, ndim=2] field, cnp.ndarray[cnp.double_t, ndim=2] field0, float a, float dx, float dy, int timesteps, int image_interval):
    """Run fixed number of time steps of heat equation"""

    cdef float dx2 = dx**2
    cdef float dy2 = dy**2

    # For stability, this is the largest interval possible
    # for the size of the time-step:
    cdef float dt = dx2*dy2 / ( 2*a*(dx2+dy2) )    
    cdef int m

    for m in range(1, timesteps+1):
        evolve(field, field0, a, dt, dx2, dy2)
        if m % image_interval == 0:
            write_field(field, m)

cpdef init_fields(str filename):
    # Read the initial temperature field from file
    cdef cnp.ndarray[cnp.double_t, ndim=2] field = np.loadtxt(filename)
    cdef cnp.ndarray[cnp.double_t, ndim=2] field0 = field.copy() # Array for field of previous time step
    return field, field0

cpdef write_field(cnp.ndarray[cnp.double_t, ndim=2] field, int step):
    plt.gca().clear()
    plt.imshow(field)
    plt.axis('off')
    # plt.savefig('heat_{0:03d}.png'.format(step))


