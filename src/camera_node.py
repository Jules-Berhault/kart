#! /usr/bin/env python

import numpy as np
import cv2
import sys
import rospy
from std_msgs.msg import Float64


if __name__ == "__main__":
	# Node initalization
	rospy.init_node('camera_node', anonymous=True)
	pub_error = rospy.Publisher('error', Float64, queue_size=1000)
	rate = rospy.Rate(10)

	# image settings
	WIDTH = 640
	HEIGHT = 480
	cam = cv2.VideoCapture(0)
	cam.set(3, WIDTH)
	cam.set(4, HEIGHT)

	# Taking a matrix of size 5 as the kernel for morphomat
	kernel = np.ones((30, 30), np.uint8)

	while not rospy.is_shutdown():
		# Reading camera flow picture by picture
		ret_val, frame = cam.read()
		# TODO Crop image with parameters
		crop_img = frame[379:480, 0:640]

		# Convert to grayscale
		gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

		# Gaussian blur
		blur = cv2.GaussianBlur(gray, (5, 5), 0)

		# Color thresholding
		ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

		# Dilatation and Erosion
		img_dilation = cv2.dilate(thresh, kernel, iterations=4)
		img_erosion = cv2.erode(img_dilation, kernel, iterations=2)

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
			rospy.loginfo(" error : %s", str(error), logger_name="Camera Node :")
			pub_error.publish(error)
		except:
			rospy.logwarn("Unable to get the line center", logger_name="Camera Node :")

		"""backtorgb = cv2.cvtColor(img_erosion, cv2.COLOR_GRAY2RGB)
		for i in range(-5, 5):
			backtorgb[:, cx+i] = [255, 0, 0]
		cv2.imshow('my webcam', backtorgb)"""

		rate.sleep()
