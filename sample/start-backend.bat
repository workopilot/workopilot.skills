@echo off
chcp 65001 >nul

echo ======================================
echo 🚀 启动喔壳 Skills Demo 后端服务
echo ======================================

cd backend

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.9 或更高版本
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv\" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

echo 📦 安装依赖...
pip install -q -r requirements.txt

echo.
echo ✅ 准备完成，启动服务...
echo.

python app.py
