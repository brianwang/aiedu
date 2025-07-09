from config import settings
from app.api import auth, question, exam, learning
from database import engine, Base
import sys
from pathlib import Path
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

sys.path.append(str(Path(__file__).parent))

# 导入所有模型以确保SQLAlchemy关系正确配置
from app.models import *

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    logger.info("应用启动中...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库初始化完成")
    yield
    # 关闭时执行
    logger.info("应用关闭中...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI智能教育平台 - 提供个性化的学习体验",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 中间件配置
# CORS配置 - 开发环境允许所有本地源
cors_origins = ["*"] if settings.debug else settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "your-domain.com"]
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "detail": str(exc) if settings.debug else "请联系管理员"
        }
    )


# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(question.router, prefix="/api/v1")
app.include_router(exam.router, prefix="/api/v1")
app.include_router(learning.router, prefix="/api/v1")

# 尝试导入题库路由（如果存在）
try:
    from app.api import question_bank
    app.include_router(question_bank.router, prefix="/api/v1")
    logger.info("题库路由加载成功")
except ImportError as e:
    logger.warning(f"题库路由未找到，跳过加载: {e}")
except Exception as e:
    logger.warning(f"题库路由加载失败，跳过加载: {e}")

# 尝试导入分析路由（如果存在）
try:
    from app.api import analytics
    app.include_router(analytics.router, prefix="/api/v1")
    logger.info("分析路由加载成功")
except ImportError as e:
    logger.warning(f"分析路由未找到，跳过加载: {e}")
except Exception as e:
    logger.warning(f"分析路由加载失败，跳过加载: {e}")

# 尝试导入AI路由（如果存在）
try:
    from app.api import ai
    app.include_router(ai.router, prefix="/api/v1")
    logger.info("AI路由加载成功")
except ImportError as e:
    logger.warning(f"AI路由未找到，跳过加载: {e}")
except Exception as e:
    logger.warning(f"AI路由加载失败，跳过加载: {e}")


@app.get("/")
async def read_root():
    """根路径"""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8111,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
