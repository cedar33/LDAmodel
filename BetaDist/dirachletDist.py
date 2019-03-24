from betaFunction import gamma_func
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import time


def delta_func(alpha):
    '''alpha: list'''
    numerator = 1
    denominator = 0
    for a in alpha:
        numerator *= gamma_func(a)
        denominator += a
    denominator = gamma_func(denominator)
    return numerator/denominator

def diric_dist(p, alpha, delta):
    factor = 1
    for _p, a in zip(p, alpha):
        factor *= _p**(a-1)
    return factor/delta
print("start calculate")


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = np.arange(0, 1, 0.01)
Y = np.arange(0, 1, 0.01)
dim_0 = []
alpha = np.array([2, 2, 2])
for i in range(100):
    print(i)
    delta = delta_func(alpha)
    dim_1 = []
    for x in X:
        dim_2 = []
        for y in Y:
            z = 1-x-y
            if z > 0:
                dim_2.append(diric_dist([x,y,z], alpha, delta=delta))
            else:
                dim_2.append(0)
        dim_1.append(dim_2)
    dim_0.append(np.array(dim_1))
    alpha = alpha + 0.1

R = dim_0
X, Y = np.meshgrid(X, Y)

# Plot the surface.
# surf = ax.plot_surface(X, Y, R, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)

# Customize the z axis.
# ax.set_zlim(0, 10)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)

# plt.show()
# Begin plotting.
surf = None
tstart = time.time()
while 1:
    ax.set_zlim(0, 30)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    for R in dim_0:
        # If a line collection is already remove it before drawing.
        if surf:
            ax.collections.remove(surf)
        # Plot the new wireframe and pause briefly before continuing.
        surf = ax.plot_surface(X, Y, R, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        # fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.pause(.2)
    print('Average FPS: %f' % (100 / (time.time() - tstart)))
