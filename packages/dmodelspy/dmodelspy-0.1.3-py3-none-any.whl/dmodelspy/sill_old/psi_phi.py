from numpy import dot, zeros, concatenate, eye, pi
from numpy.linalg import solve

from .gauleg import gauleg
from .T import T


def psi_phi(h):
    """
    compute the functions phi(t) and psi(t)

    Using the Nystrom routine with the  N-point Gauss-Legendre rule
    (Numerical Recipes in Fortran 77 (1992), 18.1 Fredholm Equations of the
    Second Kind, p. 782.)

    :param h:     dimensionless source depth
    :returns: phi, psi, t, w
              phi and psi are expressions from Appendix A of Fialko et al
              (2001), equation (A1). phi and psi are used in the definition
              of the functions PHI and PSI. See also A_B.m and Fialko et al
              (2001), eq. (26), p. 184.
              t and w are the abscissas and weights from the Gauss-Legendre
              quadrature rule (t is a value between 0 and 1; length(t) = M)

    ###########################################################################
    # Fialko, Y, Khazan, Y and M. Simons (2001). Deformation due to a
    #  pressurized horizontal circular crack in an elastic half-space, with
    #  applications to volcano geodesy. Geophys. J. Int., 146, 181-190
    # Press W. et al. (1992). Numerical Recipes in Fortran 77. 2nd Ed,
    #  Cambridge University Press. Available on-line at www.nrbook.com/fortran/
    ###########################################################################
    """
    t, w = gauleg(0, 1, 41)

    # Solution at the quadrature points r(j) **********************************
    g = dot(-2, t) / pi
    d = concatenate((g, zeros(g.shape))).T
    T1, T2, T3, T4 = T(h, t, t)

    T1tilde = zeros(T1.shape)
    T2tilde = zeros(T1.shape)
    T3tilde = zeros(T1.shape)
    T4tilde = zeros(T1.shape)
    N = t.size
    for j in range(N):
        T1tilde[:, j] = dot(w[j], T1[:, j])
        T2tilde[:, j] = dot(w[j], T2[:, j])
        T3tilde[:, j] = dot(w[j], T3[:, j])
        T4tilde[:, j] = dot(w[j], T4[:, j])

    Ktilde = concatenate((concatenate((T1tilde, T3tilde)),
                          concatenate((T4tilde, T2tilde))),
                         axis=1)

    y = solve((eye(dot(2, N), dot(2, N)) - dot((2 / pi), Ktilde)), d)

    phi = y[: N]
    psi = y[N: 2*N]
    # phi=y[arange(1,N)]
    # psi=y[arange(N + 1,dot(2,N))]

    return phi, psi, t, w
