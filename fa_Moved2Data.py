#!/usr/bin/python3
import os
import shutil
import m_CLEAN_UP_TEMP
'''
将temp中识别后的文件（记得人工审核一下再运行此脚本）移动到相应的目录。
单人面孔将创建单独的文件夹。
已识别的数据将储存在./FR_DATA
'''

WINDOWS=os.sep=="\\"
SS=os.sep

def __findUnknown(str):
	un=False
	if 'unknown' in str:
		un=True
	else:
		un=False
	return un

def __returnPersonName(fileName):
	#Aaron_Peirsol-19.013784
	str=fileName.split("-")
	#ext=fileName.split(".")
	#name=str[0]+"."+ext[-1]
	return str[0]

def __moveSingleFaceData():
	folder=["tempSingle","temp"]
	for x in folder:
		person=os.listdir("./{0}{1}{2}".format(SS,x,SS))
		for unit in person:
			if unit != ".keep":
				if (__findUnknown(unit)):
					src = ".{0}{1}{2}".format(SS, x, SS) + unit
					dst = ".{0}FR_DATA{1}B-Unknown{2}".format(SS, SS, SS) + unit
					# print(src+" to "+dst)
					shutil.move(src, dst)
				else:
					src = ".{0}{1}{2}".format(SS, x, SS) + unit
					dst = ".{0}FR_DATA{1}D-Singleface{2}".format(SS, SS, SS) + __returnPersonName(unit) + SS + unit
					personDir = ".{0}FR_DATA{1}D-Singleface{2}".format(SS, SS, SS) + __returnPersonName(unit)
					if not os.path.exists(personDir):
						print("Mkdir...{0}".format(__returnPersonName(unit)))
						os.makedirs(personDir)  # 创建目录
					else:
						pass
					shutil.move(src, dst)

def __moveMultiFacesData():
	person=os.listdir(".{0}tempMore{1}".format(SS,SS))
	#print(person)
	for unit in person:
		if unit != ".keep":
			src = ".{0}tempMore{1}".format(SS, SS) + unit
			dst = ".{0}FR_DATA{1}E-Morefaces{2}".format(SS, SS, SS) + unit
			# print(src+"  to  "+dst)
			shutil.move(src, dst)

#mainX
def Moving():
	try:
		__moveSingleFaceData()
		__moveMultiFacesData()
	except Exception as e:
		raise e
	finally:
		m_CLEAN_UP_TEMP.cleanUpTemp()
	print("\n\033[5;31;40m文件已经添加到数据库，下面如有报错，请忽略。\033[0m\n")


if __name__ == "__main__":
	Moving()
