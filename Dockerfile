# 使用官方Python运行时作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ ./backend/

# 复制前端构建文件
COPY frontend/dist/ ./frontend/dist/

# 创建必要的目录
RUN mkdir -p backend/logs backend/uploads

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 