import rospy
import numpy as np
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


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
cmd_pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
# u1_pub = rospy.Publisher("u1", Float64, queue_size=10)
# u2_pub = rospy.Publisher("u2", Float64, queue_size=10)
rospy.Subscriber("error", Float64, error_callback)

msg = Twist()

r = rospy.Rate(20) # 20hz

while not rospy.is_shutdown():
    # Computing the command to set
    u2 = compute_u2(error)
    msg.linear.x = u1
    msg.angular.z = u2
    cmd_pub.publish(msg)
    
    # Sleeping
    r.sleep()