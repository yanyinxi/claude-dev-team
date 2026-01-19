"""
管理员路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from core.database import get_db
from core.security import get_current_user
from models.db import User, Question
from models.schema import QuestionResponse

router = APIRouter()


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """验证管理员权限"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


@router.get("/admin/questions", response_model=List[QuestionResponse])
async def list_all_questions(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """获取所有题目"""
    result = await db.execute(select(Question).order_by(Question.id))
    questions = result.scalars().all()
    return questions


@router.post("/admin/questions", response_model=QuestionResponse)
async def create_question(
    question_data: dict,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """创建新题目"""
    question = Question(**question_data)
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question


@router.put("/admin/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: dict,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """更新题目"""
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    for key, value in question_data.items():
        setattr(question, key, value)

    await db.commit()
    await db.refresh(question)
    return question


@router.delete("/admin/questions/{question_id}")
async def delete_question(
    question_id: int,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """删除题目"""
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")

    await db.execute(delete(Question).where(Question.id == question_id))
    await db.commit()
    return {"message": "题目已删除"}
