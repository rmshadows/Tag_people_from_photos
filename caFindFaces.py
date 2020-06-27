# -*- coding: utf-8 -*-
'''
将需要识别的人物图片分类成无面孔、单人、多人并分配到临时目录。
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
	dir = "./INPUT_PIC"
	pic = (os.listdir(dir))
	for file in pic:
		time=datetime.now()
		srcFile = dir + "/" + file
		dstFile = dir + "/{0}.{1}".format(time,fex(srcFile))
		try:
			os.rename(srcFile,dstFile)
		except Exception as e:
			print(e)
			print("Rename file fail.")
		else:
			#print("Rename file success.")
			pass
	pic = (os.listdir(dir))
	n = 1
	for file in pic:
		srcFile = dir + "/" + file
		dstFile = dir + "/{0}.{1}".format(n,fex(srcFile))
		try:
			os.rename(srcFile,dstFile)
		except Exception as e:
			print(e)
			print("Rename file fail.")
		else:
			#print("Rename file success.")
			pass
		n += 1
	print("Renamed.")

def checkFaces(file):
	# Load the jpg file into a numpy array
	inputPic = "./INPUT_PIC/"+file
	image = face_recognition.load_image_file(inputPic)

	# Find all the faces in the image using the default HOG-based model.
	# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
	# See also: find_faces_in_picture_cnn.py
	face_locations = face_recognition.face_locations(image)
	faceNum = len(face_locations)
	print("Found {0} face(s) in {1} photograph.".format(faceNum ,file), end = " ==> ")

	for face_location in face_locations:
		# Print the location of each face in this image
		top, right, bottom, left = face_location
		print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

		'''
		# You can access the actual face itself like this:
		face_image = image[top:bottom, left:right]
		pil_image = Image.fromarray(face_image)
		pil_image.show()
		'''
	return faceNum

def copyFiles():
	#print("\n")
	try:
		commandInput = 'cp ./INPUT_PIC/0* ./tempNone'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("No None fece")
	try:
		commandInput = 'cp ./INPUT_PIC/1* ./tempSingle'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("No Singleface")
	try:
		commandInput = 'cp ./INPUT_PIC/MF* ./tempMore'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("No Morefaces")

def fileCtrl():
	print("File Control Start")
	dir = "./INPUT_PIC"
	pic = (os.listdir(dir))

	if len(pic)>=8:
		taskNum = int(len(pic)/4)
		taskLef = len(pic)%4
		ga=pic[0:taskNum]
		gb=pic[taskNum:taskNum*2]
		gc=pic[taskNum*2:taskNum*3]
		gd=pic[taskNum*3:taskNum*4]

		thread1 = TaskSubmit("1", ga)
		thread2 = TaskSubmit("2", gb)
		thread3 = TaskSubmit("3", gc)
		thread4 = TaskSubmit("4", gd)
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
			gf=pic[taskNum*4:taskNum*4+taskLef]
			thread5 = TaskSubmit("5",gf)
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
		n=1
		for file in pic:
			time=datetime.now()#获取当前时间
			srcFile = dir + "/" + file
			if checkFaces(file)>=2:
				print(fex(srcFile))
				dstFile = dir + "/MF{0}.{1}".format(time,fex(srcFile))
			else:
				dstFile = dir + "/{0}F{1}.{2}".format(checkFaces(file),time,fex(srcFile))
			try:
				os.rename(srcFile,dstFile)
			except Exception as e:
				print(e)
				print("Rename file fail.")
			else:
				print("Rename file success.")
			n+=1
			print("\033[1;36;40m{} of {}\033[0m".format(n,len(pic)))

class TaskSubmit (threading.Thread):
	def __init__(self,id ,listIn):
		threading.Thread.__init__(self)
		self.id = id
		self.listIn = listIn
	def run(self):
		print ("开始线程：" + self.id)
		doTask(self.listIn)
		print ("退出线程：" + self.id)

def doTask(listIn):
	for x in listIn:
		time=datetime.now()#获取当前时间
		srcFile = "./INPUT_PIC/{0}".format(x)
		if checkFaces(x)>=2:
			dstFile = "./INPUT_PIC/MF{0}.{1}".format(time,fex(srcFile))
		else:
			dstFile = "./INPUT_PIC/{0}F{1}.{2}".format(checkFaces(x),time,fex(srcFile))
		try:
			os.rename(srcFile,dstFile)
		except Exception as e:
			print(e)
			print("Rename file fail.")
		else:
			#print("Rename file success.")
			pass
		#print("\033[1;36;40m{} of {}\033[0m".format(n,len(pic)))

def FindFaces():
	renameFile()
	fileCtrl()
	copyFiles()

if __name__ == "__main__":
	FindFaces()
