# -*- coding: utf-8 -*-
'''
删除临时目录中的未知人物识别
'''
import os

WINDOWS=os.sep=="\\"
SS=os.sep

#mainX
def cleanUpTemp():
	if WINDOWS:
		try:
			commandInput = 'del /S /Q .\\tempMore\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 0")

		try:
			commandInput = 'del /S /Q .\\tempNone\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 1")

		try:
			commandInput = 'del /S /Q .\\tempSingle\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 2")
		try:
			commandInput = 'del /S /Q .\\temp\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 3")
		try:
			commandInput = 'del /S / .\\tempFaceRecognition\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 4")
		print("Windows - 请检查temp* 内的文件是否清除。")
	else:
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
		try:
			commandInput = 'rm ./temp/*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 3")

		try:
			commandInput = 'rm ./tempFaceRecognition/*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 4")
		print("\n\033[5;31;40m临时文件已经清除。下面如有报错，请忽略。\033[0m\n")

if __name__ == "__main__":
	cleanUpTemp()
