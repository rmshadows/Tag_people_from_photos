#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
同训练脚本，只不过是四线程
记得修改最后一行main方法中的参数，因为KnownTest是调试程序用的训练数据
'''
import os
import pickle
import threading
from datetime import datetime
from math import sqrt
from os import listdir
from os.path import isdir, join

import face_recognition
from face_recognition import face_locations
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn import neighbors

import m_Wait

WINDOWS = os.sep == "\\"
SS = os.sep
verbose = True


def __train(train_dir, model_save_path="", verbose=False, n_neighbors=None, knn_algo='ball_tree'):
    """
    训练模型的方法
    :param train_dir: 训练材料文件夹
    :param model_save_path:  模型保存路径
    :param verbose:  是否可视化
    :param n_neighbors:
    :param knn_algo:
    :return:
    """
    X = []
    y = []
    T1 = []
    T2 = []
    T3 = []
    T4 = []
    person = listdir(train_dir)
    if (len(person) > 10) & (not WINDOWS):
        group = (int)(len(person) / 4)
        left = len(person) % 4
        # print(group)
        gbn = group * 2
        gcn = group * 3
        gdn = group * 4
        ga = person[0:group]
        gb = person[group:gbn]
        gc = person[gbn:gcn]
        gd = person[gcn:gdn]
        if left == 0:
            pass
        else:
            gd = gd + person[gdn:gdn + left]
        thread1 = TaskSubmit("1", train_dir, ga, T1, 31)
        thread2 = TaskSubmit("2", train_dir, gb, T2, 34)
        thread3 = TaskSubmit("3", train_dir, gc, T3, 32)
        thread4 = TaskSubmit("4", train_dir, gd, T4, 36)
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        X = thread1.returnX() + thread2.returnX() + thread3.returnX() + thread4.returnX()
        y = thread1.returnY() + thread2.returnY() + thread3.returnY() + thread4.returnY()
    else:
        TASK = __calcTask(train_dir)
        n = 0
        num = 1
        for class_dir in listdir(train_dir):
            n += 1
            print("\n\033[1;33;40m添加第{}个训练对象 \033[0m:\033[1;36;40m".format(n) + class_dir + "\033[0m")
            if not isdir(join(train_dir, class_dir)):
                continue
            for img_path in image_files_in_folder(join(train_dir, class_dir)):
                image = face_recognition.load_image_file(img_path)
                if verbose:
                    print("\033[1;34;40m添加第({0}/{1})个文件 \033[0m:\033[1;38;40m".format(num, TASK) + img_path + "\033[0m")
                if not WINDOWS:
                    m_Wait.view(num, TASK, "31", "")
                num += 1
                faces_bboxes = face_locations(image)
                if len(faces_bboxes) != 1:
                    if verbose:
                        print("\033[1;31;40mWARN："
                              "\033[0m image {} not fit "
                              "for __training: {}".format(img_path,
                                                          "didn't find a face" if len(
                                                              faces_bboxes) < 1 else "found more than one face"))
                    continue
                X.append(face_recognition.face_encodings(image, known_face_locations=faces_bboxes)[0])
                y.append(class_dir)
    
    if n_neighbors is None:
        n_neighbors = int(round(sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically as:", n_neighbors)
    
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)
    print("Generating...")
    if model_save_path != "":
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
    return knn_clf


def __calcTask(path):
    """
    计算任务量
    :param path:
    :return:
    """
    dirs = listdir(path)
    task = 0
    for person in dirs:
        sub_dir = join(path, person)
        num = len(listdir(sub_dir))
        task = task + num
    return task


def doTask(train_dir, listIn, Temp, id, color):
    X = []
    y = []
    T = 0
    for x in listIn:
        T = T + len(listdir(join(train_dir, x)))
    n = 1
    for class_dir in listIn:  # Person
        if verbose:
            print("\033[1;{0};40m线程-".format(color) + id + "-正在添加：\033[0m:" + class_dir)
        if not isdir(join(train_dir, class_dir)):  # 跳过目录
            continue
        for img_path in image_files_in_folder(join(train_dir, class_dir)):
            # print("\033[1;33;40m-"+id+"-进度:\033[0m\033[1;36;40m({0}/{1})\033[0m".format(n,T))
            if (not verbose):
                if not WINDOWS:
                    m_Wait.view(n, T, color, " ")
            n += 1
            image = face_recognition.load_image_file(img_path)
            faces_bboxes = face_locations(image)
            if len(faces_bboxes) != 1:
                continue
            X.append(face_recognition.face_encodings(image, known_face_locations=faces_bboxes)[0])
            y.append(class_dir)
    listIn.clear()
    Temp.clear()
    listIn = X
    Temp = y
    return listIn, Temp


class TaskSubmit(threading.Thread):
    def __init__(self, id, train_dir, listIn, Temp, color):
        threading.Thread.__init__(self)
        self.id = id
        self.train_dir = train_dir
        self.listIn = listIn
        self.Temp = Temp
        self.color = color
    
    def returnX(self):
        try:
            return self.X
        except Exception:
            return None
    
    def returnY(self):
        try:
            return self.y
        except Exception:
            return None
    
    def run(self):
        if verbose:
            print("开始线程：" + self.id + "\n")
        X, y = doTask(self.train_dir, self.listIn, self.Temp, self.id, self.color)
        if verbose:
            print("退出线程：" + self.id + "\n")
        self.X = X
        self.y = y

        
def main(train_dir, model_save_path):
    """
    # mainX
    :param train_dir:
    :param model_save_path:
    :return:
    """
    print("\033[5;33;40m开始训练模型(4线程)....\033[0m\n")
    get_time = str(datetime.now()).replace(":", "").replace(" ", "")
    if WINDOWS:
        # ./F/T/
        knn_clf = __train(join("FR_DATA", "{0}{1}".format(train_dir, get_time)),
                          join("KNN_MOD", model_save_path),
                          verbose)
    else:
        knn_clf = __train(join("FR_DATA", train_dir),
                          join("KNN_MOD", "{0}{1}".format(model_save_path, get_time)),
                          verbose)
    print("\n\033[5;31;40m模型训练结束，已经导出到KNN_MOD文件夹下。\033[0m\n")


if __name__ == "__main__":
    # 训练的文件夹/输出模型文件名
    # main("KnowTest","KnownTest")
    main("A-KnownPeople", "KnownPeople")
