#!/usr/bin/env python
import cv2
import glob
import os
import numpy
from PIL import Image, ImageChops

path = '/home/simran/Desktop/OCR_APP2/Images/'
i=0
size=(28,28)
imagePath = sorted(glob.glob(path + '*.jpg')) 
for img in imagePath:
	thumbnail = Image.open(img)
	thumbnail.thumbnail(size, Image.ANTIALIAS)
	F_OUT = os.path.join(path, str(i).zfill(4)+'.jpg')

	offset_x = max((size[0] - thumbnail.size[0]) // 2, 0)
	offset_y = max((size[1] - thumbnail.size[1]) // 2, 0)
	offset_tuple = (offset_x, offset_y) #pack x and y into a tuple

	# create the image object to be the final product
	final_thumb = Image.new(mode='RGB',size=size,color=(255,255,255,0))
	# paste the thumbnail into the full sized image
	final_thumb.paste(thumbnail, offset_tuple)
	# save (the PNG format will retain the alpha band unlike JPEG)
	final_thumb.save(F_OUT)
	i=i+1
