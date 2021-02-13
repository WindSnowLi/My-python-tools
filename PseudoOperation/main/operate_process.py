# -*- coding:utf-8 -*-


# 控制鼠标
# 读鼠标坐标
import json
import os
import time
from threading import Thread

import cv2
from PIL import ImageGrab
from pynput.keyboard import Key

import pynput

status_flag = True
mouse = pynput.mouse.Controller()
calibration = [0, 0]


def make_screenshot(x1, y1, x2, y2):
    """截图

    :param x1: 开始截图的x1坐标
    :param y1: 开始截图的x1标
    :param x2: 开始截图的x2坐标
    :param y2: 结束截图的y2坐标
    :return: None
    """
    # id: 图片ID
    global id
    bbox = (x1, y1, x2, y2)
    im = ImageGrab.grab(bbox)
    im.save('./temp/present.png')  # 保存截图文件的路径


def identify_pictures(img1Path, img2Path):
    img = cv2.imread(img1Path, 0)
    img2 = img.copy()
    template = cv2.imread(img2Path, 0)
    w, h = template.shape[::-1]

    meth = 'cv2.TM_CCOEFF'
    img = img2.copy()

    method = eval(meth)

    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc


def setPosition(x, y):
    global mouse
    # 本人电脑点击时鼠标坐标会放大偏移，大概会放大1.25倍
    mouse.position = (x / 1.25, y / 1.25)


def setLeftPress():
    global mouse
    mouse.press(pynput.mouse.Button.left)


def setLeftRelease():
    global mouse
    mouse.release(pynput.mouse.Button.left)


def setRightPress():
    global mouse
    mouse.press(pynput.mouse.Button.right)


def setRightRelease():
    global mouse
    mouse.release(pynput.mouse.Button.right)


def on_press(key):
    # 监听按键
    print('{0} pressed'.format(key))


def on_release(key):
    global status_flag
    # 监听释放
    print('{0} release'.format(key))
    if key == Key.esc:
        status_flag = False
        return status_flag


# 通过查找原始鼠标下的图片位置与现在鼠标下的位置进行对比，计算偏移量
def calibration_offset(i):
    make_screenshot(i['x'] - 150 + calibration[0], i['y'] - 100 + calibration[1], i['x'] + 150 + calibration[0],
                    i['y'] + 100 + calibration[1])
    inner_top_left = identify_pictures('./temp/present.png', './pic/' + str(i['id']) + '.png')
    outside = (
        i['x'] - 150 + inner_top_left[0] + calibration[0], i['y'] - 100 + inner_top_left[1] + calibration[1])

    calibration[0] = outside[0] - (i['x'] - 75)
    calibration[1] = outside[1] - (i['y'] - 50)


def operate_mouse():
    global status_flag
    record = []
    with open("./record.txt", 'r') as fp:
        for line in fp:
            record.append(json.loads(line.replace("\'", "\"")))
    for i in record:
        # print(i)
        if not status_flag:
            break
        if i['event'] == 'move':
            if i['id'] % 100 == 0 and (i['x'] >= 200 or i['x'] <= 1920 - 200) and (i['y'] > 100 or i['y'] < 1080 - 100):
                calibration_offset(i)
            i['x'] = i['x'] + calibration[0]
            i['y'] = i['y'] + calibration[1]
            setPosition(i['x'], i['y'])
        elif i['event'] == 'click':
            calibration_offset(i)
            setPosition(i['x'] + calibration[0], i['y'] + calibration[1])
            if i['action'] == 'pressed':
                if i['button'] == 'Button.left':
                    setLeftPress()
                elif i['button'] == 'Button.right':
                    setRightPress()
            elif i['action'] == 'released':
                if i['button'] == 'Button.left':
                    setLeftRelease()
                elif i['button'] == 'Button.right':
                    setRightRelease()
        time.sleep(i['time'])
    status_flag = False
    print("end")


def listener_key():
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release)as listener:
        listener.join()


if __name__ == '__main__':
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    t1 = Thread(target=operate_mouse)
    t2 = Thread(target=listener_key)
    t1.start()
    t2.start()
