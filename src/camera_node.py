

import numpy as np
import cv2
import sys
""" from mrpiZ_lib import *
 """
import rospy
from std_msgs.msg import Float64

dt=0.1





""" initialisation du node """
rospy.init_node('camera_node', anonymous=True)

# image size
WIDTH = 640
HEIGHT = 480

# turn coeff
COEFF = 0.05
# base robot speed in straight line
SPEED = 30

cam = cv2.VideoCapture(0)
cam.set(3, WIDTH)
cam.set(4, HEIGHT)
while not rospy.is_shutdown():
    ret_val, frame = cam.read()
    crop_img = frame[379:480, 0:640]
        
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Find the contours of the frame

    result = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    contours, hierarchy = result if len(result) == 2 else result[1:3]
    cv2.imshow('my webcam', thresh)



    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        # Skip to avoid div by zero
        if int(M['m00']) == 0:
            continue

    # Get the line center
    try:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(cx)
    except:
        pass
    if cv2.waitKey(1) == 27: 
        break  # esc to quit
cv2.destroyAllWindows()



