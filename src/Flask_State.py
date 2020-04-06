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
    cmd_msg = msg.data

threading.Thread(target=lambda: rospy.init_node('REST_node', disable_signals=True)).start()
rospy.Subscriber('/listener', Float64, ros_callback)
#pub = rospy.Publisher('/talker', Float64, queue_size=10)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>Salut</h1>"

@app.route('/state')
def state():
    print(os.getcwd())
    s = "<h1>{}</h1>".format(cmd_msg)
    return s


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
