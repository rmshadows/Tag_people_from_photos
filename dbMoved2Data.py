import os
import shutil
import eaCLEAN_UP_TEMP
'''
将temp中识别后的文件（记得人工审核一下再运行此脚本）移动到相应的目录。
单人面孔将创建单独的文件夹。
已识别的数据将储存在./FR_DATA
'''
def findUnknown(str):
	un=False
	if 'unknown' in str:
		un=True
	else:
		un=False
	return un

def returnPersonName(fileName):
	#Aaron_Peirsol-19.013784
	str=fileName.split("-")
	#ext=fileName.split(".")
	#name=str[0]+"."+ext[-1]
	return str[0]

def moveSingleFaceData():
	person=os.listdir("./tempSingle/")
	#print(person)
	for unit in person:
		if(findUnknown(unit)):
			src="./tempSingle/"+unit
			dst="./FR_DATA/B-Unknown/"+unit
			#print(src+" to "+dst)
			shutil.move(src,dst)
		else:
			src="./tempSingle/"+unit
			dst="./FR_DATA/D-Singleface/"+returnPersonName(unit)+"/"+unit
			personDir = "./FR_DATA/D-Singleface/"+returnPersonName(unit)
			if not os.path.exists(personDir):
				print("Mkdir...{}".format(returnPersonName(unit)))
				os.makedirs(personDir)	# 创建目录
			else:
				pass
			shutil.move(src,dst)

def moveMultiFacesData():
	person=os.listdir("./tempMore/")
	#print(person)
	for unit in person:
		src="./tempMore/"+unit
		dst="./FR_DATA/E-Morefaces/"+unit
		#print(src+"  to  "+dst)
		shutil.move(src,dst)

def Moving():
	try:
		moveSingleFaceData()
		moveMultiFacesData()
	except Exception as e:
		raise e
	finally:
		eaCLEAN_UP_TEMP.cleanUpTemp()
	print("\n\033[5;31;40m文件已经添加到数据库，下面如有报错，请忽略。\033[0m\n")


if __name__ == "__main__":
	Moving()