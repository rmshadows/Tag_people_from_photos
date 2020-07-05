# -*- coding: utf-8 -*-
'''
虽然是10线程，但好像没四线程的快。
这个是我测试用的，本来下用for循环，循环定义参数，但是。。。没成功……放弃了。
'''
from math import sqrt
from sklearn import neighbors
from os import listdir
from os.path import isdir, join, isfile, splitext
import pickle
import face_recognition
from face_recognition import face_locations
from face_recognition.face_recognition_cli import image_files_in_folder
import threading
from datetime import datetime
import os
import Wait

WINDOWS=os.sep=="\\"
SS=os.sep
#修改这里显示详情
verbose=False

def __train(train_dir, model_save_path = "",verbose=False, n_neighbors = None, knn_algo = 'ball_tree' ):
	X = []
	y = []

	person = listdir(train_dir)
	if (len(person)>10)&(not WINDOWS):
		group = (int)(len(person)/10)
		left = len(person)%10
		g1 = person[0:group]
		g2 = person[group:group*2]
		g3 = person[group*2:group*3]
		g4 = person[group*3:group*4]
		g5 = person[group*4:group*5]
		g6 = person[group*5:group*6]
		g7 = person[group*6:group*7]
		g8 = person[group*7:group*8]
		g9 = person[group*8:group*9]
		g10 = person[group*9:group*10]
		if left == 0:
			pass
		else:
			g10 = g10+person[group*10:group*10+left]
		thread1 = TaskSubmit("1",train_dir,g1,31)
		thread2 = TaskSubmit("2",train_dir,g2,32)
		thread3 = TaskSubmit("3",train_dir,g3,33)
		thread4 = TaskSubmit("4",train_dir,g4,34)
		thread5 = TaskSubmit("5",train_dir,g5,35)
		thread6 = TaskSubmit("6",train_dir,g6,36)
		thread7 = TaskSubmit("7",train_dir,g7,37)
		thread8 = TaskSubmit("8",train_dir,g8,33)
		thread9 = TaskSubmit("9",train_dir,g9,31)
		thread10 = TaskSubmit("10",train_dir,g10,32)
		thread1.start()
		thread2.start()
		thread3.start()
		thread4.start()
		thread5.start()
		thread6.start()
		thread7.start()
		thread8.start()
		thread9.start()
		thread10.start()
		
		thread1.join()
		thread2.join()
		thread3.join()
		thread4.join()
		thread5.join()
		thread6.join()
		thread7.join()
		thread8.join()
		thread9.join()
		thread10.join()

		X = thread1.returnX()+thread2.returnX()+thread3.returnX()+thread4.returnX()+thread5.returnX()+thread6.returnX()+thread7.returnX()+thread8.returnX()+thread9.returnX()+thread10.returnX()
		y = thread1.returnY()+thread2.returnY()+thread3.returnY()+thread4.returnY()+thread5.returnY()+thread6.returnY()+thread7.returnY()+thread8.returnY()+thread9.returnY()+thread10.returnY()

	else:
		TASK = __calcTask(train_dir)
		n = 0
		num = 1
		for class_dir in listdir(train_dir):
			n += 1
			if verbose:
				print("\033[1;33;40m添加第{}个训练对象 \033[0m:\033[1;36;40m".format(n) + class_dir + "\033[0m")
			if not isdir(join(train_dir, class_dir)):
				print("continue.")
				continue
			for img_path in image_files_in_folder(join(train_dir, class_dir)):
				image = face_recognition.load_image_file(img_path)
				if verbose:
					print("\033[1;34;40m添加第({0}/{1})个文件 \033[0m:\033[1;38;40m".format(num,TASK) + img_path + "\033[0m")
				Wait.view(num,TASK,"31"," ")

				num+=1
				faces_bboxes = face_locations(image)
				if len(faces_bboxes) != 1:
					if verbose:
						print("\033[1;31;40mWARN：\033[0m image {} not fit for __training: {}".format(img_path, "didn't find a face" if len(faces_bboxes) < 1 else "found more than one face"))
					continue
				X.append(face_recognition.face_encodings(image, known_face_locations=faces_bboxes)[0])
				y.append(class_dir)

	if n_neighbors is None:
		n_neighbors = int(round(sqrt(len(X))))
		if verbose:
			print("Chose n_neighbors automatically as:", n_neighbors)

	knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
	knn_clf.fit(X, y)
	print("Generating...")
	if model_save_path != "":
		with open(model_save_path, 'wb') as f:
			pickle.dump(knn_clf, f)
	return knn_clf

def __calcTask(path):
	dir = listdir(path)
	task = 0
	for person in dir:
		subDir = path+SS+person
		num = len(listdir(subDir))
		task = task + num
	return task

def doTask(train_dir,listIn,id,color):
	X = []
	y = []
	T = 0
	temp=[]
	for x in listIn:
		T = T+len(listdir(join(train_dir,x)))
	n = 1
	for class_dir in listIn:#Person
		if verbose:
			print("\033[1;{0};40m线程-{1}-正在添加：{2}\033[0m:".format(color,id,class_dir))
		if not isdir(join(train_dir, class_dir)):#跳过目录
			continue
		for img_path in image_files_in_folder(join(train_dir, class_dir)):
			if verbose:
				print("-"+id+"-进度:({0}/{1})".format(n,T))
			Wait.view(n,T,color," ")
			n+=1
			image = face_recognition.load_image_file(img_path)
			faces_bboxes = face_locations(image)
			if len(faces_bboxes) != 1:
				continue
			X.append(face_recognition.face_encodings(image, known_face_locations=faces_bboxes)[0])
			y.append(class_dir)
	listIn.clear()
	temp.clear()
	listIn = X
	temp = y
	return listIn,temp

class TaskSubmit (threading.Thread):
	def __init__(self,id ,train_dir ,listIn ,color):
		threading.Thread.__init__(self)
		self.id = id
		self.train_dir = train_dir
		self.listIn = listIn
		self.color = color
	def returnX(self):
		try:
			return self.X
		except Exception:
			return None
	def returnY(self):
		try:
			return self.y
		except Exception:
			return None
	def run(self):
		if verbose:
			print ("开始线程：" + self.id + "\n")
		X,y = doTask(self.train_dir ,self.listIn,self.id,self.color)
		if verbose:
			print ("退出线程：" + self.id + "\n")
		self.X=X
		self.y=y

#mainX
def main(train_dir,model_save_path):
	print("\033[5;33;40m开始训练模型(10线程)....\033[0m\n")
	time=datetime.now()
	if WINDOWS:
		TI=str(time).replace(":","")
		knn_clf = __train(".\\FR_DATA\\"+train_dir+"\\",".\\KNN_MOD\\"+model_save_path+TI.replace(" ",""),verbose)
	else:
		knn_clf = __train("./FR_DATA/"+train_dir+"/","./KNN_MOD/"+model_save_path+str(time).replace(" ",""),verbose)
	print("\n\033[5;31;40m模型训练结束，已经导出到KNN_MOD文件夹下。\033[0m\n")

if __name__ == "__main__":
	#训练的文件夹/输出模型文件名
	#main("G-WorldWidePeople","WorldWideKnown")
	main("A-KnownPeople","KnownPeople")
