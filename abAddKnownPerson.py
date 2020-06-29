# -*- coding: utf-8 -*-
import os

'''
把处理过的、经过人工审核的已知人物移动到人像库(./FR_DATA/A-KnownPeople/)中
'''

def addPerson(name):
	try:
		commandInput = "mv ./Prescreen/{0} ./FR_DATA/A-KnownPeople/".format(name)
		commandImplementation = os.popen(commandInput)
		print("Person created.")
	except Exception as e:
		raise e

def addPicture(name):
	try:
		commandInput = "mv ./Prescreen/{0}/* ./FR_DATA/A-KnownPeople/{1}/".format(name,name)
		commandImplementation = os.popen(commandInput)
		print("Person existed,adding....")
	except Exception as e:
		raise e

def addSingleDir(name):
	try:
		com="mkdir ./FR_DATA/D-Singleface/{0}".format(name)
		mkdir = os.popen(com)
	except Exception as e:
		raise e

def addKnowPeople():
	add = os.listdir("./Prescreen")
	for name in add:
		if not os.path.exists("./FR_DATA/A-KnownPeople/{0}".format(name)):
			addPerson(name)
		else:
			addPicture(name)
		if not os.path.exists("./FR_DATA/D-Singleface/{0}".format(name)):
			addSingleDir(name)
		else:
			pass
	print("人物添加完毕。")
	try:
		commandInput = "rm -r ./Prescreen/*"
		commandImplementation = os.popen(commandInput)
		print("Remove Prescreen....")
	except Exception as e:
		raise e


if __name__ == "__main__":
	addKnowPeople()
	print("\033[5;31;40m训练材料移动工作结束，接下来请进行模型训练。下面如果有报错，请忽略。\033[0m\n")
