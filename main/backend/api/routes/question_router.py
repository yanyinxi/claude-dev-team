"""
题目路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import get_current_user
from models.db import User
from models.schema import QuestionResponse
from services.question_service import QuestionService


router = APIRouter()


@router.get("/questions/random", response_model=QuestionResponse)
async def get_random_question(
    module: Optional[str] = Query(None, description="模块: vocabulary/grammar/reading"),
    difficulty: Optional[int] = Query(None, ge=1, le=5, description="难度等级 1-5"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取随机题目
    根据模块和难度获取一道随机题目
    """
    return await QuestionService.get_random_question(db, module, difficulty)
