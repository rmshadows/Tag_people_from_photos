#!/bin/bash
# 用于生成可用的发行版

# 生成文件夹名
RELEASE='FaceRecognitionAuxiliary'

mkdir $RELEASE
# 复制脚本
cp -r * $RELEASE
cd $RELEASE
rm -r $RELEASE
rm -r ./FR_DATA
mkdir ./FR_DATA
mkdir ./FR_DATA/A-KnownPeople ./FR_DATA/B-Unknown ./FR_DATA/C-Noneface ./FR_DATA/D-Singleface ./FR_DATA/E-Morefaces
rm -r ./INPUT_PIC/*
rm -r ./Prescreen/*
rm -r ./tempMore/*
rm -r ./tempNone/*
rm -r ./tempSingle/*
rm -r ./temp/*
rm -r ./tempFaceRecognition/*



