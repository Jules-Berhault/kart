import numpy as np
import cv2
import sys
import time 
""" from mrpiZ_lib import *
 """

dt=0.05
cam = cv2.VideoCapture('video_test.mp4')

# Taking a matrix of size 5 as the kernel 
kernel = np.ones((30,30), np.uint8) 



while(cam.isOpened()):
    time.sleep(dt)
    ret, frame = cam.read()
    # get dimensions of image
    dimensions = frame.shape
    
    # height, width, number of channels in image
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2] 
    crop_img = frame[379:480, 0:640]
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """ #filtre de canny
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    cv2.imshow('my webcam', lines)
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(edges,(x1,y1),(x2,y2),(0,0,255),2)
        
    cv2.imshow('my webcam', edges) """

    
    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    # Color thresholding
    ret,thresh = cv2.threshold(blur,180,255,cv2.THRESH_BINARY)

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
        print(cx-width/2)
    except:
        pass

    backtorgb = cv2.cvtColor(img_erosion,cv2.COLOR_GRAY2RGB)
    for i in range (-5, 5) :
        for j in range (-5, 5) :
            backtorgb[cy+j, cx+i] = [255, 0, 0]
    cv2.imshow('my webcam', backtorgb)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
