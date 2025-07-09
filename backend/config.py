import os
from typing import Optional, List
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

    # AI配置 - OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.7

    # AI配置 - DeepSeek
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = 'https://api.deepseek.com'
    deepseek_model: str = 'deepseek-chat'
    deepseek_max_tokens: int = 2000
    deepseek_temperature: float = 0.7

    # AI配置 - 智谱AI
    zhipu_api_key: Optional[str] = None
    zhipu_base_url: str = 'https://open.bigmodel.cn/api/paas/v4'
    zhipu_model: str = 'glm-4'

    # AI配置 - 通义千问
    qwen_api_key: Optional[str] = None
    qwen_base_url: str = 'https://dashscope.aliyuncs.com/api/v1'
    qwen_model: str = 'qwen-turbo'

    # AI配置 - 百度文心
    wenxin_api_key: Optional[str] = None
    wenxin_secret_key: Optional[str] = None
    wenxin_base_url: str = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat'
    wenxin_model: str = 'ernie-bot-4'

    # AI服务配置
    ai_service_timeout: int = 30
    ai_service_retries: int = 3
    ai_fallback_enabled: bool = True
    ai_cache_enabled: bool = True
    ai_cache_ttl: int = 3600  # 1小时

    # AI功能开关
    ai_question_generation: bool = True
    ai_smart_grading: bool = True
    ai_learning_analysis: bool = True
    ai_personalized_recommendation: bool = True
    ai_exam_generation: bool = True
    ai_learning_plan: bool = True
    ai_wrong_question_analysis: bool = True
    ai_learning_motivation: bool = True
    ai_learning_style_analysis: bool = True

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
