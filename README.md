 ### 简单人脸管理

 - 版本：Python 3.8

 - 平台：仅支持Linux

 - 用途：仅限于个人使用，协助照片分类，帮助标记人物。本项目基于 face_recognition > https://github.com/ageitgey/face_recognition

 ### 安装：
 
 首先安装face_recognition模块(需要sudo权限、cmake `sudo apt install cmake` 等，dlib要编译)。具体可以参考face_recognition的[中文文档](https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md)：
 
 `sudo pip install face_recognition`
 
 国内用户可以用清华镜像，快很多(后面如果报错说缺什么模块的，一样。`pip install xxx` ,记得看下`pip --version` 是哪个python版本的pip。)：
 
 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple face_recognition`
 
 - 关于修改pip：
 
 `type pip`查看pip在哪里
 
 `vi /usr/bin/pip` 假如pip在“/usr/bin/”下，用vi打开，把#!后面的打开pip的python改成3.8版本就是(前提是你装了python3.8)。
 
 `git clone https://github.com/rmshadows/Tag_people_from_photos`
 
 `cd Tag_people_from_photos`
 
 第一次使用请执行：
 
 `sudo chmod +x RESET_FRS.sh`

 `./RESET_FRS.sh`
 
 - 使用：
 
 `python3 xxx.py`
 
文件分类（前缀）：

- a-本地人像识别库处理

- b-模型训练操作

- c-待识别图片预处理

- d-主程序（开始识别）

- e-清除工作

- f-演示Demo

- g-其他

 ### 标准流程：
 
 注:=======>是要人工参与审核的步骤
 
一、添加已知人像：得有已知人像库才能进行人脸识别。所以这一步是添加已知人脸.

1.将人像文件夹放入Prescreen中：PrescreenPicture.py 过滤不合适的图像。
注意：人名中不可出现“-”

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

=======>2.人工复查Perscreen文件夹中的文件，确认无误：AddKnownPerson.py添加到已知人像库。    FR_DATA/A-KnownPeople/

二、建立已知人像库模型到KNN_MOD：

单线程：TrainingOneProcessing.py

4线程：Four_processing_training.py

10线程：Training_multi_processing_of_Ten.py

[10线程好像并没有更快的样子，略过吧。]

三、待识别文件处理：

1.FindFaces.py 分配文件到temp目录。

=======>2.到temp目录检查文件是否正确

四、开始识别：

1.FaceRecognition_KNN.py

=======>2.到temp目录检查识别结果是否正确

3.Moved2Data.py添加识别后的文件到数据库。

 ### 其他：
一、有演示用的Demo：

FaceRecognitionDemo：演示人脸识别。可以直接识别已训练的世界知名人物5000人。

TrainingDemo：演示训练。训练完后的模型保存在KNN_MOD，需要自己修改FaceRecognitionDemo中的参数才能使用。

二、清空已识别的人物数据：

ebCLEAN_UP_FRed.py

三、清除所有FRS数据：

RESET_FRS.sh

四、查找某人：

gaFindSomebody.py

五、重新识别已识别人物

gbReFaceRecognition.py

 ### 截屏

![0](https://images.gitee.com/uploads/images/2020/0627/230648_1e922454_7423713.png "屏幕截图.png")
![1](https://images.gitee.com/uploads/images/2020/0627/230714_fe2be21f_7423713.png "屏幕截图.png")
![2](https://images.gitee.com/uploads/images/2020/0627/230730_b25555a8_7423713.png "屏幕截图.png")
![3](https://images.gitee.com/uploads/images/2020/0627/230747_9f5f01ec_7423713.png "屏幕截图.png")
![4](https://images.gitee.com/uploads/images/2020/0627/230807_f8aeb779_7423713.png "屏幕截图.png")

 ### 许可
 
[LICENSE](https://github.com/rmshadows/Tag_people_from_photos/blob/master/LICENSE)

 ### 感谢
 
 再次感谢face_recognition项目 > https://github.com/ageitgey/face_recognition
