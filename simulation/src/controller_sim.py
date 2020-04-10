#! /usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


def error_callback(data):
    global error
    error = data.data


def compute_u2(e):
    el = [0, 0]
    kp = 4
    kd = 0.000
    el[0] = el[1]
    el[1] = e
    return kp*e + kd*(el[1] - el[0]) 

def compute_u1(e):
    u1=20
    el = [0, 0]
    kp = 1
    kd = 0.000
    el[0] = el[1]
    el[1] = e
    return u1 - kd*abs(el[1] - el[0]) 


if __name__ == "__main__":
    # Variables
    error = 0
    u1, u2 = 20, 0

    # ROS
    rospy.init_node('driver_node')
    cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("error", Float64, error_callback)
    r = rospy.Rate(20)

    msg = Twist()

    while not rospy.is_shutdown():
        # Computing the command to set
        u2 = compute_u2(error)
        u1= compute_u1(error)
        msg.linear.x = u1
        msg.angular.z = u2
        cmd_pub.publish(msg)

        # Sleeping
        r.sleep()
