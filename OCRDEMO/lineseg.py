import cv2
import PIL
from PIL import Image
import numpy as np
#import image
image = cv2.imread('/home/simran/Desktop/OCRDEMO/bw_cropped.jpg')
#cv2.imshow('orig',image)
#cv2.waitKey(0)

#grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray',gray)
#cv2.waitKey(0)

#binary
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
#cv2.imshow('second',thresh)
#cv2.waitKey(0)

#dilation
kernel = np.ones((5,100), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
#cv2.imshow('dilated',img_dilation)
#cv2.waitKey(0)

#find contours
im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#sort contours
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)

    # Getting ROI
    #roi = image[y:y+h, x:x+w]
    img = image[y:y+h, x:x+w]
    cv2.imwrite('/home/simran/Desktop/OCRDEMO/dummy.jpg',img)
    baseheight = 50
    img = Image.open('/home/simran/Desktop/OCRDEMO/dummy.jpg')
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save('/home/simran/Desktop/OCRDEMO/Line_images/'+str(i)+'.jpg')
    # show ROI
    #cv2.imshow('segment no:'+str(i),roi)
    cv2.rectangle(image,(x,y),( x + w, y + h ),(0,0,255),1)
    #cv2.waitKey(0)

cv2.imshow('marked areas',image)
cv2.waitKey(0)
