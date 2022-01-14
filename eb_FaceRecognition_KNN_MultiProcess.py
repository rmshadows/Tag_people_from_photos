#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
识别temp目录中已经分好类的图片，最后一行的参数是修改识别所用的模型KNN_MOD中是我训练好了的一些人物。

This is an example of using the k-nearest-neighbors (KNN) algorithm for face recognition.
When should I use this example?
This example is useful when you wish to recognize a large set of known people,
and make a prediction for an unknown person in a feasible computation time.
Algorithm Description:
The knn classifier is first trained on a set of labeled (known) faces and can then predict the person
in an unknown image by finding the k most similar faces (images with closet face-features under eucledian distance)
in its training set, and performing a majority vote (possibly weighted) on their label.
For example, if k=3, and the three closest face images to the given image in the training set are one image of Biden
and two images of Obama, The result would be 'Obama'.
* This implementation uses a weighted vote, such that the votes of closer-neighbors are weighted more heavily.
Usage:
1. Prepare a set of images of the known people you want to recognize. Organize the images in a single directory
   with a sub-directory for each known person.
2. Then, call the 'train' function with the appropriate parameters. Make sure to pass in the 'model_save_path' if you
   want to save the model to disk so you can re-use the model without having to re-train it.
3. Call 'predict' and pass in your trained model to recognize the people in an unknown image.
NOTE: This example requires scikit-learn to be installed! You can install it with pip:
$ pip3 install scikit-learn
'''
import os
import pickle
import threading
import time
from datetime import datetime
from os import listdir
from os.path import join, isfile, splitext

import face_recognition
import numpy as np
import psutil
from PIL import Image, ImageFont, ImageDraw
from face_recognition import face_locations

import m_Wait

SEE_ALL_FACES = False
WINDOWS = os.sep == "\\"
SS = os.sep
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ERROR_REPORT = ""
CQUA = 0.2


def __getSize(path):
    s = os.path.getsize(path)
    return s


def __predict(X_img_path, knn_clf=None, model_save_path="", DIST_THRESH=0.2):
    isCprs = False
    """
    recognizes faces in given image, based on a trained knn classifier
    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_save_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param DIST_THRESH: (optional) distance threshold in knn classification. the larger it is, the more chance of misclassifying an unknown person to a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'N/A' will be passed.
    """
    if not isfile(X_img_path) or splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("invalid image path: {}".format(X_img_path))
    
    if knn_clf is None and model_save_path == "":
        raise Exception("must supply knn classifier either thourgh knn_clf or model_save_path")
    if knn_clf is None:
        with open(model_save_path, 'rb') as f:
            knn_clf = pickle.load(f)
    # 如果图片大于1.5M，压缩。
    if (__getSize(X_img_path) >= 1500000):
        img = Image.open(X_img_path)
        w, h = img.size
        qua = CQUA
        w, h = round(w * qua), round(h * qua)
        img = img.resize((w, h), Image.ANTIALIAS)
        X_img = np.array(img)
        print("压缩图片...")
        isCprs = True
    else:
        X_img = face_recognition.load_image_file(X_img_path)
    # X_img = face_recognition.load_image_file(X_img_path)
    X_faces_loc = face_locations(X_img)
    if len(X_faces_loc) == 0:
        return []
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_faces_loc)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    is_recognized = [closest_distances[0][i][0] <= DIST_THRESH for i in range(len(X_faces_loc))]
    # predict classes and cull classifications that are not with high confidence
    return [(pred, loc) if rec else ("N/A", loc) for pred, loc, rec in
            zip(knn_clf.predict(faces_encodings), X_faces_loc, is_recognized)], isCprs


def __show_prediction_labels_on_image(name, ext, img_path, predictions, isCprs):
    """
    Shows the face recognition results visually.

    :param img_path: path to image to be recognized
    :param predictions: results of the predict function
    :return:
    """
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)
    
    word_css = join("zh.ttf")
    font = ImageFont.truetype(word_css, 20)
    
    for name, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        if isCprs:
            A = left / CQUA
            B = top / CQUA
            C = right / CQUA
            D = bottom / CQUA
            draw.rectangle(((A, B), (C, D)), outline=(0, 0, 255))
        else:
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        
        print("Drawing" + name)
        # name = name.encode("UTF-8")
        
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        if isCprs:
            A = left / CQUA
            B = (bottom - text_height + 20) / CQUA
            C = right / CQUA
            D = bottom / CQUA
            # 文字位置
            E = (left + 6) / CQUA
            F = (bottom - text_height + 13) / CQUA
            draw.rectangle(((A, B), (C, D)), fill=(0, 0, 255), outline=(0, 0, 255))
            # word_css  = ".{0}msyh.ttc".format(SS)
            word_css = join("zh.ttf")
            font = ImageFont.truetype(word_css, 20)
            
            draw.text((E, F), name, font=font, fill=(255, 255, 255, 255))
        else:
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, font=font, fill=(255, 255, 255, 255))
    del draw
    
    # Display the resulting image
    if (SEE_ALL_FACES):
        pil_image.show()
    get_time = str(datetime.now())[17:]
    # 保存识别的图片
    pa = join("tempFaceRecognition", "{0}{1}.{2}".format(name, get_time, ext))
    pil_image.save(pa.replace("N/A", ""))


# 得到扩展名
def __fex(path):
    ex = os.path.splitext(path)[1]
    return ex[1:]


def __faceRec(toRec, mod, dist):
    global ERROR_REPORT
    TASK = listdir(join(toRec))  # ./folder/*
    if len(TASK) < 20 | WINDOWS:
        for img_path in TASK:  # ./folder/*
            if img_path != ".keep":
                NA = ""  # Name
                ext = __fex(join(toRec, img_path))  # get ext
                # ./folder/xxx.jpg  None  ./KNN_MOD/{model}
                try:
                    preds, isCprs = __predict(join(toRec, img_path), None,
                                      join("KNN_MOD", mod), dist)
                    for name, (top, right, bottom, left) in preds:
                        NA = name
                        print("- Found \033[1;32;40m{}\033[0m at ({}, {})".format(name, left, top))
                    # Name  ext  ./{folder}/xxx.jpg  preds
                    __show_prediction_labels_on_image(NA, ext, join(toRec, img_path), preds, isCprs)
                    
                    if len(preds) == 0:
                        print("ERROR-None face")
                    if len(preds) == 1:
                        src_file = join(toRec, img_path)
                        # 获取当前时间
                        get_time = str(datetime.now())[17:]
                        if preds[0][0] == "N/A":
                            dst_file = join(toRec, "unknown-{0}.{1}".format(get_time, __fex(src_file)))
                        else:
                            dst_file = join(toRec, "{0}-{1}.{2}".format(preds[0][0], get_time, __fex(src_file)))
                        # 显示正处理的文件
                        print(dst_file)
                        try:
                            os.rename(src_file, dst_file)
                        except Exception as e:
                            print(e)
                        else:
                            pass
                    else:
                        if __fex(join(toRec, img_path)) == "png":
                            __tagPeople("png", toRec, img_path, preds)
                        if __fex(join(toRec, img_path)) == "jpg":
                            __tagPeople("jpg", toRec, img_path, preds)
                        if __fex(join(toRec, img_path)) == "jpeg":
                            __tagPeople("jpeg", toRec, img_path, preds)
                except Exception as e:
                    ERROR_REPORT = "{}\n{}{}".format(ERROR_REPORT, e, img_path)
        # raise e
    else:
        taskNum = int(len(TASK) / 4)
        taskLef = len(TASK) % 4
        # 创建新线程
        thread1 = __TaskSubmit("1", TASK[0:taskNum], toRec, mod, dist)
        thread2 = __TaskSubmit("2", TASK[taskNum:taskNum * 2], toRec, mod, dist)
        thread3 = __TaskSubmit("3", TASK[taskNum * 2:taskNum * 3], toRec, mod, dist)
        thread4 = __TaskSubmit("4", TASK[taskNum * 3:taskNum * 4], toRec, mod, dist)
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
            thread5 = __TaskSubmit("5", TASK[taskNum * 4:taskNum * 4 + taskLef], toRec, mod, dist)
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


def __tagPeople(fext, toRec, img_path, preds):
    n = 1
    tempName = join(toRec, img_path)
    for x in preds:
        src_file = tempName
        print("文件{0}:".format(img_path), end="")
        print("发现:" + x[0], end="  ")
        if x[0] == "N/A":
            if n == 1:
                get_time = str(datetime.now())[17:]
                dst_file = join(toRec, "unknown{0}".format(get_time))
            else:
                get_time = str(datetime.now())[17:]
                dst_file = "{0}-{1}{2}".format(tempName[:-9], "unknown", get_time)
            n += 1
        else:
            if n == 1:
                get_time = str(datetime.now())[17:]
                dst_file = join(toRec, "{0}{1}".format(x[0], get_time))
            else:
                get_time = str(datetime.now())[17:]
                dst_file = "{0}-{1}{2}".format(tempName[:-9], x[0], get_time)
            n += 1
        try:
            tempName = dst_file
            os.rename(src_file, dst_file)
        except Exception as e:
            print(e)
    src_file = tempName
    get_time = str(datetime.now())[17:]
    dst_file = "{0}-{1}.{2}".format(tempName[:-9], get_time, fext)
    try:
        os.rename(src_file, dst_file)
    except Exception as e:
        print(e)
    print("\n")


def doTask(who, toRec, mod, dist):
    global ERROR_REPORT
    ta = 0
    for img_path in who:  # ./folder/*
        if img_path != ".keep":
            ta += 1
            m_Wait.view(ta, len(who), "31", "")
            NA = ""  # Name
            ext = __fex(join(toRec, img_path))  # get ext
            # ./folder/xxx.jpg  None  ./KNN_MOD/{model}
            try:
                preds, isCprs = __predict(join(toRec, img_path), None,
                                          join("KNN_MOD", mod), dist)
                for name, (top, right, bottom, left) in preds:
                    NA = name
                    print("- Found \033[1;32;40m{}\033[0m at ({}, {})".format(name, left, top))
                __show_prediction_labels_on_image(NA, ext, join(toRec, img_path), preds, isCprs)
                # time.sleep(0.2)
                if len(preds) == 0:
                    print("ERROR-None face")
                if len(preds) == 1:
                    src_file = join(toRec, img_path)
                    get_time = str(datetime.now())[17:]
                    if preds[0][0] == "N/A":
                        dst_file = join(toRec, "unknown-{0}.{1}".format(get_time, __fex(src_file)))
                    else:
                        dst_file = join(toRec, "{0}-{1}.{2}".format(preds[0][0], get_time, __fex(src_file)))
                    # 显示正处理的文件
                    print(dst_file)
                    try:
                        os.rename(src_file, dst_file)
                    except Exception as e:
                        print(e)
                    else:
                        pass
                else:
                    if __fex(join(toRec, img_path)) == "png":
                        __tagPeople("png", toRec, img_path, preds)
                    if __fex(join(toRec, img_path)) == "jpg":
                        __tagPeople("jpg", toRec, img_path, preds)
                    if __fex(join(toRec, img_path)) == "jpeg":
                        __tagPeople("jpeg", toRec, img_path, preds)
            except Exception as e:
                ERROR_REPORT = "".format(ERROR_REPORT, e, img_path)
            # raise e


class __TaskSubmit(threading.Thread):
    def __init__(self, id, who, toRec, mod, dist):
        threading.Thread.__init__(self)
        self.id = id
        self.who = who
        self.toRec = toRec
        self.mod = mod
        self.dist = dist
        self.result = "1"
    
    def run(self):
        print("开始线程：" + self.id + " on stat " + self.result)
        doTask(self.who, self.toRec, self.mod, self.dist)
        self.result = "0"
        print("退出线程：" + self.id + " on stat " + self.result)


def __killPro(second, pro):
    time.sleep(second)
    print("展示时间：" + str(second) + "秒")
    for proc in psutil.process_iter():  # 遍历当前process
        if proc.name() == pro:  # 如果process的name是display
            proc.kill()  # 关闭该process


# SystemExit()

def __move2temp():
    """
    把无法精确识别的图片移动到temp
    :return:
    """
    if WINDOWS:
        try:
            # move .\Prescreen\{name} .\FR_DATA\A-KnownPeople\
            commandInput = "move /Y .\\tempSingle\\unknown* .\\temp\\"
            commandImplementation = os.popen(commandInput)
            print("Moving file")
        except Exception as e:
            raise e
    else:
        try:
            # mv ./Prescreen/{name} ./FR_DATA/A-KnownPeople/
            commandInput = "mv ./tempSingle/unknown* ./temp/"
            commandImplementation = os.popen(commandInput)
            print("Moving file...")
        except Exception as e:
            raise e


def __firmly2tempS():
    """
    temp到tempSingle
    :return:
    """
    if WINDOWS:
        try:
            # move .\Prescreen\{name} .\FR_DATA\A-KnownPeople\
            commandInput = "move /Y .\\temp\\* .\\tempSingle\\"
            commandImplementation = os.popen(commandInput)
            print("Moving file")
        except Exception as e:
            raise e
    else:
        try:
            # mv ./Prescreen/{name} ./FR_DATA/A-KnownPeople/
            commandInput = "mv ./temp/* ./tempSingle/"
            commandImplementation = os.popen(commandInput)
            print("Moving file...")
        except Exception as e:
            raise e


# mainX
def FaceRecognitionKNN(model_name):
    print("Moving files in temp to tempSingle...")
    __firmly2tempS()
    m_Wait.waiting(1.5)
    print("\033[5;33;40m开始识别tempSingle目录下的分类文件(单线程)....\033[0m\n")
    print("处理单人面孔(dist=0.2)：")
    __faceRec("tempSingle", model_name, 0.2)
    m_Wait.waiting(1)
    # 不确定的放在temp文件夹
    __move2temp()
    m_Wait.waiting(1)
    print("处理单人面孔：(dist=0.6)")
    __faceRec("temp", model_name, 0.6)
    m_Wait.waiting(1)
    print("处理多人面孔：(dist=0.6)")
    __faceRec("tempMore", model_name, 0.6)
    print("\033[1;32;41m{0}\033[0m".format(ERROR_REPORT))
    print("\033[5;31;40m--------识别完毕--------\033[0m")


if __name__ == "__main__":
    FaceRecognitionKNN("KnownPeople")
    if SEE_ALL_FACES:
        # 延时5秒
        __killPro(5, "display")
        SystemExit()
    print("\n\033[5;31;40m识别完毕,接下来请再次到temp*目录下人工复审识别结果(注意：temp目录中是不确定的识别)。\033[0m\n")
