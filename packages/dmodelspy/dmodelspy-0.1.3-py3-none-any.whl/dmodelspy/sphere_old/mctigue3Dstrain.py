from numpy import min, max

from .mctigue3Ddispl import mctigue3Ddispl


def mctigue3Dstrain(x0, y0, z0, P_G, a, nu, x, y, z):
    """
    3D Green's function for spherical source

    All parameters are in SI (MKS) units
    :param x0,y0: coordinates of the center of the sphere
    :param z0: depth of the center of the sphere (positive downward and
        defined as distance below the reference surface)
    :param P_G: dimensionless excess pressure (pressure/shear modulus)
    :param a: radius of the sphere
    :param nu: Poisson's ratio
    :param x,y: benchmark location
    :param z: depth within the crust (z=0 is the free surface)
    :returns: eea: areal strain
              gamma1: shear strain
              gamma2: shear strain
    :rtype: numpy arrays

    Reference ***************************************************************
    Battaglia M. et al. Implementing the spherical source
    equation (5) and (6)
    STRAIN ******************************************************************
    """
    h = 0.001 * abs(max(x) - min(x))

    # derivatives
    up, _, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x + h, y, z)
    um, _, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x - h, y, z)
    dudx = 0.5 * (up - um) / h
    up, _, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x, y + h, z)
    um, _, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x, y - h, z)
    dudy = 0.5 * (up - um) / h
    _, vp, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x + h, y, z)
    _, vm, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x - h, y, z)
    dvdx = 0.5 * (vp - vm) / h
    _, vp, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x, y + h, z)
    _, vm, _ = mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x, y - h, z)
    dvdy = 0.5 * (vp - vm) / h

    # Strains
    eea = dudx + dvdy
    gamma1 = dudx - dvdy
    gamma2 = dudy + dvdx

    return eea, gamma1, gamma2
