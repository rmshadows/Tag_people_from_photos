import os
from datetime import datetime
import caFindFaces
import daFaceRecognition_KNN
import dbMoved2Data
import Wait
'''
重新识别已识别的人物
'''
WINDOWS=os.sep=="\\"
SS=os.sep

def __MoveData():
	people=os.listdir(".{0}FR_DATA{1}D-Singleface{2}".format(SS,SS,SS))
	for who in people:
		if WINDOWS:
			try:
				commandInput = "move /Y .\\FR_DATA\\D-Singleface\\{0}\\* .\\INPUT_PIC\\".format(who)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print("MOVE FILE ERROR.")
		else:
			try:
				commandInput = "mv ./FR_DATA/D-Singleface/{0}/* ./INPUT_PIC".format(who)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print("MOVE FILE ERROR.")
	if WINDOWS:
		try:
			commandInput = "move /Y .\\FR_DATA\\E-Morefaces\\* .\\INPUT_PIC\\"
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("MOVE FILE ERROR.")
	else:
		try:
			commandInput = "mv ./FR_DATA/E-Morefaces/* ./INPUT_PIC"
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("MOVE FILE ERROR.")

if __name__ == "__main__":
	__MoveData()
	Wait.waiting(2)
	caFindFaces.FindFaces()
	Wait.waiting(3)
	print("开始识别。")
	daFaceRecognition_KNN.FaceRecognitionKNN("WorldWideKnown_202006")
	Wait.waiting(2)
	print("开始添加数据。")
	dbMoved2Data.Moving()
	print("重新识别完毕。")