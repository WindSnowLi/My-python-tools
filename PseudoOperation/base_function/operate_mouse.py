# -*- coding:utf-8 -*-


# 控制鼠标
# 读鼠标坐标
import pynput

mouse = pynput.mouse.Controller()
print('The current pointer position is {0}'.format(mouse.position))
# 设置鼠标坐标
mouse.position = (10, 20)
print('Now we have moved it to {0}'.format(mouse.position))
# 移动鼠标到相对位置
mouse.move(5, -5)
# 按住和放开鼠标
mouse.press(pynput.mouse.Button.left)  # 按住鼠标左键
mouse.release(pynput.mouse.Button.left)  # 放开鼠标左键
# 点击鼠标
mouse.click(pynput.mouse.Button.left, 2)  # 点击鼠标2下
# 鼠标滚轮
mouse.scroll(0, 2)  # 滚动鼠标
