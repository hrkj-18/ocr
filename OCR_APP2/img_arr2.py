from PIL import Image                                                            
import numpy                                                                     
import glob
import os
import cv2
import pickle
from keras.models import model_from_yaml

import sys


def load_model(bin_dir):


imageFolderPath = '/home/nausheen/Desktop/OCR_APP/Images'
#imagePath = glob.glob(imageFolderPath + '/0001.png') 
#im_array = numpy.array( [numpy.array(Image.open(img).convert('L'), 'f') for img in imagePath] )
#im_arr1 = im_array.reshape(28,28).reshape(1,-1)
result_array = numpy.array([])
model = load_model("/home/nausheen/Desktop/OCR_APP/bin")
mapping = pickle.load(open('/home/nausheen/Desktop/OCR_APP/bin/mapping.p', 'rb'))
#sorted(glob.glob('*.png'))
imagePath = sorted(glob.glob(imageFolderPath + '/*.png')) 

im_array = numpy.array( [numpy.array(Image.open(img).convert('L'), 'f') for img in imagePath] )
for img in imagePath:
    
    x=numpy.array(Image.open(img).convert('L'), 'f')
    x = x.reshape(28,28).reshape(1,28,28,1)

    # reshape image data for use in neural network
   # x = x.reshape(1,28,28,1)

    # Convert type to float32
   # x = x.astype('float32')

    # Normalize to prevent issues with model
    x /= 255
    out = model.predict(x)
    response = {'prediction': chr(mapping[(int(numpy.argmax(out, axis=1)[0]))]),
                'confidence': str(max(out[0]) * 100)[:6]}

    print(out)
'''
i=0
while i<(len(glob.glob(imageFolderPath + '/*.png')) ):
	im_array[i].reshape(28,28).reshape(1,-1)
	result_array = numpy.append(result_array, im_array[i])
	#array.append(np.float32((im_array[i].reshape(28,28).reshape(1,-1)))
	
	i=i+1
for i  in range(len(result_array)):
	if(result_array[i]<=127):
		result_array[i]=255
	else:
		result_array[i]=0


result_array2=result_array.reshape(-1,784)
#print(result_array)
orig_stdout = sys.stdout
f = open('/home/nausheen/Desktop/OCR_APP/out.txt', 'w')
sys.stdout = f
i=0

while i< len(result_array2):
	print(result_array2[i])
	i=i+1
sys.stdout = orig_stdout
f.close()
os.system("sed -i 's/\./,/g' /home/nausheen/Desktop/OCR_APP/out.txt")
'''
#os.system('rm -rf /home/nausheen/Desktop/OCR_APP/Images && mkdir /home/nausheen/Desktop/OCR_APP/Images')
#numpy.append(im_arr, [im_array.reshape(28,28).reshape(1,-1)] )
#print(array)
