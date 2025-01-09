#!/bin/bash

# 检查是否提供了路径参数
if [ -z "$1" ]; then
    echo "请提供一个路径作为参数"
    exit 1
fi

# 获取输入的路径
root_dir="$1"

# 检查路径是否存在
if [ ! -d "$root_dir" ]; then
    echo "路径不存在: $root_dir"
    exit 1
fi

# 遍历根目录下的所有文件夹
for dir in "$root_dir"/*; do
    if [ -d "$dir/.git" ]; then
        echo "正在执行 git pull: $dir"
        (cd "$dir" && git pull)
    fi
done