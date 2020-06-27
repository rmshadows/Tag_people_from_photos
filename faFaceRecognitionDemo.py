# -*- coding: utf-8 -*-
'''
演示须知：
添加待识别的人脸图片到INPUT_PIC文件夹中。
在下方标记处修改成你自己训练的模型。
'''
import caFindFaces
import daFaceRecognition_KNN
import dbMoved2Data

if __name__ == "__main__":
	caFindFaces.FindFaces()
	print("开始识别。")
	#这里就是识别模型，默认采用WorldWideKnown_202006
	daFaceRecognition_KNN.FaceRecognitionKNN("WorldWideKnown_202006")
	print("开始添加数据。")
	dbMoved2Data.Moving()
