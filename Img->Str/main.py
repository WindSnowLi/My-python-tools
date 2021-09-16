# encoding:utf-8

# 简笔画图片转字符串

import cv2

# 字符
char = [' ', '`', '.', '^', ',', ':', '~', '"', '<', '!', 'c', 't', '+', '{', 'i', '7', '?', 'u', '3', '0', 'p',
        'w', '4', 'A', '8', 'D', 'X', '%', '#', 'H', 'W', 'M']
# 对应的字符
target = [0, 5, 7, 9, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 59,
          61, 63, 66,
          68, 70]


def get_index(num):
    """
    查找像素值对应字符
    :param num:
    :return:
    """
    if num > 70:
        return ' '
    for _ in range(0, 5):
        if num not in target:
            num = num + 1
            if num > 70:
                return ' '
        else:
            return char[target.index(num)]


def get_block(img, x, y, block_size):
    """
    获取块平均像素值
    :param img: 图片
    :param x: 起点X轴
    :param y: 起点y轴
    :param block_size: 块边长
    :return: 块平均像素值
    """
    rs = 0
    for i in range(block_size):
        if x + i >= img.shape[0]:
            return int(rs / block_size ** 2)
        for j in range(block_size):
            if y + i >= img.shape[1]:
                return int(rs / block_size ** 2)
            rs = rs + img[x + i][y + j]
    return int(rs / block_size ** 2)


if __name__ == '__main__':
    # 读取图片
    img = cv2.imread('./test.jpg')
    # 转为灰度图
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    height, width = img.shape
    # 最大宽度设为192
    rate = width / 192
    if rate > 1:
        width = int(width / rate)
        height = int(height / rate)
    # 重设为宽度小于192的图片
    img = cv2.resize(img, (width, height))

    with open('./pic.txt', 'w') as fp:
        step = 4
        for i in range(0, height, step):
            for j in range(0, width, step):
                # 反转图片并把像素值设为0~70
                value = 70 - int(get_block(img, i, j, step) * 70 / 255)
                fp.write(str(get_index(value)) + ' ')
            fp.write('\n')
