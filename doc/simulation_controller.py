import numpy as np
from roblib import *

# Car variables
L = 0.1
dt = 0.01
old_theta = 0
R = 15
omega = 1

def f(X, U):
    x, y, theta, v, delta = (X.flatten()).tolist()
    u1, u2 = (U.flatten()).tolist()
    return np.array([v*np.cos(delta)*np.cos(theta), v*np.cos(delta)*np.sin(theta), v*sin(delta)/L, u1, u2])

def target(t):
    
    w = R * np.array([[np.cos(omega*t)], [np.sin(omega*t)]])
    dw = R * omega * np.array([[-np.sin(omega*t)], [np.cos(omega*t)]])
    return w, dw

def control(X, w, dw):
    global old_theta
    x, y, theta, v, delta = (X.flatten()).tolist()

    a1, a2, a3, a4 = 1, 5, 1, 1/10
    
    d = np.sqrt((w[0, 0]-x)**2 + (w[1, 0]-y)**2)
    
    dtheta = -(theta - old_theta)/dt
    old_theta = theta
    
    u = np.array([[a1 * d + a2 * (np.linalg.norm(dw) - v)], [a3 * sawtooth(np.arctan2(w[1, 0]-y, w[0, 0] - x) - theta) + a4 * dtheta]])
    return u


if __name__ == "__main__":
    X = np.array([15, -1, np.pi/2, 1, 0])
    ax = init_figure(-30, 30, -30, 30)
    dt = 0.01
    angle = arange(0, 2*pi, 0.1)    
    traceX = R*cos(angle)
    traceY = R*sin(angle)
    
    for t in np.arange(0, 100, dt):
        clear(ax)
        plot(traceX, traceY, 'g')
        w, dw= target(t)
        U = control(X, w, dw)
        X = X + dt*f(X, U)
        
        draw_tank(X)
        plt.scatter(w[0], w[1], color='crimson')
        plt.pause(0.001)