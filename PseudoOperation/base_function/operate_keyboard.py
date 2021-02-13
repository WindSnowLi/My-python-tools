# -*- coding:utf-8 -*-


# 控制键盘
from pynput.keyboard import Key, Controller

keyboard = Controller()
# 按键盘和释放键盘
keyboard.press(Key.space)
keyboard.release(Key.space)

# 按小写的a
keyboard.press('a')
keyboard.release('a')

# 按大写的A
keyboard.press('A')
keyboard.release('A')

# 按住shift在按a
with keyboard.pressed(Key.shift):
    # Key.shift_l, Key.shift_r, Key.shift
    keyboard.press('a')
    keyboard.release('a')

# 直接输入Hello World
keyboard.type('Hello World')
