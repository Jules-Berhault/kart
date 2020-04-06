#! /usr/bin/env python

import os
import rospy
import threading

from flask import Flask

from std_msgs.msg import Float64

# Global Variables
cmd_msg = 0;

def ros_callback(msg):
    global cmd_msg
    cmd_msg = msg

threading.Thread(target=lambda: rospy.init_node('REST_node', disable_signals=True)).start()
rospy.Subscriber('/listener', Float64, ros_callback)
#pub = rospy.Publisher('/talker', Float64, queue_size=10)

app = Flask(__name__)

@app.route('/')
def hello_world():
    # msg = Float64()
    # msg.data = 1.0
    # pub.publish(msg)

    mots = [str(cmd_msg)]
    return render_template('index.html', titre="Bienvenue !", mots=mots)


if __name__ == '__main__':
    #app.run(host=os.environ['ROS_IP'], port=3000)
    app.run(host='0.0.0.0', port=3000)
