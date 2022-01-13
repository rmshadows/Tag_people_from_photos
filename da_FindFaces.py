#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading
from datetime import datetime
from os.path import join

import face_recognition
import numpy as np
from PIL import Image

import m_Wait

"""
将需要识别的人物图片分类成无面孔、单人、多人并分配到temp开头的临时目录。
"""

# 是否找到脸部信息
SEE_ALL_FACES = False
# 是否是Windows
WINDOWS = os.sep == "\\"
# 文价分隔符
SS = os.sep
# 错误信息
ERROR_REPORT = ""


def __getSize(path):
    """
    # 获取文件大小
    :param path:
    :return:
    """
    s = os.path.getsize(path)
    return s


def __fex(path):
    """
    # 返回扩展名
    :param path:
    :return:
    """
    ex = os.path.splitext(path)[1]
    return ex[1:]


def __renameFile():
    """
    # 重命名
    :return:
    """
    # ./INPUT_PIC
    input_path = join("INPUT_PIC")
    # ./INPUT_PIC/*
    for picture in os.listdir(input_path):
        get_time = str(datetime.now()).replace(" ", "").replace(":", "")
        # ./INPUT_PIC/xxx.jpg
        src_file = os.path.join(input_path, picture)
        # ./INPUT_PIC/{time}.{ext}
        dst_file = join(input_path, "{0}.{1}".format(get_time, __fex(src_file)))
        try:
            os.rename(src_file, dst_file)
        except Exception as e:
            print(e)
        else:
            pass
    pics = (os.listdir(input_path))  # ./INPUT_PIC/*
    n = 1
    for picture in pics:
        # ./INPUT_PIC/xxx.jpg
        src_file = join(input_path, picture)
        # ./INPUT_PIC/{n}.{ext}
        dst_file = join(input_path, "{0}.{1}".format(n, __fex(src_file)))
        try:
            os.rename(src_file, dst_file)
        except Exception as e:
            print(e)
        else:
            pass
        n += 1


def __checkFaces(file):
    """
    查找人脸
    :param file:
    :return:
    """
    global ERROR_REPORT
    try:
        # Load the jpg file into a numpy array
        input_picture = join("INPUT_PIC", file)
        # 如果图片大于1.5M，压缩。
        if __getSize(input_picture) >= 1500000:
            img = Image.open(input_picture)
            w, h = img.size
            qua = 0.2
            w, h = round(w * qua), round(h * qua)
            img = img.resize((w, h), Image.ANTIALIAS)
            image = np.array(img)
            print("压缩图片...")
        else:
            image = face_recognition.load_image_file(input_picture)
        # print("加载完成	")
        
        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py
        
        # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        face_locations = face_recognition.face_locations(image)
        # print("定位完成")
        face_num = len(face_locations)
        print("Found \033[1;33;40m{0} face(s)\033[0m: in \033[1;35;40m{1} photograph.\033[0m:".format(face_num, file),
              end=" ==> ")
        
        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location
            print(
                "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                      right))
            
            if SEE_ALL_FACES:
                # You can access the actual face itself like this:
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                pil_image.show()
        # print("Next")
        return face_num
    except Exception as e:
        # raise e
        ERROR_REPORT = "{0}\n{1}{2}".format(ERROR_REPORT, e, file)
        print(e)


def __copyFiles():
    """
    复制文识别结果到temp
    :return:
    """
    if WINDOWS:
        try:
            # copy ./INPUT_PIC/0* ./tempNone
            commandInput = 'copy /Y .\\INPUT_PIC\\0* .\\tempNone'
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print(e)
        try:
            # cp ./INPUT_PIC/1* ./tempSingle
            commandInput = 'copy /Y .\\INPUT_PIC\\1* .\\tempSingle'
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print("No Singleface")
        try:
            # cp ./INPUT_PIC/MF* ./tempMore
            commandInput = 'copy /Y .\\INPUT_PIC\\MF* .\\tempMore'
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print(e)
    else:
        try:
            # cp ./INPUT_PIC/0* ./tempNone
            commandInput = 'cp ./INPUT_PIC/0* ./tempNone'
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print("No None fece")
        try:
            # cp ./INPUT_PIC/1* ./tempSingle
            commandInput = 'cp ./INPUT_PIC/1* ./tempSingle'
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print("No Singleface")
        try:
            # cp ./INPUT_PIC/MF* ./tempMore
            commandInput = 'cp ./INPUT_PIC/MF* ./tempMore'
            commandImplementation = os.popen(commandInput)
        except Exception as e:
            print(e)


def __fileCtrl():
    """
    INPUT_PIC文价处理
    :return:
    """
    # print("File Control Start")
    input_path = join("INPUT_PIC")
    pics = (os.listdir(input_path))  # ./INPUT_PIC/*
    
    # if (len(pics)>=8)|(not WINDOWS):
    if (len(pics) >= 8) & (not WINDOWS):
        taskNum = int(len(pics) / 4)
        taskLef = len(pics) % 4
        ga = pics[0:taskNum]
        gb = pics[taskNum:taskNum * 2]
        gc = pics[taskNum * 2:taskNum * 3]
        gd = pics[taskNum * 3:taskNum * 4]
        
        thread1 = TaskSubmit("1", ga)
        thread2 = TaskSubmit("2", gb)
        thread3 = TaskSubmit("3", gc)
        thread4 = TaskSubmit("4", gd)
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
            gf = pics[taskNum * 4:taskNum * 4 + taskLef]
            thread5 = TaskSubmit("5", gf)
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
        n = 1
        for picture in pics:  # ./INPUT_PIC/xxx.jpg
            get_time = str(datetime.now()).replace(" ", "").replace(":", "")  # 获取当前时间
            # ./INPUT_PIC/xxx.jpg
            src_file = join(input_path, picture)
            if __checkFaces(picture) >= 2:
                print(__fex(src_file))
                # ./INPUT_PIC/MF{time}{ext}
                dst_file = join(input_path, "MF{0}.{1}".format(get_time, __fex(src_file)))
            else:
                dst_file = join(input_path, "{0}F{1}.{2}".format(__checkFaces(picture), get_time, __fex(src_file)))
            try:
                os.rename(src_file, dst_file)
            except Exception as e:
                print(e)
            else:
                pass
            n += 1
            print("\033[1;36;40m{} of {}\033[0m".format(n, len(pics)))


class TaskSubmit(threading.Thread):
    def __init__(self, id, listIn):
        threading.Thread.__init__(self)
        self.id = id
        self.listIn = listIn
    
    def run(self):
        print("开始线程：" + self.id + "\n")
        doTask(self.listIn)
        print("退出线程：" + self.id + "\n")


def doTask(listIn):
    n = 1
    total = len(listIn)
    for x in listIn:
        # 获取当前时间
        get_time = str(datetime.now()).replace(" ", "").replace(":", "")
        src_file = join("INPUT_PIC", x)
        if __checkFaces(x) >= 2:
            dst_file = join("INPUT_PIC", "MF{0}.{1}".format(get_time, __fex(src_file)))
        else:
            dst_file = join("INPUT_PIC", "{0}F{1}.{2}".format(__checkFaces(x), get_time, __fex(src_file)))
        try:
            os.rename(src_file, dst_file)
        except Exception as e:
            print(e)
        m_Wait.view(n, total, "31", "")
        n += 1

        
def FindFaces():
    """
    # mainX
    :return:
    """
    print("\033[5;33;40m开始分类待识别的照片....\033[0m\n")
    __renameFile()
    __fileCtrl()
    __copyFiles()
    print("\033[1;32;41m{0}\033[0m".format(ERROR_REPORT))


if __name__ == "__main__":
    FindFaces()
    print("\n\033[5;31;40m待识别文件分类结束，接下来请人工复审temp*目录下的文件是否正确分类，如下方有报错，请忽略。\033[0m\n")
