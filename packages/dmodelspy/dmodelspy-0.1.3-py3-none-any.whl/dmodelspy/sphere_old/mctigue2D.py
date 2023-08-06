from numpy import dot, multiply, sqrt, array


def mctigue2D(x0: float, y0: float, z0: float, P_G: float, a: float, nu: float,
              x, y):
    """
    Spherical source, forward model based on eq. (52) & (53) by McTigue (1988)

    All parameters are in SI (MKS) units
    :param x0,y0: coordinates of the center of the sphere
    :param z0: depth of the center of the sphere (positive downward and
        defined as distance below the reference surface)
    :param P_G: dimensionless excess pressure (pressure/shear modulus)
    :param a: radius of the sphere
    :param nu: Poisson's ratio
    :param x,y: benchmark location
    :kind x,y: numpy.1darray()s, same shape
    :returns: u: horizontal (East component) deformation
              v: horizontal (North component) deformation
              w: vertical (Up component) deformation
           dwdx: ground tilt (East component)
           dwdy: ground tilt (North component)

    Reference ***************************************************************
    McTigue, D.F. (1987). Elastic Stress and Deformation Near a Finite
    Spherical Magma Body: Resolution of the Point Source Paradox. J. Geophys.
    Res. 92, 12,931-12,940.
    """
    x = array(x, ndmin=1)
    y = array(y, ndmin=1)
    assert x.shape == y.shape
    # translate the coordinates of the points where the displacement is
    # computed in the coordinates system centered in (x0,y0)
    xxn = x - x0
    yyn = y - y0

    # radial distance from source center to points where we compute ur and uz
    r = sqrt(xxn**2. + yyn**2.)

    # dimensionless coordinates
    csi = xxn / z0
    psi = yyn / z0
    rho = r / z0
    e = a / z0

    # constant and expression used in the formulas
    f1 = 1. / (rho**2 + 1.)**1.5
    f2 = 1. / (rho**2 + 1.)**2.5
    c1 = e**3. / (7. - 5.*nu)

    # displacement (dimensionless) [McTigue (1988), eq. (52) and (53)]
    uzbar = e**3. * (1.-nu) *\
        multiply(f1, (1. - dot(c1, ((0.5*(1.+nu))
                                    - 3.75*(2.-nu) / (rho**2 + 1.)))))
    urbar = multiply(rho, uzbar)
    # displacement (dimensional)
    u = P_G * z0 * urbar * xxn / r
    v = P_G * z0 * urbar * yyn / r
    w = P_G * z0 * uzbar

    # GROUND TILT *************************************************************
    # see equation (5) in documentation
    dwmul = (3. - dot(c1, (1.5*(1.+nu)) - (18.75*(2.-nu)) / (rho**2. + 1.)))
    dwdx = -(1.-nu) * P_G * e**3. * csi * f2 * dwmul
    dwdy = -(1.-nu) * P_G * e**3. * psi * f2 * dwmul

    return u, v, w, dwdx, dwdy
