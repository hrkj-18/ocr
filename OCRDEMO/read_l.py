# import the necessary packages
import argparse
import cv2
import ast
#boxes=[(275, 272, 544, 333), (261, 186, 604, 247)]
ap = argparse.ArgumentParser()
ap.add_argument("-tl", "--template_label", required=True, help="Path to the image")
ap.add_argument("-tt", "--template_type", required=True, help="Path to the image")
args = vars(ap.parse_args())
template_l = args["template_label"]
with open(template_l) as f:
        #Content_list is the list that contains the read lines.     
	content_list = f.read().split(',')
labels=[]
for x in content_list[:-1]:
	labels.append(x) 

print(labels)

template_t = args["template_type"]
with open(template_t) as f:
        #Content_list_t is the list that contains the read lines.     
	content_list = f.read().split(',')
types=[]
for x in content_list[:-1]:
	types.append(x) 

print(types)
