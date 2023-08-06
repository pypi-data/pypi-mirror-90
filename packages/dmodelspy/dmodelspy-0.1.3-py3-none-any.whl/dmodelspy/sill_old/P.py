from numpy import dot, log, zeros


def P(h, x):
    """
    :param h:     dimensionless source depth
    :param x:     dummy variable

    P1-P4 are expressions from Appendix A of Fialko et al (2001). Used in the
    definition of the functions T1 - T4 (see T.m)

    ###########################################################################
    # Fialko, Y, Khazan, Y and M. Simons (2001). Deformation due to a
    # pressurized horizontal circular crack in an elastic half-space, with
    # applications to volcano geodesy. Geophys. J. Int., 146, 181-190
    ###########################################################################
    """
    outP = zeros((4, x.size))
    # P1(x), pg 189
    outP[0, :] = (dot(12, h**2) - x**2) / (dot(4, h**2) + x**2)**3
    # P2(x), pg 189
    outP[1, :] = log(4*h**2 + x**2)\
        + (8*h**4 + dot(2*x**2, h**2) - x**4) / (dot(4, h**2) + x**2)**2
    # P3(x), pg 189
    outP[2, :] = dot(2, (8*h**4 - dot(2*x**2, h**2) + x**4))\
        / (4*h**2 + x**2)**3
    # P4(x), pg 189
    outP[3, :] = (dot(4, h**2) - x**2) / (dot(4, h**2) + x**2)**2

    return outP
