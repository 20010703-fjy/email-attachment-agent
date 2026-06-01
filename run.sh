#!/bin/bash

# 163邮箱附件下载器启动脚本

cd "$(dirname "$0")"

if [ ! -f ".env" ]; then
    echo "错误: 未找到 .env 文件，请先复制 config.example.env 为 .env 并配置"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt

echo "启动附件下载器..."
python3 main.py
