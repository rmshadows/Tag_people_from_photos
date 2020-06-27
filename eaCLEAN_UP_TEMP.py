# -*- coding: utf-8 -*-
'''
删除临时目录中的未知人物识别
'''
#from PIL import Image
import os

def cleanUpTemp():
	try:
		commandInput = 'rm ./tempMore/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 0")

	try:
		commandInput = 'rm ./tempNone/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 1")

	try:
		commandInput = 'rm ./tempSingle/*'
		commandImplementation = os.popen(commandInput)
	except Exception as e:
		print("ERROR 2")

if __name__ == "__main__":
	cleanUpTemp()