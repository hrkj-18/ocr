from PIL import Image                                                                                                                                 
import glob
import os
import cv2
from scipy.misc import imsave, imread, imresize
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#from keras.layers import Conv2D, MaxPooling2D, Convolution2D, Dropout, Dense, Flatten, LSTM
from keras.models import Sequential, save_model, load_model
from keras.utils import np_utils
from scipy.io import loadmat
import pickle
import argparse
import keras
import numpy as np
import argparse
from keras.models import model_from_yaml
import re
import base64
import pickle
import h5py

def load_model(bin_dir):
    
	'''
	Load model from .yaml and the weights from .h5

	    Arguments:
	        bin_dir: The directory of the bin (normally bin/)

	    Returns:
	        Loaded model from file

	'''
	# load YAML and create model
	yaml_file = open('%s/model.yaml' % bin_dir, 'r')
	loaded_model_yaml = yaml_file.read()
	yaml_file.close()
	model = model_from_yaml(loaded_model_yaml)

	# load weights into new model
	model.load_weights('%s/model.h5' % bin_dir)
	return model

bin_dir = r'/home/simran/Desktop/OCRDEMO/char_bin'
model  = load_model(bin_dir)
#model = load_model('/home/simran/Keras_Alphabet_Model.h5')


dic1 = {0:'0',
       1:'1',
       2:'2',
       3:'3',
       4:'4',
       5:'5',
       6:'6',
       7:'7',
       8:'8',
       9:'9',
	10:'A',
       11:'B',
       12:'C',
       13:'D',
       14:'E',
       15:'F',
       16:'G',
       17:'H',
       18:'I',
       19:'J',
       20:'K',
       21:'L',
       22:'M',
       23:'N',
       24:'O',
       25:'P',
       26:'Q',
       27:'R',
       28:'S',
       29:'T',
       30:'U',
       31:'V',
       32:'W',
       33:'X',
       34:'Y',
       35:'Z',
       36:'a',
       37:'b',
       38:'c',
       39:'d',
       40:'e',
       41:'f',
       42:'g',
       43:'h',
       44:'i',
       45:'j',
       46:'k',
       47:'l',
       48:'m',
       49:'n',
       50:'o',
       51:'p',
       52:'q',
       53:'r',
       54:'s',
       55:'t',
       56:'u',
       57:'v',
       58:'w',
       59:'x',
       60:'y',
       61:'z'
      }

	   
dic2 = {0:'A',
       1:'B',
       2:'C',
       3:'D',
       4:'E',
       5:'F',
       6:'G',
       7:'H',
       8:'I',
       9:'J',
       10:'K',
       11:'L',
       12:'M',
       13:'N',
       14:'O',
       15:'P',
       16:'Q',
       17:'R',
       18:'S',
       19:'T',
       20:'U',
       21:'V',
       22:'W',
       23:'X',
       24:'Y',
       25:'Z'
       }



imageFolderPath = '/home/simran/Desktop/OCRDEMO/Images'
n=os.popen('find Images -type d | wc -l').read()
n = int(n)
#print(n)
n=n-1
Lines = []

for i in range(0,n):
	imagePath = sorted(glob.glob(imageFolderPath +'/'+str(i).zfill(4)+ '/*.jpg')) 
	line = np.array( [np.array(Image.open(img).convert('L'), 'f') for img in imagePath] )
	if(np.shape(line)[0]!=0):
		#print(line)
		Lines.append(line)
#print(Lines)
for i in range (len(Lines)):
	Lines[i]=np.reshape(Lines[i],(-1,1,28,28,1))
	#Lines[i]=np.reshape(Lines[i],(-1,1,784))
	Lines[i]=Lines[i].astype('float32')
	Lines[i] /= 255
	#print(np.shape(Lines[i]))


out_string=[[]]
h=0
output_line=[]
output_max=[]
for k in range(len(Lines)):
	for m in range(len(Lines[k])):
		#Lines[k][m].reshape(1,28,28,1)
		#print(np.shape(Lines[k][m]))
		#h=h+1
		#print(h)
		#output=model.predict_proba(Lines[k][m])
		#output=model.predict(Lines[k])
		output=model.predict_classes(Lines[k][m])
		output_line.append(output)
	output_max.append(output_line)
	#output_line[k]=[dic.get(n, n) for n in output_line]
	#print(output_line)
	output_line=[]

#print(output_max)

goat=[]
goat_real=[]
for i in range(len(output_max)):
	for j in range(len(output_max[i])):
		goat.append(output_max[i][j][0])
	goat_real.append(goat)
	goat=[]
#print(goat_real)

new_goat=[]
for i in range(len(goat_real)):
    new_goat.append([dic2.get(n, n) for n in goat_real[i]])
#print(new_goat)

for i in range(len(new_goat)):
    for j in range(len(new_goat[i])):
        new_goat[i]=''.join(new_goat[i])

#print(new_goat)
'''
for i in range(len(new_goat)):
	print(new_goat[i])
'''
print(new_goat)

orig_stdout = sys.stdout
f = open('/home/simran/Desktop/OCRDEMO/out.txt', 'w')
sys.stdout = f
i=0


for i in range(len(new_goat)):
	print(new_goat[i])
	print("\n")
sys.stdout = orig_stdout
f.close()


#Lines.append(line)
#print(Lines)