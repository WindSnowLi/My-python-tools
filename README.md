# [PythonExample](https://github.com/WindSnowLi/My-python-tools)

关于pyhon的小例子
___

## 1. [PseudoOperation](https://github.com/WindSnowLi/My-python-tools/tree/main/PseudoOperation)

通过简单的记录鼠标坐标，并通过计算鼠标下图片的偏移来完成简单的位置校准，用于在微偏移的界面模拟鼠标操作

1. [记录部分](https://github.com/WindSnowLi/My-python-tools/blob/main/PseudoOperation/main/record_process.py)
2. [操作部分](https://github.com/WindSnowLi/My-python-tools/blob/main/PseudoOperation/main/operate_process.py)

___

## 2. [DownloadM3u8](https://github.com/WindSnowLi/My-python-tools/blob/main/DownloadM3u8)

1. [下载网站的m3u8视频](https://github.com/WindSnowLi/My-python-tools/blob/main/DownloadM3u8/dv.py)
2. [合并成完整视频文件](https://github.com/WindSnowLi/My-python-tools/blob/main/DownloadM3u8/marge.py)

___

## 3. [PythonGetCookie](https://github.com/WindSnowLi/My-python-tools/tree/main/PythonGetCookie)

### 3.1 仅通过python3网络库获取请求cookie

```python
def get_cookie(url)
```

### 3.2 通过浏览器获取cookie(firefox与chrome类似)

```python
def firefox_get_cookies(url)
```

___

## 4. [VerifyIP]((https://github.com/WindSnowLi/My-python-tools/tree/main/VerifyIP))

备份并更新系统hosts文件中的IP信息

1. ```# MY_MUST_START``` 需要更新的开始标识
2. ```# MY_MUST_END``` 需要更新的结束标识

___

## 5. [QR-Code](https://github.com/WindSnowLi/My-python-tools/tree/main/QR-Code)

1. 二维识别码

————

## 6. [Read-MNIST](https://github.com/WindSnowLi/My-python-tools/tree/main/Read-MNIST)

1. 需自行解压数据集至.py文件同级目录

___

## 7. [Windows11Reg](https://github.com/WindSnowLi/My-python-tools/tree/main/Windows11Reg)

1. Windows11开始菜单与Windows10开始菜单转换（新版已失效）
2. *需重启电脑*

### 依赖

1. pip install pywin32
___

## 8. [send_mail](https://github.com/WindSnowLi/My-python-tools/tree/main/send_mail)

1. python3发送邮件

---

## 9. [ResizeImg](https://github.com/WindSnowLi/My-python-tools/tree/main/ResizeImg)

1. 使用`opencv-python`的`resize`函数
2. Linux使用`pip3 install opencv-python`、Windows使用`pip install opencv-python`安装`opencv-python`
3. 用于重设图片大小，主要用来遇到图片大小限制时缩放图片

---

## 10. [Img->ico](https://github.com/WindSnowLi/My-python-tools/tree/main/Img->ico)

1. Python3修改图片格式为ico
2. *有时会遇到将图片修改为ico格式，但是轻量级的工具不好找，在这里借用pillow库达到了这个效果*

---

## 11. [Img->Str](https://github.com/WindSnowLi/My-python-tools/tree/main/Img->Str)

1. 简笔画图片转字符串
2. 示例图片

![img](./Img->Str/test.jpg)

3. 结果

![img](./Img->Str/rs.png)

---

## 12. [CheckID](https://github.com/WindSnowLi/My-python-tools/tree/main/CheckID)

1. 校验身份证号是否合法

---
