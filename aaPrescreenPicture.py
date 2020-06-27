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

#from PIL import Image
import face_recognition
import os
from datetime import datetime
import threading

def fex(path): 
	ex=os.path.splitext(path)[1]
	return ex[1:]

def renameFile():
	dir = "./Prescreen"
	folder = (os.listdir(dir))#显示预筛选文件夹下的人物文件夹
	for person in folder:
		personDir = "./Prescreen/"+person
		pic = (os.listdir(personDir))
		#len(pic)
		for file in pic:
			time=datetime.now()
			srcFile = dir + "/" + person +"/	"+ file
			dstFile = dir + "/{0}/{1}.{2}".format(person,time,fex(srcFile))
			try:
				os.rename(srcFile,dstFile)
			except Exception as e:
				print(e)
				print("Rename file fail.")
			else:
				#print("Rename file success.")
				pass
		pic = (os.listdir(personDir))
		n = 1
		for file in pic:
			srcFile = personDir + "/" + file
			dstFile = personDir + "/{0}.{1}".format(n,fex(srcFile))
			try:
				os.rename(srcFile,dstFile)
			except Exception as e:
				print(e)
				print("Rename file fail.")
			else:
				print("Rename file success.")
			n += 1

def checkFaces(file):
	# Load the jpg file into a numpy array
	inputPic = file
	image = face_recognition.load_image_file(inputPic)

	# Find all the faces in the image using the default HOG-based model.
	# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
	# See also: find_faces_in_picture_cnn.py
	face_locations = face_recognition.face_locations(image)
	faceNum = len(face_locations)
	print("Found {0} face(s) in {1} photograph.".format(faceNum ,file), end = " ==> ")
	'''
	for face_location in face_locations:
		# Print the location of each face in this image
		top, right, bottom, left = face_location
		print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

		# You can access the actual face itself like this:
		face_image = image[top:bottom, left:right]
		pil_image = Image.fromarray(face_image)
		pil_image.show()
	'''
	return faceNum

def filePrescreen():
	print("Prescreen Start")
	renameFile()
	dir = "./Prescreen"
	folder = (os.listdir(dir))
	for person in folder:
		personDir = "./Prescreen/"+person
		pic = (os.listdir(personDir))
		if len(pic)>=20:
			taskNum = int(len(pic)/4)
			taskLef = len(pic)%4
			# 创建新线程
			thread1 = TaskSubmit("1", pic[0:taskNum],person)
			thread2 = TaskSubmit("2", pic[taskNum:taskNum*2,person])
			thread3 = TaskSubmit("3", pic[taskNum*2:taskNum*3],person)
			thread4 = TaskSubmit("4", pic[taskNum*3:taskNum*4],person)
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
				thread5 = TaskSubmit("5", pic[taskNum*4:taskNum*4+taskLef],person)
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
			for file in pic:
				time=datetime.now()#获取当前时间
				srcFile = personDir + "/" + file  #"./Prescreen/"+person+ "/" +file
				if checkFaces(srcFile)!=1:
					dstFile = personDir + "/rm{0}".format(time)
				else:
					dstFile = personDir + "/1F{0}.{1}".format(time,fex(srcFile))
				try:
					os.rename(srcFile,dstFile)
				except Exception as e:
					print(e)
					print("Rename file fail.")
				else:
					print("Rename file success.")
	rmFiles()

def doTask(who,person):
	for f in who:
		time=datetime.now()#获取当前时间
		srcFile = "./Prescreen/{0}/{1}".format(person,f)
		if checkFaces(srcFile)!=1:
				dstFile = "./Prescreen/{0}/rm{1}.{2}".format(person,time,fex(srcFile))
		else:
			dstFile = "./Prescreen/{0}/1F{1}.{2}".format(person,time,fex(srcFile))
		try:
			os.rename(srcFile,dstFile)
		except Exception as e:
			print("Rename file fail.")
			print(e)
		else:
			print("Rename file success.")

class TaskSubmit (threading.Thread):
	def __init__(self,id ,who,person):
		threading.Thread.__init__(self)
		self.id = id
		self.who = who
		self.person = person
	def run(self):
		print ("开始线程：" + self.id)
		doTask(self.who,self.person)
		print ("退出线程：" + self.id)

def rmFiles():
	print("\nDelete files...")
	dir = "./Prescreen"
	folder = (os.listdir(dir))#显示预筛选文件夹下的人物文件夹
	for person in folder:
		try:
			commandInput = 'rm ./Prescreen/' + person + "/rm*"
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("REMOVE FILE ERROR.")

if __name__ == "__main__":
	filePrescreen()
