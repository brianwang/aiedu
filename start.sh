#!/bin/bash

echo "🚀 AI智能教育平台启动脚本"
echo "================================"

# 检查Python环境
echo "📋 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 错误：未找到Python环境，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python环境检查完成"

# 检查Node.js环境
echo "📋 检查Node.js环境..."
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到Node.js环境，请先安装Node.js 16+"
    exit 1
fi

echo "✅ Node.js环境检查完成"

# 启动后端
echo "🔧 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    $PYTHON_CMD -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# 安装依赖
echo "📦 安装后端依赖..."
pip install -r requirements.txt

# 启动后端服务
echo "🚀 启动后端服务 (端口: 8111)..."
$PYTHON_CMD main.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo "🔧 启动前端服务..."
cd ../frontend

# 安装依赖
echo "📦 安装前端依赖..."
npm install

# 启动前端服务
echo "🚀 启动前端服务 (端口: 5173)..."
npm run dev &
FRONTEND_PID=$!

echo "================================"
echo "✅ 服务启动完成！"
echo "📱 前端地址: http://localhost:5173"
echo "🔧 后端地址: http://localhost:8111"
echo "📚 API文档: http://localhost:8111/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 