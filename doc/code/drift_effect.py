#! /usr/bin python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import integrate


def graph_show(title, t, x, y, z, l1, l2, l3, xl, yl, c):
    fig = plt.figure()
    x, y, z = x.flatten(), y.flatten(), z.flatten()
    values = np.vstack((x, y, z))
    plt.clf()
    plt.title(title)
    plt.grid(True)
    #plt.axis([np.min(t), np.max(t), np.min(values)-0.1*np.max(values), np.max(values*1.1)])
    plt.plot(t, x, label=l1, color=c, linewidth=2)
    #plt.plot(t, y, color="green", label=l2)
    #plt.plot(t, z, color="blue", label=l3
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.legend(loc="best")
    return fig


if __name__=="__main__":
    # Reading Data
    df = pd.read_csv("accelerometer.csv", sep=";")
    data = df.values.astype(float)
    t, ax, ay, az, _ = np.split(data, 5, 1)
    
    # Accelerations
    ax = 10*(ax.flatten())
    ay = 10*(ay.flatten())
    az = 10*(az.flatten())
    t = t.flatten()
    a_fig = graph_show("Acceleration", t, ax, ay, az, r"$a_x$", r"$a_y$", r"$a_z$", r"time ($s$)", r"acceleration ($m.s^{-2})$", "purple")
    
    # Speed
    vx = integrate.cumtrapz(ax, t, initial=0)
    vy = integrate.cumtrapz(ax, t, initial=0)
    vz = integrate.cumtrapz(ax, t, initial=0)
    v_fig = graph_show("Speed", t, vx, vy, vz, r"$v_x$", r"$v_y$", r"$v_z$", r"time ($s$)", r"velocity ($m.s^{-1}$)", "crimson")
    
    # Position
    x = integrate.cumtrapz(vx, t, initial=0)
    y = integrate.cumtrapz(vy, t, initial=0)
    z = integrate.cumtrapz(vz, t, initial=0)
    p_fig = graph_show("Position", t, x, y, z, r"$x$", r"$y$", r"$z$", r"time ($s$)", r"position ($m$)", "teal")
    
    plt.show()