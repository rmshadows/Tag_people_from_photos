# -*- coding:utf-8 -*-

import time
import sys

def __view_bar(sec,num,total):
	rate = num / total #得到现在的比率，0<rate<1
	rate_num = int(rate * 100) #将比率百分化，0<rate_num<100
	r = '\r[%s%s]' % ("\033[1;32;40m█\033[0m"*num, " "*(100-num)) #进度条封装
	sys.stdout.write(r) #显示进度条
	sys.stdout.write(" - 还有\033[1;31;40m{0}\033[0m秒。".format(sec))
	#sys.stdout.write(str(num)+'%') #显示进度百分比
	sys.stdout.flush() #使输出变得平滑

def view(num,total,color,STR):
	rate = num / total #得到现在的比率，0<rate<1
	rate_num = int(rate * 100) #将比率百分化，0<rate_num<100
	r = '\r[%s%s]' % ("\033[1;{0};40m█\033[0m".format(color)*rate_num, " "*(100-rate_num)) #进度条封装
	sys.stdout.write(r) #显示进度条
	if STR=="":
		sys.stdout.write(str(rate*100)[:5]+'%') #显示进度百分比
	else:
		sys.stdout.write(STR) #显示进度条
	#sys.stdout.write(str(rate*100)[:5]+'%\n') #显示进度百分比
	sys.stdout.flush() #使输出变得平滑

def waiting(sec):
	ti = sec/100
	for i in range(0, 101):
		time.sleep(ti)
		if i>=99:
			sec="0.000000000000000000"
		else:
			sec-=ti
		__view_bar(str(sec),i, 100)
	print("\n")

if __name__ == '__main__':
	waiting(10)