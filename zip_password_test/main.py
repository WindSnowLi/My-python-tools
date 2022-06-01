import multiprocessing
import zipfile
import time
import os

# 字母数字表
table = [chr(i) for i in range(97, 123)]

num = [chr(i) for i in range(48, 58)]

sum_table = table + num

flag = True


# 全排列
def permutation(n):
    if n == 1:
        return sum_table
    else:
        result = []
        for i in range(len(sum_table)):
            for j in permutation(n-1):
                result.append(sum_table[i] + j)
        return result


pd_table = []

# for i in range(4):
pd_table = permutation(5)


# 测试压缩包密码
def zip_test(zip_name, password):
    try:
        zip_file = zipfile.ZipFile(zip_name, 'r')
        zip_file.extractall(pwd=password.encode())
        print(password)
        global flag
        # 成功解压其余线程终止
        flag = False
    except:
        pass


def zip_test_all(zip_name, list):
    for i in list:
        global flag
        if not flag:
            return
        zip_test(zip_name, i)


if __name__ == '__main__':
    zip_name = 'readme.zip'

    process_list = []
    for i in range(8):
        # 实例化进程对象
        p = multiprocessing.Process(
            target=zip_test_all, args=(zip_name,
                                       pd_table[int(i*len(pd_table)/8):int((i+1)*len(pd_table)/8)],))
        p.start()
        process_list.append(p)

    for i in process_list:
        p.join()

    print('结束')
