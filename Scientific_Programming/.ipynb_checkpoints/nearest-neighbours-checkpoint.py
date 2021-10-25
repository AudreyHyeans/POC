#!/usr/bin/env python3
"""
nearest neighbours algorithm in 2d
"""

import numpy as np
import matplotlib.pyplot as plt
import random

#Set plot style
plt.rcParams.update({
    "lines.linewidth": 2,
    "axes.grid": True,
    #"text.usetex": True,
    #"font.family": "serif",
})
n_pts = 10

x = np.random.random_sample(n_pts)
y = np.random.random_sample(n_pts)

# We attribute an integer label from 0 to 1 for each point
# corresonding to its place in the x and y arrays.
# Then we will work on sorted arrays along x and y axis.
xi_srt = np.argsort(x)
yi_srt = np.argsort(y)

# These arrays help us to find where an
# point is located in the sorted array.
whr_xi = np.argsort(xi_srt)
whr_yi = np.argsort(yi_srt)

for i in range(1,n_pts-1):
    xi = xi_srt[i]

    nghbr = True
    d_ngbrx = 1
    d_ngbry = 1
    j = 1
    dr1 = abs(whr_yi[xi]-whr_yi[xi_srt[i+1]])
    dl1 = abs(whr_yi[xi]-whr_yi[xi_srt[i-1]])
    d1 = dr1 if dr1 <
    for j in range(-d1,d1+1):
        d_ngbrx = j**2
        d_ngbrx += abs(whr_yi[xi]-whr_yi[xi_srt[i+j]])**2

        d_ngbry += abs(whr_yi[xi]-whr_xi(xi_srt[i+1]))**2
        d_ngbry = abs(whr_xi[xi]-whr_xi(xi_srt[i+1]))**2
