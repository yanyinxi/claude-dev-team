"""
抢答模式 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import get_current_user
from models.schema import (
    SpeedQuizStartRequest,
    SpeedQuizSubmitRequest,
    SpeedQuizStartResponse,
    SpeedQuizSubmitResponse,
    SpeedQuizStatsResponse,
    SpeedQuizHistoryResponse
)
from services.speed_quiz_service import SpeedQuizService

router = APIRouter(prefix="/speed-quiz", tags=["speed-quiz"])
service = SpeedQuizService()


@router.post("/start", response_model=SpeedQuizStartResponse)
async def start_battle(
    request: SpeedQuizStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """开始抢答"""
    try:
        return await service.start_battle(db, current_user.id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submit", response_model=SpeedQuizSubmitResponse)
async def submit_answer(
    request: SpeedQuizSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """提交答案"""
    try:
        return await service.submit_answer(db, current_user.id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stats", response_model=SpeedQuizStatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取战绩统计"""
    return await service.get_stats(db, current_user.id)


@router.get("/history", response_model=SpeedQuizHistoryResponse)
async def get_history(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取历史记录"""
    return await service.get_history(db, current_user.id, page, page_size)
