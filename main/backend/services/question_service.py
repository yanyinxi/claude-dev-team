"""
题目服务
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from models.db import Question
from models.schema import QuestionResponse
from core.exceptions import NotFoundException


class QuestionService:
    """题目服务类"""

    @staticmethod
    async def get_random_question(
        db: AsyncSession,
        module: Optional[str] = None,
        difficulty: Optional[int] = None
    ) -> QuestionResponse:
        """
        获取随机题目
        可以根据模块和难度筛选
        """
        # 构建查询
        query = select(Question)

        # 添加筛选条件
        if module:
            query = query.where(Question.module == module)
        if difficulty:
            query = query.where(Question.difficulty == difficulty)

        # 随机排序并获取一条
        query = query.order_by(func.random()).limit(1)

        result = await db.execute(query)
        question = result.scalar_one_or_none()

        if not question:
            raise NotFoundException("question", 0)

        return QuestionResponse.model_validate(question)
