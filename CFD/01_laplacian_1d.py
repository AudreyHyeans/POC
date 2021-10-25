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
#%%
#1st question)

plt.ion()
plt.close("all")

# set up a spatial discretization
L = 2.*np.pi
nx = 50

# define the x locations
dx = L/nx
#dx est le pas
xe = np.arange(nx+1)*dx

# set up an analytical function
def phi_analytical(x):
    return np.sin(x)


# discrete phi
phi = phi_analytical(xe)


#xe are the coordinate of the edges
f1 = plt.figure()
plt.plot(xe, phi)


# boundary values
a = phi_analytical(0)
b = phi_analytical(L)

print("boundary conditions")
print(f"  - phi(0) = {a}")
print(f"  - phi(L) = {b}")

# TODO compute the discrete f_i, plot it, compare it to the analytical
# solution and compute the Linfinity norm

#we initialize f as a vector of zeros, nx+1 is the number of edges
f = np.zeros((nx+1,))

#we delete the extreme edges = 0 and L because we can't compute the derivation 
#at these points 
f[0] = np.nan
f[-1] = np.nan

#we compute the discret function f
for i in range(1,nx):
    #we compute at the 2nd order to be more precise. 
    #The more we increase the derivation order, the more we have an exact estimation 
    #of the discret f.
    f[i] = (phi[i+1] + phi[i-1] - 2*phi[i]) / dx**2

#we define the analytical function
def analytic_function(x):
    return -np.sin(x)


#figure that compares the 2 solutions : analytical and discret

error = f - analytic_function(xe)
#error is an array

#for f = -sin(x)
f3 = plt.figure()
plt.title('Analytical and discret function with the error')
plt.plot(xe,f, label = 'Discret solution')
plt.plot(xe,analytic_function(xe),'magenta', label = 'Analytical solution')
plt.plot(xe, error,'--', label='difference between analytical and discret')
plt.legend()
plt.grid()

f4 = plt.figure()
plt.title('error ie the difference between f and f_analytic')
plt.plot(xe,error)
plt.grid()


#%%
#2nd question)
# TODO: convergence study: plot the Linf error as a function of nx in
# a log-log plot. Show that the discretization is second order
# Hint: compute the error for these resolutions
#
# >>> nxs = 10*(2**np.arange(10))

#we define the resolution
nxs = 10*(2**np.arange(10))


#I couldn't print the correct graph and find alpha,
#Indeed I plot a constant function, my norm is constant, I don't understand why
def function_norm_error(nxs):
    eps = np.zeros((nxs.size,))
    for i in range (len(nxs)):
        error = f - analytic_function(xe)
        """we define the infinite norm of the error"""
        eps[i] = np.linalg.norm(error[1:-1], ord=np.inf)
    return(eps)

norm = function_norm_error(nxs)
print(norm)
print(error)
#In order to observe the Linf error as a function of nx
f3 = plt.figure()
plt.title('Log of the norm error')
plt.loglog(nxs,norm)
plt.ylim(1*10**(-3),2*10**(-3))
print(norm)  


# evaluate the slope

p = np.polyfit(np.log(nxs), np.log(norm), 1)

print(p)
#we can deduce that the eps is proportionnal to nx**(-alpha) or to h**alpha, here alpha is the 

#%%
#3rd question
# TODO: rewrite the laplacian in vectorized form = without loop


#entre les points d'indices i-1 et i+1 on a un écart de 2*dx, donc on décale la liste de 2 termes
#le point d'indice i se situe au milieu(écart de dx avec les autres termes), donc on décale de 1 seulement.
f =  (phi[2:] + phi[:-2] - 2*phi[1:-1]) /dx**2
# TODO: compute the laplacian with a matrix * vector operation hint:
# define the Laplacian matrix, if A is the matrix, A.dot(phi) does the
# matrix * vector multiplication

#This is a way to create the matrix M but it is not the most rapidly. 


#I define the matrix M full of zeros
nx=50
M = np.zeros((nx+1,nx+1))
#indexes of my matrix
m = np.arange(0,nx+1)
#bondary conditions
a = phi_analytical(0)
b = phi_analytical(L)
#print(a,b)

#in order to have my whole problem (differential equation and boundaries),
#I add the boundaries a,b resp. at the first and last lines of M
M[ [m[0]] , [m[0:nx]] ] = a
M[ [m[nx]] , [m[0:nx]] ] = b
M[[m],[m]] = -2/(dx**2)
#terms below and upon the diagonal
M[ [m[1:nx+1]] , [m[0:nx]] ] = 1/(dx**2)
M[ [m[0:nx]] , [m[1:nx+1]] ] = 1/(dx**2)
#print(M)

#I plot the function f
f = M.dot(phi)
f[0] = np.nan
f[-1] = np.nan
print(f)
f4 = plt.figure()
plt.plot(xe,f, 'orange',label = 'Laplacian computed with a matrix*vector')
plt.legend()
#%%
#4th question)

# TODO retrieve the discretized phi using f and (a, b) by solving
# the system of equation. Use np.linalg.solve
discretized_phi = np.linalg.solve(M,analytic_function(xe))
f5 = plt.figure()
plt.plot(xe,discretized_phi,'pink', label = 'Dicretized phi using linalg.solve')
plt.legend()

# TODO redo the computation with a sparse matrix instead of full matrix

# hint:

# from scipy.sparse import linalg
# from scipy import -1
M_truncated = M[1:-1,1:-1]
print('M_truncated', M_truncated)
print('M_truncated.shape', M_truncated.shape)

#test
def truncated_matrice(nx):
    Test = np.arange((nx+1)**2)
    #permet de reshape une matrice, on peut passer de 2D à 3D
    Test.shape = (nx+1,nx+1)
    Test_concatenate = Test[1:-1,1:-1]
    print(Test.shape, Test_concatenate.shape)
from scipy.sparse import linalg
from scipy import sparse
from numpy import linalg
#matrice singulière?
print('determinant de M_truncated', linalg.det(M_truncated))
#ATTENTION, il faut copier la matrice, sinon on modifie f et f_truncated.
f_truncated = f[1:-1].copy()
f_truncated[0] -= a/dx**2
f_truncated[-1] -= b/dx**2

phi_truncated = linalg.solve(M_truncated, f_truncated)
print('phi_truncated', phi_truncated)
print('f_truncated',f_truncated)
print('f',f)

phi_solution = np.zeros((nx+1),)
phi_solution[0] = a
phi_solution[-1]  = b
phi_solution = phi_truncated[1:-1]
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

