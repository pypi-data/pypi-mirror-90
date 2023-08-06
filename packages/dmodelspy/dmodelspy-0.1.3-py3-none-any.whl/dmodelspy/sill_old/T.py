from numpy import zeros, dot, multiply

from .P import P


def T(h, t, r):
    """
    :param h:     dimensionless source depth
    :param r:     dummy variable (used to integrate along the sill
        dimenionless radius)
    :param t:     dummy variable

    :returns: T1-T4,  expressions from Appendix A of Fialko et al (2001),
        equations (A2) - (A5). T1-T4 are used in the definition of the
        functions phi and psi (see phi_psi.m)

    # *************************************************************************
    # Fialko, Y, Khazan, Y and M. Simons (2001). Deformation due to a
    # pressurized horizontal circular crack in an elastic half-space, with
    # applications to volcano geodesy. Geophys. J. Int., 146, 181-190
    # *************************************************************************
    """
    M = t.size
    N = r.size
    T1 = zeros((M, N))
    T2 = T1.copy()
    T3 = T1.copy()

    for i in range(M):
        Pm = P(h, t[i] - r)
        Pp = P(h, t[i] + r)
        T1[i, :] = dot(dot(4, h**3), (Pm[0, :] - Pp[0, :]))
        T2[i, :] = multiply((h / (multiply(t[i], r))), (Pm[1, :] - Pp[1, :]))\
            + dot(h, (Pm[2, :] + Pp[2, :]))
        T3[i, :] = multiply((h**2. / r),
                            (Pm[3, :] - Pp[3, :]
                             - multiply(dot(2, r),
                                        (multiply((t[i] - r), Pm[0, :])
                                         + multiply((t[i] + r), Pp[0, :])))))

    T4 = T3.T
    return T1, T2, T3, T4
