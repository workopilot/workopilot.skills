#!/bin/bash

echo "======================================"
echo "🚀 启动喔壳 Skills Demo 前端服务"
echo "======================================"

cd frontend

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    echo "请先安装 Node.js 16 或更高版本"
    exit 1
fi

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖..."
    npm install
else
    echo "✅ 依赖已安装"
fi

echo ""
echo "✅ 准备完成，启动服务..."
echo ""

npm run dev
