# 所有文件修改文件后缀，第一个参数是筛选原本类型，第二个参数是修改后的类型
import os
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <old_type> <new_type>")
        return
    old_type = sys.argv[1]
    new_type = sys.argv[2]
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(old_type):
                old_name = os.path.join(root, file)
                new_name = old_name.replace(old_type, new_type)
                os.rename(old_name, new_name)
                print("Rename %s to %s" % (old_name, new_name))

if __name__ == "__main__":
    main()
