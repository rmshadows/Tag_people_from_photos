# -*- coding: utf-8 -*-

import time
import psutil


def __killPro(second,pro):
	time.sleep(second)
	print("展示时间："+str(second)+"秒")
	for proc in psutil.process_iter():  # 遍历当前process
		if proc.name() == pro:  # 如果process的name是display
			proc.kill()  # 关闭该process
	#SystemExit()

if __name__ == "__main__":
	__killPro(0,"display")
	SystemExit()
