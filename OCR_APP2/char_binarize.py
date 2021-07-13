import cv2
import glob
import os
import numpy
from PIL import Image   

path = '/home/simran/Desktop/OCR_APP2/Images'
i=0
imagePath = sorted(glob.glob(path + '/*.jpg')) 
for img in imagePath:
	image = cv2.imread(img,0)
	#print(img)
	ret,thresh  = cv2.threshold(image, 100, 255, cv2.THRESH_OTSU)
	cv2.imshow("bw",thresh)
	cv2.imwrite(os.path.join(path, str(i).zfill(4)+'.jpg'), thresh)
	i=i+1

