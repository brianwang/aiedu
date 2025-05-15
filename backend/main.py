from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import question, auth
from database.database import engine, Base

app = FastAPI()

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(question.router,
                   prefix="/api/questions",
                   tags=["questions"])


@app.on_event("startup")
async def startup():
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
