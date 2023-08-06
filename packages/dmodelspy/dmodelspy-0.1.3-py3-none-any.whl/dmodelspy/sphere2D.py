from dataclasses import dataclass

from numpy import dot, multiply, sqrt, array


@dataclass
class Sphere2D:

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
    x0: float
    y0: float
    z0: float
    P_G: float
    a: float
    nu: float

    def _calc_base(self):
        """
        Parameters that don't depend on the station positions
        """
        # dimensionless coordinates
        e = self.a / self.z0
        # constant and expression used in the formulas
        c1 = e**3. / (7. - 5.*self.nu)
        return e, c1

    def _prep_arrays(self, x, y):
        """
        Prepare arrays
        """
        x = array(x, ndmin=1)
        y = array(y, ndmin=1)
        assert x.shape == y.shape

        # translate the coordinates of the points where the displacement is
        # computed in the coordinates system centered in (x0,y0)
        xxn = x - self.x0
        yyn = y - self.y0
        # radial distance from source center to ur and uz points
        r = sqrt(xxn**2. + yyn**2.)

        # dimensionless coordinates
        csi = xxn / self.z0
        psi = yyn / self.z0
        rho = r / self.z0
        f1 = 1. / (rho**2 + 1.)**1.5
        f2 = 1. / (rho**2 + 1.)**2.5

        return x, y, xxn, yyn, r, csi, psi, rho, f1, f2

    def calc_displ(self, x, y):
        x, y, xxn, yyn, r, csi, psi, rho, f1, _ = self._prep_arrays(x, y)
        e, c1 = self._calc_base()

        # displacement (dimensionless) [McTigue (1988), eq. (52) and (53)]
        uzbar = e**3. * (1.-self.nu) *\
            multiply(f1, (1. - dot(c1, ((0.5*(1.+self.nu))
                                        - 3.75*(2.-self.nu) / (rho**2 + 1.)))))
        urbar = multiply(rho, uzbar)
        # displacement (dimensional)
        u = self.P_G * self.z0 * urbar * xxn / r
        v = self.P_G * self.z0 * urbar * yyn / r
        w = self.P_G * self.z0 * uzbar

        return u, v, w

    def calc_tilt(self, x, y):
        x, y, xxn, yyn, r, csi, psi, rho, _, f2 = self._prep_arrays(x, y)
        e, c1 = self._calc_base()
        # see equation (5) in documentation
        dwmul = (3. - dot(c1, (1.5*(1.+self.nu)) - (18.75*(2.-self.nu))
                 / (rho**2. + 1.)))
        dwdx = -(1.-self.nu) * self.P_G * e**3. * csi * f2 * dwmul
        dwdy = -(1.-self.nu) * self.P_G * e**3. * psi * f2 * dwmul

        return dwdx, dwdy

    def calc_strain(self, x, y):
        """
        Calculate strain parameters

        :param x, y, z:      same as in calc()
        :returns: eea, gamma1, gamma2 (areal, shear1 & shear2)
        """
        h = 0.001 * abs(max(x) - min(x))

        up, _, _ = self.calc_displ(x + h, y)
        um, _, _ = self.calc_displ(x - h, y)
        dudx = 0.5 * (up - um) / h
        up, _, _ = self.calc_displ(x, y + h)
        um, _, _ = self.calc_displ(x, y - h)
        dudy = 0.5 * (up - um) / h
        _, vp, _ = self.calc_displ(x + h, y)
        _, vm, _ = self.calc_displ(x - h, y)
        dvdx = 0.5 * (vp - vm) / h
        _, vp, _ = self.calc_displ(x, y + h)
        _, vm, _ = self.calc_displ(x, y - h)
        dvdy = 0.5 * (vp - vm) / h

        eea = dudx + dvdy
        gamma1 = dudx - dvdy
        gamma2 = dudy + dvdx

        return eea, gamma1, gamma2

    def calc_all(self, x, y):
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
        u, v, w = self.calc_displ(x, y)
        dwdx, dwdy = self.calc_tilt(x, y)
        eea, gamma1, gamma2 = self.calc_strain(x, y)

        return u, v, w, dwdx, dwdy, eea, gamma1, gamma2
