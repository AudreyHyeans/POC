"""
 compute phi(x) for x in [0, L]

 with 

 d^2 phi / dx^2 = f(x)

 f(x) given and with boundary conditions

 phi(0) = a
 phi(L) = b

 using finite differences

 1/ Start from a solution phi(x) and compute a, b and the discrete f_i

 2/ Use f_i, a and b to retrieve the discrete phi_i
"""
import numpy as np
import matplotlib.pyplot as plt

plt.ion()
plt.close("all")

# set up a spatial discretization
L = 2.*np.pi
nx = 500

# define the x locations
dx = L/nx
xe = np.arange(nx+1)*dx

# set up an analytical function
def phi_analytical(x):
    # return x**2/2
    return np.sin(x)


# discrete phi
phi = phi_analytical(xe)

plt.figure()
plt.plot(xe, phi)

# boundary values
a = phi_analytical(0)
b = phi_analytical(L)
print("boundary conditions")
print(f"  - phi(0) = {a}")
print(f"  - phi(L) = {b}")

# TODO compute the discrete f_i, plot it, compare it to the analytical
# solution and compute the Linfinity norm
f = np.zeros((nx+1,))


# TODO: convergence study: plot the Linf error as a function of nx in
# a log-log plot. Show that the discretization is second order
# Hint: compute the error for these resolutions
#
# >>> nxs = 10*(2**np.arange(10))

nxs = 10*(2**np.arange(10))



# TODO: rewrite the laplacian in vectorized form = without loop


# TODO: compute the laplacian with a matrix * vector operation hint:
# define the Laplacian matrix, if A is the matrix, A.dot(phi) does the
# matrix * vector multiplication

# TODO retrieve the discretized phi using f and (a, b) by solving
# the system of equation. Use np.linalg.solve



# TODO redo the computation with a sparse matrix instead of full matrix

# hint:

# from scipy.sparse import linalg
# from scipy import sparse

from scipy.sparse import linalg
from scipy import sparse



# TODO compute the discrete phi from the discrete f using Neumann
# boundary conditions (the value of the derivative is imposed at
# endpoints) hint: copy-paste the Dirichlet BC case and adapt it to
# the Neumann BC case


# TODO adapt the Dirichlet case in the case of a non-uniform
# discretization Instead of using

# >>> xe = np.arange(nx+1)*dx

# use

# >>> xe = g( np.arange(nx+1)/(nx+1) )

# with

# def g(x):    
#     return L*x**2

