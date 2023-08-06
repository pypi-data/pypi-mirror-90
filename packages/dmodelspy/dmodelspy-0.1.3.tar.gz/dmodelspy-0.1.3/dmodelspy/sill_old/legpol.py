from numpy import ones, zeros, arange, multiply, dot


def legpol(x, N):
    """
    Legendre polynomial, Bonnetis recursion formula

    Reference: http://en.wikipedia.org/wiki/Legendre_polynomials
    :param x:
    :kind x: np.array of size=(1,M)
    :param N:
    :returns: pN, dpN

    Note
    index n in wiki goes from 0 to N, in MATLAB j goes from 1 to N+1. To
    obtain the right coefficients we introduced j = n+1 -> n = j-1
    Reversed for python implementation
    """
    P = ones((N+1, x.size))
    dP = zeros((N, x.size))
    P[1, :] = x
    for j in arange(1, N):
        P[j+1, :] = (multiply(dot((2*j+1), x), P[j, :]) - j*P[j-1, :]) / (j+1)
        dP[j, :] = dot(j, (multiply(x, P[j, :]) - P[j-1, :])) / (x ** 2 - 1)

    pN = P[N-1, :]
    dpN = dP[N-1, :]

    return pN, dpN
