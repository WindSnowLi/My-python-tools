# -*- coding: UTF-8 -*-

from http import cookiejar
from urllib import request
from pip._vendor import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import json


# 使用python库直接获取cookie
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


# 需要安装火狐浏览器，并下载geckodriver驱动
# 通过火狐浏览器获取cookie
# 通过正常的浏览器请求，优点是在js中的请求也会发起，因为不是所有的请求都会有set-cookie写入
# 缺点是加载慢
def firefox_get_cookies(url):
    """

    :param url: 请求连接
    :return:
    """
    c_service = Service('geckodriver')
    driver = any
    try:
        c_service.command_line_args()
        c_service.start()
        firefox_options = Options()
        # 不启动界面显示- linux下命令行模式必须启用
        firefox_options.add_argument('-headless')
        driver = Firefox(options=firefox_options)
        driver.get(url)
        # 第一次请求浏览器一般无法显示cookie
        # 等待第一次加载完成
        time.sleep(2)
        # 刷新
        driver.refresh()
        # 等待第二次加载完成
        time.sleep(2)
        return driver.get_cookies()
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        c_service.stop()


if __name__ == '__main__':
    # 只会获取当前连接写入的cookie
    print(get_cookie('https://www.baidu.com'))
    # 附带的请求写入的cookie也可以查询得到
    print(firefox_get_cookies('https://www.baidu.com'))
