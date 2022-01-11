 ### 简单de离线人脸管理

 - 版本：Python 3.9+

 - 最新版本：v1.3.3

 - 平台： 首选Linux(已测试)。Windows也可以运行(未完全测试。但据说Windows运行效率只有Linux平台的四分之一。)。OSX(未测试。苹果系统环境搭建请见原项目文档，可能需要自己修改部分源码)。

 - 用途：仅限于个人使用，协助照片分类，帮助标记人物。本项目基于 face_recognition > https://github.com/ageitgey/face_recognition

 - 原理：通过训练一个模型来识别人脸。所以首先要训练模型（用已知人物照片作为训练内容）。训练完成就可以进行人脸识别了。

 ### 目录结构（这里显示的是1.0版本的目录）：

![constru](https://images.gitee.com/uploads/images/2020/0628/113927_8d40ba65_7423713.png "屏幕截图.png")


  --+--FRS-2020-+-FR_DATA-+-A-KnownPeople-+-PersonA-+-Person1.jpg      存放已知人物图片，用于训练对象，训练时填文件夹“A-KnownPeople”
                |         |               |         +-Person2.jpg
                |         |               |         +-......
                |         |               +-PersonB-+-Person1.jpg
                |         |               |         +-Person2.jpg
                |         |               |         +-......
                |         |               +-......
                |         |                    
                |         +-B-Unknown                                   存放识别后仍未知人物图片。
                |         |                       
                |         +-C-Noneface                                  存放识别无面孔的照片（未启用）
                |         |                                  
                |         +-D-Singleface-+-PersonA-+-Person1.jpg        存放识别后已知的单面孔人物图片
                |         |              |         +-Person2.jpg
                |         |              |         +-......
                |         |              +-PersonB-+-Person1.jpg
                |         |              |         +-Person2.jpg
                |         |              |         +-......
                |         |              +-......
                |         |                  
                |         +-E-Morefaces                                 存放识别后已知的多面孔人物图片
                |                               
                +-INPUT_PIC                                             存放需要识别人物的图片
                |                     
                +-KNN_MOD                                               存放训练出的模型
                |              
                +-Prescreen-+-PersonA-+-Person1.jpg                     临时存放需要预处理的训练材料
                |           |         +-Person2.jpg
                |           |         +-......
                |           +-PersonB-+-Person1.jpg
                |           |         +-Person2.jpg
                |           |         +-......
                |           +-......
                |
                +-temp                                                  临时存放dc二次识别的单人图片
                |
                +-tempMore                                              临时存放分类好的待识别多面孔图片
                |
                +-tempNone                                              临时存放分类好的待识别无面孔图片
                |
                +-tempSingle                                            临时存放分类好的待识别单面孔图片
                |
                +-tempFaceRecognition                                   存放识别的结果，图片带有识别方框


 ### Linux从零开始安装：

1. 首先：更新你的python3和pip：`apt-get update` `apt-get upgrade python3` `apt upgrade python3-pip`

1. 然后安装face_recognition模块(需要sudo权限、cmake `sudo apt-get install cmake` 等，dlib要编译)。具体可以参考face_recognition的[中文文档](https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md)：
`sudo pip3 install face_recognition`国内用户可以用清华镜像，快很多(后面如果报错说缺什么模块的，一样。`pip install xxx` ,记得看下`pip --version` 是哪个python版本的pip。)：`pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple face_recognition`

1. 克隆本仓库：`git clone https://gitee.com/rmshadows/Tag_people_from_photos.git`

1. 安装其他依赖：`cd Tag_people_from_photos` `pip3 install -r requirements.txt`

 - 关于修改pip(可以忽略不看)：

 `type pip`查看pip在哪里

 `vi /usr/bin/pip` 假如pip在“/usr/bin/”下，用vi打开，把#!后面的打开pip的python改成3.8版本就是(前提是你装了python3.8)。

 `git clone https://github.com/rmshadows/Tag_people_from_photos`

 `cd Tag_people_from_photos`

 ### Windows从零开始安装（只测试了Win 10系统）：

 1. 安装Cmake：去[Cmake官网](https://cmake.org/download/)下载Cmake，然后把Cmake添加到系统环境变量中。

 1. 下载Python3.8：[Python官网](https://www.python.org/downloads/)，安装完记得添加python环境变量，当然还有安装目录下Script文件夹中的pip的环境变量！两个环境变量哦～

 1. 下载Visual Studio：巨硬[官网下载](https://visualstudio.microsoft.com/zh-hans/)，记住，是VS不是VSC，看清楚。下载安装包后打开，选择C++桌面应用开发，确保右边安装列表中有“Windows上的Cmake”选项打勾。

 1. 在命令行输入`python --version` 、 `pip --version` 、 `cmake` 如果三个命令都有反应，那就是OK了。

 1. 以上三个安装完毕后，打开命令行。运行`pip install pip -U`更新pipy。然后运行`pip install dlib`。等待完成，这个会久一点，因为dlib需要编译。dlib安装成功后，输入`pip install face_recognition`，这个很快的。

 1. 上面步骤都成功了，环境基本搭建完成。失败的话请挪步[这里](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)。接下来克隆本仓库，没有git的[下载](https://git-scm.com/downloads)一个或者去我[项目地址](https://gitee.com/rmshadows/Tag_people_from_photos)下载源代码包。`git clone https://github.com/rmshadows/Tag_people_from_photos`

 1. 进入项目文件夹`cd Tag_people_from_photos` 安装其他依赖包：`pip3 install -r requirements.txt`

 1. 到这里就都搭建完毕了。现在Visual Studio和Cmake你可以卸载掉。

 - Windows下默认禁用多线程方法，自己改下源码，把那个`not WINDOWS`注释掉就是。

 Windows须知：我不能保证源代码在Windows可以很好的运行，因为我在Windows上做测试的时间不多，所以有些小问题还是有各位亲们自己修改下源代码解决了。Windows用户需要 **自己搭建** [原项目(face_recognition)](https://github.com/ageitgey/face_recognition)的环境 **并修改少许源代码** ，如何搭建请参考原项目的说明文档([中文版传送门](https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md))和ISSUES中的[指南](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)。也可以试用我搭建好环境了的Linux Lite[虚拟机](https://pan.baidu.com/s/1ULEPSIigSrtbVC4QHHMw2Q)[提取码：90km]。你当然也可以使用Adam Geitgey大神为原项目提供的Ubuntu虚拟机镜像文件安装配置虚拟机（比我提供的大很多，但下载速度可能？？你们自己试试。），然后git clone本仓库。（需要电脑中安装VMWare Player，Vbox好像不能直接使用这个镜像，但没事，你可以先用vm把虚拟机导出为ova格式，就可导入VBox了。）[VBox下载](https://mirrors.tuna.tsinghua.edu.cn/help/virtualbox/)

 - **_虚拟机须知：_** 性能真的和物理机没法比，卡顿可能有，习惯就好，黑屏就重启。卡卡卡卡卡反正……所以还是自己搭建环境撒。

 -  **注意** ： **我提供的** 虚拟机中的演示已经过期(Demo in Virtual machine is out to date ,try the lastest release!)，请更新到最新版本:`git clone https://gitee.com/rmshadows/Tag_people_from_photos.git`

 -  **我提供的** 虚拟机已知问题：虚拟系统是基于Ubuntu的Linux_lite系统，界面与windows较像且体积较小（4.8G），固采用。(1)虚拟机中的AddKnowPerson.py不能正常运行，请下载最新版本的文件。addKnowPerson.py CANOT WORK CORRECTLY ，PLEASE DOWNLOAD THE LASTEST RELEASE.(2)虚拟机里的faxxxdemo脚本可能无法正常运行，但你只需要把demo中的Moving方法注释掉，或者分步运行就没问题了。算是个小小的bug吧，因为物理机里运行没这个问题。（Note:The faxxxdemo.py may not work correct in virtual machine ,but just comment out the daxxx.facerxxxKNN() method and run it separately ,it will work correctly.）

![vbox](https://images.gitee.com/uploads/images/2020/0628/212812_1ca99837_7423713.png "屏幕截图.png")


 ### 使用

 1. **第一次** 使用，Linux请执行： `sudo chmod +x RESET_FRS.sh` 和 `./RESET_FRS.sh` 。Windows用户当然是运行那个bat文件了好吧。

 1. 运行脚本： `python3 xxx.py` xxx是要运行的脚本的名字。 Windows的话一般是`python xxx.py` (只装了一个Python吧？)

 **脚本文件分类**（前缀）：

 -注：加粗的是我**自己**正在使用的，用作处理的脚本。具体你们可以根据自己的需求选择合适的脚本处理文件。

- a-本地人像识别库处理
  
  * aaPrescreenPicture:删除提供的训练材料中的多人相片和无人脸照片。
  
    - (Line27)SEE_ALL_FACES:True则显示识别出的面部信息图片。
  
    - (Line100)filePrescreen():供外部调用的方法。
  
    - (Line153)__rmFiles():注释掉后不会删除文件，可以用来检查，再手动删除不合格图像。
    
    - (Line219)__killPro(5,"display"):main方法中的killPro方法，5表示图片显示延时5秒后关闭，display表示打开的图片在进程中的名字叫做"display"。Windows记得改这个，去任务管理器寻找你的默认图片打开方式的进程叫什么，填进去。
    
  * **abAddKnownPerson**:添加处理过的训练材料到A-KnownPeople中。并自动平衡每个文件夹中的图片数量。
  
    - (Line69)addKnowPeople():供外部调用的方法。
  
  * **acPrescreenFaceOnly**:将提供的素材中识别到的人脸截取出来。
  
    - (Line28)SEE_ALL_FACES:True则显示识别出的面部信息图片。
  
    - (Line85-86)face_locations...:模型切换，默认86行的HOG模型。85行的CNN模型识别准，但速度慢（有条件的修改源码，使用显卡加速）。
  
    - (Line89-111)for face_location in face_locations...:这里可以调整截取脸部的图片大小。
  
    - (Line125)filePrescreen():供外部调用的方法。
  
    - (Line178)__rmFiles():是否删除文件，否就注释掉。
  
    - (Line258)__killPro(5,"display"):main方法中的killPro方法，5表示图片显示延时5秒后关闭，display表示打开的图片在进程中的名字叫做"display"
  
  * adBalanceTrain:平衡每个训练人物文件夹中的图片数量。
  
    - (Line37)bala():供外部调用的方法。

- b-模型训练操作

  * baTrainingOneProcessing:单线程训练脚本。
  
    - (Line74)main(train_dir,model_save_path):供外部调用的方法。参数:训练的文件夹/输出模型文件名
  
    - (Line87)单独运行请注意main("A-KnownPeople","KnownPeople")中的参数。默认训练A-KnownPeople，导出KnownPeople。
  
  * **bbFour_processing_training**:四线程训练脚本。
  
    - (Line21)verbose:True显示正在处理的人物信息。
  
    - (Line164)main(train_dir,model_save_path):供外部调用的方法。参数:训练的文件夹/输出模型文件名
  
    - (Line177)单独运行请注意main("A-KnownPeople","KnownPeople")中的参数。默认训练A-KnownPeople，导出KnownPeople。
  
  * bcTraining_multi_processing_of_Ten:十线程训练脚本。
  
    - (Line22)verbose:True显示正在处理的人物信息。
  
    - (Line186)main(train_dir,model_save_path):供外部调用的方法。参数:训练的文件夹/输出模型文件名
  
    - (Line199)单独运行请注意main("A-KnownPeople","KnownPeople")中的参数。默认训练A-KnownPeople，导出KnownPeople。

- c-待识别图片预处理
  
  * **caFindFaces**:将待识别的图片分类到各个tmep目录下。
  
    - (Line14)SEE_ALL_FACES:True则显示识别出的面部信息图片。
  
    - (Line81-82)face_locations...:模型切换，默认82行的HOG模型。81行的CNN模型识别准，但速度慢（有条件的修改源码，使用显卡加速）。
  
    - (Line237)FindFaces():供外部调用的方法。

- d-主程序（开始识别）
  
  * daFaceRecognition_KNN:单线程识别。
  
    - (Line19)SEE_ALL_FACES:True则显示识别结果，带方框。

    - (Line26)DIST_THRESH:调整识别阀值，默认0.5.越小越精确，但识别出的人可能越少。
  
    - (Line77)font = ImageFont.truetype(word_css,20):设置字体。word_css是76行的字体文件，20是字号。
  
    - (Line78-79)draw.rectangle...:调整脸部方框和标签大小。
  
    - (Line189)FaceRecognitionKNN(model_name):供外部调用的方法。model_name是要使用的KNN_MOD文件夹中的模型文件。
  
    - (Line200)FaceRecognitionKNN("KnownPeople"):单独运行请注意FaceRecognitionKNN("KnownPeople")中的参数。默认使用“KnownPeople”模型识别。
  
    - (Line203)__killPro(5,"display"):main方法中的killPro方法，5表示图片显示延时5秒后关闭，display表示打开的图片在进程中的名字叫做"display"
  
  * **dbMoved2Data**:移动识别完的数据到FR_DATA数据库中，并清除tempXXX文件夹中的图片，INPUT_PIC要手动清除。
  
    - (Line59)Moving():供外部调用的方法。
  
  * **dcFaceRecognition_KNN_MultiProcess**:四线程识别脚本，遇到大图片会进行压缩。分两次识别，第一次识别的DIST_THRESH阀值是0.1。第二次阀值是0.6。识别后的tempSingle中是比较准确的结果。其他tempXXX中的结果可能不是很准。
  
    - (Line42)SEE_ALL_FACES:True则显示识别结果，带方框。
  
    - (Line47)CQUA:遇到大图片时，要压缩的比例。0.2的意思就是保留原图20%的大小。
  
    - (Line73)if (__getSize(X_img_path)>=1500000):图片超过多大需要进行压缩，默认1.5Mib，即1500000。
  
    - (Line107)font = ImageFont.truetype(word_css,20):设置字体。word_css是106行的字体文件，20是字号。
  
    - (Line109-118)for name, (top, right, bottom, left) in predictions...:调整脸部方框大小。
  
    - (Line125-141)if isCprs...:调整姓名标签大小。
  
    - (Line149)pa = "...:保持到tempFaceRecognition文件夹的图片名字。
  
    - (Line373)FaceRecognitionKNN(model_name):供外部调用的方法。model_name是要使用的KNN_MOD文件夹中的模型文件。
  
    - (Line379,384,387)__faceRec("tempSingle",model_name ,0.1)...:用来调整阀值。前面那个是识别的文件夹名。后面是DIST_THRESH（调整识别阀值，一次识别默认0.1.越小越精确，但识别出的人可能越少。二次识别是0.6）
  
    - (Line392)FaceRecognitionKNN("KnownPeople"):单独运行请注意FaceRecognitionKNN("KnownPeople")中的参数。默认使用“KnownPeople”模型识别。
  
    - (Line395)__killPro(5,"display"):main方法中的killPro方法，5表示图片显示延时5秒后关闭，display表示打开的图片在进程中的名字叫做"display"
  
- e-清除工作
  
  * eaCLEAN_UP_TEMP:清除tempXXX中的数据。
  
    - (Line11)cleanUpTemp():供外部调用的方法。
  
  * ebCLEAN_UP_FRed:清除已经识别的人物信息。
  
    - (Line11)cleanUpRecognized():供外部调用的方法。
  
- f-演示Demo(不建议日常使用)
  
  * faFaceRecognitionDemo:演示用的Demo，自动识别INPUT_PIC中的图片。使用WorldWideKnown_202006模型。
  
  * fbTrainingDemo:演示用的Demo，自动训练。可能需要修改下参数。
  
- 其他
  
  * gaFindSomebody:从已识别的人物中搜索某人。
  
    - (Line64)FindSomebody(name):供外部调用的方法。name是检索词。
  
    - (Line72)FindSomebody("Albert"):单独运行请自行修改括号中的字符串为你要搜索的字符串。
    
  * gbReFaceRecognition:重新识别已识别过的人物。××不建议使用××。使用请自行修改参数。
  
  * Kill:杀死某个进程。
  
    - (Line16)__killPro(0,"display"):0是时间，0秒。display是进程名称。参数自行修改。
  
  * Wait:等待时间、显示进度。
  
    - (Line18)view(num,total,color,STR):供外部调用的显示进度的方法。num是进度条进度，total是进度条总量，color是进度条颜色("31"(红)，"32"(绿)..."36","37")，STR是结尾字符串放空表示("")末尾显示百分比。
  
    - (Line30)waiting(sec):供外部调用的设置等待时间的方法。sec是时间，单位是秒。
  
 ### 标准使用流程(一步一步来)：

 注:标记“「￥」”的是要人工参与重复审核的步骤，保证数据正确性。

 **一、添加已知人像：** 这是离线人脸识别，所以首先你得有已知姓名的人的人像库为训练材料，训练出模型后才能进行人脸识别。不用担心，这很简单的，让我一步一步跟你慢慢道来：

1.将人像文件夹放入Prescreen中：用aaPrescreenPicture.py 过滤掉不合适的图像。比如照片中没有面孔、照片中有多张面孔、照片中模糊面孔，这些可不是好的训练材料，所以要预筛选出合适的训练材料，这样训练出的模型才有意义。

  **_!!如果你提供的训练素材中有很多多人照片，请用acPrescreenPicture.py，这个是直接分离面孔的脚本。运行完后，直接到对应文件夹下面剔除错误人脸即可。_** 

 **注意：文件夹Person是某个人的名字，人名中不可出现 “-” 符号。** 放入Prescreen文件夹下面的训练材料结构是这样的，PersonA文件夹就是那个人的名字，文件夹里面装的是那个人的照片。你最好在文件夹里放入的图片最好仅有他正脸，一张图有一张目标人物的正脸，这才是咱们要的训练材料。

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

你可以在main方法中修改`SEE_ALL_FACES`为True，显示识别出的人脸。修改__killPro(5,"display")中的第一个参数，可以控制前面图片显示的时间，比如默认是5，意思就是5秒后关闭，“display”则是所显示的图片在任务管理器中的进程名，一般不用修改。

![prescreen](https://images.gitee.com/uploads/images/2020/0629/231950_b30aae01_7423713.png "屏幕截图.png")

「￥」2.运行完PrescreenPicture.py后，请人工复查Perscreen子文件夹中的图片文件，确保无误。想要更精确的识别，修改模型为CNN「慢」`face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")`

 - 确认标准：

 (1) 以某人名字命名的文件夹中仅有某人的照片，而不是其他人的。

 (2) 照片中只能识别出有且只有一张人脸，而且是目标人物的脸，最好是清晰的、正面的。

3.确认完毕后，请运行AddKnownPerson.py ，这将会把Prescreen文件夹下的子文件夹添加到已知人像库（FR_DATA/A-KnownPeople/）中，咱们训练用的材料就是存在A-KnownPeople中。随后还会在FR_DATA/的D-Singleface文件夹中新建人物专属文件夹，以后识别出某个人的单人照片会储存在D-Singleface中的。

二、训练人脸模型————建立已知人像库模型到KNN_MOD：

单线程：TrainingOneProcessing.py

4线程：Four_processing_training.py

10线程：Training_multi_processing_of_Ten.py

[10线程好像并没有更快的样子，略过吧。]

不管是单线程还是多线程训练，都要记得修改：main方法中的参数（模型材料地址和导出模型的名称），一般情况下，main("G-WorldWidePeople","WorldWidePeople")中，前者填的是`A-KnownPeople`，后者是你希望导出的模型名称，比如`my_fr_mod`

导出的模型会储存在KNN_MOD文件夹中，记得把后面的时间去掉，为了区别，导出的模型后默认带有训练时间。

![train](https://images.gitee.com/uploads/images/2020/0629/232434_ff411fcb_7423713.png "屏幕截图.png")

三、待识别文件处理：既然模型训练好了，咱们就可以用来识别人脸了。

首先，把你要识别的照片扔进INPUT_PIC文件夹中，然后运行FindFace.py，这个脚本会帮你归类图片，分成单张面孔、多面孔和没有面孔三类图片。

1.运行FindFaces.py 分配图片文件到tempXXX目录。

「￥」2.请你到tempXXX目录下检查文件是否正确，一共有四个temp开头的文件夹，但你现在需要的是检查tempSingle、tempMore和tempNone。

 - 检查标准：

(1)文件夹中没有被错误发配的图片，比如无面孔文件夹中有你需要识别的人（但FRS居然没有识别出人脸，可能是人脸模糊、过小。这个得调源代码，调整识别精度和识别范围灵敏度。如何调整，请参见[原项目的说明文档](https://github.com/ageitgey/face_recognition)）

(2)去除你觉得多余的，不想识别的图片。

四、开始识别：

检查完毕，咱们就可以开始识别了！识别后你会发现，照片被重命名为识别出的人物的姓名。

1.运行FaceRecognition_KNN.py

 _同样，记得先修改main方法中的参数：FaceRecognitionKNN("WorldWideKnown_202006")，这个WorldWideKnown_202006是我训练好的包含5000个世界知名人物的人脸模型，现在你请把它替换成 **你自己训练的模型** 的名字！_ 

同样可以修改SEE_ALL_FACES参数来决定是否显示人脸和killPro中的时间延时参数。

![Main](https://images.gitee.com/uploads/images/2020/0629/233928_2b9bc3f2_7423713.png "屏幕截图.png")

「￥」2.这里是单线程识别，不用着急。如果你文件多，你可以自己修改源代码，让他变成多线程。到tempXXX目录检查识别结果是否正确，和刚才一样。只不过现在多了个tempFaceRecognition文件夹，这里放的是具体的程序识别出的人脸，你可以在里面很直观看到图片中用蓝色方框标记出了具体面部信息。这个文件夹里的内容不会自动清除，需要定期手动删除。

 - 检查标准：

(1)识别结果正确无误，没有张冠李戴。

(2)图片全部有识别结果（即使是未知人物也标记了N/A或者unknow），多面孔中的文件命名方式是“personA-personB.jpg”。

3.检查完毕后，运行Moved2Data.py添加识别后的文件到数据库中（在FR_DATA中）。

 ### 其他：

一、有演示用的Demo：

演示Demo其实就是省去人工检查，自动运行，一键识别。但这样会出现差错，比如张冠李戴、人物未识别到等。

FaceRecognitionDemo.py：演示人脸识别。可以直接识别已训练的世界知名人物5000人。

TrainingDemo.py：演示训练。训练完后的模型保存在KNN_MOD，需要自己修改FaceRecognitionDemo中的参数才能使用。

二、清空已识别的人物数据：

ebCLEAN_UP_FRed.py 清理tempXXX目录下的文件。

三、清除所有FRS数据：

RESET_FRS.sh 清除已识别人物的信息。

四、查找某人：

gaFindSomebody.py 查找已识别数据库中是否有某人。

五、重新识别已识别人物

gbReFaceRecognition.py 重新识别已识别过的人物。

 ### 截屏

![输入图片说明](https://images.gitee.com/uploads/images/2020/0629/224033_dc3fb134_7423713.png "屏幕截图.png")

- 训练模型：

![0](https://images.gitee.com/uploads/images/2020/0628/110830_d8900709_7423713.png "屏幕截图.png")

 - 识别中...

![2](https://images.gitee.com/uploads/images/2020/0627/230730_b25555a8_7423713.png "屏幕截图.png")

 - 识别单人面孔（每人一个文件夹）：

![4](https://images.gitee.com/uploads/images/2020/0628/110924_cd058f8a_7423713.png "屏幕截图.png")

 - 识别多人面孔（注意文件名，两个人的名字）：

![5](https://images.gitee.com/uploads/images/2020/0628/111010_05ef2cc7_7423713.png "屏幕截图.png")

![Windows01](https://images.gitee.com/uploads/images/2020/0701/182814_7e25466a_7423713.png "屏幕截图.png")

![Windows02](https://images.gitee.com/uploads/images/2020/0701/182839_2c8af54c_7423713.png "屏幕截图.png")

![ERROR](https://images.gitee.com/uploads/images/2020/0705/154610_32173f10_7423713.png "屏幕截图.png")


 ### 许可

[LICENSE](https://github.com/rmshadows/Tag_people_from_photos/blob/master/LICENSE)

 ### 感谢

 再次感谢face_recognition项目 > https://github.com/ageitgey/face_recognition

 1.3.3 更新：
  - 添加了aa、ac的错误反馈，扩增了面部剪辑图。
  - ca新增大图片压缩，加速分类。
  - da、dc解决的中文乱码问题，更正了压缩图片的脸框位置和文字位置。
  - dc中增加二次识别，第一次识别(仅单人)阀值为0.1(严格)，第一次识别的结果在temp中。第二次为0.6(模糊识别)。
  - 新增ad，用来平衡训练模型中的照片数量。
