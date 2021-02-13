# -*- coding:utf-8 -*-


# 监听键盘
import pynput
from pynput.keyboard import Key


def on_press(key):
    # 监听按键
    print('{0} pressed'.format(key))


def on_release(key):
    # 监听释放
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False


# 连接事件以及释放
with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

"""
一个鼠标监听器是一个线程。线程，所有的回调将从线程调用。从任何地方调用pynput.mouse.Listener.stop，或者调用
pynput.mouse.Listener.StopException或从回调中返回False来停止监听器。

对于鼠标来说，api就上面几个。但是对于键盘来说还要别的，详细的查看：http://pythonhosted.org/pynput/index.html
"""
