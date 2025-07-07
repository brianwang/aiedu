#!/bin/bash

# AI智能教育平台启动脚本

echo "🚀 启动AI智能教育平台..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "❌ 错误: 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

# 检查Node.js版本
node_version=$(node --version 2>&1 | grep -oP '\d+')
if [[ $node_version -lt 16 ]]; then
    echo "❌ 错误: 需要Node.js 16或更高版本，当前版本: $node_version"
    exit 1
fi

# 检查pnpm是否安装
if ! command -v pnpm &> /dev/null; then
    echo "📦 安装pnpm..."
    npm install -g pnpm
fi

# 启动后端
echo "🔧 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 数据库迁移
echo "🗄️ 执行数据库迁移..."
alembic upgrade head

# 启动后端服务
echo "🚀 启动后端服务 (端口: 8111)..."
python main.py &
BACKEND_PID=$!

cd ..

# 启动前端
echo "🎨 启动前端服务..."
cd frontend

# 安装依赖
echo "📦 安装前端依赖..."
pnpm install

# 启动开发服务器
echo "🚀 启动前端服务 (端口: 5173)..."
pnpm dev &
FRONTEND_PID=$!

cd ..

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if curl -s http://localhost:8111/health > /dev/null; then
    echo "✅ 后端服务启动成功: http://localhost:8111"
else
    echo "❌ 后端服务启动失败"
fi

if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ 前端服务启动成功: http://localhost:5173"
else
    echo "❌ 前端服务启动失败"
fi

echo ""
echo "🎉 AI智能教育平台启动完成！"
echo "📖 后端API文档: http://localhost:8111/docs"
echo "🌐 前端应用: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 