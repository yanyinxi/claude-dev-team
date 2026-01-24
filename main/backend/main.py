"""
KET备考系统 - FastAPI应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from core.database import init_db


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


# 注册路由 - 使用延迟导入避免循环依赖
from api.routes.auth_router import router as auth_router
from api.routes.question_router import router as question_router
from api.routes.answer_router import router as answer_router
from api.routes.progress_router import router as progress_router
from api.routes.admin_router import router as admin_router
from api.routes.speed_quiz_router import router as speed_quiz_router
from api.routes.monitor_router import router as monitor_router
from api.routes.alarm_router import router as alarm_router
from tasks.ai_digest.router import router as ai_digest_router

app.include_router(auth_router, prefix="/api/v1", tags=["认证"])
app.include_router(question_router, prefix="/api/v1", tags=["题目"])
app.include_router(answer_router, prefix="/api/v1", tags=["答题"])
app.include_router(progress_router, prefix="/api/v1", tags=["进度"])
app.include_router(admin_router, prefix="/api/v1", tags=["管理员"])
app.include_router(speed_quiz_router, prefix="/api/v1", tags=["抢答"])
app.include_router(monitor_router, prefix="/api/v1", tags=["监控"])
app.include_router(ai_digest_router, tags=["AI 日报"])
app.include_router(alarm_router, prefix="/api/v1", tags=["闹钟"])


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
