# -*- coding: utf-8 -*-
'''
识别temp目录中已经分好类的图片，最后一行的参数是修改识别所用的模型KNN_MOD中是我训练好了的一些人物。
'''
from math import sqrt
from sklearn import neighbors
from os import listdir
from os.path import isdir, join, isfile, splitext
import pickle
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import face_recognition
from face_recognition import face_locations
from face_recognition.face_recognition_cli import image_files_in_folder
from datetime import datetime
import os
import time
import psutil

SEE_ALL_FACES=False
WINDOWS=os.sep=="\\"
SS=os.sep
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ERROR_REPORT=""


def __predict(X_img_path, knn_clf = None, model_save_path ="", DIST_THRESH = 0.5):
	"""
	recognizes faces in given image, based on a trained knn classifier
	:param X_img_path: path to image to be recognized
	:param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
	:param model_save_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
	:param DIST_THRESH: (optional) distance threshold in knn classification. the larger it is, the more chance of misclassifying an unknown person to a known one.
	:return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
		For faces of unrecognized persons, the name 'N/A' will be passed.
	"""
	if not isfile(X_img_path) or splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
		raise Exception("invalid image path: {}".format(X_img_path))

	if knn_clf is None and model_save_path == "":
		raise Exception("must supply knn classifier either thourgh knn_clf or model_save_path")
	if knn_clf is None:
		with open(model_save_path, 'rb') as f:
			knn_clf = pickle.load(f)
	X_img = face_recognition.load_image_file(X_img_path)
	X_faces_loc = face_locations(X_img)
	if len(X_faces_loc) == 0:
		return []
	faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_faces_loc)
	closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
	is_recognized = [closest_distances[0][i][0] <= DIST_THRESH for i in range(len(X_faces_loc))]
	# predict classes and cull classifications that are not with high confidence
	return [(pred, loc) if rec else ("N/A", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_faces_loc, is_recognized)]


def __show_prediction_labels_on_image(name,ext,img_path, predictions):
	"""
	Shows the face recognition results visually.

	:param img_path: path to image to be recognized
	:param predictions: results of the predict function
	:return:
	"""
	pil_image = Image.open(img_path).convert("RGB")
	draw = ImageDraw.Draw(pil_image)

	for name, (top, right, bottom, left) in predictions:
		# Draw a box around the face using the Pillow module
		draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

		# There's a bug in Pillow where it blows up with non-UTF-8 text
		# when using the default bitmap font
		#name = name.encode("UTF-8")

		# Draw a label with a name below the face
		text_width, text_height = draw.textsize(name)
		word_css  = ".{0}zh.ttf".format(SS)
		font = ImageFont.truetype(word_css,20)
		draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
		draw.text((left + 6, bottom - text_height - 5), name,font=font, fill=(255, 255, 255, 255))

	# Remove the drawing library from memory as per the Pillow docs
	del draw

	# Display the resulting image
	if (SEE_ALL_FACES):
		pil_image.show()
	time=datetime.now()
	#保存识别的图片
	pa=".{0}tempFaceRecognition{1}{2}{3}.{4}".format(SS,SS,name,str(time)[17:],ext)
	pil_image.save(pa.replace("N/A",""))

#得到扩展名
def __fex(path): 
	ex=os.path.splitext(path)[1]
	return ex[1:]

def __faceRec(toRec,mod):
	global ERROR_REPORT
	for img_path in listdir(".{0}{1}".format(SS,toRec)):#./toRec/*
		NA = ""#Name
		ext = __fex(join(".{0}{1}".format(SS,toRec), img_path))#get ext
		#./folder/xxx.jpg  None  ./KNN_MOD/{model}
		try:
			preds = __predict(join(".{0}{1}".format(SS,toRec), img_path) ,None,".{0}KNN_MOD{1}{2}".format(SS,SS,mod))
			for name, (top, right, bottom, left) in preds:
				NA=name
				print("- Found \033[1;32;40m{}\033[0m at ({}, {})".format(name, left, top))
			#Name  ext  ./{folder}/xxx.jpg  preds
			#print("NA="+NA)
			#print("pathA="+os.path.join(".{0}{1}".format(SS,toRec), img_path))
			__show_prediction_labels_on_image(NA,ext,os.path.join(".{0}{1}".format(SS,toRec), img_path), preds)

			if len(preds)==0:
				print("ERROR-None face")
			if(len(preds)==1):
				srcFile = ".{0}{1}{2}{3}".format(SS,toRec,SS,img_path)
				time=datetime.now()#获取当前时间
				if preds[0][0]=="N/A":
					#./toRec/unknow-
					dstFile = ".{0}{1}{2}unknown-{3}.{4}".format(SS,toRec,SS,str(time)[17:],__fex(srcFile))
				else:
					dstFile = ".{0}{1}{2}{3}-{4}.{5}".format(SS,toRec,SS,preds[0][0],str(time)[17:],__fex(srcFile))
				#显示正处理的文件
				print(dstFile)
				try:
					os.rename(srcFile,dstFile)
				except Exception as e:
					print(e)
				else:
					pass
			else:
				if(__fex(".{0}{1}{2}{3}".format(SS,toRec,SS,img_path))=="png"):
					__tagPeople("png",toRec,img_path,preds)
				if(__fex(".{0}{1}{2}{3}".format(SS,toRec,SS,img_path))=="jpg"):
					__tagPeople("jpg",toRec,img_path,preds)
				if(__fex(".{0}{1}{2}{3}".format(SS,toRec,SS,img_path))=="jpeg"):
					__tagPeople("jpeg",toRec,img_path,preds)
		except Exception as e:
			ERROR_REPORT="{}\n{}{}".format(ERROR_REPORT,e,img_path)
			#raise e


def __tagPeople(fext,toRec,img_path,preds):
	n=1
	tempName=join(toRec,img_path)
	for x in preds:
		srcFile = tempName
		print("文件{0}:".format(img_path),end="")
		print("发现:"+x[0],end="  ")
		if x[0]=="N/A":
			if n==1:
				time=datetime.now()
				dstFile = ".{0}{1}{2}{3}{4}".format(SS,toRec,SS,"unknown",str(time)[17:])
			else:
				time=datetime.now()
				dstFile = "{0}-{1}{2}".format(tempName[:-9],"unknown",str(time)[17:])
			n+=1
		else:
			if n==1:
				time=datetime.now()
				dstFile = ".{0}{1}{2}{3}{4}".format(SS,toRec,SS,x[0],str(time)[17:])
			else:
				time=datetime.now()
				dstFile = "{0}-{1}{2}".format(tempName[:-9],x[0],str(time)[17:])
			n+=1
		try:
			tempName=dstFile
			os.rename(srcFile,dstFile)
		except Exception as e:
			print(e)
	srcFile = tempName
	time=datetime.now()
	dstFile = "{0}-{1}.{2}".format(tempName[:-9],str(time)[17:],fext)
	try:
		os.rename(srcFile,dstFile)
	except Exception as e:
		print(e)
	print("\n")

def __killPro(second,pro):
	time.sleep(second)
	print("展示时间："+str(second)+"秒")
	for proc in psutil.process_iter():  # 遍历当前process
		if proc.name() == pro:  # 如果process的name是display
			proc.kill()  # 关闭该process
	#SystemExit()

#mainX
def FaceRecognitionKNN(model_name):
	print("\033[5;33;40m开始识别temp*目录下的分类文件(单线程)....\033[0m\n")
	print("处理单人面孔：")
	__faceRec("tempSingle",model_name)
	print("处理多人面孔：")
	__faceRec("tempMore",model_name)
	print("\033[5;31;40m--------识别完毕--------\033[0m")
	print("\033[1;32;41m{0}\033[0m".format(ERROR_REPORT))

if __name__ == "__main__":
	#SEE_ALL_FACES=True
	FaceRecognitionKNN("KnownPeople")
	if SEE_ALL_FACES:
		#延时5秒
		__killPro(5,"display")
		SystemExit()
	print("\n\033[5;31;40m识别完毕,接下来请再次到temp*目录下人工复审识别结果。\033[0m\n")
