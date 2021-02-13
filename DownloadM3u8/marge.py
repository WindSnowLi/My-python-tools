# -*- coding: UTF-8 -*-
from genericpath import exists
import os

# ts文件夹
path = '20210131182221'
# 目标文件保存文件夹
save_path = 'marge'
# 获取ts文件目录
file_list = os.listdir(path)
# 排序ts文件，我的是以1.ts、2.ts、3.ts、4.ts这种，排序的依据是从零个字符到倒数.之前那一个
file_list.sort(key=lambda x:int(x[0:len(x)-3]))

# 保存目标目录如果不存在则创建
if not os.path.exists(save_path):
    os.mkdir(save_path)


# 以二进制打开目标文件
target = open('./'+save_path+'/'+path+'.ts', "ab+")
# 以二进制打开ts表，依次以二进制写入目标文件
for temp in file_list:
    temp_file = open(path+'/'+temp, "rb+")
    target.write(temp_file.read())
    temp_file.close()
    print(temp)
target.close()
