from numpy import zeros, dot, arange, cos, pi, abs, finfo, multiply

from .legpol import legpol


def gauleg(x1, x2, N):
    """
    Return abcissas and weights of the Gaussian- Legendre quadrature

    Loosely based on SUBROUTINE gauleg (Numerical Recipes in Fortran 77, 4.5)
    :param x1: lower integration limit
    :param x2: upper integration limit
    :param N: length of arrays to return
    :returns: x, w: abcissas and weights arrays
    :rtype: (1,N) numpy.array

    Note:
    tested against the "High-precision Abscissas and Weights for Gaussian
    Quadrature of high order." table from http://www.holoborodko.com/pavel/
    click on Numerical Methods then Numerical Integration. The Table is at
    the end of the page
    >> gauleg(-1, 1, 11)
    ****** for N = 11
     Abscissas x                      Weights w
     0                               0.2729250867779006307144835
    +-0.2695431559523449723315320 	0.2628045445102466621806889
    +-0.5190961292068118159257257 	0.2331937645919904799185237
    +-0.7301520055740493240934163 	0.1862902109277342514260976
    +-0.8870625997680952990751578 	0.1255803694649046246346943
    +-0.9782286581460569928039380 	0.0556685671161736664827537
    *************************************************************************
    """
    z = zeros((N))
    xm = dot(0.5, (x2 + x1))
    xl = dot(0.5, (x2 - x1))

    for n in arange(N):
        z[n] = cos(dot(pi, (n+1 - 0.25)) / (N+0.5))
        z1 = dot(100, z[n])
        while abs(z1 - z[n]) > finfo(float).eps:
            pN, dpN = legpol(z[n], N+1)
            z1 = z[n]
            z[n] = z1 - pN / dpN

    _, dpN = legpol(z, N+1)
    x = xm - dot(xl, z)
    w = dot(2, xl) / (multiply((1 - z**2), dpN**2))

    return x, w
