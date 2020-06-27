 ### 简单人脸管理

 - 版本：Python 3.8

 - 平台：仅支持Linux

 - 用途：仅限于个人使用，协助照片分类，帮助标记人物。本项目基于 face_recognition > https://github.com/ageitgey/face_recognition

 ### 安装：
 
 首先安装face_recognition模块：
 `sudo pip install face_recognition`
 
 `git clone https://github.com/rmshadows/Tag_people_from_photos`
 
 `cd Tag_people_from_photos`
 
 第一次使用请执行：
 `sudo chmod +x RESET_FRS.sh`

 `./RESET_FRS.sh`
 
文件分类（前缀）：

- a-本地人像识别库处理

- b-模型训练操作

- c-待识别图片预处理

- d-主程序（开始识别）

- e-清除工作

- f-演示Demo

- g-其他

 ### 标准流程：
 
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

=======>2.人工复查Perscreen文件夹中的文件，确认无误：0-1-AddKnownPerson.py添加到已知人像库。    FR_DATA/A-KnownPeople/

二、建立已知人像库模型到KNN_MOD：
单线程：TrainingOneProcessing.py
4线程：Four_processing_training.py
10线程：Training_multi_processing_of_Ten.py

三、待识别文件处理：
1.2-0-FindFaces.py 分配文件到temp目录。

=======>2.到temp目录检查文件是否正确

四、开始识别：
FaceRecognition_KNN.py

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












