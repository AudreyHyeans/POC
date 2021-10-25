import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse import linalg as la


plt.ion()
import matplotlib as mpl

#plt.close('all')

mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 12
mpl.rcParams['lines.markeredgewidth'] = 2
mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.labelsize'] = 14

nx = 8
ny = 4

Lx = 4
Ly = 2

shape = (ny, nx)
dx = Lx/nx
dy = Ly/ny

xc = (np.arange(nx)+0.5)*dx
yc = (np.arange(ny)+0.5)*dy

xxc, yyc = np.meshgrid(xc, yc)


# define msk
msk = np.ones(shape, dtype="b")
msk[:ny//3, :nx//3] = 0

print(msk)
N = msk.sum()
print("N=",N)


# define G
G = np.zeros(ny*nx, dtype="i")
G[:] = -1
G[msk.flat>0] = np.arange(N)
G.shape = shape

j, i = np.where(msk == 1)

# define laplacian

# regular neighbours West, East, South and North
#it's a dictionnary : there's a word : the definition here it's the label of the data and then the definition of it.
#For instance we can write the density of the ocean at a point:
parameters {"rho":1000., "g":9.81, "Lx":250.}
type(parameters)
parameters.keys()
parameters["g"]
neighbours = {
    (-1, 0): dx/dy,
    (1, 0): dx/dy,
    (0, -1): dy/dx,
    (0, 1): dy/dx
    }


data = np.zeros((5*N,))
rows = np.zeros((5*N,), dtype=int)
cols = np.zeros((5*N,), dtype=int)
count = 0

for k in range(N):
    nbneighb = 0
    cdiag = 0.
    j0, i0 = j[k], i[k]
    #loop on the neighbours
    for who, coef in neighbours.items():
        dj, di = who[0], who[1]
        j1 = j0+dj
        i1 = i0+di
        inside = ( (0 <= i1 < nx) and (0<= j1 < ny))
        # set the coefficient only if the neighbour is inside the grid
        if inside:
            l = G[j1, i1]
            # and is interior
            if l > -1:
                rows[count], cols[count], data[count] = k, l, coef
                count += 1
                nbneighb += coef
                cdiag -= coef
            else:
                cdiag -= 2*coef
        else:            
            cdiag -= 2*coef
        
    rows[count], cols[count], data[count] = k, k, cdiag
    count += 1
        
A = sparse.coo_matrix(
    (data[:count], (rows[:count], cols[:count])),
    shape=(N, N) ).tocsr()

if True:
    b = np.zeros((N,))
    b[N//5] = 1
    b[3*N//5] =-1
    b *= dx*dy
    x = la.spsolve(A, b)
    phi = np.zeros(shape)
    phi[G>-1] = x

    plt.figure()
    plt.imshow(phi, origin="lower")
    plt.colorbar()
else:
    d2 = (xxc-Lx*.3)**2 + (yyc-Ly*.7)**2
    rhs = np.exp(-d2/(2*0.1**2))
    d2 = (xxc-Lx*.6)**2 + (yyc-Ly*.2)**2
    rhs -= np.exp(-d2/(2*0.1**2))

    b = rhs[G>-1]
    b *= dx*dy
    x = la.spsolve(A, b)
    phi = np.zeros(shape)
    phi[G>-1] = x
    phi[G==-1] = np.nan

    plt.figure()
    plt.contourf(xc,yc, phi, 20)
    plt.colorbar()
    #plt.tight_layout()
    plt.axis("equal")
    plt.axis([0, Lx, 0, Ly])
