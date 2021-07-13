from flask import Flask, request, jsonify,render_template
import os
import subprocess
from firebase import firebase
import pyrebase
import base64
import json
import webbrowser
import urllib
import glob
import cv2
import PyPDF2
import sys
from PIL import Image, ImageChops
import numpy as np
import requests 
import tabula
import lineseg
import textseg
import char_binarize
import char_padding
import read_single
import draw
import read
import roi2
import upload_text_files
from gtts import gTTS
from matplotlib import pyplot as plt
from flask_mysqldb import MySQL
import pymysql
from flask.ext.mysqldb import MySQL
import time	
import datetime

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
# conn = pymysql.connect(host='local',user='root',password='')
# mysql = MySQL(app)
# connection = 
# cur = mysql.connection.cursor()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'auth'
app.config['MYSQL_HOST'] = '127.168.1.1'
ts = time.time()
mysql = MySQL(app)
# mysql.init_app(app)

@app.route('/filename', methods = ["GET","POST"])
def filename():
	# conn = mysql.connector.connect(host = "127.168.1.1", user = "root", password = "", database= "auth") 
	# con = mysql.connection()
	cur = mysql.connection.cursor()
	# cur.execute('''SELECT * FROM users''')
	filename = request.form.get('filename')
	# return filename
	data = request.form.get('data')
	# return data
	user = user_loggedin
	return user
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return st
	cur.execute("INSERT into text_files values('" + filename + "','" + st + "','" + user + "','" + data + "')")
	con.commit()
	return	"Data Entered"	
	# return str(rv)

@app.route('/sign_up_ctrl', methods = ["GET","POST"])
def sign_up_ctrl():
	
	cur = mysql.connection.cursor()
	
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')
	user_loggedin  = username
	cur.execute("""INSERT into users values(%s,%s,%s)""", (username,email,password))
	mysql.connection.commit()
	
	return render_template('index.html')


@app.route('/login_ctrl', methods = ["GET","POST"])
def login_ctrl():
	
	cur = mysql.connection.cursor()
	
	usrname = request.form.get('username')
	global user_loggedin
	user_loggedin = usrname
	password = request.form.get('password')
	query = "SELECT * FROM users where username ='" + usrname + "' and  password='" + password +"'"
	duser = cur.execute(query)
	if '1' == str(duser):
		return render_template('index.html')
	else:
		return render_template('login.html')
	cur.execute("""INSERT into users values(%s,%s,%s)""", (username,email,password))
	mysql.connection.commit()
	
	return render_template('index.html')	



@app.route('/', methods = ["GET","POST"])
def index():
	return render_template('index.html')	
	
@app.route('/select', methods = ["GET","POST"])
def select():
	return render_template('upload.html')	

@app.route('/login', methods = ["GET","POST"])
def login():
	return render_template('login.html')	



@app.route('/pdf_to_word_result', methods = ["POST"])
def pdf_to_word_result():
	
	target = os.path.join(APP_ROOT, 'pdfs/')
	print(target)
	if not os.path.isdir(target):
		os.mkdir(target)
		print(request.files.getlist("file"))
	for upload in request.files.getlist("file"):
		print(upload)
		print("{} is the file name".format(upload.filename))
		filename = 'outputGenerated.pdf'
		# This is to verify files are supported
		ext = os.path.splitext(filename)[1]
		if ext == ".pdf":
		    print("File supported moving on...")
		else:
		    render_template("Error.html", message="Files uploaded are not supported...")
		destination = "/".join([target, filename])
		print("Accept incoming file:", filename)
		print("Save it to:", destination)
		upload.save(destination)
		

	pdfFileObj = open('/home/abid/Android_Projects/Android_and_Web/pdfs/outputGenerated.pdf', 'rb')
	# df = tabula.read_pdf('/home/abid/Android_Projects/Android_and_Web/pdfs/'+upload.filename)
	# tabula.convert_into('/home/abid/Android_Projects/Android_and_Web/pdfs/'+upload.filename,'output.csv',output_format='csv')
	# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
	# # printing number of pages in pdf file
	# n=pdfReader.numPages
	# #redirect output to file
	# orig_stdout = sys.stdout
	# f=open("/home/abid/Android_Projects/Android_and_Web/pdfs/pdf.txt","w")
	# sys.stdout = f
	# for i in range(0,n):
	# # creating a page object
	# 	pageObj = pdfReader.getPage(i)
	# 	print(pageObj.extractText())

	# sys.stdout = orig_stdout
	# f.close()
	 
	# # closing the pdf file object
	# pdfFileObj.close()
	os.system('pdftotext -layout /home/abid/Android_Projects/Android_and_Web/pdfs/outputGenerated.pdf /home/abid/Android_Projects/Android_and_Web/pdfs/outputGenerated.doc')
	
	# with open ("/home/abid/Android_Projects/Android_and_Web/pdfs/outputGenerated.txt", "r") as myfile:
	return "File downloaded"
	# return render_template('')	


def black_and_white(input_image_path,
    output_image_path):
   color_image = Image.open(input_image_path)
   bw = color_image.convert('L')
   bw.save(output_image_path)



@app.route('/retrive', methods = ['GET','POST'])
def retrive():	
	firebase1 = firebase.FirebaseApplication('https://friendlychat-3d8f7.firebaseio.com/imgPath/', None)
	result = firebase1.get('/imgPath', None)
	print(type(result))
	for i in result:
		for k in result[i]:
			imageurl = result[i][k]
	print(imageurl)

	# for k in result.items():
	# 	print(k);

	# return jsonify({'ans':result})
	# webbrowser.open(result)		
	r = requests.get(imageurl, allow_redirects=True)
	open('google.jpeg', 'wb').write(r.content)
	
	# col = Image.open("google.jpeg")
	# gray = col.convert('L')
	# bw = gray.point(lambda x: 0 if x<128 else 255, '1')
	# bw.save("result_bw.jpeg")
	
	
	# img = cv2.imread('google.jpeg',0)
	# ret,thresh=cv2.threshold(img, 100, 255, cv2.THRESH_OTSU)

	# cv2.imshow('image',thresh)
	# cv2.waitKey(1000)
	# cv2.destroyAllWindows()
	# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# cv2.imwrite('google1.jpeg',thresh)
	
	size = (700,700)

	image = Image.open('google.jpeg')
	image.thumbnail(size, Image.ANTIALIAS)
	image_size = image.size
	thumb = image.crop( (0, 0, size[0], size[1]) )

	offset_x = max( (size[0] - image_size[0]) // 2, 0 )
	offset_y = max( (size[1] - image_size[1]) // 2, 0 )

	image = ImageChops.offset(thumb, offset_x, offset_y)
	thumb.save('cropped.jpg')
	black_and_white('cropped.jpg',
        'bw_cropped.jpg')

	lineseg.Lineseg()
	textseg.Textseg()
	# cv2.destroyWindow("Detected text")
	char_padding.Char_padding()
	print('charpad')
	char_binarize.Char_binarize()
	print('charbin')
	cv2.destroyWindow("bw")
	read_single.Read()
	with open ("out.txt", "r") as myfile:
		data=myfile.readlines()
	temp = open('out.txt','r').read()
	language = 'en'

	# myobj = gTTS(text=data, lang=language, slow=False)

	# myobj.save("welcome.mp3")
	 
	# # Playing the converted file
	# os.system("mpg321 welcome.mp3")
	# return temp
	# result = "Abid  Harsh Vishal Simran Riya Nausheen"
	return render_template("retrive.html",result = data)
	# open('google.jpeg', 'wb').write(r.content)

	# return ("Image Downloaded")

@app.route('/template_match', methods = ["GET","POST"])
def template_match():
	firebase1 = firebase.FirebaseApplication('https://friendlychat-3d8f7.firebaseio.com/imgPath/', None)
	result = firebase1.get('/imgPath', None)
	print(type(result))
	for i in result:
		for k in result[i]:
			imageurl = result[i][k]
	print(imageurl)

	# for k in result.items():
	# 	print(k);

	# return jsonify({'ans':result})
	# webbrowser.open(result)		
	r = requests.get(imageurl, allow_redirects=True)
	open('google.jpeg', 'wb').write(r.content)
	
	# col = Image.open("google.jpeg")
	# gray = col.convert('L')
	# bw = gray.point(lambda x: 0 if x<128 else 255, '1')
	# bw.save("result_bw.jpeg")
	
	
	# img = cv2.imread('google.jpeg',0)
	# ret,thresh=cv2.threshold(img, 100, 255, cv2.THRESH_OTSU)

	# cv2.imshow('image',thresh)
	# cv2.waitKey(1000)
	# cv2.destroyAllWindows()
	# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# cv2.imwrite('google1.jpeg',thresh)
	draw.Draw();
	roi2.Roi2();
	read.Read();
	size = (700,700)

	image = Image.open('google.jpeg')
	image.thumbnail(size, Image.ANTIALIAS)
	image_size = image.size
	thumb = image.crop( (0, 0, size[0], size[1]) )

	offset_x = max( (size[0] - image_size[0]) // 2, 0 )
	offset_y = max( (size[1] - image_size[1]) // 2, 0 )

	image = ImageChops.offset(thumb, offset_x, offset_y)
	thumb.save('cropped.jpg')
	black_and_white('cropped.jpg',
        'bw_cropped.jpg')

	lineseg.Lineseg()
	textseg.Textseg()
	# cv2.destroyWindow("Detected text")
	char_padding.Char_padding()
	print('charpad')
	char_binarize.Char_binarize()
	print('charbin')
	# cv2.destroyWindow("bw")
	# read_single.Read()

	with open ("out.txt", "r") as myfile:
		data=myfile.readlines()
	temp = open('out.txt','r').read()

	# return temp
	# result = "Abid  Harsh Vishal Simran Riya Nausheen"
	return render_template("retrive.html",result = data)
	# open('google.jpeg', 'wb').write(r.content)

	# return ("Image Downloaded")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8098, debug=True)
