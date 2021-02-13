# pip install Pillow
from datetime import datetime

from PIL import ImageGrab
import time


def make_screenshot(x1, y1, x2, y2):
    """截图

    :param x1: 开始截图的x1坐标
    :param y1: 开始截图的x1标
    :param x2: 开始截图的x2坐标
    :param y2: 结束截图的y2坐标
    :return: None
    """
    bbox = (x1, y1, x2, y2)
    im = ImageGrab.grab(bbox)
    im.save('saved_screenshot_%d.png' % (float(time.time()) * 10000000))  # 保存截图文件的路径


if __name__ == '__main__':
    print("start")
    start = datetime.now()
    make_screenshot(0, 0, 360, 480)  # 起点，终点
    end = datetime.now()
    print((end - start).total_seconds())
