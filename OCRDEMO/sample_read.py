#import the necessary packages
import argparse
import cv2
import os 
import sys
import ast
#boxes=[(275, 272, 544, 333), (261, 186, 604, 247)]
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to the image")
ap.add_argument("-tt", "--template_type", required=True, help="Path to the image")
#ap.add_argument("-i", "--img", required=True, help="Path to the image")
args = vars(ap.parse_args())
template = args["template"]
#img = args["img"]
template_type = args["template_type"]
# with open(template_label) as f:
# 	content_list = f.readlines()
# 	for x in content_list:
# 		content_list
#content_list = [x.strip('\n') for x in content_list]

#print(content_list)

#print(template_labels)
with open(template_type) as f:
    #Content_list is the list that contains the read lines.     
	template_types= f.read().split(',')
i=0
ic=0
os.system('mkdir -p /home/simran/Desktop/OCRDEMO/D_images')
for x in template_types:
	x=x.rstrip('\n')
	if x=='2':
		os.system('mv /home/simran/Desktop/OCRDEMO/Line_images/'+str(i)+'.jpg  /home/simran/Desktop/OCRDEMO/D_images/'+str(ic)+'.jpg')
		ic=ic+1
	i=i+1
