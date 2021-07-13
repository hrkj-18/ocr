# import the necessary packages
import argparse
import numpy as np
import cv2
import sys
from PIL import Image, ImageChops

def black_and_white(input_image_path,
    output_image_path):
   color_image = Image.open(input_image_path)
   bw = color_image.convert('L')
   bw.save(output_image_path)
   #cv2.imshow("bw", bw)
   #cv2.imwrite("bw_warped.jpg", output_image_path)
   #cv2.waitKey(0)

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 

	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect
def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
	# return the warped image
	return warped

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
number = 0
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping,number

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		if number==0:
			refPt = [(x, y)]
		else:
			refPt.append((x, y))
		number=number+1
		if number>4:
			cropping = False


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
#image = cv2.imread(args["image"])
# resize image so it can be processed
# choose optimal dimensions such that important content is not lost
size = (700,700)

image = Image.open(args["image"])
image.thumbnail(size, Image.ANTIALIAS)
image_size = image.size

thumb = image.crop( (0, 0, size[0], size[1]) )

offset_x = max( (size[0] - image_size[0]) // 2, 0 )
offset_y = max( (size[1] - image_size[1]) // 2, 0 )

image = ImageChops.offset(thumb, offset_x, offset_y)
thumb.save('/home/simran/Desktop/OCRDEMO/x.jpg')
image = cv2.imread('/home/simran/Desktop/OCRDEMO/x.jpg')

clone = image.copy()
cv2.namedWindow("image")

cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	# if the 'r' key is pressed, reset the cropping region
	if key == ord("s"):
		black_and_white('/home/simran/Desktop/OCRDEMO/x.jpg',
        '/home/simran/Desktop/OCRDEMO/bw_cropped.jpg')
		break

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 4:
	
	chords = "[({}, {}), ({}, {}), ({}, {}), ({}, {})]".format(refPt[0][0],refPt[0][1],refPt[1][0],refPt[1][1],refPt[2][0],refPt[2][1],refPt[3][0],refPt[3][1])
	
	pts = np.array(eval(chords), dtype = "float32")
	 
	# apply the four point tranform to obtain a "birds eye view" of
	# the image
	cropped = four_point_transform(image, pts)
	#cropped = cv2.adaptiveThreshold(cropped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
	#ret,cropped = cv2.threshold(cropped,127,255,cv2.THRESH_TOZERO_INV)
	#cropped = cv2.adaptiveThreshold( cropped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

	cv2.imwrite("/home/simran/Desktop/OCRDEMO/cropped.jpg", cropped)
	#cv2.imshow("cropped", cropped)
	#cv2.waitKey(0)
	black_and_white('/home/simran/Desktop/OCRDEMO/cropped.jpg',
        '/home/simran/Desktop/OCRDEMO/bw_cropped.jpg')
	img = cv2.imread('/home/simran/Desktop/OCRDEMO/bw_cropped.jpg')
	cv2.imshow("bw_cropped", img)
	cv2.waitKey(0)
	
#cv2.imwrite("warped.jpg", warped)
	
# close all open windows
cv2.destroyAllWindows()
sys.exit()
