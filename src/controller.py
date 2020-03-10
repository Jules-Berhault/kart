import rospy
from std_msgs.msg import Float64
import numpy as np


def error_callback(data):
    global error
    error = data.data
    
def compute_u2(e) :
    Kp = 0.01
    return np.tanh(Kp*e)

# Variables
error = 0
u1, u2 = 0.1, 0

# ROS
rospy.init_node('driver_node')
u1_pub = rospy.Publisher("u1", Float64, queue_size=10)
u2_pub = rospy.Publisher("u2", Float64, queue_size=10)
rospy.Subscriber("error", Float64, error_callback)

r = rospy.Rate(20) # 20hz

while not rospy.is_shutdown():
    # Computing the command to set
    u2 = compute_u2(error)
    u1_pub.publish(u1)
    u2_pub.publish(u2)
    
    # Sleeping
    r.sleep()