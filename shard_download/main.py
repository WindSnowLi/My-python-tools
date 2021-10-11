import math
from concurrent.futures import ProcessPoolExecutor

import requests

# 设置超时时间为30s
# socket.setdefaulttimeout(30)

# 默认每个片最小2MB
DEFAULT_MIN_PART = 2048 * 1024

# 每个组分配下载量大小
GROUP_PART = 0

# 最大进程<=10
MAX_THREAD = 10


def make_file_buff(name, length):
    """
    生成整个文件大小的空文件
    :param name: 文件名
    :param length: 总字节数
    """
    with open(name, 'wb') as f:
        f.seek(length - 1)
        f.write(b'\x00')


def write_part(name, index, part):
    """
    写入片
    :param name: 文件名
    :param index: 第几个片
    :param part: 二进制片
    """
    with open(name, 'rb+') as f:
        f.seek(index * GROUP_PART + DEFAULT_MIN_PART)
        f.write(part)


def down_part(url, name, index):
    """
    下载片
    :param url: url链接
    :param name: 文件名
    :param index: 下载第几个片
    :return: 片的索引
    """
    while True:
        try:
            write_part(name, index, requests.get(url, headers={'Range': 'bytes=%d-%d' % (
                index * GROUP_PART + DEFAULT_MIN_PART, (index + 1) * GROUP_PART + DEFAULT_MIN_PART)}).content)
            return index
        except Exception as e:
            print(e)


if __name__ == '__main__':
    url = 'https://download.dbeaver.com/community/21.2.2/dbeaver-ce_21.2.2_amd64.deb'
    # 解析文件名
    file_name = url[url.rindex('/') + 1:]
    # 默认下载2M的开头
    res = requests.get(url, headers={'Range': 'bytes=0-%d' % DEFAULT_MIN_PART})
    # 根据返回的头信息解析总长度
    content_length = res.headers['Content-Range']
    # 总长度
    size = int(content_length[content_length.index('/') + 1:])
    # 创建空白文件
    make_file_buff(file_name, size)
    with open(file_name, 'rb+') as f:
        f.write(res.content)

    # 如果总长度小于最小片，则已经下载完成
    if size <= DEFAULT_MIN_PART:
        exit(0)
    # 以最小片计算所需线程数
    workers = math.ceil(size / DEFAULT_MIN_PART) - 1
    # 大于10则限定在10以内
    if workers >= 10:
        GROUP_PART = math.ceil((size - DEFAULT_MIN_PART) / 10)
    else:
        GROUP_PART = math.ceil((size - DEFAULT_MIN_PART) / DEFAULT_MIN_PART)

    # 最终实际线程数
    workers = math.ceil((size - DEFAULT_MIN_PART) / GROUP_PART)

    # 最多10个进程同时下载
    processPool = ProcessPoolExecutor(max_workers=MAX_THREAD)

    futures = {}
    for i in range(0, workers):
        # 提交进程下载
        job = processPool.submit(down_part, url, file_name, i)
        futures[job] = i
    for job in futures:
        re = job.result()
        if re != -1:
            print('片{0}下载结束'.format(re))
