# -*- coding: utf-8 -*-
'''
演示前的工作：
添加要训练的材料到 Prescreen文件夹中：
结构：
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

'''
import aaPrescreenPicture
import abAddKnownPerson
import baTrainingOneProcessing

if __name__ == "__main__":
	print("处理训练材料。")
	aaPrescreenPicture.filePrescreen()
	print("添加训练素材。")
	abAddKnownPerson.addTrainLib()
	print("开始训练。")
	#训练文件夹（FR_DATA中）和训练模型名称（在KNN_MOD中）
	baTrainingOneProcessing.main("A-KnownPeople","KnowPeopleDemo")
	print("训练完毕。")