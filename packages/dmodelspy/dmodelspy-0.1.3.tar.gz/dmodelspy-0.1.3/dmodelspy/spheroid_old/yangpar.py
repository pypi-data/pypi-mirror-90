from numpy import dot, log, sqrt, pi


def yangpar(a, b, lambda_, mu, nu, P):
    """
    Compute the parameters for the spheroid model

    Formulas from [1] Yang et al (JGR,1988)
    Corrections from [2] Newmann et al (JVGR, 2006), Appendix
    :param a: semimajor axis [m]
    :param b: semiminor axis [m]
    :param lambda: Lame's constant [Pa]
    :param mu: shear modulus [Pa]
    :param nu: Poisson's ratio
    :param P: excess pressure (stress intensity on the surface)
              [pressure units]
    :returns: a1, b1    pressure (stress) [units of P] from [1]
              c         prolate ellipsoid focus [m]
              Pdila     pressure (proportional to double couple forces)
                        [units of P] from [1]
              Pstar     pressure [units of P]

    Notes:
    [-]   : dimensionless
    """
    # epsn = 1e-10
    c = sqrt(a**2 - b**2)

    a2 = a**2
    a3 = a**3
    b2 = b**2
    c2 = c**2
    c3 = c**3
    c4 = c**4
    c5 = c**5
    ac = (a - c) / (a + c)

    coef1 = dot(dot(dot(2, pi), a), b2)
    den1 = dot(dot(8, pi), (1 - nu))

    Q = 3 / den1
    R = (1 - dot(2, nu)) / den1

    Ia = dot(-coef1, (2 / (dot(a, c2)) + log(ac) / c3))
    Iaa = dot(-coef1, (2 / (3*a3*c2) + 2 / (a*c4) + log(ac) / c5))

    a11 = dot(dot(2, R), (Ia - dot(4, pi)))
    a12 = dot(dot(-2, R), (Ia + dot(4, pi)))
    a21 = dot(dot(Q, a2), Iaa) + dot(R, Ia) - 1
    a22 = dot(dot(-Q, a2), Iaa) - dot(Ia, (dot(2, R) - Q))

    den2 = dot(3, lambda_) + dot(2, mu)
    num2 = dot(3, a22) - a12
    den3 = dot(a11, a22) - dot(a12, a21)
    num3 = a11 - dot(3, a21)

    Pdila = dot(dot(P, (dot(2, mu) / den2)), (num2 - num3)) / den3
    Pstar = dot(dot(P, (1 / den2)),
                (dot(num2, lambda_) + dot(2*(lambda_ + mu), num3))) / den3

    a1 = dot(dot(-2, b2), Pdila)
    b1 = dot(dot(3, (b2 / c2)), Pdila) + dot(dot(2, (1 - dot(2, nu))), Pstar)

    return a1, b1, c, Pdila, Pstar
