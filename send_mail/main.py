# 这里有个坑，当主机名是中文时会报错，报错信息如下
"""
    hostname, aliases, ipaddrs = gethostbyaddr(name)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2 in position 0: invalid continuation byte
"""
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(server, user, passwd, content, subject, to_user):
    """
    发送普通邮件
    :param server: 定义服务
    :param user: 发件人账号
    :param passwd: 密码或者授权码
    :param content: 内容
    :param subject: 设置主题
    :param to_user: 收件人
    :return: 无
    """
    # 以HTML格式发送，可以自定义样式以静态网页的的方式发送
    message = MIMEText(content, "HTML")
    # message = MIMEText('普通文本' , 'plain', 'utf-8')
    # 设置主题
    message["subject"] = subject
    # 发件人
    message["From"] = user
    # 收件人
    message["To"] = to_user
    try:
        # 定义邮箱服务器，Linux服务器需要使用465端口，否则会因为安全问题发送失败
        smtp_email = smtplib.SMTP_SSL(server, 465)
        # user:邮箱账号，password:授权码
        smtp_email.login(user=user, password=passwd)
        # from_addr:收件方显示发送人 ，to_addrs:发送到的邮箱，msg:要发送的信息
        smtp_email.sendmail(from_addr=user, to_addrs=to_user,
                            msg=message.as_string())
        # 退出邮箱
        smtp_email.quit()
    except Exception as e:
        print(e)
        print("邮件发送失败")


def send_mails_with_file(server, user, passwd, content, subject, to_user, file_path, file_name):
    """
    发送带附件的邮件
    :param server: 定义服务
    :param user: 发件人账号
    :param passwd: 密码或者授权码
    :param content: 内容
    :param subject: 设置主题
    :param to_user: 收件人
    :param file_path: 文件路径
    :param file_name: 附件文件路径
    :return: 无
    """

    # 用来发送文本和附件的对象
    message = MIMEMultipart()
    # 设置主题
    message["subject"] = subject
    # 发件人
    message["From"] = user
    # 收件人
    message["To"] = to_user

    # 推荐使用html格式的正文, 会炫酷很多
    content = MIMEText(content, "HTML")
    # content = MIMEText('普通文本' , 'plain', 'utf-8')
    # 添加文本一个附件
    # enclosure = MIMEText('自己读取出来文本或字符串', 'plain', 'utf-8')

    # 读取二进制文件
    enclosure = MIMEApplication(open(file_path, 'rb').read())
    # 在这里直接无脑二进制流
    enclosure["Content-Type"] = 'application/octet-stream'
    # 设置附件头，添加文件名
    enclosure.add_header('Content-Disposition', 'attachment',
                         # 可以在这指定文本的编码，具体参数示例  filename=('编码', '', file_name)
                         filename=(file_name))

    # 将内容附加到邮件主体中
    message.attach(content)
    message.attach(enclosure)

    try:
        # 定义邮箱服务器，Linux服务器需要使用465端口，否则会因为安全问题发送失败
        smtp_email = smtplib.SMTP_SSL(server, 465)
        # user:邮箱账号，password:授权码
        smtp_email.login(user=user, password=passwd)
        # from_addr:收件方显示发送人 ，to_addrs:发送到的邮箱，msg:要发送的信息
        smtp_email.sendmail(from_addr=user, to_addrs=to_user,
                            msg=message.as_string())
        # 退出邮箱
        smtp_email.quit()
    except Exception as e:
        print(e)
        print("邮件发送失败")


if __name__ == "__main__":
    send_mail(server='smtp.qq.com',
              user='***@qq.com',
              passwd='***',
              content='这是普通邮件',
              subject='这是普通邮件的主题',
              to_user='***@qq.com')

    send_mails_with_file(server='smtp.qq.com',
                         user='***@qq.com',
                         passwd='***',
                         content='这是附件邮件',
                         subject='这是附件邮件的主题',
                         to_user='***@qq.com',
                         file_path=r'D:\1.jpg',
                         file_name='图片.jpg')
