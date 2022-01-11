#!/bin/bash
# 用于复制新的脚本到应用文件夹

set -uex

# 文件夹路径
FolderPath='FaceRecognitionAuxiliary'

if ! [ -d $FolderPath ];then
  echo "没有这个文件夹"
  exit 1
fi

# 复制脚本
cp *.py $FolderPath
cp *.sh $FolderPath
cp *.bat $FolderPath
cp *.md $FolderPath
cp LICENSE $FolderPath
cp *.txt $FolderPath
cp *.ttf $FolderPath
rm -r $FolderPath/__pycache__
