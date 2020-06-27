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

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict(X_img_path, knn_clf = None, model_save_path ="", DIST_THRESH = .5):
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

def draw_preds(img_path, preds):
	"""
	shows the face recognition results visually.
	:param img_path: path to image to be recognized
	:param preds: results of the predict function
	:return:
	"""
	source_img = Image.open(img_path).convert("RGBA")
	draw = ImageDraw.Draw(source_img)
	for pred in preds:
		loc = pred[1]
		name = pred[0]
		# (top, right, bottom, left) => (left,top,right,bottom)
		draw.rectangle(((loc[3], loc[0]), (loc[1],loc[2])), outline="red")
		draw.text((loc[3], loc[0] - 30), name, font=ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30))
	source_img.show()

def fex(path): 
	ex=os.path.splitext(path)[1]
	return ex[1:]

def faceRec(toRec,mod):
	for img_path in listdir("./{}".format(toRec)):
		preds = predict(join("./{}".format(toRec), img_path) ,None,"./KNN_MOD/{}".format(mod))
		#preds = predict(join("./{}".format(toRec), img_path) ,None,"."./KNN_MOD/{}".format(mod))

		if len(preds)==0:
			print("ERROR-None face")
		if(len(preds)==1):
			srcFile = "./{0}/{1}".format(toRec,img_path)
			time=datetime.now()#获取当前时间
			if preds[0][0]=="N/A":
				dstFile = "./{0}/unknown-{1}.{2}".format(toRec,str(time)[17:],fex(srcFile))
			else:
				dstFile = "./{0}/{1}-{2}.{3}".format(toRec,preds[0][0],str(time)[17:],fex(srcFile))
			print(dstFile)
			try:
				os.rename(srcFile,dstFile)
			except Exception as e:
				print("Rename file fail.")
				print(e)
			else:
				#print("Rename file success.")
				pass
		else:
			#A Long If:
			if(fex("./{}/{}".format(toRec,img_path))=="png"):
				n=1
				tempName=join(toRec,img_path)
				#print(tempName)
				for x in preds:
					srcFile = tempName
					print("发现:"+x[0],end="  ")
					if x[0]=="N/A":
						if n==1:
							time=datetime.now()
							dstFile = "./{0}/{1}{2}".format(toRec,"unknown",str(time)[17:])
						else:
							time=datetime.now()
							dstFile = "{0}-{1}{2}".format(tempName[:-9],"unknown",str(time)[17:])
						n+=1
					else:
						if n==1:
							time=datetime.now()
							dstFile = "./{0}/{1}{2}".format(toRec,x[0],str(time)[17:])
						else:
							time=datetime.now()
							dstFile = "{0}-{1}{2}".format(tempName[:-9],x[0],str(time)[17:])
						n+=1
					try:
						tempName=dstFile
						os.rename(srcFile,dstFile)
					except Exception as e:
						print("Rename file fail.")
						print(e)
					else:
						#print("Rename file success.")
						pass
				srcFile = tempName
				#print(srcFile)
				time=datetime.now()
				dstFile = "{0}-{1}.png".format(tempName[:-9],str(time)[17:],)
				#print(dstFile)
				try:
					os.rename(srcFile,dstFile)
				except Exception as e:
					print("Rename file fail.")
					print(e)
				else:
					#print("Rename file success.")
					pass
				print("\n")
			else:
				pass
			if(fex("./{}/{}".format(toRec,img_path))=="jpg"):
				n=1
				tempName=join(toRec,img_path)
				#print(tempName)
				for x in preds:
					srcFile = tempName
					print("发现:"+x[0],end="  ")
					if x[0]=="N/A":
						if n==1:
							time=datetime.now()
							dstFile = "./{0}/{1}{2}".format(toRec,"unknown",str(time)[17:])
						else:
							time=datetime.now()
							dstFile = "{0}-{1}{2}".format(tempName[:-9],"unknown",str(time)[17:])
						n+=1
					else:
						if n==1:
							time=datetime.now()
							dstFile = "./{0}/{1}{2}".format(toRec,x[0],str(time)[17:])
						else:
							time=datetime.now()
							dstFile = "{0}-{1}{2}".format(tempName[:-9],x[0],str(time)[17:])
						n+=1
					try:
						tempName=dstFile
						os.rename(srcFile,dstFile)
					except Exception as e:
						print("Rename file fail.")
						print(e)
					else:
						#print("Rename file success.")
						pass
				srcFile = tempName
				#print(srcFile)
				time=datetime.now()
				dstFile = "{0}-{1}.jpg".format(tempName[:-9],str(time)[17:],)
				#print(dstFile)
				try:
					os.rename(srcFile,dstFile)
				except Exception as e:
					print("Rename file fail.")
					print(e)
				else:
					#print("Rename file success.")
					pass
				print("\n")
			else:
				pass
			if(fex("./{}/{}".format(toRec,img_path))=="jpeg"):
				n=1
				tempName=join(toRec,img_path)
				#print(tempName)
				for x in preds:
					srcFile = tempName
					print("发现:"+x[0],end="  ")
					if x[0]=="N/A":
						if n==1:
							time=datetime.now()
							dstFile = "./{0}/{1}{2}".format(toRec,"unknown",str(time)[17:])
						else:
							time=datetime.now()
							dstFile = "{0}-{1}{2}".format(tempName[:-9],"unknown",str(time)[17:])
						n+=1
					else:
						if n==1:
							time=datetime.now()
							dstFile = "./{0}/{1}{2}".format(toRec,x[0],str(time)[17:])
						else:
							time=datetime.now()
							dstFile = "{0}-{1}{2}".format(tempName[:-9],x[0],str(time)[17:])
						n+=1
					try:
						tempName=dstFile
						os.rename(srcFile,dstFile)
					except Exception as e:
						print("Rename file fail.")
						print(e)
					else:
						#print("Rename file success.")
						pass
				srcFile = tempName
				#print(srcFile)
				time=datetime.now()
				dstFile = "{0}-{1}.jpeg".format(tempName[:-9],str(time)[17:],)
				#print(dstFile)
				try:
					os.rename(srcFile,dstFile)
				except Exception as e:
					print("Rename file fail.")
					print(e)
				else:
					#print("Rename file success.")
					pass
				print("\n")
			else:
				pass

def FaceRecognitionKNN(model_name):
	faceRec("tempSingle",model_name)
	faceRec("tempMore",model_name)

if __name__ == "__main__":
	FaceRecognitionKNN("WorldWideKnown_202006")
