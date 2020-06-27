# -*- coding: utf-8 -*-
'''
删除已识别的数据
'''
#from PIL import Image
import os

def cleanUpRecognized():
	try:
		commandInput = 'rm ./FR_DATA/B-Unknown/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 0")

	try:
		commandInput = 'rm ./FR_DATA/C-Noneface/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 1")

	try:
		commandInput = 'rm -r ./FR_DATA/D-Singleface/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 2")

	try:
		commandInput = 'rm ./FR_DATA/E-Morefaces/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 3")

if __name__ == "__main__":
	cleanUpRecognized()
