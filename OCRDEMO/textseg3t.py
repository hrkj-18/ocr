import numpy as np	
import cv2
import os
import glob
from PIL import Image, ImageChops
import sys

def  textSeg():
	imageFolderPath = '/home/simran/Desktop/OCRDEMO/Line_images/'
	i=0
	
	n= len(glob.glob(imageFolderPath + '*.jpg')) #total number of images
	print(n)
	cur_n=0
	j=0 #n is starts with zero
	while cur_n<n:
		img1= imageFolderPath + str(j) + '.jpg'
		if (os.path.isfile(img1)==bool(True)):
			print("img")

			img = cv2.imread(img1)
			l=j	#LINE NUMBER
			#iterate through images
			j+=1

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
			bounding_boxes_final=[]
			for contour in contours:
				# get rectangle bounding contour
				[x, y, w, h] = cv2.boundingRect(contour)

				# Don't plot small false positives that aren't text
				if w < 2 or h < 10:
				    continue
				# Don't plot Large false positives that aren't text
				elif w >55 or h > 55:
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
			
			path = '/home/simran/Desktop/OCRDEMO/Images/'
			#print(len(bounding_boxes))
			#group boxes
			line=[]
			#print(bounding_boxes)
			os.system('mkdir -p Images/'+str(l).zfill(4))
			p_x,p_y,p_w,p_h=bounding_boxes[0][0],bounding_boxes[0][1],bounding_boxes[0][2],bounding_boxes[0][3]
			i=0
			for (x, y, w, h) in bounding_boxes:
				
				if(x>p_x ):
					if(y>p_y):
						if((x+w) < (p_x+p_w)):
							if((y+h) < (p_y+p_h)):
								cv2.rectangle(img_copy2, (x, y), (x + w, y + h), (0, 255, 0), 1)
						else:
							p_x,p_y,p_w,p_h=x,y,w,h
							cv2.rectangle(img_copy2, (x, y), (x + w, y + h), (0, 0, 255), 1)
							bounding_boxes_final.append((x,y,w,h))
					else:
						p_x,p_y,p_w,p_h=x,y,w,h
						cv2.rectangle(img_copy2, (x, y), (x + w, y + h), (0, 0, 255), 1)
						bounding_boxes_final.append((x,y,w,h))
									
				
				else:
					p_x,p_y,p_w,p_h=x,y,w,h
					cv2.rectangle(img_copy2, (x, y), (x + w, y + h), (0, 0, 255), 1)
					bounding_boxes_final.append((x,y,w,h))
					i=i+1
			cv2.imshow('Logic', img_copy2)
			cv2.waitKey(0)
			line=[]
			i=0
			l=cur_n
			os.system('mkdir -p Images/'+str(l).zfill(4))
			for (x, y, w, h) in bounding_boxes_final:
				
				crop = img[y:y+h, x:x+w]
				line.append((x,y,w,h))
				cv2.imwrite('crop.jpg',crop)
				
				F_OUT = os.path.join(path ,str(l).zfill(4)+'/'+str(i).zfill(4)+'.jpg')

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
			cur_n=cur_n+1
		else:
			j+=1
			

			
		
textSeg()
	#cv2.waitKey(0)
