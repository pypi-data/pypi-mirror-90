from dataclasses import dataclass, field

from numpy import (abs, arange, array, concatenate, cos, cosh, dot, exp, eye,
                   finfo, log, max, min, multiply, ones, pi, sqrt, sin, sinh,
                   zeros)
from numpy.linalg import solve
from scipy.special import jv as besselj


@dataclass
class Sill:
    """
    3D Green's function for sill-like source (Fialko et al., GJI, 2001)

    A pressurized sill-like source using the finite penny-crack model
    of Fialko et al (GJI, 2001)
    All parameters are in SI (MKS) units
    :param x0,y0:     coordinates of the center of the sphere
    :param z0:        depth of the center of the sill (positive downward and
                      defined as distance below the reference surface)
    :param P_G:       dimensionless excess pressure (pressure/shear modulus)
    :param a:         radius of the sphere
    :param nu:        Poisson's ratio

    """
    # There are two typos in the published paper
    # eq (12) and (13)
    #     (1) 2*Uz and 2*Ur must be replaced by Uz and Ur
    #     (2) dcsi/sinh(csi*h) must be replaced by dcsi
    # eq (24)
    #      (1-exp(-2*a)) must be replaced by exp(-a)
    x0: float
    y0: float
    z0: float
    P_G: float
    a: float
    nu: float
    # attributes affecting cached attributes
    _a: float = field(init=False, repr=False)
    _nu: float = field(init=False, repr=False)
    _P_G: float = field(init=False, repr=False)
    _z0: float = field(init=False, repr=False)
    # Cached variables
    _dV: float = field(init=False, repr=False, default=None)
    _csi_col: array = field(init=False, repr=False)
    _wcsi_col: array = field(init=False, repr=False)
    _Aarr: array = field(init=False, repr=False)
    _Barr: array = field(init=False, repr=False)
    
    @property
    def a(self) -> float:
        return self._a
    
    @a.setter
    def a(self, a: float):
        self._a = a
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
    
    def _calc_base(self):
        """
        Calculate base (cached) parameters

        Generates self.(_dV, _csi_col, _wcsi_row, _Aarr, _Barr)
        """
        # General parameters
        eps = 1e-08
        h = self._z0 / self._a                      # dimensionless source depth

        # solve for PHI and PSI, Fialko et al. (2001), eq. (26)
        # ascissas and weights for Gauss-Legendre quadrature
        csi1, w1 = _gauleg(eps, 10, 41)
        csi2, w2 = _gauleg(10, 60, 41)
        csi = concatenate((csi1, csi2))
        wcsi = concatenate((w1, w2))
        
        self._csi_col = csi.reshape((-1, 1))
        self._wcsi_row = wcsi.reshape((1, -1))

        phi, psi, t, wt = _psi_phi(h)
        wt_col = wt.reshape((-1, 1))
        t_col = t.reshape((-1, 1))
        phi_col = phi.reshape((-1, 1))
        psi_col = psi.reshape((-1, 1))
        csi_t = self._csi_col @ t.reshape((1, -1))
        # Gauss-Legendre quadrature
        PHI = sin(csi_t) @ (wt_col * phi_col)
        PSI = (sin(csi_t) / (csi_t) - cos(csi_t)) @ (wt_col * psi_col)

        # compute A and B, Fialko et al. (2001), eq. (24)
        # NOTE error in eq (24), (1-exp(-2*a)) must be replaced by exp(-a)
        a = h * self._csi_col
        self._Aarr = exp(-a) * (a * PSI + (1 + a) * PHI)
        self._Barr = exp(-a) * ((1 - a) * PSI - a * PHI)

        # Volume change
        dV = -4*pi * (1-self._nu) * self._P_G * self._a**3. * dot(
                   t_col.T, wt_col * phi_col)
        self._dV = dV[0][0]

    def calc_displ(self, x, y, z):
        """
        Calculate displacement

        :param x,y:       benchmark location
        :param z:         depth within the crust (z=0 is the free surface)
        :kind x, y, z: 1d arrays
        :returns:   u, v, w:  E, N and Up deformation components
        """
        if self._dV is None:
            self._calc_base()

        # Coordinates transformation
        x = (array(x, ndmin=1) - self.x0) / self.a
        y = (array(y, ndmin=1) - self.y0) / self.a
        z = (array(z, ndmin=1) - self.z0) / self.a
        # print(f'{x.shape=}')
        # print(f'{x=}')
        # compute radial distance
        r = sqrt(x**2 + y**2)
        h = self.z0 / self.a                      # dimensionless source depth

        # compute Uz and Ur, Fialko et al. (2001), eq. (12) and (13)
        # NOTE there are two errors in eq (12) and (13)
        # (1) 2*Uz and 2*Ur must be replaced by Uz and Ur
        # (2) dcsi/sinh(csi*h) must be replaced by dcsi
        Uz = zeros(r.shape)
        Ur = zeros(r.shape)
        csi_z_h = (z+h) * self._csi_col
        for i in arange(r.size):
            J0 = besselj(0, r[i] * self._csi_col)
            Uzi = J0 * (((1 - 2*self.nu) * self._Barr - csi_z_h * self._Aarr) * sinh(csi_z_h)
                        + (2*(1-self.nu) * self._Aarr - csi_z_h * self._Barr) * cosh(csi_z_h))
            Uz[i] = dot(self._wcsi_row, Uzi)
            J1 = besselj(1, r[i] * self._csi_col)
            Uri = J1 * (((1 - 2*self.nu) * self._Aarr + csi_z_h * self._Barr) * sinh(csi_z_h)
                        + (2*(1-self.nu) * self._Barr + csi_z_h * self._Aarr) * cosh(csi_z_h))
            Ur[i] = dot(self._wcsi_row, Uri)

        # Deformation components
        u = self.a * self.P_G * Ur * x / r
        v = self.a * self.P_G * Ur * y / r
        w = -self.a * self.P_G * Uz

        for var in [u, v, w]:
            var = var.reshape(x.shape)
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


def _legpol(x, N):
    """
    Legendre polynomial, Bonnetis recursion formula

    Reference: http://en.wikipedia.org/wiki/Legendre_polynomials
    :param x:
    :kind x: np.array of size=(1,M)
    :param N:
    :returns: pN, dpN

    Note
    index n in wiki goes from 0 to N, in MATLAB j goes from 1 to N+1. To
    obtain the right coefficients we introduced j = n+1 -> n = j-1
    Reversed for python implementation
    """
    P = ones((N+1, x.size))
    dP = zeros((N, x.size))
    P[1, :] = x
    for j in arange(1, N):
        P[j+1, :] = (multiply(dot((2*j+1), x), P[j, :]) - j*P[j-1, :]) / (j+1)
        dP[j, :] = dot(j, (multiply(x, P[j, :]) - P[j-1, :])) / (x ** 2 - 1)

    pN = P[N-1, :]
    dpN = dP[N-1, :]

    return pN, dpN


def _gauleg(x1, x2, N):
    """
    Return abcissas and weights of the Gaussian- Legendre quadrature

    Loosely based on SUBROUTINE gauleg (Numerical Recipes in Fortran 77, 4.5)
    :param x1: lower integration limit
    :param x2: upper integration limit
    :param N: length of arrays to return
    :returns: x, w: abcissas and weights arrays
    :rtype: (1,N) numpy.array

    Note:
    tested against the "High-precision Abscissas and Weights for Gaussian
    Quadrature of high order." table from http://www.holoborodko.com/pavel/
    click on Numerical Methods then Numerical Integration. The Table is at
    the end of the page
    >> _gauleg(-1, 1, 11)
    ****** for N = 11
     Abscissas x                      Weights w
     0                               0.2729250867779006307144835
    +-0.2695431559523449723315320 	0.2628045445102466621806889
    +-0.5190961292068118159257257 	0.2331937645919904799185237
    +-0.7301520055740493240934163 	0.1862902109277342514260976
    +-0.8870625997680952990751578 	0.1255803694649046246346943
    +-0.9782286581460569928039380 	0.0556685671161736664827537
    *************************************************************************
    """
    z = zeros((N))
    xm = dot(0.5, (x2 + x1))
    xl = dot(0.5, (x2 - x1))

    for n in arange(N):
        z[n] = cos(dot(pi, (n+1 - 0.25)) / (N+0.5))
        z1 = dot(100, z[n])
        while abs(z1 - z[n]) > finfo(float).eps:
            pN, dpN = _legpol(z[n], N+1)
            z1 = z[n]
            z[n] = z1 - pN / dpN

    _, dpN = _legpol(z, N+1)
    x = xm - dot(xl, z)
    w = dot(2, xl) / (multiply((1 - z**2), dpN**2))

    return x, w


def _psi_phi(h):
    """
    compute the functions phi(t) and psi(t)

    Using the Nystrom routine with the  N-point Gauss-Legendre rule
    (Numerical Recipes in Fortran 77 (1992), 18.1 Fredholm Equations of the
    Second Kind, p. 782.)

    :param h:     dimensionless source depth
    :returns: phi, psi, t, w
              phi and psi are expressions from Appendix A of Fialko et al
              (2001), equation (A1). phi and psi are used in the definition
              of the functions PHI and PSI. See also A_B.m and Fialko et al
              (2001), eq. (26), p. 184.
              t and w are the abscissas and weights from the Gauss-Legendre
              quadrature rule (t is a value between 0 and 1; length(t) = M)

    ###########################################################################
    # Press W. et al. (1992). Numerical Recipes in Fortran 77. 2nd Ed,
    #  Cambridge University Press. Available on-line at www.nrbook.com/fortran/
    ###########################################################################
    """
    t, w = _gauleg(0, 1, 41)

    # Solution at the quadrature points r(j) **********************************
    g = dot(-2, t) / pi
    d = concatenate((g, zeros(g.shape))).T
    T1, T2, T3, T4 = _calc_T(h, t, t)

    T1tilde = zeros(T1.shape)
    T2tilde = zeros(T1.shape)
    T3tilde = zeros(T1.shape)
    T4tilde = zeros(T1.shape)
    N = t.size
    for j in range(N):
        T1tilde[:, j] = dot(w[j], T1[:, j])
        T2tilde[:, j] = dot(w[j], T2[:, j])
        T3tilde[:, j] = dot(w[j], T3[:, j])
        T4tilde[:, j] = dot(w[j], T4[:, j])

    Ktilde = concatenate((concatenate((T1tilde, T3tilde)),
                          concatenate((T4tilde, T2tilde))),
                         axis=1)

    y = solve((eye(dot(2, N), dot(2, N)) - dot((2 / pi), Ktilde)), d)

    phi = y[: N]
    psi = y[N: 2*N]
    # phi=y[arange(1,N)]
    # psi=y[arange(N + 1,dot(2,N))]

    return phi, psi, t, w


def _calc_P(h, x):
    """
    :param h:     dimensionless source depth
    :param x:     dummy variable

    P1-P4 are expressions from Appendix A of Fialko et al (2001). Used in the
    definition of the functions T1 - T4 (see T.m)
    """
    outP = zeros((4, x.size))
    # P1(x), pg 189
    outP[0, :] = (dot(12, h**2) - x**2) / (dot(4, h**2) + x**2)**3
    # P2(x), pg 189
    outP[1, :] = log(4*h**2 + x**2)\
        + (8*h**4 + dot(2*x**2, h**2) - x**4) / (dot(4, h**2) + x**2)**2
    # P3(x), pg 189
    outP[2, :] = dot(2, (8*h**4 - dot(2*x**2, h**2) + x**4))\
        / (4*h**2 + x**2)**3
    # P4(x), pg 189
    outP[3, :] = (dot(4, h**2) - x**2) / (dot(4, h**2) + x**2)**2

    return outP


def _calc_T(h, t, r):
    """
    :param h:     dimensionless source depth
    :param r:     dummy variable (used to integrate along the sill
        dimenionless radius)
    :param t:     dummy variable

    :returns: T1-T4,  expressions from Appendix A of Fialko et al (2001),
        equations (A2) - (A5). T1-T4 are used in the definition of the
        functions phi and psi (see phi_psi.m)
    """
    M = t.size
    N = r.size
    T1 = zeros((M, N))
    T2 = T1.copy()
    T3 = T1.copy()

    for i in range(M):
        Pm = _calc_P(h, t[i] - r)
        Pp = _calc_P(h, t[i] + r)
        T1[i, :] = dot(dot(4, h**3), (Pm[0, :] - Pp[0, :]))
        T2[i, :] = multiply((h / (multiply(t[i], r))), (Pm[1, :] - Pp[1, :]))\
            + dot(h, (Pm[2, :] + Pp[2, :]))
        T3[i, :] = multiply((h**2. / r),
                            (Pm[3, :] - Pp[3, :]
                             - multiply(dot(2, r),
                                        (multiply((t[i] - r), Pm[0, :])
                                         + multiply((t[i] + r), Pp[0, :])))))

    T4 = T3.T
    return T1, T2, T3, T4
