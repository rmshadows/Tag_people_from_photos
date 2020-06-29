# -*- coding: utf-8 -*-
'''
删除临时目录中的未知人物识别
'''
import os

#mainX
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
	print("\n\033[5;31;40m临时文件已经清除。下面如有报错，请忽略。\033[0m\n")

if __name__ == "__main__":
	cleanUpTemp()