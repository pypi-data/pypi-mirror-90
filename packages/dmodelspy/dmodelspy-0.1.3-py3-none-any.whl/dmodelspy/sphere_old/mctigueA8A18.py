from numpy import multiply, dot, exp
from scipy.special import jv as besselj


def mctigueA8A18(tt, nu, rho, zzn):
    """
    First free surface correction

    Displacement functions (A8) and (A18) of McTigue (1987)
    """
    sigma = multiply(dot(0.5, tt), exp(-tt))
    tau1 = sigma.copy()
    A8 = multiply(multiply(multiply(dot(0.5, sigma),
                                    ((1 - dot(2, nu)) - multiply(tt, zzn))),
                           exp(multiply(-tt, zzn))),
                  besselj(1, multiply(tt, rho)))
    A18 = multiply(multiply(multiply(dot(0.5, tau1),
                                     (dot(2, (1 - nu)) - multiply(tt, zzn))),
                            exp(multiply(-tt, zzn))),
                   besselj(1, multiply(tt, rho)))
    return A8 + A18
