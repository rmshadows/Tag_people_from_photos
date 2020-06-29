# -*- coding: utf-8 -*-
import os

'''
把处理过的、经过人工审核的已知人物移动到人像库(./FR_DATA/A-KnownPeople/)中
'''

#新建人物
def __addPerson(name):
	try:
		#mv ./Prescreen/{name} ./FR_DATA/A-KnownPeople/
		commandInput = "mv ./Prescreen/{0} ./FR_DATA/A-KnownPeople/".format(name)
		commandImplementation = os.popen(commandInput)
		print("Person created.")
	except Exception as e:
		raise e

#添加到已有
def __addPicture(name):
	try:
		#mv ./Prescreen/{name}/* ./FR_DATA/A-KnownPeople/{name}/
		commandInput = "mv ./Prescreen/{0}/* ./FR_DATA/A-KnownPeople/{1}/".format(name,name)
		commandImplementation = os.popen(commandInput)
		print("Person existed,adding....")
	except Exception as e:
		raise e

#单人目录添加
def __addSingleDir(name):
	try:
		#mkdir ./FR_DATA/D-Singleface/{name}
		com="mkdir ./FR_DATA/D-Singleface/{0}".format(name)
		mkdir = os.popen(com)
	except Exception as e:
		raise e

#主要方法X
def addKnowPeople():
	add = os.listdir("./Prescreen")#./Prescreen/*
	for name in add:
		#./FR_DATA/A-KnownPeople/{name}
		if not os.path.exists("./FR_DATA/A-KnownPeople/{0}".format(name)):
			__addPerson(name)
		else:
			__addPicture(name)
		#./FR_DATA/D-Singleface/{name}
		if not os.path.exists("./FR_DATA/D-Singleface/{0}".format(name)):
			__addSingleDir(name)
		else:
			pass
	print("人物添加完毕。")
	try:
		#rm -r ./Prescreen/*
		commandInput = "rm -r ./Prescreen/*"
		commandImplementation = os.popen(commandInput)
		print("Remove Prescreen....")
	except Exception as e:
		raise e

if __name__ == "__main__":
	addKnowPeople()
	print("\033[5;31;40m训练材料移动工作结束，接下来请进行模型训练。下面如果有报错，请忽略。\033[0m\n")