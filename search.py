import cv2
import numpy as np
import sys
import sqlite3
import os

def showImage(img):
	cv2.imshow('result', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def getLocalFeature(img, x, y):
	eight_bit = 0
	for (line, row, i) in [(x+1, y, 0), (x+1, y-1, 1), (x, y-1, 2), (x-1, y-1, 3), (x-1, y, 4), (x-1, y+1, 5), (x, y+1, 6), (x+1, y+1, 7)]:
		if img[line, row] == 255:
			eight_bit = eight_bit + 2 ** i
	return eight_bit

def getGlobalFeature(img, x, y):
	all_pixel = cv2.countNonZero(img)
	eight_bit = 0
	height, width = img.shape
	if height >= width:
		radius = (height, height)
	else:
		radius = (width, width)

	for i in range(0, 8):
		mask = np.zeros((height, width, 1), np.uint8)
		cv2.ellipse(mask, center=(x, y), axes=radius, angle=0, startAngle=(-22.5 + 45 * i), endAngle=(45 + 45 * i), color=255, thickness=cv2.cv.CV_FILLED)
		masked = cv2.bitwise_and(img, img, mask=mask)
		
		c = cv2.countNonZero(masked) - 1
		s = c / (all_pixel - 1)
		if s > 0.15:
			eight_bit = eight_bit + 2 ** i
	return eight_bit


# set first argment which is sketch file name  
###########################################################################

#file_name = sys.argv[1]
file_name = "c_sketch.png"

global_feature = []
local_feature = []

img = cv2.imread('./sketch/' + file_name)
g_img = cv2.bilateralFilter(img, 9, 75, 75)
c_img = cv2.Canny(g_img, 50, 150)

for y in range(0, c_img.shape[1] - 1):
	for x in range(0, c_img.shape[0] - 1):
		global_feature.append(getGlobalFeature(c_img, x, y))
		local_feature.append(getLocalFeature(c_img, x, y))

biggest = [0, 0]
		g_sum = 0
for j in range(0, 3):
	if gl_sum > biggest[0]:
		biggest[0] = gl_sum
		biggest[1] = image
	for m in range(0, 8):
		for g in range(0, 256):
			for l in range(0, 256):
				if sketch > image:
					gl_sum += image
				else:
					gl_sum =+ sketch


showImage(biggest[1])






