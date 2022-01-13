#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
训练材料预处理，保存成单个脸部图片
只有当你的训练材料中有很多多人照片才这么做
请将训练材料放在Prescreen文件夹中。
结构要求：
    -+-PersonA-+-1.jpg
     |         +-2.jpg
     |         +-...
     |
     +-PersonB-+-1.jpg
     |         +-2.jpg
     |         +-...
     |
     +-PersonC-+-1.jpg
               +-2.jpg
               +-...
'''

import os
import threading
import time
from datetime import datetime
from os.path import join

import face_recognition
import psutil
from PIL import Image

# 是否显示识别到的人脸
SEE_ALL_FACES = False
WINDOWS = os.sep == "\\"
SS = os.sep
ERROR_INFO = ""


def tsleep(n):
    time.sleep(n)


def __fex(path):
    """
    获取扩展名
    :param path:
    :return:
    """
    ex = os.path.splitext(path)[1]
    return ex[1:]


def __renameFile():
    """
    重命名文件
    将Prescreen中的文件重命名为 {序号}.{扩展名}
    :return:
    """
    # ./Prescreen目录
    prescreen_path = join("Prescreen")
    # person_name : Prescreen/person_name
    for person_name in os.listdir(prescreen_path):
        if person_name != ".keep":  # 排除.keep文件
            person_path = join("Prescreen", person_name)
            person_pics = os.listdir(person_path)  # ./Prescreen/person_name/*
            # 首先将文件全部随机重命名
            for picture in person_pics:  # ./Prescreen/person_name/xxx.jpg
                get_time = datetime.now()
                # ./Prescreen/person_name/xxx.jpg
                src_file = join(prescreen_path, person_name, picture)
                # dst=./Prescreen/{人名}/{时间后面的秒数}.{扩展名}
                sec_str = str(get_time)[17:]
                dst_file = join(prescreen_path, person_name, "{0}.{1}".format(sec_str.replace(" ", ""), __fex(src_file)))
                try:
                    # 重命名
                    os.rename(src_file, dst_file)
                except Exception as e:
                    print(e)
            person_pics = os.listdir(person_path)
            n = 1
            # 接下来按序号命名
            # picture :Prescreen/person_name/xxx
            for picture in person_pics:
                # Prescreen/person_name/xxx.jpg
                src_file = join(person_path, picture)
                # dst=Prescreen/person_name/{n}.{ext}
                dst_file = join(person_path, "{0}.{1}".format(n, __fex(src_file)))
                try:
                    os.rename(src_file, dst_file)
                except Exception as e:
                    print(e)
                n += 1


def __checkFaces(file, person):
    """
    # Find faces in pictures
    并裁剪人脸
    FRS开头是裁剪后的文件
    :param file: 文件路径裁剪的文件路径
    :param person: 裁剪后要保存到的人名文件夹
    :return:
    """
    global ERROR_INFO
    try:
        # Load the jpg file into a numpy array
        inputPic = file
        image = face_recognition.load_image_file(inputPic)
        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py
        # CNN:
        # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        # 这里使用HOG模型
        face_locations = face_recognition.face_locations(image)
        faceNum = len(face_locations)
        print("Found \033[1;33;40m{0}\033[0m: face(s) in \033[1;35;40m{1}\033[0m: photograph.".format(faceNum, file),
              end=" ==> ")
        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location
            print("A face is located at pixel location Top: "
                  "{}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,right))
            if (top - 200 < 0):
                if (top - 150 < 0):
                    if (top - 100 < 0):
                        T = top
                    else:
                        T = top - 100
                else:
                    T = top - 150
            else:
                T = top - 200
            B = bottom + 100
            if (left - 100 < 0):
                L = left
            else:
                L = left - 100
            R = right + 100
            tsleep(0.2)
            print(T, B, L, R)
            face_image = image[T:B, L:R]
            pil_image = Image.fromarray(face_image)
            if (SEE_ALL_FACES):
                pil_image.show()
            get_time = str(datetime.now())[17:]
            # .{/}Prescreen{/}{person}{/}FRS{time}
            pil_image.save(join("Prescreen", person, "FRS{0}.{1}".format(get_time, __fex(file))))
    except Exception as e:
        ERROR_INFO = "{0}\n{1}".format(ERROR_INFO, e)
        print("\033[1;32;41m{0}\033[0m".format(e))
        raise e
    return faceNum


def filePrescreen():
    """
    供外界调用的方法
    :return:
    """
    print("Prescreen Start......\n")
    __renameFile()
    prescreen_path = join("Prescreen")
    # ./Prescreen/*
    for person in os.listdir(prescreen_path):  # ./Prescreen/person/
        if person != ".keep":
            person_path = join(prescreen_path, person)
            # ./Prescreen/person/
            pics = (os.listdir(person_path))  # ./Prescreen/person/*
            if (len(pics) >= 20) & (not WINDOWS):  # ./Prescreen/person/下的图片20张以上
                taskNum = int(len(pics) / 4)
                taskLef = len(pics) % 4
                # 创建新线程
                thread1 = __TaskSubmit("1", pics[0:taskNum], person)
                thread2 = __TaskSubmit("2", pics[taskNum:taskNum * 2], person)
                thread3 = __TaskSubmit("3", pics[taskNum * 2:taskNum * 3], person)
                thread4 = __TaskSubmit("4", pics[taskNum * 3:taskNum * 4], person)
                if taskLef == 0:
                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()
                    thread1.join()
                    thread2.join()
                    thread3.join()
                    thread4.join()
                else:
                    thread5 = __TaskSubmit("5", pics[taskNum * 4:taskNum * 4 + taskLef], person)
                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()
                    thread5.start()
                    thread1.join()
                    thread2.join()
                    thread3.join()
                    thread4.join()
                    thread5.join()
            else:
                for picture in pics:  # ./Prescreen/person/xxx.jpg
                    time = datetime.now()  # 获取当前时间
                    # "./Prescreen/"+person+ "/" +picture
                    src_file = join(person_path, picture)
                    if __checkFaces(src_file, person) == 0:
                        # ./Prescreen/person/rm{time}
                        dst_file = join(person_path, "rm{0}".format(str(time)[17:].replace(" ", "")))
                    else:
                        # ./Prescreen/person/1F{时间}.{扩展名}
                        dst_file = join(person_path, "1F{0}.{1}".format(str(time)[17:].replace(" ", ""), __fex(src_file)))
                    try:
                        os.rename(src_file, dst_file)
                    except Exception as e:
                        print(e)
                    else:
                        pass
    __rmFiles()


def doTask(who, person):
    for f in who:  # f=(xxx.jpg)
        time = datetime.now()  # 获取当前时间
        src_file = "./Prescreen/{0}/{1}".format(person, f)  # ./Prescreen/{person}/{xxx.jpg}
        if __checkFaces(src_file, person) == 0:
            # ./Prescreen/person/rm{}{}
            dst_file = "./Prescreen/{0}/rm{1}.{2}".format(person, str(time)[17:].replace(" ", ""), __fex(src_file))
        else:
            dst_file = "./Prescreen/{0}/1F{1}.{2}".format(person, str(time)[17:].replace(" ", ""), __fex(src_file))
        try:
            os.rename(src_file, dst_file)
        except Exception as e:
            print(e)
        else:
            pass


class __TaskSubmit(threading.Thread):
    def __init__(self, id, who, person):
        threading.Thread.__init__(self)
        self.id = id
        self.who = who
        self.person = person
        self.result = "1"
    
    def run(self):
        print("开始线程：" + self.id + " on stat " + self.result)
        doTask(self.who, self.person)
        self.result = "0"
        print("退出线程：" + self.id + " on stat " + self.result)


def __rmFiles():
    """
    删除无法识别人脸的文件
    :return:
    """
    print("\nDelete files...")
    prescreen_path = join("Prescreen")
    # 显示预筛选文件夹下的人物文件夹#./Prescreen/*
    for person in os.listdir(prescreen_path):  # ./Prescreen/person
        if person != ".keep":
            if WINDOWS:
                try:
                    # del .\Prescreen\{person}\rm*
                    commandInput = 'del /S /Q .\\Prescreen\\' + person + "\\rm*"
                    commandImplementation = os.popen(commandInput)
                    print("Del...")
                except Exception as e:
                    print(e)
                try:
                    # del .\Prescreen\{person}\rm*
                    commandInput = 'del /S /Q .\\Prescreen\\' + person + "\\MF*"
                    commandImplementation = os.popen(commandInput)
                    print("Del...")
                except Exception as e:
                    print(e)
            else:
                try:
                    # rm ./Prescreen/{person}/rm*
                    commandInput = 'rm ./Prescreen/' + person + "/rm*"
                    commandImplementation = os.popen(commandInput)
                except Exception as e:
                    print("REMOVE FILE ERROR.")
                try:
                    # rm ./Prescreen/{person}/rm*
                    commandInput = 'rm ./Prescreen/' + person + "/MF*"
                    commandImplementation = os.popen(commandInput)
                except Exception as e:
                    print("REMOVE FILE ERROR.")


def __killPro(second, pro):
    """
    延时杀死进程
    :param second:
    :param pro: 进程名
    :return:
    """
    time.sleep(second)
    print("展示时间：" + str(second) + "秒")
    for proc in psutil.process_iter():  # 遍历当前process
        if proc.name() == pro:  # 如果process的name是display
            proc.kill()  # 关闭该process


if __name__ == "__main__":
    # True是显示识别出的图像
    # SEE_ALL_FACES=True
    filePrescreen()
    print("\033[1;32;41m{0}\033[0m".format(ERROR_INFO))
    print("\n\033[5;31;40m训练材料预处理结束，请进行人工复审。下面如果有报错，请忽略。\033[0m\n")
    if SEE_ALL_FACES:
        # 延时5秒
        __killPro(5, "display")
        SystemExit()
    print("\nFinish.")
