#! /usr/bin/env python3

import os
import rospy
import rospkg
import threading
import cv2

from flask import Flask, render_template, Response

from sensor_msgs.msg import Image

frame = 0

camera = cv2.VideoCapture(0)

def image_callback(msg):
    global frame
    frame = msg.data

threading.Thread(target=lambda: rospy.init_node('mjpg_server_node', disable_signals=True)).start()
rospy.Subscriber('/image_raw', Image, image_callback)

app = Flask(__name__)

def gen():
    while True:
        _, frame = cv2.imencode('.JPEG', camera.read()[1])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tostring() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
