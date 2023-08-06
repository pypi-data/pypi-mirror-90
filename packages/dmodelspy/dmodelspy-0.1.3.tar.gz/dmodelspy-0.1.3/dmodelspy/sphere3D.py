from dataclasses import dataclass

from numpy import exp, sqrt, zeros, dot, multiply, shape, arange, array, pi
from scipy.integrate import quad as quadl
from scipy.special import jv as besselj


@dataclass
class Sphere3D:
    """
    3D Green's function for spherical source

    All parameters are in SI (MKS) units
    :param x0,y0: coordinates of the center of the sphere
    :param z0: depth of the center of the sphere (positive downward and
        defined as distance below the reference surface)
    :param P_G: dimensionless excess pressure (pressure/shear modulus)
    :param a: radius of the sphere
    :param nu: Poisson's ratio

    Reference ************************************************************
    McTigue, D.F. (1987). Elastic Stress and Deformation Near a Finite
    Spherical Magma Body: Resolution of the Point Source Paradox. J. Geophys.
    Res. 92, 12,931-12,940.
    """
    x0: float
    y0: float
    z0: float
    P_G: float
    a: float
    nu: float

    @property
    def dV(self) -> float:
        "Injection volume"
        # from between equations 1 and 2: dV = pi * p_0 * a**3 / G
        # and since P_G = p_0/G we have
        return pi * self.P_G * self.a**3.

    def calc_displ(self, x, y, z):
        """
        Calculate displacement

        :param x,y:       benchmark location
        :param z:         depth within the crust (z=0 is the free surface)
        :kind x, y, z: 1d arrays
        :returns:   u, v, w:  E, N and Up deformation components
        """
        x = array(x, ndmin=1)
        y = array(y, ndmin=1)
        z = array(z, ndmin=1)
        assert x.shape == y.shape
        # translate the coordinates of the points where the displacement is
        # computed in the coordinates system centered in (x0, y0)
        xxn = x - self.x0
        yyn = y - self.y0
        # radial distance from source center to points where we compute ur & uz
        r = sqrt(xxn**2 + yyn**2)
        # dimensionless parameters used in the formulas
        rho = r / self.z0
        e = self.a / self.z0
        zeta = z / self.z0

        # DIMENSIONLESS DISPLACEMENT *********************************
        # leading order solution for a pressurized sphere in an unbounded
        # region based on equation (11) of McTigue (1987)
        uz0 = (1 - zeta) * 0.25 * e**3 / (rho**2 + (1 - zeta)**2)**1.5
        # return equation (14) when zeta=0
        ur0 = dot(dot(e**3, 0.25), rho) / (rho**2 + (1 - zeta)**2)**1.5

        # first free surface correction, equations (A7), (A8), (A17) and (A18)
        # return equation (22) and (23) when csi = 0
        Auz1 = zeros((zeta.size, rho.size))
        Aur1 = zeros((zeta.size, rho.size))
        for i in arange(zeta.size):
            for j in arange(rho.size):
                args = (self.nu, float(rho[j]), float(zeta[i]))
                Auz1[i, j], _ = quadl(mctigueA7A17, 0, 50, args=args)
                Aur1[i, j], _ = quadl(mctigueA8A18, 0, 50, args=args)

        # higher order cavity correction, equations (38) and (39)
        R = sqrt(rho**2 + (1 - zeta)**2)
        sint = rho / R
        cost = (1 - zeta) / R
        
        ###########
        # The following do not depend on x, y, z and could be separated, but
        # but they're too quick to care about...
        C3 = [dot(e, (1 + self.nu)) / (dot(12, (1 - self.nu))),
              dot(dot(5, e**3), (2 - self.nu))
              / (dot(24, (7 - dot(5, self.nu))))]
        D3 = [dot(-e**3, (1 + self.nu)) / 12,
              dot(e**5, (2 - self.nu)) / (dot(4, (7 - self.nu)))]
        P0 = 1
        dP0 = 0
        ###########
        
        P2 = dot(0.5, (dot(3, cost**2) - 1))
        dP2 = dot(3, cost)
        ur38 = -0.5 * P0 * D3[0] / R**2\
            + multiply((C3[1] * (5 - 4*self.nu) - 1.5 * D3[1] / R**2), P2)\
            / R**2
        ut39 = dot(-(2 * C3[0] * (1 - self.nu) - 0.5 * D3[0] / R**2), dP0)\
            - multiply((C3[1] * (1 - (2*self.nu)) + (0.5*D3[1]) / R**2), dP2)\
            / R**2
        ut39 = multiply(ut39, sint)
        Auz3 = multiply(ur38, cost) - multiply(ut39, sint)
        Aur3 = multiply(ur38, sint) + multiply(ut39, cost)
        # Force Auz3 and Aur3 to be 2D
        Auz3 = Auz3.reshape(Auz3.shape[0], -1)
        Aur3 = Aur3.reshape(Aur3.shape[0], -1)

        # sixth order surface correction, return eq (50) and (51) when zeta=0
        Auz6 = zeros((zeta.size, rho.size))
        Aur6 = zeros((zeta.size, rho.size))
        for i in arange(zeta.size):
            for j in arange(rho.size):
                args = (self.nu, float(rho[j]), float(zeta[i]))
                Auz6[i, j], _ = quadl(mctigueA7A17a, 0, 50, args=args)
                Aur6[i, j], _ = quadl(mctigueA8A18a, 0, 50, args=args)

        # total surface displacement, return eq (52) and (53) when zeta = 0
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
        u = multiply(ur, xxn.reshape(xxn.shape[0], -1)) / r.reshape(r.shape[0],
                                                                    -1)
        v = multiply(ur, yyn.reshape(yyn.shape[0], -1)) / r.reshape(r.shape[0],
                                                                    -1)
        w = uz.copy()
        # print(f'{u.shape=}, {v.shape=}, {w.shape=}')

        # DIMENSIONAL DISPLACEMENT **********
        u = dot(dot(u, self.P_G), self.z0)
        v = dot(dot(v, self.P_G), self.z0)
        w = dot(dot(w, self.P_G), self.z0)

        u = u.reshape(x.shape)
        v = v.reshape(x.shape)
        w = w.reshape(x.shape)
        return u, v, w

    def calc_tilt(self, x, y, z):
        """
        Calculate tilt parameters

        :param x, y, z:      same as in calc()
        :returns:   dwdx, dwdy      ground tilts (East, North)
        """
        h = 0.001 * abs(max(x) - min(x))

        # East component
        _, _, wp = self.calc_displ(x + h, y, z)
        _, _, wm = self.calc_displ(x - h, y, z)
        dwdx = 0.5 * (wp - wm) / h
        # North component
        _, _, wp = self.calc_displ(x, y + h, z)
        _, _, wm = self.calc_displ(x, y - h, z)
        dwdy = 0.5 * (wp - wm) / h

        return dwdx, dwdy

    def calc_strain(self, x, y, z):
        """
        Calculate strain parameters

        :param x, y, z:      same as in calc()
        :returns: eea, gamma1, gamma2 (areal, shear1 & shear2)
        """
        h = 0.001 * abs(max(x) - min(x))

        up, _, _ = self.calc_displ(x + h, y, z)
        um, _, _ = self.calc_displ(x - h, y, z)
        dudx = 0.5 * (up - um) / h
        up, _, _ = self.calc_displ(x, y + h, z)
        um, _, _ = self.calc_displ(x, y - h, z)
        dudy = 0.5 * (up - um) / h
        _, vp, _ = self.calc_displ(x + h, y, z)
        _, vm, _ = self.calc_displ(x - h, y, z)
        dvdx = 0.5 * (vp - vm) / h
        _, vp, _ = self.calc_displ(x, y + h, z)
        _, vm, _ = self.calc_displ(x, y - h, z)
        dvdy = 0.5 * (vp - vm) / h

        eea = dudx + dvdy
        gamma1 = dudx - dvdy
        gamma2 = dudy + dvdx

        return eea, gamma1, gamma2

    def calc_all(self, x, y, z):
        """
        Calculate all 3D Green's function parameters

        :param x, y, z:      same as in calc()
        :returns:   u         horizontal (East component) deformation
                    v         horizontal (North component) deformation
                    w         vertical (Up component) deformation
                    dwdx      ground tilt (East component)
                    dwdy      ground tilt (North component)
                    eea       areal strain
                    gamma1    shear strain
                    gamma2    shear strain
        """
        u, v, w = self.calc_displ(x, y, z)
        dwdx, dwdy = self.calc_tilt(x, y, z)
        eea, gamma1, gamma2 = self.calc_strain(x, y, z)

        return u, v, w, dwdx, dwdy, eea, gamma1, gamma2


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
