from dataclasses import dataclass

from numpy import dot, multiply, sqrt, array, pi


@dataclass
class Mogi:

    """
    Mogi source

    All parameters are in SI (MKS) units
    :param x0,y0: coordinates of the center of the sphere
    :param z0: depth of the center of the sphere (positive downward and
        defined as distance below the reference surface)
    :param dV: injection (or removal) volume
    
    Poisson's ratio is assumed to be 0.25 (mu = lambda)

    :reference: Mogi1958
    """
    x0: float
    y0: float
    z0: float
    dV: float

    def calc_displ(self, x, y):
        """
        Calculate displacement for a Mogi source
        :param x,y: benchmark location
        :kind x,y: numpy.1darray()s, same shape
        :returns: u: horizontal (East component) deformation
                  v: horizontal (North component) deformation
                  w: vertical (Up component) deformation
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

        # displacement (dimensional)
        u = 0.75 * (self.dV/pi) * r / (self.z0**2 + r**2)**1.5
        v = u.copy()
        w = 0.75 * (self.dV/pi) * self.z0 / (self.z0**2 + r**2)**1.5

        return u, v, w

    def calc_tilt(self, x, y):
        """
        Calculate tilt parameters

        :param x, y:      as in calc_displ()
        :returns:   dwdx, dwdy      ground tilts (East, North)
        """
        h = 0.001 * abs(max(x) - min(x))

        # East component
        _, _, wp = self.calc_displ(x + h, y)
        _, _, wm = self.calc_displ(x - h, y)
        dwdx = 0.5 * (wp - wm) / h
        # North component
        _, _, wp = self.calc_displ(x, y + h)
        _, _, wm = self.calc_displ(x, y - h)
        dwdy = 0.5 * (wp - wm) / h

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
