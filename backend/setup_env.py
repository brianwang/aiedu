#!/usr/bin/env python3
"""
设置环境变量脚本
"""
import os
from pathlib import Path

def setup_env():
    """设置环境变量"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env文件已存在")
        return
    
    # 创建.env文件
    env_content = """# 应用配置
APP_NAME=AI智能教育平台
APP_VERSION=1.0.0
DEBUG=true

# 数据库配置
DATABASE_URL=sqlite:///./sql_app.db

# JWT配置
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS配置
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://localhost:4173"]

# 文件上传配置
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# AI配置 - DeepSeek
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_MAX_TOKENS=2000
DEEPSEEK_TEMPERATURE=0.7

# AI配置 - OpenAI (可选)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# AI服务配置
AI_SERVICE_TIMEOUT=30
AI_SERVICE_RETRIES=3
AI_FALLBACK_ENABLED=true
AI_CACHE_ENABLED=true
AI_CACHE_TTL=3600

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ .env文件已创建")
    print("📝 请编辑.env文件，设置您的DeepSeek API密钥：")
    print("   DEEPSEEK_API_KEY=your-actual-deepseek-api-key")
    print("")
    print("🔗 获取DeepSeek API密钥：")
    print("   https://platform.deepseek.com/")

if __name__ == "__main__":
    setup_env() 