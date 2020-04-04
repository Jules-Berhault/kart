#! /usr/bin/env python

import numpy as np
import cv2
import sys
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def imageCallback(data):
	global frame, WIDTH, HEIGHT
	try:
		frame = CvBridge().imgmsg_to_cv2(data, "bgr8")
		frame = frame.astype(np.uint8)
		#rospy.loginfo(frame.shape)
	except CvBridgeError, e:
		print e
	
	
	

if __name__ == "__main__":
	# Node initalization
	rospy.init_node('camera_node', anonymous=True)
	rospy.Subscriber("image", Image, imageCallback)
	pub_error = rospy.Publisher('error', Float64, queue_size=1000)
	rate = rospy.Rate(10)
	frame = np.ones((512, 768, 3)).astype(np.uint8)
	WIDTH, HEIGHT = 190, 200

	# Taking a matrix of size 5 as the kernel for morphomat
	kernel = np.ones((3, 3), np.uint8)

	while not rospy.is_shutdown():
		# Reading camera flow picture by picture
		
		frame = frame[200:400, 250:440]
		try:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			blur = cv2.GaussianBlur(gray, (5, 5), 0)
			ret, thresh = cv2.threshold(blur, 135, 255, cv2.THRESH_BINARY)
			img_dilation = cv2.dilate(thresh, kernel, iterations=5)
			img_erosion = cv2.erode(img_dilation, kernel, iterations=8)
			# Finding the contours of the frame
			result = cv2.findContours(img_erosion.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
			contours, hierarchy = result if len(result) == 2 else result[1:3]

			# Find the biggest contour (if detected)
			if len(contours) > 0:
				c = max(contours, key=cv2.contourArea)
				M = cv2.moments(c)

				# Skip to avoid div by zero
				if int(M['m00']) == 0:
					continue

			# Getting the line center
			try:
				cx = int(M['m10']/M['m00'])
				error = cx-WIDTH/2

				# Publishing Informations
				rospy.loginfo(" error : %s", str(cx), logger_name="Camera Node :")
				pub_error.publish(error)
			except:
				rospy.logwarn("Unable to get the line center", logger_name="Camera Node :")
				
			cv2.imshow("frame", img_erosion)
			cv2.waitKey(3)
		
		except:
			continue
			
		rate.sleep()
