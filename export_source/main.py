import chardet
import os

# 获取文件编码
def get_encoding(file_path):
    with open(file_path, 'rb') as f:
        return chardet.detect(f.read())['encoding']


if __name__ == "__main__":
    rs = ''
    for i in os.listdir():
        if i.endswith('hpp') or i.endswith('cpp') or i.endswith('h') or i.endswith('rc'):
            print(get_encoding(i))
            with open(i, 'r', encoding=get_encoding(i)) as fp:
                for line in fp:
                    # 如果line是空白字符串或者全为空格
                    if line.isspace():
                        continue
                    rs += line
    with open('rs.txt', 'w+', encoding='utf8') as fp:
        fp.write(rs)
