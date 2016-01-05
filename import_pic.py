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
	eight_bit = []
	for (line, row, i) in [(x+1, y, 0), (x+1, y-1, 1), (x, y-1, 2), (x-1, y-1, 3), (x-1, y, 4), (x-1, y+1, 5), (x, y+1, 6), (x+1, y+1, 7)]:
		if img[line, row] == 255:
			eight_bit.append(1)
		elif img[line, row] == 0:
			eight_bit.append(0)
		else:
			eight_bit.append(-1)
	return eight_bit

def getGlobalFeature(img, x, y):
	all_pixel = cv2.countNonZero(img)
	eight_bit = []
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
			b = 1
		elif s <= 0.15:
			b = 0
		else:
			b = -1
		eight_bit.append(b)
	return eight_bit

def toString(eight_bit):
	s = ''
	for i in range(0, 8):
		s = s + str(eight_bit[i])
	return s

def createTable():
	conn = sqlite3.connect('./images.db')
	c = conn.cursor()
	c.execute('''create table if not exists canny(name string,
																						global_feature text,
																						local_feature text)''')

def insertDB(name, global_feature, local_feature):
	conn = sqlite3.connect('./images.db')
	c = conn.cursor()
	c.execute("insert or replace into canny values(?, ?, ?);", [name, global_feature, local_feature])
	conn.commit()

def getFileName():
	files = os.listdir('./canny')
	#delete .DS_Store
	del files[0]
	return files

###########################################################################

files_name = getFileName()

for file_name in files_name:
	local_feature = ""
	global_feature = ""
	name = file_name

	img = cv2.imread('./canny/' + name, 0)

	for y in range(0, img.shape[1] - 1):
		for x in range(0, img.shape[0] - 1):
			global_feature = global_feature + "/" + toString(getGlobalFeature(img, x, y))
			local_feature = local_feature + "/" + toString(getLocalFeature(img, x, y))
	
	createTable()
	insertDB(name, global_feature, local_feature)


