import numpy as np	
import cv2
import os
import glob
from PIL import Image, ImageChops
import sys

imageFolderPath = '/home/simran/Desktop/OCR_APP2/Line_images/'
i=0
j= len(glob.glob(imageFolderPath + '*.jpg')) - 1

while j>=0:
	img = cv2.imread(imageFolderPath + str(j) + '.jpg')
	#iterate through images
	j-=1

	img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 40, 255, cv2.THRESH_BINARY)
	image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
	ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV

	
	kernel = np.ones((1,1), np.uint8)
	#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	eroded = cv2.erode(new_img, kernel, iterations=3)  # dilate , more the iteration more the dilation
	#cv2.imshow('final1',eroded)
	dilated = cv2.dilate(eroded, kernel, iterations=1)

	#cv2.imshow('final',dilated)
	# for cv2.x.x

	(_,contours, hierarchy) = cv2.findContours(dilated,  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # get contours

	# for cv3.x.x comment above line and uncomment line below

	#image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	img_copy=img.copy()
	img_copy2=img.copy()
	bounding_boxes = []
	for contour in contours:
		# get rectangle bounding contour
		[x, y, w, h] = cv2.boundingRect(contour)

		# Don't plot small false positives that aren't text
		if w < 2 or h < 17:
		    continue
		# Don't plot Large false positives that aren't text
		elif w >50 or h > 50:
		    continue

		# draw rectangle around contour on original image
		cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 0, 255), 1)
		bounding_boxes.append((x,y,w,h))
	cv2.imshow('Detected text', img_copy)
	cv2.waitKey(0)
	#sort bounding boxes
	if(len(bounding_boxes) <= 1):
		continue
	max_width = max(bounding_boxes, key=lambda r: r[0] + r[2])[0]
	max_height = max(bounding_boxes, key=lambda r: r[3])[3]

	nearest = max_height * 1.4
	bounding_boxes.sort(key=lambda r: (int(nearest * round(float(r[1])/nearest)) * max_width + r[0]))
	
	path = '/home/simran/Desktop/OCR_APP2/Images/'
	#print(len(bounding_boxes))
	for (x, y, w, h) in bounding_boxes:
		crop = img[y:y+h, x:x+w]
		cv2.imwrite('crop.jpg',crop)
		
		F_OUT = os.path.join(path , str(i).zfill(4)+'.jpg')

		size = (20,20)

		image = Image.open('crop.jpg')
		image.thumbnail(size, Image.ANTIALIAS)
		image_size = image.size

		thumb = image.crop( (0, 0, size[0], size[1]) )

		offset_x = max( (size[0] - image_size[0]) // 2, 2 )
		offset_y = max( (size[1] - image_size[1]) // 2, 2 )
		offset_tuple = (offset_x, offset_y) #pack x and y into a tuple
		# create the image object to be the final product
		final_thumb = Image.new(mode='RGB',size=size,color=(255,255,255,0))
		# paste the thumbnail into the full sized image
		final_thumb.paste(image, offset_tuple)

		#thumb = ImageChops.offset(thumb, offset_x, offset_y)
		final_thumb.save(F_OUT)

		i=i+1
	#cv2.waitKey(0)
	

"""
img = cv2.imread('/home/simran/resize/image1.jpg')
img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 40, 255, cv2.THRESH_BINARY)
image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV

'''
    line  8 to 12  : Remove noisy portion 
'''
kernel = np.ones((1,1), np.uint8)
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
eroded = cv2.erode(new_img, kernel, iterations=3)  # dilate , more the iteration more the dilation
#cv2.imshow('final1',eroded)
dilated = cv2.dilate(eroded, kernel, iterations=1)

#cv2.imshow('final',dilated)
# for cv2.x.x

(_,contours, hierarchy) = cv2.findContours(dilated,  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # get contours

# for cv3.x.x comment above line and uncomment line below

#image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
img_copy=img.copy()
img_copy2=img.copy()
bounding_boxes = []
for contour in contours:
	# get rectangle bounding contour
	[x, y, w, h] = cv2.boundingRect(contour)

	# Don't plot small false positives that aren't text
	if w < 2 or h < 10:
	    continue
	# Don't plot Large false positives that aren't text
	elif w >45 or h > 45:
	    continue

	# draw rectangle around contour on original image
	cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 0, 255), 1)
	bounding_boxes.append((x,y,w,h))
cv2.imshow('captcha_result', img_copy)
cv2.waitKey(0)

max_width = max(bounding_boxes, key=lambda r: r[0] + r[2])[0]
max_height = max(bounding_boxes, key=lambda r: r[3])[3]
nearest = max_height * 1.4
bounding_boxes.sort(key=lambda r: (int(nearest * round(float(r[1])/nearest)) * max_width + r[0]))
i=0
path = '/home/simran/resize'
#print(len(bounding_boxes))
for (x, y, w, h) in bounding_boxes:
	crop = img[y:y+h, x:x+w]
	cv2.imwrite('crop.jpg',crop)
	
	F_OUT = os.path.join(path , str(i).zfill(4)+'.jpg')

	size = (20,20)

	image = Image.open('crop.jpg')
	image.thumbnail(size, Image.ANTIALIAS)
	image_size = image.size

	thumb = image.crop( (0, 0, size[0], size[1]) )

	offset_x = max( (size[0] - image_size[0]) // 2, 2 )
	offset_y = max( (size[1] - image_size[1]) // 2, 2 )
	offset_tuple = (offset_x, offset_y) #pack x and y into a tuple
	# create the image object to be the final product
	final_thumb = Image.new(mode='RGB',size=size,color=(255,255,255,0))
	# paste the thumbnail into the full sized image
	final_thumb.paste(image, offset_tuple)

	#thumb = ImageChops.offset(thumb, offset_x, offset_y)
	final_thumb.save(F_OUT)

	#resize_img =cv2.resize(crop, (28,28))
	#resize_img = resize_img.astype(np.uint8)
	#cv2.imshow("Image", resize_img )
	#cv2.imwrite(os.path.join(path , str(i).zfill(4)+'.png'), resize_img)
	i=i+1
	#cv2.waitKey(0)


# write original image with added contours to disk

#while(cv2.waitKey()!=ord('q')):
#    continue
cv2.destroyAllWindows()

"""
