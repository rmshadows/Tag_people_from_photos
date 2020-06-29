# -*- coding: utf-8 -*-
'''
训练材料预处理，过滤掉多面孔、无面孔图片。
请将训练材料放在Prescreen文件夹中。
结构要求：
    -+-PersonA-+-1.jpg
     |         +-2.jpg
     |         +-...
     |
     +-PersonB-+-1.jpg
     |         +-2.jpg
     |         +-...
     |
     +-PersonC-+-1.jpg
               +-2.jpg
               +-...
'''

from PIL import Image
import psutil
import face_recognition
import os
from datetime import datetime
import threading
import time

SEE_ALL_FACES=False

#获取扩展名
def __fex(path): 
	ex=os.path.splitext(path)[1]
	return ex[1:]

#重命名
def __renameFile():
	dir = "./Prescreen"#./Prescreen目录
	folder = (os.listdir(dir))#显示预筛选文件夹下的人物文件夹#./Prescreen/*
	for person in folder:#./Prescreen/person
		personDir = "./Prescreen/"+person
		pic = (os.listdir(personDir))#./Prescreen/person/*
		for file in pic:#./Prescreen/person/xxx.jpg
			time=datetime.now()
			srcFile = dir + "/" + person +"/"+ file#./Prescreen/person/xxx.jpg
			#dst=./Prescreen/{人名}/{时间后面的秒数}.{扩展名}
			dstFile = dir + "/{0}/{1}.{2}".format(person,str(time)[17:],__fex(srcFile))
			try:
				os.rename(srcFile,dstFile)#重命名
			except Exception as e:
				print(e)
			else:
				pass
		pic = (os.listdir(personDir))#./Prescreen/person/*
		n = 1
		for file in pic:#./Prescreen/person/file
			srcFile = personDir + "/" + file#./Prescreen/person/xxx.jpg
			#dst=./Prescreen/person/{n}.{ext}
			dstFile = personDir + "/{0}.{1}".format(n,__fex(srcFile))
			try:
				os.rename(srcFile,dstFile)
			except Exception as e:
				print(e)
			else:
				pass
			n += 1

#Find faces in pictures
def __checkFaces(file):
	# Load the jpg file into a numpy array
	inputPic = file
	image = face_recognition.load_image_file(inputPic)

	# Find all the faces in the image using the default HOG-based model.
	# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
	# See also: find_faces_in_picture_cnn.py
	face_locations = face_recognition.face_locations(image)
	faceNum = len(face_locations)
	print("Found \033[1;33;40m{0}\033[0m: face(s) in \033[1;35;40m{1}\033[0m: photograph.".format(faceNum ,file), end = " ==> ")
	if(SEE_ALL_FACES):
		for face_location in face_locations:
			# Print the location of each face in this image
			top, right, bottom, left = face_location
			print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
			# You can access the actual face itself like this:
			face_image = image[top:bottom, left:right]
			pil_image = Image.fromarray(face_image)
			pil_image.show()
	return faceNum

#MainX
def filePrescreen():
	print("Prescreen Start......\n")
	__renameFile()
	dir = "./Prescreen"
	folder = (os.listdir(dir))#./Prescreen/*
	for person in folder:#./Prescreen/person/
		personDir = "./Prescreen/"+person#./Prescreen/person/
		pic = (os.listdir(personDir))#./Prescreen/person/*
		if len(pic)>=20:#./Prescreen/person/下的图片20张以上
			taskNum = int(len(pic)/4)
			taskLef = len(pic)%4
			# 创建新线程
			thread1 = __TaskSubmit("1", pic[0:taskNum],person)
			thread2 = __TaskSubmit("2", pic[taskNum:taskNum*2],person)
			thread3 = __TaskSubmit("3", pic[taskNum*2:taskNum*3],person)
			thread4 = __TaskSubmit("4", pic[taskNum*3:taskNum*4],person)
			if taskLef==0:
				thread1.start()
				thread2.start()
				thread3.start()
				thread4.start()
				thread1.join()
				thread2.join()
				thread3.join()
				thread4.join()
			else:
				thread5 = __TaskSubmit("5", pic[taskNum*4:taskNum*4+taskLef],person)
				thread1.start()
				thread2.start()
				thread3.start()
				thread4.start()
				thread5.start()
				thread1.join()
				thread2.join()
				thread3.join()
				thread4.join()
				thread5.join()
		else:
			for file in pic:#./Prescreen/person/xxx.jpg
				time=datetime.now()#获取当前时间
				srcFile = personDir + "/" + file #"./Prescreen/"+person+ "/" +file
				if __checkFaces(srcFile)!=1:#如果脸的数量不是一的不要
					#./Prescreen/person/rm{time}
					dstFile = personDir + "/rm{0}".format(str(time)[17:])
				else:
					#./Prescreen/person/1F{时间}.{扩展名}
					dstFile = personDir + "/1F{0}.{1}".format(str(time)[17:],__fex(srcFile))
				try:
					os.rename(srcFile,dstFile)
				except Exception as e:
					print(e)
				else:
					pass
	__rmFiles()

def doTask(who,person):
	for f in who:#f=(xxx.jpg)
		time=datetime.now()#获取当前时间
		srcFile = "./Prescreen/{0}/{1}".format(person,f)#./Prescreen/{person}/{xxx.jpg}
		if __checkFaces(srcFile)!=1:
			#./Prescreen/person/rm{}{}
			dstFile = "./Prescreen/{0}/rm{1}.{2}".format(person,str(time)[17:],__fex(srcFile))
		else:
			dstFile = "./Prescreen/{0}/1F{1}.{2}".format(person,str(time)[17:],__fex(srcFile))
		try:
			os.rename(srcFile,dstFile)
		except Exception as e:
			print(e)
		else:
			pass

class __TaskSubmit (threading.Thread):
	def __init__(self,id ,who,person):
		threading.Thread.__init__(self)
		self.id = id
		self.who = who
		self.person = person
	def run(self):
		print ("开始线程：" + self.id)
		doTask(self.who,self.person)
		print ("退出线程：" + self.id)

def __rmFiles():
	print("\nDelete files...")
	dir = "./Prescreen"
	folder = (os.listdir(dir))#显示预筛选文件夹下的人物文件夹#./Prescreen/*
	for person in folder:#./Prescreen/person
		try:
			#rm ./Prescreen/{person}/rm*
			commandInput = 'rm ./Prescreen/' + person + "/rm*"
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("REMOVE FILE ERROR.")

def __killPro(second,pro):
	time.sleep(second)
	print("展示时间："+str(second)+"秒")
	for proc in psutil.process_iter():  # 遍历当前process
		if proc.name() == pro:  # 如果process的name是display
			proc.kill()  # 关闭该process

if __name__ == "__main__":
	#True是显示识别出的图像
	SEE_ALL_FACES=True
	filePrescreen()
	print("\n\033[5;31;40m训练材料预处理结束，请进行人工复审。下面如果有报错，请忽略。\033[0m\n")
	if SEE_ALL_FACES:
		#延时5秒
		__killPro(5,"display")
		SystemExit()
	print("\nFinish.")