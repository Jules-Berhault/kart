#! /usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Twist


def cmd_callback(cmd):
	global u1
	global u2
	u1 = int(500000 * cmd.linear.x) + 1500000
	u2 = int(500000 * cmd.angular.z) + 1500000

# def u1_callback(cmd):
#     global u1
#     u1 = int(500000 * cmd.data) + 1500000

# def u2_callback(cmd):
#     global u2
#     u2 = int(500000 * cmd.data) + 1500000

if __name__ == "__main__":
    # Command variables
    u1, u2 = 1500000, 1500000

    # ROS
    rospy.init_node('driver_node')
    rospy.Subscriber("cmd_vel", Twist, cmd_callback)
    # rospy.Subscriber("u1", Float64, u1_callback)
    # rospy.Subscriber("u2", Float64, u2_callback)

    r = rospy.Rate(20) # 20hz

    while not rospy.is_shutdown():
        # Setting up the duty cycle
        with open("/sys/class/pwm/pwmchip0/pwm0/duty_cycle", 'w') as f:
            f.write(str(u1))
        with open("/sys/class/pwm/pwmchip0/pwm1/duty_cycle", 'w') as f:
            f.write(str(u2))

        # Sleeping
        r.sleep()
