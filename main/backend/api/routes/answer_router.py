"""
答题路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import get_current_user
from models.db import User
from models.schema import AnswerRequest, AnswerResponse
from services.progress_service import ProgressService


router = APIRouter()


@router.post("/answers", response_model=AnswerResponse)
async def submit_answer(
    request: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    提交答案
    提交用户的答案并返回结果和奖励信息
    """
    return await ProgressService.submit_answer(request, current_user, db)
