"""
KET备考系统 - FastAPI应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from core.database import init_db
from api.routes import auth_router, question_router, answer_router, progress_router, admin_router, speed_quiz_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="专为小学生设计的KET考试备考系统",
    lifespan=lifespan,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router.router, prefix="/api/v1", tags=["认证"])
app.include_router(question_router.router, prefix="/api/v1", tags=["题目"])
app.include_router(answer_router.router, prefix="/api/v1", tags=["答题"])
app.include_router(progress_router.router, prefix="/api/v1", tags=["进度"])
app.include_router(admin_router.router, prefix="/api/v1", tags=["管理员"])
app.include_router(speed_quiz_router.router, prefix="/api/v1", tags=["抢答"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用KET备考系统API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
