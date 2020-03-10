import numpy as np
import cv2
import sys
import rospy
from std_msgs.msg import Float64


""" initialisation du node """
rospy.init_node('camera_node', anonymous=True)
pub = rospy.Publisher('error', Float64, queue_size=10)

""" creation publisher  """
pub_error = rospy.Publisher('error', Float64,queue_size=1000)
""" Rate """
rate = rospy.Rate(1/dt) # 10hz

# image size
WIDTH = 640
HEIGHT = 480
cam = cv2.VideoCapture(0)
cam.set(3, WIDTH)
cam.set(4, HEIGHT)

r = rospy.Rate(20) # 20hz

while not rospy.is_shutdown():
    # Crop the image
    ret_val, frame = cam.read()
    crop_img = frame[379:480, 0:640]
        
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)

    # Find the contours of the frame
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=3)
    thresh = cv2.erode(thresh, kernel, iterations=3)
    result = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    contours, hierarchy = result if len(result) == 2 else result[1:3]
    #cv2.imshow('my webcam', thresh)

    tracked = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

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
        #cy = int(M['m01']/M['m00'])
        pub.publish(cx - WIDTH/2)
        tracked[:, cx-3:cx+3, :] = [120, 20, 140]
    except:
        pass
    backtorgb = cv2.cvtColor(img_erosion,cv2.COLOR_GRAY2RGB)
    for i in range (-5, 5) :
        for j in range (-5, 5) :
            backtorgb[cy+j, cx+i] = [255, 0, 0]
    cv2.imshow('my webcam', backtorgb)
    
    

    if cv2.waitKey(1) == 27: 
        break  # esc to quit
    
    cv2.imshow('my webcam', tracked)
    
    r.sleep()
    
cv2.destroyAllWindows()
