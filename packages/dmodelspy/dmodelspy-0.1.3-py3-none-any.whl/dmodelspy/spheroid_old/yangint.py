from numpy import sin, cos, dot, sqrt, multiply, log, arctan as atan


def yangint(x, y, z, z0, theta, a1, b1, a, b, csi, mu, nu, Pdila):
    """
    Compute the primitive of the displacement for a prolate ellipsoid

    Equation (1)-(8) from Yang et al (JGR, 1988)
    Corrections to some parameters from Newmann et al (JVGR, 2006)
    :param x,y,z:    coordinates of the point(s) where the displacement is computed [m]
    :param y0,z0:    coordinates of the center of the prolate spheroid (positive downward) [m]
    :param theta:     plunge angle [rad]
    :param a1,b1:     pressure (stress) (output from yangpar.m) [units of P]
    :param a:         semimajor axis [m]
    :param b:         semiminor axis [m]
    :param c:         focus of the prolate spheroid (output from yangpar.m) [m]
    :param mu:        shear modulus [Pa]
    :param nu:        Poisson's ratio
    :param Pdila:     pressure (proportional to double couple forces) [units of P]
    :returns: U1,U2,U3 : displacement in local coordinates [m] - see Figure 3 of Yang et al (1988)

    Notes:
    The location of the center of the prolate spheroid is (x0,y0,z0)
        with x0=0 and y0=0;
    The free surface is z=0;
    """
    # precalculate parameters that are used often
    sint = sin(theta)
    cost = cos(theta)

    # new coordinates and parameters from Yang et al (JGR, 1988), p. 4251
    # dimensions [m]
    csi2 = dot(csi, cost)
    csi3 = dot(csi, sint)

    x1 = x.copy()
    x2 = y.copy()
    x3 = z - z0
    xbar3 = z + z0

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
    #########################################################################
    # C0 = y0*cost + z0*sint;
    C0 = z0 / sint

    #########################################################################
    beta = (dot(q2, cost) + dot((1 + sint), (R2 + qbar3))) / (dot(cost, y1) + 1e-15)

    # precalculate parameters that are used often
    drbar3 = R1 + rbar3
    dqbar3 = R2 + qbar3
    dybar3 = R2 + ybar3
    lrbar3 = log(R1 + rbar3)
    lqbar3 = log(R2 + qbar3)
    lybar3 = log(R2 + ybar3)
    atanb = atan(beta)
    # primitive parameters from Yang et al (1988), p. 4252
    Astar1 = a1 / (multiply(R1, drbar3)) + multiply(b1, (lrbar3 + (r3 + csi) / drbar3))
    Astarbar1 = -a1 / (multiply(R2, dqbar3)) - multiply(b1, (lqbar3 + (q3 - csi) / dqbar3))
    A1 = csi / R1 + lrbar3
    Abar1 = csi / R2 - lqbar3
    A2 = R1 - multiply(r3, lrbar3)
    Abar2 = R2 - multiply(q3, lqbar3)
    A3 = multiply(csi, rbar3) / R1 + R1
    Abar3 = multiply(csi, qbar3) / R2 - R2
    Bstar = (a1 / R1 + multiply(2*b1, A2)) + dot((3 - 4*nu), (a1 / R2 + multiply(2*b1, Abar2)))
    B = dot(csi, (csi + C0)) / R2 - Abar2 - dot(C0, lqbar3)
    # the 4 equations below have been changed to improve the fit to internal
    # deformation
    Fstar1 = 0
    Fstar2 = 0
    F1 = 0
    F2 = 0
    f1 = dot(csi, y1) / dybar3 + dot((3 / cost**2), (multiply(multiply(y1, sint), lybar3) - multiply(y1, lqbar3) + multiply(dot(2, q2), atanb))) + multiply(2*y1, lqbar3) - multiply(4*xbar3, atanb) / cost
    f2 = dot(csi, y2) / dybar3 + dot((3 / cost**2), (multiply(multiply(q2, sint), lqbar3) - multiply(q2, lybar3) + multiply(dot(dot(2, y1), sint), atanb) + dot(cost, (R2 - ybar3)))) - dot(2*cost, Abar2) + dot((2 / cost), (multiply(xbar3, lybar3) - multiply(q3, lqbar3)))
    f3 = dot((1 / cost), (multiply(q2, lqbar3) - multiply(multiply(q2, sint), lybar3) + multiply(dot(2, y1), atanb))) + dot(2*sint, Abar2) + multiply(q3, lybar3) - csi
    # precalculate coefficients that are used often
    cstar = (dot(a, b**2) / csi**3) / (dot(16*mu, (1 - nu)))
    cdila = dot(dot(2, cstar), Pdila)
    # displacement components (2) to (7): primitive of eq(1) Yang et al (1988)
    Ustar1 = dot(cstar, (multiply(Astar1, y1) + multiply(dot((3 - 4*nu), Astarbar1), y1) + multiply(Fstar1, y1)))

    # U2star and U3star changed to improve fit to internal deformation
    Ustar2 = dot(cstar, (dot(sint, (multiply(Astar1, r2) + multiply(dot((3 - 4*nu), Astarbar1), q2) + multiply(Fstar1, q2))) + dot(cost, (Bstar - Fstar2))))

    # The formula used in the script by Fialko and Andy is different from
    # equation (4) of Yang et al (1988)
    # I use the same to continue to compare the results 2009 07 23
    # Ustar3 = cstar*(-cost*(Astarbar1.*r2 + (3-4*nu)*Astarbar1.*q2 - Fstar1.*q2) + ...
    #         sint*(Bstar+Fstar2) + 2*cost^2*z.*Astarbar1);
    ###################################################################################
    # The equation below is correct - follows equation (4) from Yang et al (1988)
    Ustar3 = dot(cstar, (dot(-cost, (multiply(Astar1, r2) + multiply(dot((3 - 4*nu), Astarbar1), q2) - multiply(Fstar1, q2))) + dot(sint, (Bstar + Fstar2))))

    Udila1 = dot(cdila, ((multiply(A1, y1) + multiply(dot((3 - 4*nu), Abar1), y1) + multiply(F1, y1)) - dot(dot(4*(1-nu), (1-2*nu)), f1)))
    Udila2 = dot(cdila, (dot(sint, (multiply(A1, r2) + multiply(dot((3 - 4*nu), Abar1), q2) + multiply(F1, q2))) - dot(4*(1 - nu)*(1 - 2*nu), f2) + dot(dot(4*(1 - nu), cost), (A2 + Abar2)) + dot(cost, (A3 - dot((3 - 4*nu), Abar3) - F2))))
    Udila3 = dot(cdila, (dot(cost, (multiply(-A1, r2) + multiply(dot((3 - 4*nu), Abar1), q2) + multiply(F1, q2))) + dot(4*(1 - nu)*(1 - 2*nu), f3) + dot(dot(4*(1 - nu), sint), (A2 + Abar2)) + dot(sint, (A3 + dot((3 - 4*nu), Abar3) + F2 - dot(2*(3 - 4*nu), B)))))

    # displacement: equation (8) from Yang et al (1988) - see Figure 3
    U1 = Ustar1 + Udila1
    U2 = Ustar2 + Udila2
    U3 = Ustar3 + Udila3

    return U1, U2, U3
