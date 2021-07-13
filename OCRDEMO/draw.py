# import the necessary packages
import argparse
import cv2
import PIL
from PIL import Image
import ast
#boxes=[(275, 272, 544, 333), (261, 186, 604, 247)]
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to the image")
args = vars(ap.parse_args())
template = args["template"]
with open(template) as f:
        #Content_list is the list that contains the read lines.     
	content_list = f.readlines()
content_list = [x.strip('\n') for x in content_list]
content_list = [ast.literal_eval(x) for x in content_list]

print(content_list)

i=0
image= cv2.imread('bw_cropped.jpg')
for x in content_list:	
	img = image[x[1]:x[3], x[0]:x[2]]
	'''
	cv2.imwrite('/home/simran/Desktop/OCRDEMO/dummy.jpg',img)
	baseheight = 50
	img = Image.open('/home/simran/Desktop/OCRDEMO/dummy.jpg')
	hpercent = (baseheight / float(img.size[1]))
	wsize = int((float(img.size[0]) * float(hpercent)))
	img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
	img.save('/home/simran/Desktop/OCRDEMO/Line_images/'+str(i)+'.jpg')
	'''
	cv2.imwrite('/home/simran/Desktop/OCRDEMO/Line_images/'+str(i)+'.jpg',img)
	cv2.rectangle(image,(x[0],x[1]),( x[2], x[3] ),(0,0,255),1)
	i=i+1

#example = cv2.rectangle(example, (content_list[0][0],content_list[0][1]), (content_list[0][2],content_list[0][3]), (0,255,0), 2)
#example = cv2.rectangle(example, (content_list[1][0],content_list[1][1]), (content_list[1][2],content_list[1][3]), (0,255,0), 2)
cv2.imshow('img',image)
cv2.waitKey(0)
