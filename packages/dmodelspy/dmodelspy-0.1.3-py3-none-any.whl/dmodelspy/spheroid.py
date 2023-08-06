from dataclasses import dataclass, field

from numpy import (arctan as atan, array, cos, dot, log, multiply, pi,
                   radians, sin, sqrt)


@dataclass
class Spheroid:
    """
    Compute displacement due to a pressurized ellipsoid

    :param x0,y0,z0:  coordinates of the center of the prolate spheroid
                      (positive downward) [m]
    :param a:         semimajor axis [m]
    :param asrat:     geometric aspect ratio [dimensionless]
    :param P_G:       dimensionless excess pressure (pressure/shear modulus)
    :param mu:        shear modulus [Pa]
    :param nu:        Poisson's ratio [dimensionless]
    :param theta:     plunge (dip) angle [deg] [90 = vertical spheroid]
    :param phi:       trend (strike) angle [deg] [0 = aligned to North]

    Uses the finite prolate spheroid model  from Yang et al (JGR,1988)
    with corrections by Newman et al (JVGR, 2006).
    """
    # The equations by Yang et al (1988) and Newman et al (2006) are valid for
    # a vertical prolate spheroid only. There is an additional typo at p4251
    # in Yang et al (1988), not reported in Newman et al. (2006), that gives
    # an error when the spheroid is tilted (plunge different from 90 deg):
    #           C0 = y0*cos(theta) + z0*sin(theta)
    # The correct equation is
    #           C0 = z0/sin(theta)
    # This error has been corrected in this script.
    x0: float
    y0: float
    z0: float
    a: float
    asrat: float
    P_G: float
    mu: float
    nu: float
    theta: float
    phi: float
    # attributes affecting cached attributes
    _z0: float = field(init=False, repr=False)
    _a: float = field(init=False, repr=False)
    _asrat: float = field(init=False, repr=False)
    _P_G: float = field(init=False, repr=False)
    _mu: float = field(init=False, repr=False)
    _nu: float = field(init=False, repr=False)
    _theta: float = field(init=False, repr=False)
    _phi: float = field(init=False, repr=False)
    # Cached variables
    _dV: float = field(init=False, repr=False, default=None)
    _a1: array = field(init=False, repr=False)
    _b1: array = field(init=False, repr=False)
    _c: array = field(init=False, repr=False)
    _Pdila: array = field(init=False, repr=False)
    _Pstar: array = field(init=False, repr=False)

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, a: float):
        self._a = a
        self._dV = None

    @property
    def asrat(self) -> float:
        return self._asrat

    @asrat.setter
    def asrat(self, asrat: float):
        asrat == min(asrat, 0.99)   # avoid singularity
        self._asrat = asrat
        self._dV = None

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, mu: float):
        self._mu = mu
        self._dV = None

    @property
    def nu(self) -> float:
        return self._nu

    @nu.setter
    def nu(self, nu: float):
        self._nu = nu
        self._dV = None

    @property
    def P_G(self) -> float:
        return self._P_G

    @P_G.setter
    def P_G(self, P_G: float):
        self._P_G = P_G
        self._dV = None

    @property
    def theta(self) -> float:
        return self._theta

    @theta.setter
    def theta(self, theta: float):
        assert theta > 0
        theta = min(theta, 89.99)
        self._theta = theta
        self._dV = None

    @property
    def phi(self) -> float:
        return self._phi

    @phi.setter
    def phi(self, phi: float):
        self._phi = phi
        self._dV = None

    @property
    def z0(self) -> float:
        return self._z0

    @z0.setter
    def z0(self, z0: float):
        self._z0 = z0
        self._dV = None

    @property
    def dV(self) -> float:
        "Volume changeq"
        if self._dV is None:
            self._calc_base()
        return self._dV

    @property
    def P(self) -> float:
        "Pressure [Pa]"
        return self.P_G * self.mu

    @property
    def lam(self) -> float:
        "Lame parameter lambda [Pa]"
        return 2 * self.mu * self.nu / (1 - 2 * self.nu)

    @property
    def b(self) -> float:
        "semiminor axis [m]"
        return self._a * self._asrat

    def _calc_base(self):
        """
        Calculate base (cached) parameters

        dV is from Newman2006, eq2
        """
        self.yangpar()
        self._dV = self.P_G * pi * self.a * self.b**2

    def calc_displ(self, x, y, z):
        """
        Calculate displacement

        :param x,y:       benchmark location
        :param z:         depth within the crust (z=0 is the free surface)
        :kind x, y, z: 1d arrays
        :returns:   u, v, w:  E, N and Up deformation components
        """
        # testing parameters ######################################
        # clear all; close all; clc;
        # a = 1000; b = 0.99*a;
        # lambda = 1; mu = lambda; nu = 0.25; P = 0.01;
        # theta = pi*89.99/180; phi = 0;
        # x = linspace(0,2E4,7);
        # y = linspace(0,1E4,7);
        # x0 = 0; y0 = 0; z0 = 5E3;
        ############################################################

        # compute the parameters for the spheroid model
        if self._dV is None:
            self._calc_base()
        # translate the coordinates of the points where the displacement is
        # computed in the coordinate systen centered in (x0,0)
        # Coordinates transformation
        x = array(x, ndmin=1)
        y = array(y, ndmin=1)
        z = array(z, ndmin=1)

        xxn = x - self.x0
        yyn = y - self.y0
        phi_rad = radians(self.phi)
        # rotate the coordinate system to be coherent with the model coordinate
        # system of Figure 3 (Yang et al., 1988)
        xxp = dot(cos(phi_rad), xxn) - dot(sin(phi_rad), yyn)
        yyp = dot(sin(phi_rad), xxn) + dot(cos(phi_rad), yyn)
        # compute displacement for a prolate ellipsoid at csi = c
        U1p, U2p, U3p = self.yangint(xxp, yyp, z, self._c)
        # compute displacement for a prolate ellipsoid at csi = -c
        U1m, U2m, U3m = self.yangint(xxp, yyp, z, -self._c)
        Upx = -U1p - U1m
        Upy = -U2p - U2m
        Upz = U3p + U3m
        # rotate horizontal displacement back (strike)
        u = dot(cos(phi_rad), Upx) + dot(sin(phi_rad), Upy)
        v = dot(-sin(phi_rad), Upx) + dot(cos(phi_rad), Upy)
        w = Upz.copy()

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

    def yangint(self, x, y, z, csi):
        """
        Compute the primitive of the displacement for a prolate ellipsoid

        Equation (1)-(8) from Yang et al (JGR, 1988)
        Corrections to some parameters from Newmann et al (JVGR, 2006)
        :param x,y,z:    coordinates of the point(s) where the displacement
            is computed [m]
        :param csi:      focus of the prolate spheroid [m]
        :returns: U1,U2,U3 : displacement in local coordinates [m] - see
            Figure 3 of Yang et al (1988)

        Notes:
        The location of the center of the prolate spheroid is (x0,y0,z0)
            with x0=0 and y0=0;
        The free surface is z=0;
        """
        # precalculate parameters that are used often
        sint = sin(radians(self.theta))
        cost = cos(radians(self.theta))

        # new coordinates and parameters from Yang et al (JGR, 1988), p. 4251
        # dimensions [m]
        csi2 = dot(csi, cost)
        csi3 = dot(csi, sint)

        x1 = x.copy()
        x2 = y.copy()
        x3 = z - self.z0
        xbar3 = z + self.z0

        y1 = x1.copy()
        y2 = x2 - csi2
        y3 = x3 - csi3
        ybar3 = xbar3 + csi3
        r2 = dot(x2, sint) - dot(x3, cost)
        q2 = dot(x2, sint) + dot(xbar3, cost)
        r3 = dot(x2, cost) + dot(x3, sint)
        q3 = dot(-x2, cost) + dot(xbar3, sint)
        rbar3 = r3 - csi
        qbar3 = q3 + csi
        R1 = sqrt(y1**2 + y2**2 + y3**2)
        R2 = sqrt(y1**2 + y2**2 + ybar3**2)
        #####################################################################
        # C0 = y0*cost + z0*sint;
        C0 = self.z0 / sint

        #####################################################################
        beta = (dot(q2, cost)
                + dot((1 + sint), (R2 + qbar3))) / (dot(cost, y1) + 1e-15)

        # precalculate parameters that are used often
        drbar3 = R1 + rbar3
        dqbar3 = R2 + qbar3
        dybar3 = R2 + ybar3
        # print(f'{R1=}, {rbar3=}')
        lrbar3 = log(R1 + rbar3)
        lqbar3 = log(R2 + qbar3)
        lybar3 = log(R2 + ybar3)
        atanb = atan(beta)
        # primitive parameters from Yang et al (1988), p. 4252
        Astar1 = (self._a1 / (multiply(R1, drbar3))
                  + multiply(self._b1, (lrbar3 + (r3 + csi) / drbar3)))
        Astarbar1 = (-self._a1 / (multiply(R2, dqbar3))
                     - multiply(self._b1, (lqbar3 + (q3 - csi) / dqbar3)))
        A1 = csi / R1 + lrbar3
        Abar1 = csi / R2 - lqbar3
        A2 = R1 - multiply(r3, lrbar3)
        Abar2 = R2 - multiply(q3, lqbar3)
        A3 = multiply(csi, rbar3) / R1 + R1
        Abar3 = multiply(csi, qbar3) / R2 - R2
        Bstar = ((self._a1 / R1 + multiply(2*self._b1, A2))
                 + dot((3 - 4*self.nu),
                       (self._a1 / R2 + multiply(2*self._b1, Abar2))))
        B = dot(csi, (csi + C0)) / R2 - Abar2 - dot(C0, lqbar3)
        # the 4 equations below have been changed to improve the fit to
        # internal deformation
        Fstar1 = 0
        Fstar2 = 0
        F1 = 0
        F2 = 0
        f1 = (dot(csi, y1) / dybar3
              + dot((3 / cost**2), (multiply(multiply(y1, sint), lybar3)
                                    - multiply(y1, lqbar3)
                                    + multiply(dot(2, q2), atanb)))
              + multiply(2*y1, lqbar3)
              - multiply(4*xbar3, atanb) / cost)
        f2 = (dot(csi, y2) / dybar3
              + dot((3 / cost**2), (multiply(multiply(q2, sint), lqbar3)
                                    - multiply(q2, lybar3)
                                    + multiply(dot(dot(2, y1), sint), atanb)
                                    + dot(cost, (R2 - ybar3))))
              - dot(2*cost, Abar2)
              + dot((2 / cost), (multiply(xbar3, lybar3)
                                 - multiply(q3, lqbar3))))
        f3 = (dot((1 / cost), (multiply(q2, lqbar3)
                               - multiply(multiply(q2, sint), lybar3)
                               + multiply(dot(2, y1), atanb)))
              + dot(2*sint, Abar2) + multiply(q3, lybar3) - csi)
        # precalculate coefficients that are used often
        cstar = (dot(self.a, self.b**2) / csi**3) / (dot(16*self.mu,
                                                     (1 - self.nu)))
        cdila = dot(dot(2, cstar), self._Pdila)
        # displacement components (2) to (7): primitive of eq(1) Yang1988
        Ustar1 = dot(cstar, (multiply(Astar1, y1)
                             + multiply(dot((3 - 4*self.nu), Astarbar1), y1)
                             + multiply(Fstar1, y1)))

        # U2star and U3star changed to improve fit to internal deformation
        Ustar2 = dot(cstar,
                     (dot(sint, (multiply(Astar1, r2)
                                 + multiply(dot((3 - 4*self.nu), Astarbar1),
                                            q2)
                                 + multiply(Fstar1, q2)))
                      + dot(cost, (Bstar - Fstar2))))

        # The formula used in the script by Fialko and Andy is different from
        # equation (4) of Yang et al (1988)
        # I use the same to continue to compare the results 2009 07 23
        # Ustar3 = cstar*(-cost*(Astarbar1.*r2
        #                        + (3-4*nu)*Astarbar1.*q2 - Fstar1.*q2)
        #                 + sint*(Bstar+Fstar2) + 2*cost^2*z.*Astarbar1)
        #####################################################################
        # The equation below is correct - follows eq4 from Yang et al (1988)
        Ustar3 = dot(cstar,
                     (dot(-cost,
                          (multiply(Astar1, r2)
                           + multiply(dot((3 - 4*self.nu), Astarbar1), q2)
                           - multiply(Fstar1, q2)))
                      + dot(sint, (Bstar + Fstar2))))

        Udila1 = dot(cdila,
                     ((multiply(A1, y1)
                       + multiply(dot((3 - 4*self.nu), Abar1), y1)
                       + multiply(F1, y1))
                      - dot(dot(4*(1-self.nu), (1-2*self.nu)), f1)))
        Udila2 = dot(cdila,
                     (dot(sint, (multiply(A1, r2)
                                 + multiply(dot((3 - 4*self.nu), Abar1), q2)
                                 + multiply(F1, q2)))
                      - dot(4*(1 - self.nu)*(1 - 2*self.nu), f2)
                      + dot(dot(4*(1 - self.nu), cost), (A2 + Abar2))
                      + dot(cost, (A3 - dot((3 - 4*self.nu), Abar3) - F2))))
        Udila3 = dot(cdila,
                     (dot(cost, (multiply(-A1, r2)
                                 + multiply(dot((3 - 4*self.nu), Abar1), q2)
                                 + multiply(F1, q2)))
                      + dot(4*(1 - self.nu)*(1 - 2*self.nu), f3)
                      + dot(dot(4*(1 - self.nu), sint), (A2 + Abar2))
                      + dot(sint, (A3 + dot((3 - 4*self.nu), Abar3)
                                   + F2 - dot(2*(3 - 4*self.nu), B)))))

        # displacement: equation (8) from Yang et al (1988) - see Figure 3
        U1 = Ustar1 + Udila1
        U2 = Ustar2 + Udila2
        U3 = Ustar3 + Udila3

        return U1, U2, U3

    def yangpar(self):
        """
        Compute the parameters for the spheroid model

        Formulas from [1] Yang et al (JGR,1988)
        Corrections from [2] Newmann et al (JVGR, 2006), Appendix

         self._a1, self._b1    pressure (stress) [units of P] from [1]
         self._c         prolate ellipsoid focus [m]
         self._Pdila     pressure (proportional to double couple forces)
                            [units of P] from [1]
         self._Pstar     pressure [units of P]

        Notes:
        [-]   : dimensionless
        """
        # epsn = 1e-10
        self._c = sqrt(self.a**2 - self.b**2)

        a2 = self.a**2
        a3 = self.a**3
        b2 = self.b**2
        c2 = self._c**2
        c3 = self._c**3
        c4 = self._c**4
        c5 = self._c**5
        ac = (self.a - self._c) / (self.a + self._c)

        coef1 = dot(dot(dot(2, pi), self.a), b2)
        den1 = dot(dot(8, pi), (1 - self.nu))

        Q = 3 / den1
        R = (1 - dot(2, self.nu)) / den1

        Ia = dot(-coef1, (2 / (dot(self.a, c2)) + log(ac) / c3))
        Iaa = dot(-coef1, (2 / (3*a3*c2) + 2 / (self.a*c4) + log(ac) / c5))

        a11 = dot(dot(2, R), (Ia - dot(4, pi)))
        a12 = dot(dot(-2, R), (Ia + dot(4, pi)))
        a21 = dot(dot(Q, a2), Iaa) + dot(R, Ia) - 1
        a22 = dot(dot(-Q, a2), Iaa) - dot(Ia, (dot(2, R) - Q))

        den2 = dot(3, self.lam) + dot(2, self.mu)
        num2 = dot(3, a22) - a12
        den3 = dot(a11, a22) - dot(a12, a21)
        num3 = a11 - dot(3, a21)

        self._Pdila = dot(dot(self.P, (dot(2, self.mu) / den2)),
                          (num2 - num3)) / den3
        self._Pstar = dot(dot(self.P, (1 / den2)),
                          (dot(num2, self.lam)
                           + dot(2*(self.lam + self.mu), num3))) / den3

        self._a1 = dot(dot(-2, b2), self._Pdila)
        self._b1 = dot(dot(3, (b2 / c2)), self._Pdila)\
            + dot(dot(2, (1 - dot(2, self.nu))), self._Pstar)

        # return a1, b1, c, Pdila, Pstar
