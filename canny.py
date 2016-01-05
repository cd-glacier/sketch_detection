import cv2
import numpy as np
import sys
import sqlite3
import os

def getFileName():
	files = os.listdir('./images')
	#delete .DS_Store
	del files[0]
	return files

###########################################################################

files_name = getFileName()

for file_name in files_name:
	name = file_name

	img = cv2.imread('./images/' + name)
	g_img = cv2.bilateralFilter(img, 9, 75, 75)
	c_img = cv2.Canny(g_img, 50, 150)

	cv2.imwrite('./canny/' + name, c_img)

