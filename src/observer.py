#!/usr/bin/env python

from geometry_msgs.msg import PointStamped, PoseStamped, TwistStamped,Twist,Quaternion
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from tf.transformations import quaternion_from_euler
import rospy
from numpy.linalg import inv
from numpy import *
from matplotlib.pyplot import scatter, show

Xhat = array([[0, 0, 30, 0]]).T   # x, y, v,delta
u1, u2 = 0, 0
x_gps,y_gps=0,0
dt = 0.01
freq = 25
q=[]
Gx=array([[100,0,0,0],[0,100,0,0],[0,0,0,0],[0,0,0,0]])
Galpha=0.01*dt*dt*array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
Gbeta=array([[5,0],[0,5]])
C=array([[1,0,0,0],[0,1,0,0]])

def kalman_predict(xup,Gup,u,Galpha,A):
    G1 = dot(dot(A ,Gup), A.T )+ Galpha
    x1 = dot(A,xup) + u    
    return(x1,G1)    

def kalman_correc(x0,G0,y,Gb,C):
    S = dot(dot(C,G0),C.T) + Gb        
    K = dot(dot(G0,C.T),inv(S))           
    ytilde = y - dot(C,x0)        
    Gup = dot((eye(len(x0))-dot(K,C)),G0) 
    xup = x0 + dot(K,ytilde)
    return(xup,Gup) 
    
def kalman(x0,G0,u,y,Galpha,Gb,A,C):
    xup,Gup = kalman_correc(x0,G0,y,Gb,C)
    x1,G1=kalman_predict(xup,Gup,u,Galpha,A)
    return(x1,G1)

def fl(xup,u):
    mx, my, v, delta = xup.flatten()
    x1 = array([[v * cos(theta) * cos(delta)], [v * cos(delta) * sin(theta)], [u[0, 0]], [u[1, 0]]])
    return x1

def u1Callback(data):
    u1 = data.data

def u2Callback(data):
    u2 = data.data


def gpsCallback(msg):
    x_gps=msg.point.x
    y_gps=msg.point.y

def imuCallback(msg):
    q.append(msg.orientation.x)
    q.append(msg.orientation.y)
    q.append(msg.orientation.z)
    q.append(msg.orientation.w)


theta=Quaternion(q[0],q[1],q[2],q[3])[2]
print(theta)




rospy.init_node('observer_node', anonymous=True)

""" creation subscriber """
state_pos = rospy.Publisher('state_pos_estime', PoseWithCovariance, queue_size=10)
state_vel = rospy.Publisher('state_vel_estime', Twist, queue_size=10)
vel_suscriber = rospy.Subscriber('u1', Float64, u1Callback)
cap_suscriber = rospy.Subscriber('u2', Float64, u2Callback)
Gps_suscriber = rospy.Subscriber('projection_node', PointStamped, gpsCallback)
Imu_suscriber = rospy.Subscriber('imu', Imu, imuCallback)

pose_ang = PoseWithCovariance()
vel=Twist()
rate = rospy.Rate(freq) # 25hz

while not rospy.is_shutdown():
    y=array([[x_gps],[y_gps]])
    A = array([[1, 0, dt*cos(xhat[3, 0]) * cos(theta), -dt*xhat[2, 0] * sin(xhat[3, 0]) * cos(theta)],
               [0, 1, dt*cos(xhat[3, 0]) * sin(theta), -dt*xhat[2, 0] * sin(xhat[3, 0]) * sin(theta)],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
    vk=fl(Xhat,u)-dot(A,Xhat)
    Xhat,Gx=kalman(Xhat,Gx,dt*vk,y,Galpha,Gbeta,eye(4)+dt*A,C)
    quat=quaternion_from_euler(0,0, Xhat[3,0])

    #-----#
    pose_ang.pose.position.x=Xhat[0,0]
    pose_ang.pose.position.y=Xhat[1,0]
    pose_ang.pose.position.z=0

    pose_ang.pose.orientation.x = quat[0]
    pose_ang.pose.orientation.y = quat[1]
    pose_ang.pose.orientation.z = quat[2]
    pose_ang.pose.orientation.w = quat[3]
    cov=zeros((6,6))
    cov[:2,:2]=Gx[:2,:2]
    pose_ang.covariance=cov

    vel.linear.x=Xhat[2,0]
    vel.linear.y=0
    vel.linear.z=0
    vel.angular.x=0
    vel.angular.y=0
    vel.angular.z=0

    state_pos.publish(pose_ang)
    state_vel.publish(vel)
    rate.sleep
    rospy.spin()

