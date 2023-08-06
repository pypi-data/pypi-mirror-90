from numpy import sqrt, zeros, dot, multiply, shape, arange, array
from scipy.integrate import quad as quadl

from .mctigueA7A17 import mctigueA7A17
from .mctigueA7A17a import mctigueA7A17a
from .mctigueA8A18 import mctigueA8A18
from .mctigueA8A18a import mctigueA8A18a


def mctigue3Ddispl(x0, y0, z0, P_G, a, nu, x, y, z):
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
    :type x,y: list or 1-D nd_array
    :param z: depth within the crust (z=0 is the free surface)
    :returns: u, v, w: horizontal (East component), horizontal (North
        component), vertical (Up component) deformation
    :rtype: numpy array for each component


    Reference ***************************************************************
    McTigue, D.F. (1987). Elastic Stress and Deformation Near a Finite
    Spherical Magma Body: Resolution of the Point Source Paradox. J. Geophys.
    Res. 92, 12,931-12,940.
    """
    x = array(x, ndmin=1)
    y = array(y, ndmin=1)
    z = array(z, ndmin=1)
    assert x.shape == y.shape
    # translate the coordinates of the points where the displacement is
    # computed in the coordinates system centered in (x0, y0)
    xxn = x - x0
    yyn = y - y0
    # radial distance from source center to points where we compute ur and uz
    r = sqrt(xxn**2 + yyn**2)
    # dimensionless parameters used in the formulas
    rho = r / z0
    e = a / z0
    zeta = z / z0

    # DIMENSIONLESS DISPLACEMENT *********************************************
    # leading order solution for a pressurized sphere in an unbounded region
    # based on equation (11) of McTigue (1987)
    uz0 = (1 - zeta) * 0.25 * e**3 / (rho**2 + (1 - zeta)**2)**1.5
    # uz0 = e^3*0.25./(rho.^2+(1-zeta).^2).^1.5
    # return equation (14) when zeta=0
    ur0 = dot(dot(e**3, 0.25), rho) / (rho**2 + (1 - zeta)**2)**1.5

    # first free surface correction, equations (A7), (A8), (A17) and (A18)
    # return equation (22) and (23) when csi = 0
    Auz1 = zeros((zeta.size, rho.size))
    Aur1 = zeros((zeta.size, rho.size))
    for i in arange(zeta.size):
        for j in arange(rho.size):
            # Auz1[i,j] = quadl(lambda xx=None: mctigueA7A17(xx, nu, rho[j],
            #     zeta[i]), 0, 50)
            # Aur1[i,j] = quadl(lambda xx=None: mctigueA8A18(xx, nu, rho[j],
            #     zeta[i]), 0, 50)
            args = (nu, float(rho[j]), float(zeta[i]))
            Auz1[i, j], _ = quadl(mctigueA7A17, 0, 50, args=args)
            Aur1[i, j], _ = quadl(mctigueA8A18, 0, 50, args=args)

    # higher order cavity correction, equations (38) and (39)
    R = sqrt(rho**2 + (1 - zeta)**2)
    sint = rho / R
    cost = (1 - zeta) / R
    C3 = [dot(e, (1 + nu)) / (dot(12, (1 - nu))),
          dot(dot(5, e**3), (2 - nu)) / (dot(24, (7 - dot(5, nu))))]
    D3 = [dot(-e**3, (1 + nu)) / 12,
          dot(e**5, (2 - nu)) / (dot(4, (7 - nu)))]
    P0 = 1
    P2 = dot(0.5, (dot(3, cost**2) - 1))
    dP0 = 0
    dP2 = dot(3, cost)
    ur38 = -0.5 * P0 * D3[0] / R**2\
        + multiply((C3[1] * (5 - 4*nu) - 1.5 * D3[1] / R**2), P2) / R**2
    ut39 = dot(-(2 * C3[0] * (1 - nu) - 0.5 * D3[0] / R**2), dP0)\
        - multiply((C3[1] * (1 - (2*nu)) + (0.5*D3[1]) / R**2), dP2) / R**2
    ut39 = multiply(ut39, sint)
    Auz3 = multiply(ur38, cost) - multiply(ut39, sint)
    Aur3 = multiply(ur38, sint) + multiply(ut39, cost)
    # Force Auz3 and Aur3 to be 2D
    Auz3 = Auz3.reshape(Auz3.shape[0], -1)
    Aur3 = Aur3.reshape(Aur3.shape[0], -1)

    # sixth order surface correction, return equation (50) and (51) when zeta=0
    Auz6 = zeros((zeta.size, rho.size))
    Aur6 = zeros((zeta.size, rho.size))
    for i in arange(zeta.size):
        for j in arange(rho.size):
            # Auz6[i,j]=quadl(lambda xx=None: mctigueA7A17a(xx,nu,rho(j),
            #     zeta(i)),0,50)
            # Aur6[i,j]=quadl(lambda xx=None: mctigueA8A18a(xx,nu,rho(j),
            #     zeta(i)),0,50)
            args = (nu, float(rho[j]), float(zeta[i]))
            Auz6[i, j], _ = quadl(mctigueA7A17a, 0, 50, args=args)
            Aur6[i, j], _ = quadl(mctigueA8A18a, 0, 50, args=args)

    # total surface displacement, return equation (52) and (53) when zeta = 0
    if shape(uz0)[0] == shape(Auz1)[1]:
        Auz1 = Auz1.T
        Aur1 = Aur1.T

    if shape(uz0)[0] == shape(Auz6)[1]:
        Auz6 = Auz6.T
        Aur6 = Aur6.T

    uz = uz0.reshape(uz0.shape[0], -1) + e**3 * (Auz1 + Auz3) + e**6 * Auz6
    # uz = e^3*Auz6;
    ur = ur0.reshape(ur0.shape[0], -1) + e**3 * (Aur1 + Aur3) + e**6 * Aur6

    # displacement components
    u = multiply(ur, xxn.reshape(xxn.shape[0], -1)) / r.reshape(r.shape[0], -1)
    v = multiply(ur, yyn.reshape(yyn.shape[0], -1)) / r.reshape(r.shape[0], -1)
    w = uz.copy()
    # print(f'{u.shape=}, {v.shape=}, {w.shape=}')

    # DIMENSIONAL DISPLACEMENT ************************************************
    u = dot(dot(u, P_G), z0)
    v = dot(dot(v, P_G), z0)
    w = dot(dot(w, P_G), z0)

    return u, v, w
