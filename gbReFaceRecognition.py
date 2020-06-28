import os
from datetime import datetime
import caFindFaces
import daFaceRecognition_KNN
import dbMoved2Data
'''
重新识别已识别的人物
'''

def MoveData():
	people=os.listdir("./FR_DATA/D-Singleface/")
	for who in people:
		try:
			commandInput = "mv ./FR_DATA/D-Singleface/{0}/* ./INPUT_PIC".format(who)
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("MOVE FILE ERROR.")
	else:
		pass
	try:
		commandInput = "mv ./FR_DATA/E-Morefaces/* ./INPUT_PIC"
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("MOVE FILE ERROR.")

if __name__ == "__main__":
	MoveData()
	caFindFaces.FindFaces()
	print("开始识别。")
	daFaceRecognition_KNN.FaceRecognitionKNN("WorldWideKnown_202006")
	print("开始添加数据。")
	dbMoved2Data.Moving()
	print("重新识别完毕。")