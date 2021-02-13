# -*- coding:utf-8 -*-
import datetime
import os
from threading import Thread

import pynput
from PIL import ImageGrab
from pynput.keyboard import Key

# 监听鼠标
last_time = datetime.datetime.now()
operate_record = []
id = 0
status_flag = True


# 截取指定位置
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
    im.save('./pic/' + str(id) + '.png')  # 保存截图文件的路径


# 监听鼠标移动，并记录移动信息
def on_move(x, y):
    global status_flag
    if not status_flag:
        return status_flag
    global last_time
    global id
    global operate_record
    # 防止读取的鼠标位置越界
    if y > 1080:
        y = 1080
    if x > 1920:
        x = 1920
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    print('Pointer moved to {0}'.format((x, y)))
    id += 1
    # 边缘位置不再进行截图
    if id % 100 == 0 and (x >= 150 or x <= 1920 - 150) and (y > 100 or y < 1080 - 100):
        make_screenshot(x - 75, y - 50, x + 75, y + 50)
    single = {'id': id, 'x': x, 'y': y, "event": "move", "button": "", 'action': '',
              'time': (datetime.datetime.now() - last_time).total_seconds()}
    last_time = datetime.datetime.now()
    operate_record.append(single)


# 监听点击信息
def on_click(x, y, button, pressed):
    global status_flag
    if not status_flag:
        return status_flag
    global last_time
    global id
    global operate_record
    # 监听鼠标点击
    print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
    id += 1
    single = {'id': id, 'x': x, 'y': y, "event": "click", "button": str(button),
              'action': 'pressed' if pressed else 'released',
              'time': (datetime.datetime.now() - last_time).total_seconds()}
    last_time = datetime.datetime.now()
    operate_record.append(single)
    make_screenshot(x - 75, y - 50, x + 75, y + 50)


# 监听键盘按键按下
def on_press(key):
    global status_flag
    if not status_flag:
        return status_flag
    # 监听按键
    print('{0} pressed'.format(key))


# 监听按键释放信息
def on_release(key):
    global status_flag
    global operate_record
    # 监听释放
    print('{0} release'.format(key))
    # 若按下的为ESC键，终止程序
    if key == Key.esc:
        with open('./record.txt', 'w') as fp:
            for i in operate_record:
                fp.write(str(i) + '\n')
        print("end")
        status_flag = False
        return status_flag


def listener_mouse():
    with pynput.mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        listener.join()


def listener_key():
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release)as listener:
        listener.join()


# 一个鼠标监听器是一个线程。线程，所有的回调将从线程调用。从任何地方调用pynput.mouse.Listener.stop，或者调用pynput.mouse.Listener.StopException或从回调中返回False来停止监听器。


if __name__ == '__main__':
    if not os.path.exists('./pic'):
        os.mkdir('./pic')
    t1 = Thread(target=listener_mouse)
    t2 = Thread(target=listener_key)
    t1.start()
    t2.start()
