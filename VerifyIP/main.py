import re
import urllib.request
import os
from shutil import copyfile
import datetime

# 需要验证的开始标识
NEED_TEST_START = "# MY_MUST_START\n"
# 需要验证的结束标识
NEED_TEST_END = "# MY_MUST_END\n"
# 系统hosts文件路径
SYSTEM_HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"


def backups_hosts():
    """
    备份原有hosts文件到~/.backups_hosts
    :return:
    """
    # 获取当前系统用户目录
    user_home_backups = os.path.expanduser('~') + '/.backups_hosts'
    if not os.path.exists(user_home_backups):
        os.mkdir(user_home_backups + '/.backups_hosts')
    copyfile(SYSTEM_HOSTS_PATH, user_home_backups + '/hosts-' +
             datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))


def get_ip(domain_name):
    """
    查询域名IP
    :param domain_name: 域名
    :return: IP列表
    """
    response = urllib.request.urlopen(
        'http://ip.tool.chinaz.com/' + domain_name)
    html = response.read().decode("utf8")
    reg_extract_element_re = r'<span class="Whwtdhalf w15-0" style="cursor:pointer;" onclick="AiWenIpData\(.*?</span>'
    reg_extract_element = re.compile(reg_extract_element_re)  # 编译一下，运行更快
    elements = reg_extract_element.findall(
        str(html.encode('raw_unicode_escape')))
    reg_extract_ip_re = re.compile(r'(?<=\>)\S+(?=\<)')
    # 可能对应多个IP，分别读取
    ip_list = []
    for temp_element in elements:
        reg_extract_ip = reg_extract_ip_re.findall(temp_element)
        ip_list.append(reg_extract_ip[0])
    return ip_list


def arrange_hosts():
    """
    读取整理hosts文件
    :return: 返回结果hosts列表
    """
    temp_hosts = []
    temp_ip_key_value = {}
    my_flag = False
    with open(SYSTEM_HOSTS_PATH, 'r') as sf:
        for line in sf:
            if len(line) == 0:
                continue

            if line == NEED_TEST_START:
                my_flag = True
            elif line == NEED_TEST_END:
                my_flag = False
            ret = re.match("^#.*", line)
            if ret:
                temp_hosts.append(line)
            else:
                line_after = re.sub('\\s{2,}|\t', ' ', line)
                ip_key_values = line_after.split(' ')
                if len(ip_key_values) > 1 and ip_key_values[0] == '127.0.0.1':
                    temp_hosts.append(line_after)
                elif len(ip_key_values) > 1:
                    if my_flag:
                        for temp_ip in get_ip(ip_key_values[1]):
                            temp_ip_str = temp_ip + ' ' + ip_key_values[1]
                            if temp_ip_str in temp_ip_key_value:
                                continue
                            temp_hosts.append(temp_ip_str)
                            temp_ip_key_value[temp_ip_str] = ''
                    else:
                        temp_hosts.append(line_after)
                        temp_ip_key_value[line_after] = ''
    return temp_hosts


def update_hosts(hosts):
    """
    写入hosts文件
    :param hosts: hosts列表
    """
    with open(SYSTEM_HOSTS_PATH, 'w') as ef:
        ef.writelines(hosts)


if __name__ == "__main__":
    backups_hosts()
    update_hosts(arrange_hosts())
