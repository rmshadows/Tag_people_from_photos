# -*- coding: utf-8 -*-
import os
import adBalanceTrain

'''
把处理过的、经过人工审核的已知人物移动到人像库(./FR_DATA/A-KnownPeople/)中
'''

WINDOWS=os.sep=="\\"
SS=os.sep

#新建人物
def __addPerson(name):
	if WINDOWS:
		try:
			#move .\Prescreen\{name} .\FR_DATA\A-KnownPeople\
			commandInput = "move /Y .\\Prescreen\\{0} .\\FR_DATA\\A-KnownPeople\\".format(name)
			commandImplementation = os.popen(commandInput)
			print("Windows - Person created.")
		except Exception as e:
			raise e
	else:
		try:
			#mv ./Prescreen/{name} ./FR_DATA/A-KnownPeople/
			commandInput = "mv ./Prescreen/{0} ./FR_DATA/A-KnownPeople/".format(name)
			commandImplementation = os.popen(commandInput)
			print("Person created.")
		except Exception as e:
			raise e

#添加到已有
def __addPicture(name):
	if WINDOWS:
		try:
			#move .\Prescreen\{name}\* .\FR_DATA\A-KnownPeople\{name}\
			commandInput = "move /Y .\\Prescreen\\{0}\\* .\\FR_DATA\\A-KnownPeople\\{1}\\".format(name,name)
			commandImplementation = os.popen(commandInput)
			print("Windows - Person existed,adding....")
		except Exception as e:
			raise e
	else:
		try:
			#mv ./Prescreen/{name}/* ./FR_DATA/A-KnownPeople/{name}/
			commandInput = "mv ./Prescreen/{0}/* ./FR_DATA/A-KnownPeople/{1}/".format(name,name)
			commandImplementation = os.popen(commandInput)
			print("Person existed,adding....")
		except Exception as e:
			raise e

#单人目录添加
def __addSingleDir(name):
	if WINDOWS:
		try:
			#mkdir .\FR_DATA\D-Singleface\{name}
			com="mkdir .\\FR_DATA\\D-Singleface\\{0}".format(name)
			mkdir = os.popen(com)
			print("Windows - mkdir...")
		except Exception as e:
			raise e
	else:
		try:
			#mkdir ./FR_DATA/D-Singleface/{name}
			com="mkdir ./FR_DATA/D-Singleface/{0}".format(name)
			mkdir = os.popen(com)
		except Exception as e:
			raise e

#主要方法X
def addKnowPeople():
	add = os.listdir(".{0}Prescreen".format(SS))#./Prescreen/*
	for name in add:
		#./FR_DATA/A-KnownPeople/{name}
		if not os.path.exists(".{0}FR_DATA{1}A-KnownPeople{2}{3}".format(SS,SS,SS,name)):
			__addPerson(name)
		else:
			__addPicture(name)
		#./FR_DATA/D-Singleface/{name}
		if not os.path.exists(".{0}FR_DATA{1}D-Singleface{2}{3}".format(SS,SS,SS,name)):
			__addSingleDir(name)
		else:
			pass
	print("人物添加完毕。")
	if WINDOWS:
		try:
			#del -r ./Prescreen/*
			commandInput = "rd /S /Q .\\Prescreen\\"
			commandImplementation = os.popen(commandInput)
			print("Remove Prescreen....")
		except Exception as e:
			raise e
		try:
			commandInput = "mkdir .\\Prescreen"
			commandImplementation = os.popen(commandInput)
			print("Windows - mkdir...")
		except Exception as e:
			raise e
	else:
		try:
			#rm -r ./Prescreen/*
			commandInput = "rm -r ./Prescreen/*"
			commandImplementation = os.popen(commandInput)
			print("Remove Prescreen....")
		except Exception as e:
			raise e

if __name__ == "__main__":
	addKnowPeople()
	adBalanceTrain.bala()
	print("\033[5;31;40m训练材料移动工作结束，接下来请进行模型训练。下面如果有报错，请忽略。\033[0m\n")
