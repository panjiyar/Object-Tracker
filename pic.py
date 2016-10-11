import cv2
import numpy as np


def reader(file, tmp, prev_center, prev_length, prev_width):

	frame = cv2.imread("pics/"+file)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	     # define range of blue color in HSV
	x = 100
	y = 250
	lower_blue = np.array([x, x, x])

	upper_blue = np.array([y,y,y])
	# Thresholding

	mask = cv2.inRange(frame, lower_blue, upper_blue)

	output = cv2.bitwise_and(frame, frame, mask=mask)


	[width, length, depth] = output.shape
	#272,640,3


	for i in range(tmp*(width/12)):
		for j in range(length):
			for k in range(depth):
				output[i,j,k] = 0

	# used in the eq y = ax + b
	a = 0
	b = 0
	
	if int(file[:8]) < (x+y)/2:

		################################################################
		#Fit a linear line through through the image and then remove
		#the points that lie below and a certain st dev above it, which
		# basically removes the road.
		#this leaves us the car.
		################################################################
		x= []
		y= []

		for i in range(width):
			for j in range(length):
				if output[i,j,0] > 0 and output[i,j,1] > 0 and output[i,j,2] > 0:
					x.append(i)
					y.append(j)

		p = np.polyfit(x,y,1)
		a = p[0]
		b = p[1]

		# print p

		for i in range(width):
			for j in range(length):
				if p[0]*i + p[1] - j > -10:
					for k in range(depth):
						output[i,j,k] = 0
		

	#Binding box
	width_allowed = prev_width/10
	length_allowed = prev_length*3/2

	right_end 	= 	0
	left_end 	= 	700
	top_end 	= 	300
	bottom_end 	= 	0


	for i in range(prev_center[0]-width_allowed, prev_center[0]+width_allowed):
		for j in range(prev_center[1]-length_allowed, prev_center[1]+length_allowed):
			if j >= 0 and j < 640 and i >=0 and i <272:
				if output[i,j,0] > 0 and output[i,j,1] > 0 and output[i,j,2] > 0:
					if j > right_end:
						right_end = j
					if j < left_end:
						left_end = j
					

	width_allowed = prev_width*3/2

	for i in range(prev_center[0]-width_allowed, prev_center[0]+width_allowed):
		for j in range(prev_center[1]-length_allowed, prev_center[1]+length_allowed):
			if j >= 0 and j < 640 and i >=0 and i <272:
				if output[i,j,0] > 0 and output[i,j,1] > 0 and output[i,j,2] > 0:
					if i > bottom_end:
						bottom_end = i
					if i < top_end:
						top_end = i

	
	if left_end == 0:
		left_end = prev_center[1]-(prev_length/2)

	#reg accounts for the loss of tires, because while cutting off the road, the tires go away too

	reg = 5

	if int(file[:8]) > 80:
		reg += 5
	if int(file[:8]) > 130:
		reg += 5
	if int(file[:8]) > 174:
		#don;t need it since, linear regression is being done anymmore
		reg = 0 
	
	for i in range(top_end, bottom_end+reg):
		frame[i,left_end,0] = 255
		frame[i,left_end,1] = 255
		frame[i,left_end,2] = 40
		frame[i,right_end,0] = 255
		frame[i,right_end,1] = 255
		frame[i,right_end,2] = 40
	for i in range(left_end, right_end):
		frame[top_end,i,0] = 255
		frame[top_end,i,1] = 255
		frame[top_end,i,2] = 40
		frame[bottom_end+reg,i,0] = 255
		frame[bottom_end+reg,i,1] = 255
		frame[bottom_end+reg,i,2] = 40


	cv2.imshow(file, frame)
	cv2.waitKey(50)
	cv2.destroyWindow(file) 

	return [left_end,right_end,top_end,bottom_end]
