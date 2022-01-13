#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
用于均衡训练文件夹中的图片
"""
import os
from datetime import datetime

WINDOWS=os.sep=="\\"
SS=os.sep


def __copyFiles(path0,path1):
	if WINDOWS:
		if os.path.isdir(path0):
			try:
				commandInput = "xcopy /C /E {} {}\\".format(path0,path1)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print(e)
		else:
			try:
				commandInput = "copy /Y {} {}".format(path0,path1)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print(e)
	else:
		try:
			commandInput = "cp -r {} {}".format(path0, path1)
			commandImplementation = os.popen(commandInput)
		except Exception as e:
			print(e)


#获取扩展名
def __fex(path): 
	ex=os.path.splitext(path)[1]
	return ex[1:]


#mainX
def bala():
	time=str(datetime.now()).replace(":","-")
	__copyFiles(".{}FR_DATA{}A-KnownPeople".format(SS,SS),".{}FR_DATA{}A-KnownPeople_bak{}".format(SS,SS,time.replace(" ","")))
	people=os.listdir(".{}FR_DATA{}A-KnownPeople".format(SS,SS))
	LEN=0
	for person in people:
		length=len(os.listdir(".{}FR_DATA{}A-KnownPeople{}{}".format(SS,SS,SS,person)))
		if length>LEN:
			LEN=length
		else:
			pass
	print("补充至数量："+str(LEN))
	for person in people:
		file=os.listdir(".{}FR_DATA{}A-KnownPeople{}{}".format(SS,SS,SS,person))
		length=len(file)
		if (length<LEN)&(length!=0):
			count=LEN - length
			print("{}补全至{}。".format(person,count))
			s=0
			for x in range(0,count):
				if s>=length:
					s=0
				else:
					pass
				TI=str(datetime.now())[-6:]
				src=".{0}FR_DATA{1}A-KnownPeople{2}{3}{4}{5}".format(SS,SS,SS,person,SS,file[s])
				ext=__fex(".{0}FR_DATA{1}A-KnownPeople{2}{3}{4}{5}".format(SS,SS,SS,person,SS,file[s]))
				dst=".{0}FR_DATA{1}A-KnownPeople{2}{3}{4}copy{5}.{6}".format(SS,SS,SS,person,SS,TI,ext)
				__copyFiles(src,dst)
				print("在{}创建文件".format(person))
				s+=1
		else:
			pass

def __delCopy():
	dir=".{}FR_DATA{}A-KnownPeople".format(SS,SS)
	people=os.listdir(dir)
	for who in people:
		if WINDOWS:
			try:
				#del .\Prescreen\{person}\rm*
				commandInput = "del /S /Q {}{}copy*".format(dir,SS)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print(e)
		else:
			try:
				#rm ./Prescreen/{person}/rm*
				commandInput = "rm {}{}copy*".format(dir,SS)
				commandImplementation = os.popen(commandInput)
			except Exception as e:
				print("REMOVE FILE ERROR.")

__delCopy()
bala()
