#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
用于均衡训练文件夹中的图片
"""
import os
from datetime import datetime
from os.path import join

WINDOWS = os.sep == "\\"
SS = os.sep


def copyFiles(path0, path1):
    if WINDOWS:
        if os.path.isdir(path0):
            try:
                commandInput = "xcopy /C /E {} {}\\".format(path0, path1)
                commandImplementation = os.popen(commandInput)
            except Exception as e:
                print(e)
        else:
            try:
                commandInput = "copy /Y {} {}".format(path0, path1)
                commandImplementation = os.popen(commandInput)
            except Exception as e:
                print(e)
    else:
        try:
            commandInput = "cp -r {} {}".format(path0, path1)
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print(e)


# 获取扩展名
def __fex(path):
    ex = os.path.splitext(path)[1]
    return ex[1:]


# mainX
def bala():
    # 首先删除拷贝
    delCopy()
    get_time = str(datetime.now()).replace(":", "-").replace(" ", "")
    # 复制原始文件夹
    copyFiles(join("FR_DATA", "A-KnownPeople"), join("FR_DATA", "A-KnownPeople_before_balance_{0}".format(get_time)))
    people = os.listdir(".{}FR_DATA{}A-KnownPeople".format(SS, SS))
    LEN = 0
    for person in people:
        length = len(os.listdir(".{}FR_DATA{}A-KnownPeople{}{}".format(SS, SS, SS, person)))
        if length > LEN:
            LEN = length
        else:
            pass
    print("补充至数量：" + str(LEN))
    for person in people:
        file = os.listdir(".{}FR_DATA{}A-KnownPeople{}{}".format(SS, SS, SS, person))
        length = len(file)
        if (length < LEN) & (length != 0):
            count = LEN - length
            print("{}补全至{}。".format(person, count))
            s = 0
            for x in range(0, count):
                if s >= length:
                    s = 0
                else:
                    pass
                time_str = str(datetime.now())[-6:]
                src = ".{0}FR_DATA{1}A-KnownPeople{2}{3}{4}{5}".format(SS, SS, SS, person, SS, file[s])
                ext = __fex(".{0}FR_DATA{1}A-KnownPeople{2}{3}{4}{5}".format(SS, SS, SS, person, SS, file[s]))
                dst = ".{0}FR_DATA{1}A-KnownPeople{2}{3}{4}copy{5}.{6}".format(SS, SS, SS, person, SS, time_str, ext)
                copyFiles(src, dst)
                print("在{}创建文件".format(person))
                s += 1
        else:
            pass


def delCopy():
    people = os.listdir(join("FR_DATA", "A-KnownPeople"))
    for name in people:
        if WINDOWS:
            try:
                # dir_path/name/copy*
                commandInput = "del /S /Q .{0}FR_DATA{1}" \
                               "A-KnownPeople{2}{3}{4}copy*".format(SS, SS, SS,
                                                                    name, SS)
                commandImplementation = os.popen(commandInput)
            except Exception as e:
                print(e)
        else:
            try:
                commandInput = "rm .{0}FR_DATA{1}A-KnownPeople{2}{3}{4}copy*".format(SS, SS, SS,
                                                                                     name, SS)
                commandImplementation = os.popen(commandInput)
            except Exception as e:
                print("REMOVE FILE ERROR.")


if __name__ == '__main__':
    delCopy()
    bala()
    # copyFiles(join("FR_DATA", "A-KnownPeople"), join("FR_DATA", "A-KnownPeople_bak"))
