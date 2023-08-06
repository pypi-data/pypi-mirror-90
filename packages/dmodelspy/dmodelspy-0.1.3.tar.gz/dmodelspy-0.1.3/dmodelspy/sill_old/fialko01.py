# Generated with SMOP  0.41-beta
# from smop.libsmop import *
# fialko01.m
from numpy import dot, max, min, abs
from .fialkodisp import fialkodisp


def fialko01(x0, y0, z0, P_G, a, nu, x, y, z):
    """
    3D Green's function for sill-like source (Fialko et al., 2001)

    All parameters are in SI (MKS) units
    :param x0,y0:     coordinates of the center of the sphere
    :param z0:        depth of the center of the sill (positive downward and
                      defined as distance below the reference surface)
    :param P_G:       dimensionless excess pressure (pressure/shear modulus)
    :param a:         radius of the sphere
    :param nu:        Poisson's ratio
    :param x,y:       benchmark location
    :param z:         depth within the crust (z=0 is the free surface)
    :returns:   u         horizontal (East component) deformation
                v         horizontal (North component) deformation
                w         vertical (Up component) deformation
                dV        volume change
                dwdx      ground tilt (East component)
                dwdy      ground tilt (North component)
                eea       areal strain
                gamma1    shear strain
                gamma2    shear strain

    Reference ***************************************************************
    Fialko, Y, Khazan, Y and M. Simons (2001). Deformation due to a
    pressurized horizontal circular crack in an elastic half-space, with
    applications to volcano geodesy. Geophys. J. Int., 146, 181-190

    Note ********************************************************************
    compute the displacement due to a pressurized sill-like source
    using the finite penny-crack model by Fialko et al (GJI,2001)
    There are two typos in the published paper
    eq (12) and (13)
     (1) 2*Uz and 2*Ur must be replaced by Uz and Ur
     (2) dcsi/sinh(csi*h) must be replaced by dcsi
    eq (24)
         (1-exp(-2*a)) must be replaced by exp(-a)
    """
    # DISPLACEMENT ************************************************************
    # compute 3D displacements
    u, v, w, dV = fialkodisp(x0, y0, z0, P_G, a, nu, x, y, z)

    # TILT ********************************************************************
    h = dot(0.001, abs(max(x) - min(x)))

    # East comonent
    _, _, wp, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x + h, y, z)
    _, _, wm, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x - h, y, z)
    dwdx = dot(0.5, (wp - wm)) / h
    # North component
    _, _, wp, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x, y + h, z)
    _, _, wm, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x, y - h, z)
    dwdy = dot(0.5, (wp - wm)) / h

    # STRAIN ******************************************************************
# Displacement gradient tensor
    up, _, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x + h, y, z)
    um, _, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x - h, y, z)
    dudx = dot(0.5, (up - um)) / h
    up, _, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x, y + h, z)
    um, _, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x, y - h, z)
    dudy = dot(0.5, (up - um)) / h
    _, vp, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x + h, y, z)
    _, vm, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x - h, y, z)
    dvdx = dot(0.5, (vp - vm)) / h
    _, vp, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x, y + h, z)
    _, vm, _, _ = fialkodisp(x0, y0, z0, P_G, a, nu, x, y - h, z)
    dvdy = dot(0.5, (vp - vm)) / h
    # Strains
    eea = dudx + dvdy
    gamma1 = dudx - dvdy
    gamma2 = dudy + dvdx

    return u, v, w, dV, dwdx, dwdy, eea, gamma1, gamma2
