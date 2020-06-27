# -*- coding: utf-8 -*-
import os

'''
把处理过的、经过人工审核的已知人物移动到人像库(./FR_DATA/A-KnownPeople/)中
'''
person = os.listdir("./Prescreen")
for x in person:
	try:
		com="mkdir ./D-Singleface/{0}".format(x)
		mkdir = os.popen(com)
	except Exception as e:
		raise e

def addTrainLib():
	try:
		commandInput = 'mv ./Prescreen/* ./FR_DATA/A-KnownPeople/'
		commandImplementation = os.popen(commandInput)
		print("File Moved")
	except Exception as e:
		print("File Moving failed.")
		raise e

if __name__ == "__main__":
	addTrainLib()
