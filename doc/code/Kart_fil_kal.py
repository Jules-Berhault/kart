from roblib import *
import random

def draw_ellipse(w_bar,Gw,eta=0.9):
    x=arange(0.0,2*pi,0.1)
    w=zeros((size(w_bar),size(x)))
    for i in range(size(w_bar)):
        for j in range(size(x)):
            w[i,j]=w_bar[i]
    wt=w+sqrt(-2*log(1-eta))*sqrtm(Gw)@array([cos(x),sin(x)])
    plot(wt[0,:],wt[1,:])

def draw_circle(c,color,linewidth1):
    s=arange(0,2*pi,0.01)
    wr=zeros((2,len(s)))
    wc=zeros((2,len(s)))
    wc[0,:]=10*2*sin(s)
    wc[1,:]=10*sin(2*s)
    for j in range(2):
        for i in range(len(s)):
            wr[j,i]=c[j]
    w=wr+wc
    plot(w[0,:],w[1,:],color,linewidth=linewidth1)

def fl(xup,u):
    mx, my, v, δ = xup.flatten()
    x1 = array([[v * cos(theta) * cos(δ)], [v * cos(δ) * sin(theta)], [u[0, 0]], [u[1, 0]]])
    return x1

def f(x,u):
    mx,my,θ,v,δ =list(x[0:5,0])
    u1,u2=list(u[0:2,0])
    return array([[v*cos(δ)*cos(θ)],[v*cos(δ)*sin(θ)],[v*sin(δ)/L],[u1],[u2]])

def control(x,w,dw,ddw):
    x=x.flatten()
    y=array([[x[0]+cos(x[2]),x[1]+sin(x[2])]]).T
    yd = (x[3]/L)*array([[cos(x[2]+x[4]),sin(x[2]+x[4])]]).T
    v = (w - y) + 2 * (dw - yd) + ddw
    A = array([[cos(x[2]+x[4]), -x[3]*sin(x[2]+x[4])], [sin(x[2]+x[4]),x[3] * cos(x[2]+x[4])]])
    b=((x[3]**2)*sin(x[4])/L**2)*array([[-sin(x[2]+x[4]),cos(x[2]+x[4])]]).T
    u =inv(A) @ (v -b) # TO DO
    return u



k=10
c=array([[0,0]]).T
L=1
x = array([[5],[5],[0],[30],[0.0]])
s=40
dt=0.01
ax=init_figure(-s,s,-s,s)
xhat=array([[0,0,30,0]]).T
Gx=array([[100,0,0,0],[0,100,0,0],[0,0,0,0],[0,0,0,0]])
Galpha=0.01*dt*dt*array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
Gbeta=array([[5,0],[0,5]])
C=array([[1,0,0,0],[0,1,0,0]])

for t in arange(0,10,dt):
    clear(ax)
    w=k*array([[2*sin(t),sin(2*t)]]).T
    dw = k*array([[2*cos(t), 2*cos(2* t)]]).T
    ddw =-k*array([[2*sin(t), 4*sin(2* t)]]).T
    theta=x[2,0]
    y=array([[x[0,0]+2*random.random(),x[1,0]+2*random.random()]]).T
    A = array([[1, 0, dt*cos(xhat[3, 0]) * cos(theta), -dt*xhat[2, 0] * sin(xhat[3, 0]) * cos(theta)],
               [0, 1, dt*cos(xhat[3, 0]) * sin(theta), -dt*xhat[2, 0] * sin(xhat[3, 0]) * sin(theta)],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])

    u = control(array([[xhat[0, 0], xhat[1, 0], theta, xhat[2, 0], xhat[3, 0]]]).T, w, dw, ddw)
    vk=fl(xhat,u)-A@xhat
    draw_ellipse(array([x[0, 0], x[1, 0]]), Gx[0:2, 0:2])
    xhat, Gx = kalman(xhat, Gx, dt* vk, y, Galpha, Gbeta,eye(4)+dt* A, C)
    x = x + dt * f(x, u)
    draw_car(x)
    draw_circle(c, 'red', 2)
    plt.scatter(w[0], w[1], s=10)
