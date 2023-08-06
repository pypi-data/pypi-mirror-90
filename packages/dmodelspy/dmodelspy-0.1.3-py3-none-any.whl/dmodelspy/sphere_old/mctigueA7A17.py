from numpy import dot, exp, multiply, sqrt
from scipy.special import jv as besselj


def mctigueA7A17(tt, nu, rho, zeta):
    """
    First free surface correction

    Displacement functions (A7) and (A17) of McTigue (1987)
    """
    R = sqrt(rho**2 + zeta**2)
    sigma = multiply(dot(0.5, tt), exp(-tt))
    tau1 = sigma.copy()
    A7 = multiply(multiply(multiply(dot(0.5, sigma),
                                    (dot(2, (1 - nu)) - multiply(tt, zeta))),
                           exp(multiply(tt, zeta))),
                  besselj(0, multiply(tt, R)))
    A17 = multiply(multiply(multiply(dot(0.5, tau1),
                                     ((1 - dot(2, nu)) - multiply(tt, zeta))),
                            exp(multiply(tt, zeta))),
                   besselj(0, multiply(tt, R)))
    return A7 + A17
