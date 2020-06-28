 ### 简单人脸管理

 - 版本：Python 3

 - 平台：仅支持Linux Windows用户可以试用我搭建好了的[虚拟机](https://pan.baidu.com/s/1ULEPSIigSrtbVC4QHHMw2Q)[提取码：90km]。虚拟系统是基于Ubuntu的Linux_lite系统，界面与windows较像且体积较小（4.8G），固采用。注意：虚拟机里的faxxxdemo脚本可能无法正常运行，但你只需要把demo中的Moving方法注释掉，或者分步运行就没问题了。算是个小小的bug吧，因为物理机里运行没这个问题。（Note:The faxxxdemo.py may not work correct in virtual machine ,but just comment out the dbMoved2Data.Moving() method and run dbMoved2Data.Moving() separately ,it will work correctly.）

![vbox](https://images.gitee.com/uploads/images/2020/0628/212812_1ca99837_7423713.png "屏幕截图.png")

 - 用途：仅限于个人使用，协助照片分类，帮助标记人物。本项目基于 face_recognition > https://github.com/ageitgey/face_recognition

 - 原理：通过训练一个模型来识别人脸。所以首先要训练模型（用已知人物照片作为训练内容）。训练完成就可以进行人脸识别了。

 ### 目录结构：

![constru](https://images.gitee.com/uploads/images/2020/0628/113927_8d40ba65_7423713.png "屏幕截图.png")

 ### 安装：
 
 首先：更新你的python3和pip：`apt-get update` `apt-get upgrade python3` `apt upgrade python3-pip`

 然后安装face_recognition模块(需要sudo权限、cmake `sudo apt-get install cmake` 等，dlib要编译)。具体可以参考face_recognition的[中文文档](https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md)：
 
 `sudo pip3 install face_recognition`
 
 国内用户可以用清华镜像，快很多(后面如果报错说缺什么模块的，一样。`pip install xxx` ,记得看下`pip --version` 是哪个python版本的pip。)：
 
 `pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple face_recognition`

 安装其他依赖：`pip3 install -r requirements.txt`
 
 - 关于修改pip(可以忽略不看)：
 
 `type pip`查看pip在哪里
 
 `vi /usr/bin/pip` 假如pip在“/usr/bin/”下，用vi打开，把#!后面的打开pip的python改成3.8版本就是(前提是你装了python3.8)。
 
 `git clone https://github.com/rmshadows/Tag_people_from_photos`
 
 `cd Tag_people_from_photos`

 ### 使用
 
 第一次使用请执行：
 
 `sudo chmod +x RESET_FRS.sh`

 `./RESET_FRS.sh`
 
 - 使用：
 
 `python3 xxx.py`
 
 脚本文件分类（前缀）：

- a-本地人像识别库处理

- b-模型训练操作

- c-待识别图片预处理

- d-主程序（开始识别）

- e-清除工作

- f-演示Demo

- g-其他

 ### 标准流程：
 
 注:标记“=======>”的是要人工参与重复审核的步骤，保证数据正确性。
 
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

FaceRecognitionDemo.py：演示人脸识别。可以直接识别已训练的世界知名人物5000人。

TrainingDemo.py：演示训练。训练完后的模型保存在KNN_MOD，需要自己修改FaceRecognitionDemo中的参数才能使用。

二、清空已识别的人物数据：

ebCLEAN_UP_FRed.py

三、清除所有FRS数据：

RESET_FRS.sh

四、查找某人：

gaFindSomebody.py

五、重新识别已识别人物

gbReFaceRecognition.py

 ### 截屏

- 训练模型：

![0](https://images.gitee.com/uploads/images/2020/0628/110830_d8900709_7423713.png "屏幕截图.png")

 - 识别中...

![2](https://images.gitee.com/uploads/images/2020/0627/230730_b25555a8_7423713.png "屏幕截图.png")

 - 识别单人面孔（每人一个文件夹）：

![4](https://images.gitee.com/uploads/images/2020/0628/110924_cd058f8a_7423713.png "屏幕截图.png")

 - 识别多人面孔（注意文件名，两个人的名字）：

![5](https://images.gitee.com/uploads/images/2020/0628/111010_05ef2cc7_7423713.png "屏幕截图.png")


 ### 许可
 
[LICENSE](https://github.com/rmshadows/Tag_people_from_photos/blob/master/LICENSE)

 ### 感谢
 
 再次感谢face_recognition项目 > https://github.com/ageitgey/face_recognition
