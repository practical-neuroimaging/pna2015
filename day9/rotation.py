import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import numpy as np

def rot(theta):
    C = np.cos(theta)
    S = np.sin(theta)

    return np.array([[C, -S],
                     [S,  C]])

theta = 20
A = rot(np.deg2rad(theta))

P0 = 4, 6
x0, y0 = P0

P1 = A.dot(P0)
x1, y1 = P1

U0 = A[0, :]
U1 = A[1, :]

plt.plot([0, x0], [0, y0], '-o', label='Original')
plt.text(x0 + 0.1, y0, '$(x_0, y_0)$', fontsize=16)

plt.plot([0, x1], [0, y1], '-o', label='Rotated')
plt.text(x1 + 0.1, y1, '$(x_1, y_1)$', fontsize=16)

#plt.plot([0, U0[0]], [0, U0[1]], linewidth=3, label='Unit vector')
plt.annotate("", xy=(U0[0], U0[1]), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->"))


N0 = np.dot(U0, P0)
N1 = np.dot(U1, P0)

NP = N0 * U0

plt.plot([0, N0], [0, 0], '-o')
plt.plot([0, NP[0]], [0, NP[1]], '-o')
plt.plot([NP[0], P0[0]], [NP[1], P0[1]], ':k')
plt.plot([N0, P1[0]], [0, P1[1]], ':k')

plt.text(U0[0] / 2, U0[1] - 0.1, '$u_0$', fontsize=16)
plt.text(0.17, 0.5, r'$\theta$', fontsize=16)
plt.text(0.9, -0.25, r'$\theta$', fontsize=16)

plt.gca().add_artist(
    Arc(xy=(0, 0), width=1.7, height=1.7,
        theta1=np.rad2deg(np.arctan2(*P0[::-1])),
        theta2=np.rad2deg(np.arctan2(*P1[::-1])))
    )

plt.gca().add_artist(
    Arc(xy=(0, 0), width=1.7, height=1.7,
        theta1=-theta,
        theta2=0,)
    )

plt.legend()
plt.axis('equal')

plt.show()
