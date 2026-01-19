"""
进度路由 - 获取学习进度、成就、错题本、学习记录
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, text
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user
from models.db import (
    User,
    WrongQuestion,
    Question,
    UserProgress,
    Achievement,
    UserAchievement,
)
from models.schema import (
    ProgressResponse,
    WrongQuestionsListResponse,
    WrongQuestionResponse,
    StudyRecordsResponse,
    StudyRecordResponse,
)


router = APIRouter()


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    获取用户学习进度
    返回：总答题数、正确数、正确率、连击数、今日完成数
    """
    # 总答题数
    result = await db.execute(
        select(func.count(UserProgress.id)).where(
            UserProgress.user_id == current_user.id
        )
    )
    total_questions = result.scalar() or 0

    # 正确数
    result = await db.execute(
        select(func.count(UserProgress.id)).where(
            and_(
                UserProgress.user_id == current_user.id, UserProgress.is_correct == True
            )
        )
    )
    correct_answers = result.scalar() or 0

    # 正确率
    accuracy = (
        round(correct_answers / total_questions * 100, 1)
        if total_questions > 0
        else 0.0
    )

    # 连击数（获取最近一次连续答对的数量）
    result = await db.execute(
        select(UserProgress)
        .where(UserProgress.user_id == current_user.id)
        .order_by(UserProgress.answered_at.desc())
        .limit(100)
    )
    progress_list = result.scalars().all()

    streak = 0
    for p in progress_list:
        if p.is_correct:
            streak += 1
        else:
            break

    # 今日完成数
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(func.count(UserProgress.id)).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.answered_at >= today_start,
            )
        )
    )
    completed_today = result.scalar() or 0

    return ProgressResponse(
        total_questions=total_questions,
        correct_answers=correct_answers,
        accuracy=accuracy,
        streak=streak,
        daily_goal=20,
        completed_today=completed_today,
    )


@router.get("/achievements", response_model=list)
async def get_achievements(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    获取用户成就列表
    返回：所有成就及解锁状态
    """
    # 获取所有成就
    result = await db.execute(select(Achievement))
    all_achievements = result.scalars().all()

    # 获取用户已解锁的成就ID
    result = await db.execute(
        select(UserAchievement.achievement_id).where(
            UserAchievement.user_id == current_user.id
        )
    )
    unlocked_ids = set(result.scalars().all())

    # 构建响应
    achievements = []
    for achievement in all_achievements:
        is_unlocked = achievement.id in unlocked_ids
        achievements.append(
            {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "badge_icon": achievement.badge_icon,
                "is_unlocked": is_unlocked,
                "unlocked_at": None,  # 可以扩展获取解锁时间
            }
        )

    return achievements


@router.get("/wrong-questions", response_model=WrongQuestionsListResponse)
async def get_wrong_questions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户错题本
    返回：错题列表及分页信息
    """
    # 获取总数量
    result = await db.execute(
        select(func.count(WrongQuestion.id)).where(
            WrongQuestion.user_id == current_user.id
        )
    )
    total = result.scalar() or 0

    # 获取错题列表
    offset = (page - 1) * page_size
    result = await db.execute(
        select(WrongQuestion)
        .options(selectinload(WrongQuestion.question))
        .where(WrongQuestion.user_id == current_user.id)
        .order_by(WrongQuestion.last_wrong_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    wrong_questions = result.scalars().all()

    # 转换为响应模型
    items = []
    for wq in wrong_questions:
        q = wq.question
        items.append(
            WrongQuestionResponse(
                id=wq.id,
                question_id=q.id,
                question_text=q.question_text,
                option_a=q.option_a,
                option_b=q.option_b,
                option_c=q.option_c,
                option_d=q.option_d,
                correct_answer=q.correct_answer,
                explanation=q.explanation,
                module=q.module,
                difficulty=q.difficulty,
                wrong_count=wq.wrong_count,
                last_wrong_at=wq.last_wrong_at,
            )
        )

    return WrongQuestionsListResponse(
        items=items, total=total, page=page, page_size=page_size
    )


@router.get("/study-records", response_model=StudyRecordsResponse)
async def get_study_records(
    year: int = Query(None, description="年份，默认今年"),
    month: int = Query(None, description="月份，默认今年"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户学习记录（用于日历展示）
    返回：每日学习记录、總學習天數、連續學習天數
    """
    import calendar

    now = datetime.utcnow()
    target_year = year or now.year
    target_month = month or now.month

    # 获取当月的学习记录
    month_start = datetime(target_year, target_month, 1)
    month_end = (
        datetime(target_year, target_month + 1, 1)
        if target_month < 12
        else datetime(target_year + 1, 1, 1)
    )

    result = await db.execute(
        select(
            func.date(UserProgress.answered_at).label("date"),
            func.count(UserProgress.id).label("count"),
            func.sum(text("CASE WHEN is_correct THEN 1 ELSE 0 END")).label("correct"),
        )
        .where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.answered_at >= month_start,
                UserProgress.answered_at < month_end,
            )
        )
        .group_by(func.date(UserProgress.answered_at))
    )
    daily_records = result.all()

    # 构建响应
    records = []
    total_score = 0
    for date, count, correct in daily_records:
        records.append(
            StudyRecordResponse(
                date=date.strftime("%Y-%m-%d")
                if isinstance(date, datetime)
                else str(date),
                questions_completed=count,
                total_score=correct * 10 if correct else 0,  # 简化计分
            )
        )
        total_score += correct * 10 if correct else 0

    # 计算学习天数
    total_days = len(records)

    # 计算连续学习天数
    consecutive_days = 0
    if records:
        # 检查今天是否学习
        today_str = now.strftime("%Y-%m-%d")
        has_today = any(r.date == today_str for r in records)

        if has_today:
            consecutive_days = 1
            # 向前计算连续天数
            check_date = now
            while True:
                check_date = check_date - timedelta(days=1)
                date_str = check_date.strftime("%Y-%m-%d")
                has_record = any(r.date == date_str for r in records)
                if has_record:
                    consecutive_days += 1
                else:
                    break
        else:
            consecutive_days = 0

    return StudyRecordsResponse(
        records=records, total_days=total_days, consecutive_days=consecutive_days
    )
