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

