from http import cookiejar
from urllib import request
import json

from pip._vendor import requests


def get_cookie(url):
    """

    :param url: 请求连接应保证服务器有set-cookie写入操作
    :return:
    """
    # 请求负载
    data = {}
    # 请求头
    headers = {}
    try:
        # 声明一个CookieJar对象实例来保存cookie
        cookie = cookiejar.CookieJar()
        # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        handler = request.HTTPCookieProcessor(cookie)
        # 通过CookieHandler创建opener
        opener = request.build_opener(handler)
        my_request = request.Request(
            url, headers=headers, data=json.dumps(data).encode("utf-8"))
        # 此处的open方法打开网页
        response = opener.open(my_request)
        # 打印cookie信息
        return requests.utils.dict_from_cookiejar(cookie)
    except Exception as e:
        print(e)
        return ''


if __name__ == '__main__':
    print(get_cookie('https://www.baidu.com'))
