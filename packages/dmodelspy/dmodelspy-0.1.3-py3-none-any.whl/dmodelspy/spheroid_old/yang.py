from numpy import dot, pi

from .yangdisp import yangdisp


def yang(x0, y0, z0, a, A, P_G, mu, nu, theta, phi, x, y, z):
    """
    3D Green's function for a spheroidal source

    all parameters are in SI (MKS) units
    # SOURCE PARAMETERS
    :param a:         semimajor axis
    :param A:         geometric aspect ratio [dimensionless]
    :param P_G:       dimensionless excess pressure (pressure/shear modulus)
    :param x0,y0:     surface coordinates of the center of the prolate spheroid
    :param z0:        depth of the center of the sphere (positive downward and
                      defined as distance below the reference surface)
    :param theta:     plunge (dip) angle [deg] [90 = vertical spheroid]
    :param phi:       trend (strike) angle [deg] [0 = aligned to North]
    # CRUST PARAMETERS
    :param mu:        shear modulus
    :param nu:        Poisson's ratio
    # BENCHMARKS
    :param x,y:       benchmark location
    :param z:         depth within the crust (z=0 is the free surface)
    :returns:   u         horizontal (East component) deformation
                v         horizontal (North component) deformation
                w         vertical (Up component) deformation
                dwdx      ground tilt (East component)
                dwdy      ground tilt (North component)
                eea       areal strain
                gamma1    shear strain
                gamma2    shear strain

    Reference ***************************************************************

    Note ********************************************************************
    compute the displacement due to a pressurized ellipsoid
    using the finite prolate spheroid model by from Yang et al (JGR,1988)
    and corrections to the model by Newmann et al (JVGR, 2006).
    The equations by Yang et al (1988) and Newmann et al (2006) are valid for a
    vertical prolate spheroid only. There is and additional typo at pg 4251 in
    Yang et al (1988), not reported in Newmann et al. (2006), that gives an
    error when the spheroid is tilted (plunge different from 90 deg):
              C0 = y0*cos(theta) + z0*sin(theta)
    The correct equation is
              C0 = z0/sin(theta)
    This error has been corrected in this script.
    *************************************************************************
    """
    # SINGULARITIES ***********************************************************
    if theta >= 89.99:
        theta = 89.99

    if A >= 0.99:
        A = 0.99

    # DISPLACEMENT ************************************************************
    # define parameters used to compute the displacement
    b = A * a
    lam = 2 * mu * nu / (1 - 2*nu)
    P = P_G * mu
    theta = pi * theta / 180
    phi = pi * phi / 180

    # compute 3D displacements
    u, v, w = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y, z)

    # TILT ********************************************************************
    h = dot(0.001, abs(max(x) - min(x)))

    # East comonent
    _, _, wp = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x+h, y, z)
    _, _, wm = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x-h, y, z)
    dwdx = dot(0.5, (wp - wm)) / h
    # North component
    _, _, wp = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y+h, z)
    _, _, wm = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y-h, z)
    dwdy = dot(0.5, (wp - wm)) / h

    # STRAIN ******************************************************************
    # Displacement gradient tensor
    up, _, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x+h, y, z)
    um, _, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x-h, y, z)
    dudx = dot(0.5, (up - um)) / h
    up, _, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y+h, z)
    um, _, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y-h, z)
    dudy = dot(0.5, (up - um)) / h
    _, vp, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x+h, y, z)
    _, vm, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x-h, y, z)
    dvdx = dot(0.5, (vp - vm)) / h
    _, vp, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y+h, z)
    _, vm, _ = yangdisp(x0, y0, z0, a, b, lam, mu, nu, P, theta, phi, x, y-h, z)
    dvdy = dot(0.5, (vp - vm)) / h
    # Strains
    eea = dudx + dvdy
    gamma1 = dudx - dvdy
    gamma2 = dudy + dvdx

    return u, v, w, dwdx, dwdy, eea, gamma1, gamma2
