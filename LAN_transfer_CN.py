# -*- coding: utf-8 -*-
from flask import Flask,send_from_directory,request,redirect,url_for
import os,psutil

path=os.getcwd()
app = Flask(__name__) 
*ipdict,=psutil.net_if_addrs().values()

ip=[]
if path[1]==':':
	command='dir /b'
	D='\\'
	B=' '
	for i in ipdict[:2]:
		ip+='http://'+i[1][1]+':5000\n',
else:
	command='ls'
	D='/'
	B='\ '
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

def html(s):
	return '<a href="{}">{}<a/>'.format(s,s)

def main(dirpath):
	dirpath1=dirpath.replace('|',D).replace(' ',B)
	if D=='\\':
		files=os.popen(command+' '+'"'+dirpath1+'"').readlines()
	else:
		files=os.popen(command+' '+dirpath1).readlines()
		
	for i in range(len(files)):
		files[i]=files[i][:-1]
		if os.path.isdir(dirpath1+D+files[i]):files[i]+='/'

	return '<h3>文件列表</h3>'+'<br/>'.join(map(html,files))+f'''<br/><h3>文件上传</h3>
    <form action="/{dirpath}upload" enctype="multipart/form-data" method="POST">
        <input type="file" name="file"><br/>
        <input type="submit" value="上传">
    </form>'''


@app.route('/')
def index():
	files=os.popen(command).readlines()
	for i in range(len(files)):
		files[i]=files[i][:-1]
		if os.path.isdir(files[i]):files[i]+='/'

	return '<h3>文件列表</h3>'+'<br/>'.join(map(html,files))+'''<br/><h3>文件上传</h3>
    <form action="/upload" enctype="multipart/form-data" method="POST">
        <input type="file" name="file"><br/>
        <input type="submit" value="上传">
    </form>'''

@app.route('/<filename>') 
def get_file(filename):
	return send_from_directory(path,filename) 

@app.route('/<filename>/') 
def get_dir(filename):
	return main(filename)

@app.route('/<dirpath>/<filename>') 
def get_file1(dirpath,filename):
	dirpath=dirpath.replace('|',D)
	return send_from_directory(dirpath,filename) 

@app.route('/<dirpath1>/<dirpath2>/')
def redict(dirpath1,dirpath2):
	return redirect('/'+dirpath1+'|'+dirpath2+'/')

@app.route('/<dirpath>upload',methods=['POST','GET'])
def upload(dirpath):
	dirpath=dirpath.replace('|',D)
	if request.method=='POST':
		f=request.files['file']
		if f:
			filename0=f.filename.replace('/','').replace(':','').replace('<','').replace('>','').replace('*','').replace('?','').replace('|','').replace('"','')
			if '\\' in filename0:
				filename1 = 'u_'+filename0[filename0.rindex('\\')+1:]
				filename='u_'+filename0[filename0.rindex('\\')+1:]
			else:
				filename1 = 'u_'+filename0
				filename='u_'+filename0
			n=0
			while os.path.isfile(dirpath+D+filename):
				n+=1
				filename='('+str(n)+')'+filename1
			print('上传文件:',filename)
			f.save(dirpath+D+filename)
			return f'<h2>上传成功! 请返回上一页面刷新查看!<br/>文件名: {filename}</h2>'
		else:
			return '<h2>未选择任何文件!请返回上一页面选择需要上传的文件!</h2>'
	if request.method=='GET':
		return '<h2>请在主页选择需要上传的文件!</h2>'

if __name__ == '__main__': 
	app.run(host='0.0.0.0')
	