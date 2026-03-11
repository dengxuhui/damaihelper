#!/bin/bash

# macOS 一键运行脚本 (使用 Homebrew Python)

set -e

# Step 1: 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "Homebrew 未安装，正在安装..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Step 2: 安装 Python 和 python-tk (GUI必需)
if ! /opt/homebrew/bin/python3.14 --version &> /dev/null; then
    echo "安装 Python..."
    brew install python@3.14
fi

# 确保安装 python-tk (Tkinter GUI 依赖)
if ! brew list python-tk@3.14 &> /dev/null; then
    echo "安装 python-tk..."
    brew install python-tk@3.14
fi

# Step 3: 删除旧虚拟环境并重新创建 (使用 Python 3.14)
if [ -d "venv" ]; then
    echo "更新虚拟环境..."
    rm -rf venv
fi
echo "创建虚拟环境..."
/opt/homebrew/bin/python3.14 -m venv venv

# Step 4: 激活虚拟环境
source venv/bin/activate

# Step 5: 安装依赖包
echo "安装依赖..."
pip install -r requirements.txt

# Step 6: 运行 gui.py
echo "启动程序..."
python GUI.py
