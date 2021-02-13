# -*- coding: UTF-8 -*-
import urllib.request
import re
from concurrent.futures import ProcessPoolExecutor
import os
import datetime
import socket

# 设置超时时间为30s
socket.setdefaulttimeout(30)

# 下载单个文件
def down(save, links, order, number):
    try:
        linking = links[0:links.rfind('/') + 1] + order
        while True:
            try:
                urllib.request.urlretrieve(linking, save + "/" + str(number) + '.ts')
                break
            except socket.timeout:
                continue
        print('进程{0}下载完成'.format(number))
        return -1
    except Exception as identifier:
        print(identifier)
        return number

# 获取m3u8中的视频列表
def getlist(links):
    request = urllib.request.Request(url=links)  # 需要通过encode设置编码 要不会报错
    response = urllib.request.urlopen(request)  # 发送请求
    logInfo = response.read().decode()  # 读取对象 将返回的二进制数据转成string类型
    reg = r'.*\.ts'
    reg_img = re.compile(reg)
    links = reg_img.findall(logInfo)
    return links

# 读取.m3u8文件中的视频列表
def read_m3u8(file_path):
    m3u8_file = open(file_path, "r", encoding='UTF-8')
    m3u8_file_str = ""
    for line in m3u8_file:
        m3u8_file_str = m3u8_file_str + line
    m3u8_file.close()
    reg = r'.*\.ts'
    reg_img = re.compile(reg)
    return reg_img.findall(m3u8_file_str)

# 使用.m3u8文件下载
def use_m3u8_down(savePath, order, number):
    try:
        urllib.request.urlretrieve(
            order, savePath + '/' + str(number) + '.ts')
        print('进程{0}下载完成'.format(number))
        return -1
    except Exception as identifier:
        print(identifier)
        return number


if __name__ == "__main__":
    link_list = 'https://**********.m3u8'
    save_path = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    save_path = "./" + save_path
    number = 0
    while True:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            break
        else:
            save_path += 'x'
    processPool = ProcessPoolExecutor(max_workers=30)
    futures = {}
    for i in getlist(link_list):
        # for i in read_m3u8('./play.m3u8'):
        try:
            number += 1
            job = processPool.submit(down, save_path, link_list, i, number)
            futures[job] = number
            print('进程{0}进入下载'.format(number))
        except Exception as e:
            print(e)
            print("Error: Unable to start {0} the thread".format(i))

    for job in futures:
        re = job.result()
        # n = futures[job]
        if re != -1:
            print('{0}下载失败'.format(re))
