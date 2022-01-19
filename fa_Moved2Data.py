#!/usr/bin/python3
import os
import shutil
from os.path import join

import m_CLEAN_UP_TEMP

'''
将temp中识别后的文件（记得人工审核一下再运行此脚本）移动到相应的目录。
单人面孔将创建单独的文件夹。
已识别的数据将储存在./FR_DATA
'''

WINDOWS = os.sep == "\\"
SS = os.sep


def __findUnknown(str):
    un = False
    if 'unknown' in str:
        un = True
    else:
        un = False
    return un


def __returnPersonName(fileName):
    # Aaron_Peirsol-19.013784
    str = fileName.split("-")
    # ext=fileName.split(".")
    # name=str[0]+"."+ext[-1]
    return str[0]


def __moveSingleFaceData():
    folder = ["tempSingle", "temp"]
    for x in folder:
        for unit in os.listdir(join(x)):
            if unit != ".keep":
                if __findUnknown(unit):
                    src = join(x, unit)
                    dst = join("FR_DATA", "B-Unknown", unit)
                    # print(src+" to "+dst)
                    shutil.move(src, dst)
                else:
                    src = join(x, unit)
                    dst = join("FR_DATA", "D-Singleface", __returnPersonName(unit), unit)
                    personDir = join("FR_DATA", "D-Singleface", __returnPersonName(unit))
                    if not os.path.exists(personDir):
                        print("Mkdir...{0}".format(__returnPersonName(unit)))
                        os.makedirs(personDir)  # 创建目录
                    else:
                        pass
                    shutil.move(src, dst)


def __moveMultiFacesData():
    for unit in os.listdir(join("tempMore")):
        if unit != ".keep":
            src = join("tempMore", unit)
            dst = join("FR_DATA", "E-Morefaces", unit)
            # print(src+"  to  "+dst)
            shutil.move(src, dst)


def __moveNoneFacesData():
    for unit in os.listdir(join("tempNone")):
        if unit != ".keep":
            src = join("tempNone", unit)
            dst = join("FR_DATA", "C-Noneface", unit)
            # print(src+"  to  "+dst)
            shutil.move(src, dst)


# mainX
def Moving():
    try:
        __moveSingleFaceData()
        __moveMultiFacesData()
        __moveNoneFacesData()
    except Exception as e:
        raise e
    finally:
        m_CLEAN_UP_TEMP.cleanUpTemp()
    print("\n\033[5;31;40m文件已经添加到数据库，下面如有报错，请忽略。\033[0m\n")


if __name__ == "__main__":
    Moving()
