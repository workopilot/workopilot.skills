#!/bin/bash

echo "======================================"
echo "🚀 启动喔壳 Skills Demo 后端服务"
echo "======================================"

cd backend

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.9 或更高版本"
    exit 1
fi

# 检查依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "🔧 激活虚拟环境..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

echo "📦 安装依赖..."
pip install -q -r requirements.txt

echo ""
echo "✅ 准备完成，启动服务..."
echo ""

python app.py
