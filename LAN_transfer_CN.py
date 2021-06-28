# -*- coding: utf-8 -*-
from flask import Flask,send_from_directory,request
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
print('-----------------------------------------------------------------------------')
print('说明: !!! 使用过程中请勿关闭此窗口 !!!')
print()
print('程序当前运行目录：')
print(path)
print()
print('局域网中任意设备浏览器打开以下http开头地址即可在程序运行目录下载或上传:')
print('',*ip,end='')
print('-----------------------------------------------------------------------------')
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

	return '<h3>文件列表</h3>'+'<br/>'.join(map(html,files))+'''<br/><h3>文件上传</h3>
    <form action="upload" enctype="multipart/form-data" method="POST">
        <input type="file" name="file"><br/>
        <input type="submit" value="上传">
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
			return '<h2>上传成功! 请返回上一页面刷新查看!</h2>'
		else:
			return '<h2>未选择任何文件!请返回上一页面选择需要上传的文件!</h2>'
	if request.method=='GET':
		return '<h2>请在主页选择需要上传的文件!</h2>'

if __name__ == '__main__': 
	app.run(host='0.0.0.0')
	
