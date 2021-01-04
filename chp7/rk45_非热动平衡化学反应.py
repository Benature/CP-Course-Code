
# 上面习题的参考解答。
import math
import matplotlib.pyplot as plt
import numpy as np


def rk45(t, x, f, dt):
    """ 显式五阶和隐式四阶龙格库塔算法，以及误差估计 """

    # Cash-Karp parameters
    a2, a3, a4, a5, a6 = 1./5., 3./10., 3./5., 1., 7./8.
    b21 = 1./5.
    b31, b32 = 3./40., 9./40.
    b41, b42, b43 = 3./10., -9./10., 6./5.
    b51, b52, b53, b54 = -11./54., 5./2., -70./27., 35./27.
    b61, b62, b63, b64, b65 = 1631./55296., 175./512., 575./13824., \
        44275./110592., 253./4096.
    c1, c2, c3, c4, c5, c6 = 37./378, 0., 250./621., 125./594., 0., 512./1771.
    d1, d2, d3, d4, d5, d6 = 2825./27648., 0., 18575./48384., 13525./55296., \
        277./14336., 1./4.
    e1, e2, e3, e4, e5, e6 = c1-d1, c2-d2, c3-d3, c4-d4, c5-d5, c6-d6

    # evaluate the function at the six points
    dx1 = f(t, x)*dt
    dx2 = f(t+a2*dt, x+b21*dx1)*dt
    dx3 = f(t+a3*dt, x+b31*dx1+b32*dx2)*dt
    dx4 = f(t+a4*dt, x+b41*dx1+b42*dx2+b43*dx3)*dt
    dx5 = f(t+a5*dt, x+b51*dx1+b52*dx2+b53*dx3+b54*dx4)*dt
    dx6 = f(t+a6*dt, x+b61*dx1+b62*dx2+b63*dx3+b64*dx4+b65*dx5)*dt
    # compute and return the error and the new value of x
    err = e1*dx1+e2*dx2+e3*dx3+e4*dx4+e5*dx5+e6*dx6
    return (x+c1*dx1+c2*dx2+c3*dx3+c4*dx4+c5*dx5+c6*dx6, err)


def ark45(t, x, f, dt, epsabs=1e-6, epsrel=1e-6):
    """ Adaptive Runge-Kutta integration step. """

    safe = 0.9  # safety factor for step estimate
    # compute the required error
    e0 = epsabs+epsrel*max(abs(x))
    dtnext = dt
    while True:
        # take a step and estimate the error
        dt = dtnext
        (result, error) = rk45(t, x, f, dt)
        e = max(abs(error))
        dtnext = dt*safe*(e0/e)**0.2
        if e < e0:  # accept step: return x, t, and dt for next step
            return (result, t+dt, dtnext)


# returns the derivative dX/dt for the chemical equation
def dXdt(t, X):
    x, y = X
    vx = 1 - (b+1)*x + a * x**2 * y
    vy = b*x - a * x**2 * y
    return np.array([vx, vy])


# reaction constants
a = 1.0  #
b = 3.0  #

# initial data
x0 = 0.0
y0 = 0.0
dt = 0.01
tmax = 35.0
x = [x0]
y = [y0]
t = [0.]

# 用ark45，变步长算法积分Belousov-Zhabotinsky reaction
# X is a vector that contains the positions
X = np.array([x0, y0])
T = 0.
while T < tmax:
    (X, T, dt) = ark45(T, X, dXdt, dt)
    x += [X[0]]
    y += [X[1]]
    t += [T]

plt.figure(figsize=(8, 8))
plt.plot(t, x, 'o-')
plt.plot(t, y, 'ro-')
plt.xlabel('t')
plt.ylabel('x & y')
plt.grid()
plt.show()
