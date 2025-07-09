import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 应用配置
    app_name: str = "AI智能教育平台"
    app_version: str = "1.0.0"
    debug: bool = True

    # 数据库配置
    database_url: str = "sqlite:///./sql_app.db"

    # JWT配置
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS配置
    allowed_origins: list = [
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://localhost:4173",
        "http://localhost:8080",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:4173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3001"
    ]

    # 文件上传配置
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB

    # AI配置
    openai_api_key: Optional[str] = None
    ai_model: str = "gpt-3.5-turbo"

    # 新增deepseek配置
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = 'https://api.deepseek.com'
    deepseek_model: str = 'deepseek-chat'

    # 邮件配置
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Redis配置（用于缓存和会话）
    redis_url: Optional[str] = None

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = False


# 创建全局设置实例
settings = Settings()

# 确保必要的目录存在
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
