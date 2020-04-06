#! /usr/bin/env python3

import os
import rospy
import rospkg
import threading

from flask import Flask, render_template
import folium

from std_msgs.msg import Float64

# Global Variables
cmd_msg = 0;

def ros_callback(msg):
    global cmd_msg
    cmd_msg = msg.data

threading.Thread(target=lambda: rospy.init_node('REST_node', disable_signals=True)).start()
rospy.Subscriber('/listener', Float64, ros_callback)
prefix = rospack.get_path('kart')

def save_map():
    map = folium.Map(location=[45.5236, -122.6750])
    rospack = rospkg.RosPack()
    map.save(prefix + '/templates/map.html')

app = Flask(__name__, template_folder=prefix + '/templates')

@app.route('/')
def home():
    save_map()
    return render_template('state.html')

@app.route('/map')
def show_map():
    save_map()
    return render_template('map.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
