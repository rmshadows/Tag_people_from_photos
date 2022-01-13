#!/usr/bin/python3
import os
from datetime import datetime
'''
从已识别的数据库中搜寻人物，结果会创建一个检索词开头的文件夹。
'''

WINDOWS=os.sep=="\\"
SS=os.sep

def __findSingleFaceData(who,time):
	person=os.listdir(".{0}FR_DATA{1}D-Singleface{2}".format(SS,SS,SS))
	found=False
	Ti = str(time).replace(":","")
	dst=".{0}{1}{2}".format(SS,who,Ti.replace(" ",""))
	os.makedirs(dst)#./{who}{time}
	for unit in person:
		if who in unit:
			found=True
			if WINDOWS:
				try:
					#mkdir ./{who}{time}/{who}
					commandInput = "mkdir {0}\\{1}",format(dst,who)
					commandImplementation = os.popen(commandInput)
				except Exception as e:
					print("MOVE FILE ERROR.")
				try:
					#copy /Y src ./{who}{time}/{who}
					commandInput = "copy /Y .\\FR_DATA\\D-Singleface\\{0}\\* {1}\\{2}".format(unit,dst,who)
					commandImplementation = os.popen(commandInput)
				except Exception as e:
					print("MOVE FILE ERROR.")
			else:
				try:
					commandInput = "cp -r ./FR_DATA/D-Singleface/{0} {1}".format(unit,dst)
					commandImplementation = os.popen(commandInput)
				except Exception as e:
					print("MOVE FILE ERROR.")
		else:
			pass
	if found:
		print("在单人面孔中发现{0}。".format(who))
	else:
		print("未发现{}的单人面孔数据。".format(who))
	return dst

def __findMultiFacesData(who,time,dst):
	person=os.listdir("./FR_DATA/E-Morefaces/")
	for unit in person:
		if who in unit:
			if WINDOWS:
				try:
					commandInput = "copy /Y ./FR_DATA/E-Morefaces/{0} {1}".format(unit,dst)
					commandImplementation = os.popen(commandInput)
				except Exception as e:
					print("MOVE FILE ERROR.")
			else:
				try:
					commandInput = "cp ./FR_DATA/E-Morefaces/{0} {1}".format(unit,dst)
					commandImplementation = os.popen(commandInput)
				except Exception as e:
					print("MOVE FILE ERROR.")

#mainX
def FindSomebody(name):
	print("\033[5;32;40m新建检索结果文件夹...\033[0m")
	time=str(datetime.now())[11:].replace(" ","")
	dst=__findSingleFaceData(name,time.replace(":",""))
	__findMultiFacesData(name,time.replace(":",""),dst)
	print("\n\033[5;31;40m检索完毕\033[0m\n")

if __name__ == "__main__":
	FindSomebody("Albert")#要查找的人名
