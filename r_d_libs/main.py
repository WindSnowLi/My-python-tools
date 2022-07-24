import os

def ls(path):
    libds = []
    libs = []
    dllds = []
    dlls = []
    # 显示文件目录并过滤
    for i in os.listdir(path):
        if i.endswith('.lib'):
            if i.endswith('d.lib'):
                libds.append(i)
            else:
                libs.append(i)
        elif i.endswith('.dll'):
            if i.endswith('d.dll'):
                dllds.append(i)
            else:
                dlls.append(i)
    # 排序
    libs.sort()
    libds.sort()
    dlls.sort()
    dllds.sort()
    return libs, libds, dlls, dllds



if __name__ == "__main__":
    path = input('请输入库路径：')
    libs, libds, dlls, dllds = ls(path)
    print('lib库文件：')
    for i in libs:
        print(i)
    
    print('libd库文件：')
    for i in libds:
        print(i)
    
    print('dll库文件：')
    for i in dlls:
        print(i)
    
    print('dlld库文件：')
    for i in dllds:
        print(i)
