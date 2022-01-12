# -*- coding: utf-8 -*-

from PIL import Image
import face_recognition
import os
from datetime import datetime
import threading
import time
import numpy as np
import Wait

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

# 获取文件大小
def __getSize(path):
    s = os.path.getsize(path)
    return s


# 返回扩展名
def __fex(path):
    ex = os.path.splitext(path)[1]
    return ex[1:]


# 重命名
def __renameFile():
    dir = ".{0}INPUT_PIC".format(SS)  # ./INPUT_PIC
    pic = (os.listdir(dir))  # ./INPUT_PIC/*
    for file in pic:
        time = datetime.now()
        # ./INPUT_PIC/xxx.jpg
        # srcFile = dir + SS + file
        srcFile = os.path.join(dir, file)
        # ./INPUT_PIC/{time}.{ext}
        TI = str(time).replace(" ", "")
        dstFile = dir + SS + "{0}.{1}".format(TI.replace(":", ""), __fex(srcFile))
        try:
            os.rename(srcFile, dstFile)
        except Exception as e:
            print(e)
        else:
            pass
    pic = (os.listdir(dir))  # ./INPUT_PIC/*
    n = 1
    for file in pic:
        srcFile = dir + SS + file  # ./INPUT_PIC/xxx.jpg
        # ./INPUT_PIC/{n}.{ext}
        dstFile = dir + SS + "{0}.{1}".format(n, __fex(srcFile))
        try:
            os.rename(srcFile, dstFile)
        except Exception as e:
            print(e)
        else:
            pass
        n += 1


def __checkFaces(file):
    global ERROR_REPORT
    try:
        # Load the jpg file into a numpy array
        inputPic = ".{0}INPUT_PIC{1}".format(SS, SS) + file
        # 如果图片大于1.5M，压缩。
        if (__getSize(inputPic) >= 1500000):
            img = Image.open(inputPic)

            w, h = img.size
            qua = 0.2
            w, h = round(w * qua), round(h * qua)
            img = img.resize((w, h), Image.ANTIALIAS)
            image = np.array(img)
            print("压缩图片...")
        else:
            image = face_recognition.load_image_file(inputPic)
        # print("加载完成	")

        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py

        # face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        face_locations = face_recognition.face_locations(image)
        # print("定位完成")
        faceNum = len(face_locations)
        print("Found \033[1;33;40m{0} face(s)\033[0m: in \033[1;35;40m{1} photograph.\033[0m:".format(faceNum, file),
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
    except Exception as e:
        # raise e
        ERROR_REPORT = "{0}\n{1}{2}".format(ERROR_REPORT, e, file)
        print(e)
    return faceNum


def __copyFiles():
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
    # print("File Control Start")
    dir = ".{0}INPUT_PIC".format(SS)
    pic = (os.listdir(dir))  # ./INPUT_PIC/*

    # if (len(pic)>=8)|(not WINDOWS):
    if (len(pic) >= 8) & (not WINDOWS):
        taskNum = int(len(pic) / 4)
        taskLef = len(pic) % 4
        ga = pic[0:taskNum]
        gb = pic[taskNum:taskNum * 2]
        gc = pic[taskNum * 2:taskNum * 3]
        gd = pic[taskNum * 3:taskNum * 4]

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
            gf = pic[taskNum * 4:taskNum * 4 + taskLef]
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
        for file in pic:  # ./INPUT_PIC/xxx.jpg
            time = datetime.now()  # 获取当前时间
            srcFile = dir + SS + file  # ./INPUT_PIC/xxx.jpg
            if __checkFaces(file) >= 2:
                print(__fex(srcFile))
                # ./INPUT_PIC/MF{time}{ext}
                TI = str(time).replace(" ", "")
                dstFile = dir + SS + "MF{0}.{1}".format(TI.replace(":", ""), __fex(srcFile))
            else:
                TI = str(time).replace(" ", "")
                dstFile = dir + SS + "{0}F{1}.{2}".format(__checkFaces(file), TI.replace(":", ""), __fex(srcFile))
            try:
                os.rename(srcFile, dstFile)
            except Exception as e:
                print(e)
            else:
                pass
            n += 1
            print("\033[1;36;40m{} of {}\033[0m".format(n, len(pic)))


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
        time = datetime.now()  # 获取当前时间
        srcFile = ".{0}INPUT_PIC{1}{2}".format(SS, SS, x)
        if __checkFaces(x) >= 2:
            TI = str(time).replace(" ", "")
            dstFile = ".{0}INPUT_PIC{1}MF{2}.{3}".format(SS, SS, TI.replace(":", ""), __fex(srcFile))
        else:
            TI = str(time).replace(" ", "")
            dstFile = ".{0}INPUT_PIC{1}{2}F{3}.{4}".format(SS, SS, __checkFaces(x), TI.replace(":", ""), __fex(srcFile))
        try:
            os.rename(srcFile, dstFile)
        except Exception as e:
            print(e)
        Wait.view(n, total, "31", "")
        n += 1


# mainX
def FindFaces():
    print("\033[5;33;40m开始分类待识别的照片....\033[0m\n")
    __renameFile()
    __fileCtrl()
    __copyFiles()
    print("\033[1;32;41m{0}\033[0m".format(ERROR_REPORT))


if __name__ == "__main__":
    FindFaces()
    print("\n\033[5;31;40m待识别文件分类结束，接下来请人工复审temp*目录下的文件是否正确分类，如下方有报错，请忽略。\033[0m\n")
