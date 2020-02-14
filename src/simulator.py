#!/usr/bin/env python

from roblib import *
from geometry_msgs.msg import PointStamped, PoseStamped, TwistStamped
from std_msgs.msg import Float64
from tf.transformations import quaternion_from_euler
import rospy
from numpy.linalg import inv
from numpy import *
from matplotlib.pyplot import scatter, show

X = array([[0, 0, 0, 0]]).T   # x, y, theta, v
u1, u2 = 0, 0
freq = 25

def u1Callback(data):
    u1 = data.data

def u2Callback(data):
    u2 = data.data


# def dynamique(u1, u2):





rospy.init_node('simulator_node', anonymous=True)

""" creation subscriber """
state_publisher = rospy.Publisher('state', PoseStamped, queue_size=10)
cap_suscriber = rospy.Subscriber('u1', Float64, u1Callback)
cap_suscriber = rospy.Subscriber('u2', Float64, u2Callback)

state = PoseStamped()
rate = rospy.Rate(freq) # 25hz

while not rospy.is_shutdown():
    state.header.stamp = rospy.Time.now()
    state.header.frame_id = "map"

    #scatter(Y[0], Y[1])
    
    Xb, Gx = observateur(theta, v, Y, Xb, Gx, dt)
    
    q = quaternion_from_euler(0,0, theta)
    
    state.pose.position.x = Xb[0]
    state.pose.position.y = Xb[1]

    # rospy.logwarn("xb : %f,  xvrai : %f" %(Xb[0], Y[0]))
    # rospy.logwarn("yb : %f,  yvrai : %f" %(Xb[1], Y[1]))
    # rospy.logwarn(" : %f" %Xb[1])

    state.pose.orientation.x = q[0]
    state.pose.orientation.x = q[1]
    state.pose.orientation.x = q[2]
    state.pose.orientation.x = q[3]

    state_publisher.publish(state)
    rate.sleep()