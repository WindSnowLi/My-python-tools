# 导出指定目录下所有*.cpp、*.h、*.ui文件的代码到out.txt文件中，忽略所有空行和注释
# 使用方法：python main.py <dir_path>

import os
import sys
import re

def export_code(dir_path):
    with open('out.txt', 'w', encoding='utf8') as out:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.cpp') or file.endswith('.h') or file.endswith('.ui'):
                    with open(os.path.join(root, file), 'r', encoding='utf8') as f:
                        for line in f:
                            org_line = line
                            line = line.strip()
                            if line and not line.startswith('//') and not '/*' in line and not '*/' in line and not '* @' in line and not '*@' in line:
                                out.write(org_line)
                        out.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py <dir_path>')
    else:
        export_code(sys.argv[1])
        # 文件只保留前32*50行和后32*50行
        with open('out.txt', 'r', encoding='utf8') as f:
            lines = f.readlines()
            # 去除非ASCII
            lines = [re.sub(r'[^\x00-\x7f]', '', line) for line in lines]
            # 去除全是空格的行，但保留非全部空格行的原来的空格
            lines = [line if line.strip() else '' for line in lines]
            
            lines = lines[:32*50] + lines[-32*50:]
        with open('out.txt', 'w', encoding='utf8') as f:
            f.writelines(lines)
        print('Export code successfully!')