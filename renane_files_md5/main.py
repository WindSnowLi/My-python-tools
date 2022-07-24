import os

# 获取文件md5值
def get_md5(file):
    import hashlib
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        md5.update(f.read())
    return md5.hexdigest()

# 读取文件列表
def read_file_list(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# 文件重命名为自身MD5
def rename_file(file_list, path):
    for file in file_list:
        md5 = get_md5(file)
        # 获取文件后缀
        suffix = os.path.splitext(file)[1]
        os.rename(file, path + '/' + md5 + suffix)


if __name__ == "__main__":
    path = input('请输入文件路径：')
    file_list = read_file_list(path)
    rename_file(file_list, path)
    print('文件重命名完成！')