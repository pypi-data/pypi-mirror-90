# Generated with SMOP  0.41-beta
# from smop.libsmop import *
# fialkodisp.m
from numpy import (sqrt, sin, cos, sinh, cosh, exp, zeros, dot, arange,
                   array, pi, concatenate)
from scipy.special import jv as besselj

from .gauleg import gauleg
from .psi_phi import psi_phi


def fialkodisp(x0, y0, z0, P_G, a, nu, x, y, z):
    """
    3D Green's function for sill-like source (Fialko et al., 2001)

    All parameters are in SI (MKS) units

    :param x0,y0:     coordinates of the center of the sphere
    :kind x0, y0: float
    :param z0:        depth of the center of the sill (positive downward and
                      defined as distance below the reference surface)
    :kind z0: float
    :param P_G:       dimensionless excess pressure (pressure/shear modulus)
    :kind P_G: float
    :param a:         radius of the sphere
    :kind a: float
    :param nu:        Poisson's ratio
    :kind nu: float
    :param x,y:       benchmark location
    :param z:         depth within the crust (z=0 is the free surface)
    :kind x, y, z: 1d arrays
    :returns:   u, v, w:  E, N and Up deformation components
                dV: volume change
    *************************************************************************
    Fialko, Y, Khazan, Y and M. Simons (2001). Deformation due to a
    pressurized horizontal circular crack in an elastic half-space, with
    applications to volcano geodesy. Geophys. J. Int., 146, 181-190
    *************************************************************************
    """
    x = array(x, ndmin=1)
    y = array(y, ndmin=1)
    z = array(z, ndmin=1)
    # General parameters *****************************************************
    eps = 1e-08
    rd = a                                 # avoid conflict with other a below
    h = z0 / rd                            # dimensionless source depth

    # Coordinates transformation *********************************************
    # translate and scale locations
    x = (x - x0) / rd
    y = (y - y0) / rd
    z = (z - z0) / rd
    # compute radial distance
    r = sqrt(x**2 + y**2)

    # solve for PHI and PSI, Fialko et al. (2001), eq. (26) *******************
    # ascissas and weights for Gauss-Legendre quadrature
    csi1, w1 = gauleg(eps, 10, 41)
    # print(f'{csi1.size=}, {w1.size=}')
    csi2, w2 = gauleg(10, 60, 41)
    # print(f'{csi2.shape=}, {w2.shape=}')
    csi = concatenate((csi1, csi2))
    wcsi = concatenate((w1, w2))
    csi_col = csi.reshape((-1, 1))
    wcsi_row = wcsi.reshape((1, -1))
    # print(f'{csi_col.shape=}, {wcsi_row.shape=}')

    phi, psi, t, wt = psi_phi(h)
    wt_col = wt.reshape((-1, 1))
    t_col = t.reshape((-1, 1))
    phi_col = phi.reshape((-1, 1))
    psi_col = psi.reshape((-1, 1))
    csi_t = csi_col @ t.reshape((1, -1))
    # Gauss-Legendre quadrature
    PHI = sin(csi_t) @ (wt_col * phi_col)
    PSI = (sin(csi_t) / (csi_t) - cos(csi_t)) @ (wt_col * psi_col)

    # compute A and B, Fialko et al. (2001), eq. (24) *************************
    # NOTE there is an error in eq (24), (1-exp(-2*a)) must be replaced by
    # exp(-a)
    a = h * csi_col
    A = exp(-a) * (a * PSI + (1 + a) * PHI)
    B = exp(-a) * ((1 - a) * PSI - a * PHI)
    # A = multiply(exp(- a),(multiply(a,PSI) + multiply((1 + a),PHI)))
    # B = multiply(exp(- a),(multiply((1 - a),PSI) - multiply(a,PHI)))
    # *************************************************************************

    # compute Uz and Ur, Fialko et al. (2001), eq. (12) and (13) **************
    # NOTE there are two errors in eq (12) and (13)
    # (1) 2*Uz and 2*Ur must be replaced by Uz and Ur
    # (2) dcsi/sinh(csi*h) must be replaced by dcsi
    Uz = zeros(r.shape)
    Ur = zeros(r.shape)
    csi_z_h = (z+h) * csi_col
    for i in arange(r.size):
        J0 = besselj(0, r[i] * csi_col)
        Uzi = J0 * (((1 - 2*nu) * B - csi_z_h * A) * sinh(csi_z_h)
                    + (2*(1-nu) * A - csi_z_h * B) * cosh(csi_z_h))
        Uz[i] = dot(wcsi_row, Uzi)
        J1 = besselj(1, r[i] * csi_col)
        Uri = J1 * (((1 - 2*nu) * A + csi_z_h * B) * sinh(csi_z_h)
                    + (2*(1-nu) * B + csi_z_h * A) * cosh(csi_z_h))
        Ur[i] = dot(wcsi_row, Uri)

    # Deformation components **************************************************
    u = rd * P_G * Ur * x / r
    v = rd * P_G * Ur * y / r
    w = -rd * P_G * Uz
    # *************************************************************************

    # Volume change ***********************************************************
    dV = -4 * pi * (1 - nu) * P_G * rd**3. * dot(t_col.T, wt_col * phi_col)
    # *************************************************************************

    return u, v, w, dV
