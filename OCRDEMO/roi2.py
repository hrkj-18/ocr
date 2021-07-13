# import the necessary packages
import argparse
import tkinter as tk
import cv2
from tkinter import filedialog
from PIL import Image, ImageChops
import sys
import os

labels=[]
types=[]
autocorrect =[]
def printlabelntype():
    global E1,top,T,A

    string = E1.get() 
    labels.append(string)
    print("label : "+string) 

    string = T.get() 
    if(string == "number"):
        types.append('0')
    elif string == "string":
        types.append('1')
    elif string == "img":
        types.append('2')
    print("type : "+string) 

    string = A.get() 
    if(string== "No"):
        autocorrect.append('0')
    elif string == "Yes":
        autocorrect.append('1')
    print("Autocorrect : "+string) 

    top.destroy()
def create_label_window():
    global top,E1,T,A
    top = tk.Tk()
    L1 = tk.Label(top, text="Label Name")
    L1.pack( side = 'left')
    E1 = tk.Entry(top, bd =5)
    E1.pack(side = 'left')
    E1.focus_set()
    T= tk.StringVar(top)
    T.set("string") # default value

    w = tk.OptionMenu(top, T, "string", "number", "img")
    w.pack(side = 'left')

    A= tk.StringVar(top)
    A.set("No") # default value

    auto = tk.OptionMenu(top, A, "No", "Yes")
    auto.pack(side = 'left')
    
 
    B1 = tk.Button(top,text='OK',command=printlabelntype)
    B1.pack(side='right')
    top.mainloop()
def printlabeltofile():
    global name,top
    name = name.get() 
    #print coordinates
    orig_stdout = sys.stdout
    f=open("/home/simran/Desktop/OCRDEMO/Templates/"+name,"w")
    sys.stdout = f
    for x in boxes:
        print(x)
    sys.stdout = orig_stdout
    f.close()
    #print labels
    orig_stdout = sys.stdout
    f=open("/home/simran/Desktop/OCRDEMO/Templates/"+name+"_l","w")
    sys.stdout = f
    for label in labels:
       print(label,end=",")
    sys.stdout = orig_stdout
    f.close()
    #print types
    orig_stdout = sys.stdout
    f=open("/home/simran/Desktop/OCRDEMO/Templates/"+name+"_t","w")
    sys.stdout = f
    for label in types:
       print(label,end=",")
    sys.stdout = orig_stdout
    f.close()
    
    #print auto
    orig_stdout = sys.stdout
    f=open("/home/simran/Desktop/OCRDEMO/Templates/"+name+"_a","w")
    sys.stdout = f
    for auto in autocorrect:
       print(auto,end=",")
    sys.stdout = orig_stdout
    f.close()
    
    top.destroy()
def create_template_window():
    global top,name
    top = tk.Tk()
    L1 = tk.Label(top, text="Template Name")
    L1.pack( side = 'left')
    name = tk.Entry(top, bd =5)
    name.pack(side = 'left')
    name.focus_set()
    B1 = tk.Button(top,text='OK',command=printlabeltofile)
    B1.pack(side='right')
    top.mainloop()
    
def black_and_white(input_image_path,
    output_image_path):
   color_image = Image.open(input_image_path)
   bw = color_image.convert('L')
   bw.save(output_image_path)

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
boxes = []
img_boxes = []
cropping = False
#for runtime drawing
x_start, y_start, x_end, y_end = 0, 0, 0, 0
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
thumb.save('/home/simran/Desktop/OCRDEMO/dummy.jpg')
black_and_white('/home/simran/Desktop/OCRDEMO/dummy.jpg',
        '/home/simran/Desktop/OCRDEMO/bw_cropped.jpg')
# load the image, clone it, and setup the mouse callback function
image = cv2.imread("bw_cropped.jpg")
clone = image.copy()

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end,refPt, cropping,clone,image

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        if len(refPt) == 2:
            roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            # keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("ROI SAVE? YES(y) or NO(n)", roi)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("y"):
                    #name = input("Enter file name ")
                    boxes.append((x_start,y_start,x_end,y_end))
                    #box.append((x_start,y_start,x_end,y_end))
                    #cv2.imwrite(name+".jpg", roi)
                    clone=image.copy()
                    image = clone.copy()
                    cv2.destroyWindow("ROI SAVE? YES(y) or NO(n)")
                    create_label_window()
                    break

                # if the 'c' key is pressed, break from the loop
                elif key == ord("n"):
                    image = clone.copy()
                    cv2.destroyWindow("ROI SAVE? YES(y) or NO(n)")
                    break

            
            #cv2.imshow("ROI", roi)

            #cv2.waitKey(0)

        #cv2.imshow("image", image)
       


# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())


cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    i=image.copy()
    # display the image and wait for a keypress
    if not cropping:
        cv2.imshow("image", image)
        
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
    
    key = cv2.waitKey(1)
    # if the 'r' key is pressed, reset the cropping region
    #if key == ord("n"):
        #image = clone.copy()
        #cv2.setMouseCallback("image", click_and_crop)
        

    # if the 'c' key is pressed, break from the loop
    if key == ord("c"):
        create_template_window()
        break

    '''
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("n"):
        image = clone.copy()
        cv2.setMouseCallback("image", click_and_crop)
        

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        print("c")
        break
        '''
#print(boxes)
#name = input("Enter Template name :")


'''
f=open("home/simran/Desktop/OCRDEMO/Templates/form","w")
f.write("\n".join(map(lambda x :str(x),boxes)))
'''
# close all open windows
#cv2.destroyAllWindows()