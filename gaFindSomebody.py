import os
from datetime import datetime
'''
从已识别的数据库中搜寻人物，结果会创建一个检索词开头的文件夹。
'''

def __findSingleFaceData(who,time):
	person=os.listdir("./FR_DATA/D-Singleface/")
	found=False
	dst="./{0}{1}".format(who,time)
	os.makedirs(dst)
	for unit in person:
		if who in unit:
			found=True
			try:
				commandInput = "cp -r ./FR_DATA/D-Singleface/{0} {1}".format(unit,dst)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print("MOVE FILE ERROR.")
		else:
			pass
	if found:
		print("在单人面孔中发现{}。".format(who))
	else:
		print("未发现{}的单人面孔数据。".format(who))
	return dst

def __findMultiFacesData(who,time,dst):
	person=os.listdir("./FR_DATA/E-Morefaces/")
	for unit in person:
		if who in unit:
			try:
				commandInput = "cp ./FR_DATA/E-Morefaces/{0} {1}".format(unit,dst)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print("MOVE FILE ERROR.")

#mainX
def FindSomebody(name):
	print("\033[5;32;40m新建检索结果文件夹...\033[0m")
	time=str(datetime.now())
	dst=__findSingleFaceData(name,time[11:])
	#print(dst)
	__findMultiFacesData(name,time,dst)
	print("\n\033[5;31;40m检索完毕\033[0m\n")

if __name__ == "__main__":
	FindSomebody("Albert")#要查找的人名
