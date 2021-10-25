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
nx = 100

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
for i in range(1, nx):
    f[i] = (phi[i+1]+phi[i-1]-2*phi[i])/dx**2
# evaluation of f @ endpoints
f[0] = np.nan
f[-1] = np.nan
plt.plot(xe, f, "+-")

# let's compare f with the true analytical
def f_analytical(x):
    return -np.sin(x)


error = f-f_analytical(xe)
plt.figure()
plt.plot(xe, error)

# let us see how the norm of the error vary with the resolution
epsilon = np.linalg.norm(error[1:-1], ord=np.inf)
print(f"resolution: {nx} /  norm of error: {epsilon:.3e}")


# TODO: convergence study: plot the Linf error as a function of nx in
# a log-log plot. Show that the discretization is second order
# Hint: compute the error for these resolutions
#
# >>> nxs = 10*(2**np.arange(10))

nxs = 10*(2**np.arange(10))


def compute_error(nxs):
    epsilon = np.zeros((nxs.size,))
    for k, nx in enumerate(nxs):
        dx = L/nx
        xe = np.arange(nx+1)*dx
        phi = phi_analytical(xe)
        f = np.zeros((nx+1,))
        for i in range(1, nx):
            f[i] = (phi[i+1]+phi[i-1]-2*phi[i])/dx**2
            # evaluation of f @ endpoints
            f[0] = np.nan
            f[-1] = np.nan

        error = f-f_analytical(xe)

        epsilon[k] = np.linalg.norm(error[1:-1], ord=np.inf)
    return epsilon


epsilon = compute_error(nxs)

plt.figure()
plt.loglog(nxs, epsilon, "+-")
plt.grid()
plt.xlabel(r"$n_x$")
plt.ylabel(r"$||\epsilon||_\infty$")

# evaluate the slope

p = np.polyfit(np.log(nxs), np.log(epsilon), 1)

print(f"slope : {p[0]:.2f}")


# TODO: rewrite the laplacian in vectorized form = without loop
def laplacian_with_loop(phi, dx):
    f = np.zeros((nx+1,))
    for i in range(1, nx):
        f[i] = (phi[i+1]+phi[i-1]-2*phi[i])/dx**2
        # evaluation of f @ endpoints
        f[0] = np.nan
        f[-1] = np.nan
    return f


def laplacian_vectorized(phi, dx):
    f = np.zeros((nx+1,))
    f[1:-1] = (phi[2:]+phi[:-2]-2*phi[1:-1])/dx**2
    f[0] = np.nan
    f[-1] = np.nan
    return f


# check that the two methods return the same result
floop = laplacian_with_loop(phi, dx)
fvect = laplacian_vectorized(phi, dx)
assert np.allclose(floop[1:-1], fvect[1:-1])


# TODO: compute the laplacian with a matrix * vector operation hint:
# define the Laplacian matrix, if A is the matrix, A.dot(phi) does the
# matrix * vector multiplication
A = np.zeros((nx+1, nx+1))
for i in range(1, nx):
    A[i, i-1] = 1/dx**2
    A[i, i+1] = 1/dx**2
    A[i, i] = -2/dx**2

A[0, 0] = np.nan
A[-1, -1] = np.nan


def laplacian_with_matrix(phi, A):
    return A.dot(phi)


fmat = laplacian_with_matrix(phi, A)

print(fmat-fvect)
assert np.allclose(floop[1:-1], fmat[1:-1])


# TODO retrieve the discretized phi using f and (a, b) by solving
# the system of equation. Use np.linalg.solve

phi_recomputed = np.linalg.solve(A, fmat)
print(phi_recomputed)

# we need to fix this nan's
Ainterior = np.zeros((nx-1, nx-1))
for i in range(nx-1):
    if i > 0:
        Ainterior[i, i-1] = 1/dx**2
    if i < nx-2:
        Ainterior[i, i+1] = 1/dx**2
    Ainterior[i, i] = -2/dx**2

rhs = floop[1:-1]
rhs[0] += -a/dx**2
rhs[-1] += b/dx**2

phi_interior = np.linalg.solve(Ainterior, rhs)
phi_recomputed[0] = a
phi_recomputed[-1] = b
phi_recomputed[1:-1] = phi_interior

plt.figure()
plt.plot(xe, phi)
plt.plot(xe, phi_recomputed, '+')


# TODO redo the computation with a sparse matrix instead of full matrix

# hint:

# from scipy.sparse import linalg
# from scipy import sparse

from scipy.sparse import linalg
from scipy import sparse

I = []
J = []
coef = []
for i in range(nx-1):
    if i > 0:
        I += [i]
        J += [i-1]
        coef += [1/dx**2]
    if i < nx-2:
        I += [i]
        J += [i+1]
        coef += [1/dx**2]
    I += [i]
    J += [i]
    coef += [-2/dx**2]

Asparse = sparse.coo_matrix((coef, (I, J)), shape=(nx-1, nx-1)).tocsr()

assert np.allclose(Asparse.todense(), Ainterior)

phi_interior = linalg.spsolve(Asparse, rhs)
phi_recomputed[0] = a
phi_recomputed[-1] = b
phi_recomputed[1:-1] = phi_interior
plt.plot(xe, phi_recomputed, 'o', alpha=0.4)



# TODO compute the discrete phi from the discrete f using Neumann
# boundary conditions (the value of the derivative is imposed at
# endpoints) hint: copy-paste the Dirichlet BC case and adapt it to
# the Neumann BC case

I = []
J = []
coef = []
for i in range(nx+1):
    cdiag = 0.
    if i > 0:
        I += [i]
        J += [i-1]
        coef += [1/dx**2]
        cdiag -= 1/dx**2
    if i < nx:
        I += [i]
        J += [i+1]
        coef += [1/dx**2]
        cdiag -= 1/dx**2
    I += [i]
    J += [i]
    coef += [cdiag]

A_neumann = sparse.coo_matrix((coef, (I, J)), shape=(nx+1, nx+1)).tocsr()

# let's check that the matrix is okay
print(A_neumann.todense()*dx**2)

# boundary conditions are A and B -> add them at the begining of the script
A = 0.
B = 1.

rhs = -np.sin(xe)
# add boundary values
rhs[0] = (rhs[0]+A/dx)/2.
rhs[-1] = (rhs[-1]-B/dx)/2.

# let's now solve
# > unfortunately it fails because ... the matrix is singular
phi_computed = linalg.spsolve(A_neumann, rhs)

# reason: phi is determined up to a constant
# let's declare that phi[-1] = 0., so the last element is not part
# of the unknown and the pb now has nx unknown -> the matrix is (nx, nx)

A_neumann2 = A_neumann[:nx, :nx]
# let's check that the matrix is okay
print(A_neumann2.todense()*dx**2)

phi_computed = np.zeros((nx+1,))
phi_computed[:nx] = linalg.spsolve(A_neumann2, rhs[:nx])


# okay that's look okay
plt.figure()
plt.plot(xe, phi_computed)

# observe that the numerical solution depends on A but not on B!!!
# you can set A or B, but not both of them. A and B are coupled


# TODO adapt the Dirichlet case in the case of a non-uniform
# discretization Instead of using

# >>> xe = np.arange(nx+1)*dx

# use

# >>> xe = g( np.arange(nx+1)/nx )

# with

# def g(x):    
#     return L*x**2

def g(x):
    return (x*0.1+2*x**2) * L

xe = g( np.arange(nx+1)/nx )
xc = g( (0.5+np.arange(nx))/nx )
dx = xe[1:]-xe[:-1]

I = []
J = []
coef = []
for i in range(nx+1):
    cdiag = 0.
    if i > 0:
        I += [i]
        J += [i-1]
        c = 1/dx[i-1]
        coef += [c]
        cdiag -= c
    if i < nx:
        I += [i]
        J += [i+1]
        c = 1/dx[i]
        coef += [c]
        cdiag  -= c
    I += [i]
    J += [i]
    coef += [cdiag]

Adirichlet = sparse.coo_matrix((coef, (I, J)), shape=(nx+1, nx+1)).tocsr()
Adirichlet = Adirichlet[1:-1,1:-1]

print(Adirichlet.todense())


def f(x):
    return np.sin(x)

def F(x):
    # double primitive of f
    return -np.sin(x)



dxe = xc[1:]-xc[:-1]
rhs = f(xe[1:-1])*dxe
a = F(0)
b = F(g(1))
rhs[0] += a/dx[0]
rhs[-1] -= b/dx[-1]

phi = np.zeros((nx+1,))
phi[0] = a
phi[-1] = b
phi[1:-1] = linalg.spsolve(Adirichlet, rhs)

plt.figure()
plt.plot(xe, -f(xe), "-", label="-f(x)")
plt.plot(xe, phi, "+", label=r"$\phi(x)$")
plt.legend()
