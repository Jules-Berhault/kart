

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

""" creation publisher  """
pub_error = rospy.Publisher('error', Float64,queue_size=1000)
""" Rate """
rate = rospy.Rate(1/dt) # 10hz

# image size
WIDTH = 640
HEIGHT = 480


# Taking a matrix of size 5 as the kernel 
kernel = np.ones((30,30), np.uint8) 

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
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)

     #dilatation
    img_dilation = cv2.dilate(thresh, kernel, iterations=4) 
    

    #erosion
    img_erosion=cv2.erode(img_dilation, kernel, iterations=2) 
    

    # Find the contours of the frame

    result = cv2.findContours(img_erosion.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    contours, hierarchy = result if len(result) == 2 else result[1:3]



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
        error=cx-WIDTH/2
        print(error)
        """ publication des commande moteur """
        pub_error.publish(error)
    except:
        pass
    backtorgb = cv2.cvtColor(img_erosion,cv2.COLOR_GRAY2RGB)
    for i in range (-5, 5) :
        for j in range (-5, 5) :
            backtorgb[cy+j, cx+i] = [255, 0, 0]
    cv2.imshow('my webcam', backtorgb)
    
    

    if cv2.waitKey(1) == 27: 
        break  # esc to quit
    rate.sleep()
cv2.destroyAllWindows()



