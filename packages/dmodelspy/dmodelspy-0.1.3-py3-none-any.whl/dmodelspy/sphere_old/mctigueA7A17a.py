from numpy import multiply, dot, exp, sqrt
from scipy.special import jv as besselj


def mctigueA7A17a(tt, nu, rho, zeta):
    """
    Sixth order free surface correction

    displacement functions (A7) and (A17) of McTigue (1987)
    Hankel transforms from Tellez et al (1997). Tables of Fourier, Laplace
    and Hankel transforms of n-dimensional generalized function. Acta
    Applicandae Mathematicae, 48, 235-284
    """
    R = sqrt(rho**2 + zeta**2)
    # equation (48)
    sigma = multiply(dot(1.5, (tt + tt**2)),
                     exp(-tt)) / (7 - dot(5, nu))
    # missing Hankel transform of second part of equation (49)
    tau = dot(tt**2.0, exp(-tt)) / (7 - dot(5, nu))
    A7 = multiply(multiply(multiply(dot(0.5, sigma),
                                    (dot(2, (1 - nu)) - multiply(tt, zeta))),
                           exp(multiply(tt, zeta))),
                  besselj(0, multiply(tt, R)))
    A17 = multiply(multiply(multiply(dot(0.5, tau),
                                     ((1 - dot(2, nu)) - multiply(tt, zeta))),
                            exp(multiply(tt, zeta))),
                   besselj(0, multiply(tt, R)))
    return A7 + A17
