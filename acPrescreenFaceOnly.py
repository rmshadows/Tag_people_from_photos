# -*- coding: utf-8 -*-
'''
训练材料预处理，保存成单个脸部图片
只有当你的训练材料中有很多多人照片才这么做
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
WINDOWS=os.sep=="\\"
SS=os.sep
ERROR_INFO=""

def TIS(n):
	time.sleep(n)

#获取扩展名
def __fex(path): 
	ex=os.path.splitext(path)[1]
	return ex[1:]

#重命名
def __renameFile():
	dir = ".{0}Prescreen".format(SS)#./Prescreen目录
	folder = (os.listdir(dir))#显示预筛选文件夹下的人物文件夹#./Prescreen/*
	for person in folder:#./Prescreen/person
		personDir = ".{0}Prescreen{1}".format(SS,SS)+person
		pic = (os.listdir(personDir))#./Prescreen/person/*
		for file in pic:#./Prescreen/person/xxx.jpg
			time=datetime.now()
			srcFile = dir + SS + person + SS + file#./Prescreen/person/xxx.jpg
			#dst=./Prescreen/{人名}/{时间后面的秒数}.{扩展名}
			TI=str(time)[17:]
			dstFile = dir + SS + "{0}{1}{2}.{3}".format(person,SS,TI.replace(" ",""),__fex(srcFile))
			try:
				os.rename(srcFile,dstFile)#重命名
			except Exception as e:
				print(e)
			else:
				pass
		pic = (os.listdir(personDir))#./Prescreen/person/*
		n = 1
		for file in pic:#./Prescreen/person/file
			srcFile = personDir + SS + file#./Prescreen/person/xxx.jpg
			#dst=./Prescreen/person/{n}.{ext}
			dstFile = personDir + SS + "{0}.{1}".format(n,__fex(srcFile))
			try:
				os.rename(srcFile,dstFile)
			except Exception as e:
				print(e)
			else:
				pass
			n += 1

#Find faces in pictures
def __checkFaces(file,person):
	global ERROR_INFO
	try:
		# Load the jpg file into a numpy array
		inputPic = file
		image = face_recognition.load_image_file(inputPic)
		# Find all the faces in the image using the default HOG-based model.
		# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
		# See also: find_faces_in_picture_cnn.py
		#CNN:
		#face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
		face_locations = face_recognition.face_locations(image)
		faceNum = len(face_locations)
		print("Found \033[1;33;40m{0}\033[0m: face(s) in \033[1;35;40m{1}\033[0m: photograph.".format(faceNum ,file), end = " ==> ")
		for face_location in face_locations:
			# Print the location of each face in this image
			top, right, bottom, left = face_location
			print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
			if (top-200<0):
				if (top-150<0):
					if (top-100<0):
						T=top
					else:
						T=top-100
				else:
					T=top-150
			else:
				T=top-200
			B=bottom+100
			if (left-100<0):
				L=left
			else:
				L=left-100
			R=right+100
			TIS(0.2)
			print(T,B,L,R)
			face_image = image[T:B, L:R]
			pil_image = Image.fromarray(face_image)
			if(SEE_ALL_FACES):
				pil_image.show()
			time=str(datetime.now())[17:]
			#.{/}Prescreen{/}{person}{/}FRS{time}
			pil_image.save(".{0}Prescreen{1}{2}{3}FRS{4}.{5}".format(SS,SS,person,SS,time,__fex(file)))
	except Exception as e:
		ERROR_INFO="{0}\n{1}".format(ERROR_INFO,e)
		print("\033[1;32;41m{0}\033[0m".format(e))
		raise e
	return faceNum

#MainX
def filePrescreen():
	print("Prescreen Start......\n")
	__renameFile()
	dir = ".{0}Prescreen".format(SS)
	folder = (os.listdir(dir))#./Prescreen/*
	for person in folder:#./Prescreen/person/
		personDir = ".{0}Prescreen{1}".format(SS,SS)+person#./Prescreen/person/
		pic = (os.listdir(personDir))#./Prescreen/person/*
		if (len(pic)>=20) & (not WINDOWS):#./Prescreen/person/下的图片20张以上
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
				srcFile = personDir + SS + file #"./Prescreen/"+person+ "/" +file
				if __checkFaces(srcFile,person)==0:
					#./Prescreen/person/rm{time}
					dstFile = personDir + SS +"rm{0}".format(str(time)[17:].replace(" ",""))
				else:
					#./Prescreen/person/1F{时间}.{扩展名}
					dstFile = personDir + SS +"1F{0}.{1}".format(str(time)[17:].replace(" ",""),__fex(srcFile))
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
		if __checkFaces(srcFile,person)==0:
			#./Prescreen/person/rm{}{}
			dstFile = "./Prescreen/{0}/rm{1}.{2}".format(person,str(time)[17:].replace(" ",""),__fex(srcFile))
		else:
			dstFile = "./Prescreen/{0}/1F{1}.{2}".format(person,str(time)[17:].replace(" ",""),__fex(srcFile))
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
		self.result="1"
	def run(self):
		print ("开始线程：" + self.id + " on stat " + self.result)
		doTask(self.who,self.person)
		self.result="0"
		print ("退出线程：" + self.id + " on stat " + self.result)

def __rmFiles():
	print("\nDelete files...")
	dir = ".{0}Prescreen".format(SS)
	folder = (os.listdir(dir))#显示预筛选文件夹下的人物文件夹#./Prescreen/*
	for person in folder:#./Prescreen/person
		if WINDOWS:
			try:
				#del .\Prescreen\{person}\rm*
				commandInput = 'del /S /Q .\\Prescreen\\' + person + "\\rm*"
				commandImplementation = os.popen(commandInput)
				print("Del...")
			except Exception as e:
				print(e)
			try:
				#del .\Prescreen\{person}\rm*
				commandInput = 'del /S /Q .\\Prescreen\\' + person + "\\1F*"
				commandImplementation = os.popen(commandInput)
				print("Del...")
			except Exception as e:
				print(e)
		else:
			try:
				#rm ./Prescreen/{person}/rm*
				commandInput = 'rm ./Prescreen/' + person + "/rm*"
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print("REMOVE FILE ERROR.")
			try:
				#rm ./Prescreen/{person}/rm*
				commandInput = 'rm ./Prescreen/' + person + "/1F*"
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
	#SEE_ALL_FACES=True
	filePrescreen()
	print("\033[1;32;41m{0}\033[0m".format(ERROR_INFO))
	print("\n\033[5;31;40m训练材料预处理结束，请进行人工复审。下面如果有报错，请忽略。\033[0m\n")
	if SEE_ALL_FACES:
		#延时5秒
		__killPro(5,"display")
		SystemExit()
	print("\nFinish.")
