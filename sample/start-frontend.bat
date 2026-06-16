@echo off
chcp 65001 >nul

echo ======================================
echo 🚀 启动喔壳 Skills Demo 前端服务
echo ======================================

cd frontend

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Node.js
    echo 请先安装 Node.js 16 或更高版本
    pause
    exit /b 1
)

REM 检查依赖
if not exist "node_modules\" (
    echo 📦 安装依赖...
    call npm install
) else (
    echo ✅ 依赖已安装
)

echo.
echo ✅ 准备完成，启动服务...
echo.

call npm run dev
