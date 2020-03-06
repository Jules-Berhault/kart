import numpy as np
from roblib import *

# Car variables
L = 0.1
dt = 0.1
old_theta = 0

def f(X, U):
    x1, x2, x3, x4, x5 = (X.flatten()).tolist()
    u1, u2 = (U.flatten()).tolist()
    return np.array([x4*np.cos(x5)*np.cos(x3, x4*np.cos(x5)*np.sin(x3), x4*sin(x5)/L, u1, u2])

def target(t):
    R = 36.5
    L = 84.39
    speed = 10 
    
    d = (t*speed) % 400
    if d < 84.39:
        x = 36.5
        y = d - 42.195
        theta = np.pi/2
        v = speed
    elif d < 200:
        x = 36.5*np.cos((d - 84.39)/36.5)
        y = 36.5*np.sin((d - 84.39)/36.5) + 42.195
        theta = np.pi/2 + np.arctan2(y - 42.195, x)
        v = speed
    elif d < 284.39:
        x = -36.5
        y = 242.195 - d
        theta = - np.pi/2
        v = speed
    else:
        x = -36.5*np.cos((d - 284.39)/36.5)
        y = -36.5*np.sin((d - 284.39)/36.5) - 42.195
        theta = np.pi/2 + np.arctan2(y + 42.195, x)
        v = speed
    return np.array([x, y, theta, v])

def control(X, w):
    global old_theta
    global L
    x1, x2, x3, x4, x5 = X.flatten()
    xc, yx, thetac, vc = w.flatten()
    A = np.array([[np.sin(x4)/L, x4*np.sin(x5)/L], [1, 0]])
    
    Y = np.array([[x3], [x4]])
    Yp = np.array([[], []])
    
    return np.linalg.solve(A, v)
    
    
if __name__ == "__main__":
    X = np.array([36.5, -42.195, np.pi/2, 10, 0])
    
    ax = init_figure(-100, 100, -100, 100)
    dt = 1
    
    p = np.arange(0, 401, 0.1)
    traj = []
    for t in p:
        traj.append([target(t)[0], target(t)[1]])
    trajectory = np.array(traj)
        
    for t in np.arange(0, 100, dt):
        clear(ax)
        plt.plot(trajectory[:, 0], trajectory[:, 1], color="firebrick", alpha = 0.6)
        w = target(t)
        
        U = control(X, w)
        X = X + dt*f(X, U)
        draw_tank(w, col="crimson", r=1)
        #draw_tank(X, col='teal', r=5)
        
        plt.pause(0.001)