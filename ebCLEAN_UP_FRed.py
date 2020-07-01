# -*- coding: utf-8 -*-
'''
删除已识别的数据
'''
import os

WINDOWS=os.sep=="\\"
SS=os.sep

#mainX
def cleanUpRecognized():
	if WINDOWS:
		try:
			commandInput = 'del /S /Q .\\FR_DATA\\B-Unknown\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 0")
		try:
			commandInput = 'del /S /Q .\\FR_DATA\\C-Noneface\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 1")
		try:
			commandInput = 'rd /S /Q .\\FR_DATA\\D-Singleface\\'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 2")
		try:
			commandInput = "mkdir .\\FR_DATA\\D-Singleface"
			commandImplementation = os.popen(commandInput)
			print("Windows - mkdir...")
		except Exception as e:
			raise e
		try:
			commandInput = 'del /S /Q .\\FR_DATA\\E-Morefaces\\*'
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print("ERROR 3")
		print("Windows - 清除已识别人物数据中...请检查是否清除。")

	else:
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
		print("\n\033[5;31;40m清除已识别人物数据中...下面如有报错，请忽略。\033[0m\n")

if __name__ == "__main__":
	cleanUpRecognized()