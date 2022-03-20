import hashlib
import sys
import os

cmd = sys.argv
path = ''
if(len(cmd) == 1):
    path = input('文件路径：')
else:
    path = cmd[1]

if not os.path.isfile(path):
    print('文件不存在')
else:
    with open(path, 'rb') as f:
        print(hashlib.md5(f.read()).hexdigest())

