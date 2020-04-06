#! /usr/bin/env python3

import os
import rospy
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
#pub = rospy.Publisher('/talker', Float64, queue_size=10)

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    map = folium.Map(location=[45.5236, -122.6750])
    map.save('./templates/map.html')
    url_for('../templates', filename='map.html')
    return render_template('state.html', iframe="map.html")

@app.route('/map')
def state():
    map = folium.Map(location=[45.5236, -122.6750])
    map.save('./templates/map.html')
    return render_template('map.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
