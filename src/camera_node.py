

import numpy as np
import cv2
import sys
from mrpiZ_lib import *
import rospy
from std_msgs.msg import Float64



""" initialisation du node """
rospy.init_node('camera_node', anonymous=True)

# image size
WIDTH = 640
HEIGHT = 480

# turn coeff
COEFF = 0.05
# base robot speed in straight line
SPEED = 30

video_capture = cv2.VideoCapture(0)
video_capture.set(3, WIDTH)
video_capture.set(4, HEIGHT)
rate = rospy.Rate(1/dt) # 10hz

while not rospy.is_shutdown():
    # Capture the frames
    ret, frame = video_capture.read()
    # Crop the image
    # Keep the 100 lower pixels
    crop_img = frame[379:480, 0:640]
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)


    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        # Skip to avoid div by zero
        if int(M['m00']) == 0:
            continue

    # Get the line center
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    rate.sleep()

