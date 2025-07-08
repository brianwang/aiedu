@echo off
chcp 65001 >nul
echo 🚀 AI智能教育平台启动脚本
echo ================================

REM 检查Python环境
echo 📋 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python环境检查完成

REM 检查Node.js环境
echo 📋 检查Node.js环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Node.js环境，请先安装Node.js 16+
    pause
    exit /b 1
)
echo ✅ Node.js环境检查完成

REM 启动后端
echo 🔧 启动后端服务...
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📦 安装后端依赖...
pip install -r requirements.txt

REM 启动后端服务
echo 🚀 启动后端服务 (端口: 8111)...
start "Backend" python main.py

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端
echo 🔧 启动前端服务...
cd ..\frontend

REM 安装依赖
echo 📦 安装前端依赖...
npm install

REM 启动前端服务
echo 🚀 启动前端服务 (端口: 5173)...
start "Frontend" npm run dev

echo ================================
echo ✅ 服务启动完成！
echo 📱 前端地址: http://localhost:5173
echo 🔧 后端地址: http://localhost:8111
echo 📚 API文档: http://localhost:8111/docs
echo.
echo 按任意键退出...
pause >nul 