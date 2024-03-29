#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
训练模型-单线程
模型文件夹：./FR_DATA/
单独运行请修改最后一行参数
因为上次调试的训练素材是G-WorldWidePeople，一直没改
'''
import os
import pickle
from datetime import datetime
from math import sqrt
from os import listdir
from os.path import isdir, join

import face_recognition
from face_recognition import face_locations
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn import neighbors

import m_Wait

verbose = False
WINDOWS = os.sep == "\\"
SS = os.sep


def __train(train_dir, model_save_path="", n_neighbors=None, knn_algo='ball_tree', verbose=False):
    """
    训练模型的方法
    :param train_dir: 训练材料
    :param model_save_path: 模型保存路径
    :param n_neighbors:
    :param knn_algo:
    :param verbose: 是否显示详情
    :return:
    """
    TASK = __calcTask(train_dir)
    X = []
    y = []
    n = 0
    num = 1
    for class_dir in listdir(train_dir):
        n += 1
        if verbose:
            print("\033[1;33;40m添加第{}个训练对象 \033[0m:\033[1;36;40m".format(n) + class_dir + "\033[0m")
        if not isdir(join(train_dir, class_dir)):
            continue
        for img_path in image_files_in_folder(join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            if verbose:
                print("\033[1;34;40m添加第({0}/{1})个文件 \033[0m:\033[1;38;40m".format(num, TASK) + img_path + "\033[0m")
            m_Wait.view(num, TASK, "32", "")
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
    
    if model_save_path != "":
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
    return knn_clf


def __calcTask(path):
    """
    # 计算任务总量
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


def main(train_dir, model_save_path):
    """
    # mainX
    :param train_dir:
    :param model_save_path:
    :return:
    """
    print("\033[5;33;40m开始训练模型(单线程)....\033[0m\n")
    get_time = str(datetime.now()).replace(":", "").replace(" ", "")
    # ./FR_DATA/"{train_dir}/		./KNN_MOD/{name}
    if WINDOWS:
        knn_clf = __train(join("FR_DATA", train_dir),
                          join("KNN_MOD", "{0}{1}".format(model_save_path, get_time)),
                          None, "ball_tree",
                          verbose)
    else:
        knn_clf = __train(join("FR_DATA", train_dir),
                          join("KNN_MOD", "{0}{1}".format(model_save_path, get_time)),
                          None,
                          "ball_tree",
                          verbose)
    print("\n\033[5;31;40m模型训练结束，已经导出到KNN_MOD文件夹下。\033[0m\n")


if __name__ == "__main__":
    # 训练的文件夹/输出模型文件名
    main("A-KnownPeople", "KnownPeople")
