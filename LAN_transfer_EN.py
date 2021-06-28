# -*- coding: utf-8 -*-
from flask import Flask,send_from_directory,request,redirect,url_for
import os,sys,socket,psutil

app = Flask(__name__) 
path=os.getcwd()
*ipdict,=psutil.net_if_addrs().values()
ip=[]

if path[1]==':':
	command='{} && cd {} && dir /b'.format(path[:2],path)
	for i in ipdict[:2]:
		ip+='http://'+i[1][1]+':5000\n',
else:
	command='cd {} && ls'.format(path)
	for i in ipdict[1:3]:
		ip+='http://'+i[0][1]+':5000\n',

print()
print('--------------------------------------------------------------------')
print('WARN: !!! DO NOT CLOSE THIS WINDOW DURING USE !!!')
print()
print('PATH：')
print(path)
print()
print("Opne the following address in browser by any device in LAN:")
print('',*ip,end='')
print('--------------------------------------------------------------------')
print()
@app.route('/')
def main():
	if path[1]==':':
		command='{} && cd {} && dir /b'.format(path[:2],path)
	else:
		command='cd {} && ls'.format(path)
	files=os.popen(command).readlines()
	def html(s):
		return '<a href="{}">{}<a/>'.format(s,s)

	return '<h3>Index of/</h3>'+'<br/>'.join(map(html,files))+'''<br/><h3>Upload</h3>
    <form action="upload" enctype="multipart/form-data" method="POST">
        <input type="file" name="file"><br/>
        <input type="submit" value="upload">
    </form>'''

@app.route('/<filename>') 
def get_image(filename): 
	return send_from_directory(path,filename) 

@app.route('/upload',methods=['POST','GET'])
def upload():
	if request.method=='POST':
		f=request.files['file']
		if f:
			f.save(f.filename)
			return '<h1>Success! Please return to previous page and refresh!</h1>'
		else:
			return '<h1>No file selected! Return to previous page and select a file!</h1>'
	if request.method=='GET':
		return '<h1>Please visit home page.</h1>'

if __name__ == '__main__': 
	app.run(host='0.0.0.0')
	
