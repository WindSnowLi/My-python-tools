import numpy as np
import cv2 as cv
import os


def mkdir_rsdir(path_root):
    """

    :param path_root: 输出根路径
    """
    path_t10k_images = path_root + '/t10k-images'
    path_train_images = path_root + '/train-images'
    if not os.path.exists(path_t10k_images):
        os.mkdir(path_t10k_images)
    if not os.path.exists(path_train_images):
        os.mkdir(path_train_images)

    for i in range(0, 10):
        if not os.path.exists(path_t10k_images + '/' + str(i)):
            os.mkdir(path_t10k_images + '/' + str(i))
        if not os.path.exists(path_train_images + '/' + str(i)):
            os.mkdir(path_train_images + '/' + str(i))


def read_pic(idx3_ubyte_fp):
    """
    读取一张图片
    :param idx3_ubyte_fp: 图片文件
    :return: img
    """
    temp_image = []
    for i in range(0, 28 * 28):
        image_data = idx3_ubyte_fp.read(1)
        temp_image.append(int.from_bytes(image_data, byteorder='big', signed=False))
        # print(int.from_bytes(image_data, byteorder='big', signed=False), end=' ')
    return np.array(temp_image, dtype=np.uint8).reshape(28, 28)


def read_lable(idx1_ubyte_fp):
    """
    读取一个标签
    :param idx1_ubyte_fp: 标签文件
    :return: 数字标签
    """
    return int.from_bytes(idx1_ubyte_fp.read(1), byteorder='big', signed=False)


if __name__ == '__main__':
    # 测试集
    t10k_idx3_ubyte_fp = open('t10k-images.idx3-ubyte', 'rb')
    # 舍去开头
    t10k_idx3_ubyte_fp.read(1 * 4 * 4)
    t10k_idx1_ubyte_fp = open('t10k-labels.idx1-ubyte', 'rb')
    # 舍去开头
    t10k_idx1_ubyte_fp.read(1 * 4 * 2)
    path_out_root = 'MNIST'
    mkdir_rsdir(path_out_root)
    t10k_all_pic = 0
    while t10k_idx1_ubyte_fp.tell() != os.path.getsize('t10k-labels.idx1-ubyte'):
        img = read_pic(t10k_idx3_ubyte_fp)
        lable = read_lable(t10k_idx1_ubyte_fp)
        cv.imwrite(
            path_out_root + '/t10k-images/' + str(lable) + '/' + str(lable) + ('_%d_10k_images.jpg' % t10k_all_pic),
            img)
        t10k_all_pic += 1

    t10k_idx3_ubyte_fp.close()
    t10k_idx1_ubyte_fp.close()

    # 训练集，与测试集一致，但懒得抽出函数

    train_idx3_ubyte_fp = open('train-images.idx3-ubyte', 'rb')
    # 舍去开头
    train_idx3_ubyte_fp.read(1 * 4 * 4)
    train_idx1_ubyte_fp = open('train-labels.idx1-ubyte', 'rb')
    # 舍去开头
    train_idx1_ubyte_fp.read(1 * 4 * 2)
    train_all_pic = 0
    while train_idx1_ubyte_fp.tell() != os.path.getsize('train-labels.idx1-ubyte'):
        img = read_pic(train_idx3_ubyte_fp)
        lable = read_lable(train_idx1_ubyte_fp)
        cv.imwrite(
            path_out_root + '/train-images/' + str(lable) + '/' + str(lable) + ('_%d_train_images.jpg' % train_all_pic),
            img)
        train_all_pic += 1

    train_idx3_ubyte_fp.close()
    train_idx1_ubyte_fp.close()
