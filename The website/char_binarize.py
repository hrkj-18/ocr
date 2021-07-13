#!/usr/bin/env python
import cv2
import glob
import os
import numpy
from PIL import Image, ImageChops
def Char_binarize():
	path = 'Images/'
	size=(28,28)
	n=os.popen('find Images -type d | wc -l').read()
	n = int(n)
	n=n-1
	for i in range(0,n):
		imagePath = sorted(glob.glob(path +str(i).zfill(4)+ '/*.jpg')) 
		j=0
	
		for img in imagePath:
			image = cv2.imread(img,0)
			#print(img)
			ret,thresh  = cv2.threshold(image, 100, 255, cv2.THRESH_OTSU)
			ret,thresh  = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY_INV)
			cv2.imshow("bw",thresh)
			cv2.imwrite(os.path.join(path, str(i).zfill(4)+'/'+str(j).zfill(4)+'.jpg'), thresh)
			j=j+1
