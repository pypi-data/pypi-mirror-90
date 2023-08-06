from numpy import dot, exp, multiply
from scipy.special import jv as besselj


def mctigueA8A18a(tt,  nu,  rho,  zeta):
    """
    Sixth order free surface correction

    displacement functions (A8) and (A18) of McTigue (1987)
    Hankel transforms from Tellez et al (1997).
    Tables of Fourier, Laplace and Hankel transforms of n-dimensional
    generalized function. Acta Applicandae Mathematicae, 48, 235-284
    """
    # equation (48)
    sigma = dot(tt ** 2.0, exp(-tt)) / (7 - dot(5, nu))
    # missing Hankel transform of second part of equation (49)
    tau = dot(tt ** 2.0, exp(-tt)) / (7 - dot(5, nu))
    A8 = multiply(multiply(multiply(dot(0.5, sigma),
                                    ((1 - dot(2, nu))
                                    - multiply(tt, zeta))),
                           exp(multiply(-tt, zeta))),
                  besselj(1, multiply(tt, rho)))
    A18 = multiply(multiply(multiply(dot(0.5, tau),
                                     (dot(2, (1 - nu))
                                     - multiply(tt, zeta))),
                            exp(multiply(- tt, zeta))),
                   besselj(1, multiply(tt, rho)))

    return A8 + A18
