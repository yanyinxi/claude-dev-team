"""
AI 日报服务层

业务逻辑：
1. 创建日报
2. 获取最新日报
3. 获取指定日期日报
4. 获取日报列表
5. 更新日报
"""

import json
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select, func

from .models import AiDigest
from .schemas import (
    AiDigestCreate,
    AiDigestUpdate,
    AiDigestResponse,
    AiDigestListItem,
)


class AiDigestService:
    """AI 日报服务"""

    @staticmethod
    async def create(db: AsyncSession, data: AiDigestCreate) -> AiDigest:
        """
        创建 AI 日报

        Args:
            db: 数据库会话
            data: 日报数据

        Returns:
            AiDigest: 创建的日报对象

        Raises:
            ValueError: 如果日期已存在
        """
        # 检查日期是否已存在
        stmt = select(AiDigest).where(AiDigest.date == data.digest_date)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError(f"日报已存在: {data.digest_date}")

        # 创建日报
        digest = AiDigest(
            date=data.digest_date,
            title=data.title,
            summary=json.dumps(
                [item.model_dump() for item in data.summary], ensure_ascii=False
            ),
            content=json.dumps(data.content, ensure_ascii=False),  # 将字典转换为 JSON 字符串
            total_items=data.total_items,
        )

        db.add(digest)
        await db.commit()
        await db.refresh(digest)

        return digest

    @staticmethod
    async def get_latest(db: AsyncSession) -> Optional[AiDigest]:
        """
        获取最新日报

        Args:
            db: 数据库会话

        Returns:
            Optional[AiDigest]: 最新日报，如果不存在返回 None
        """
        stmt = select(AiDigest).order_by(desc(AiDigest.date)).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_date(db: AsyncSession, target_date: date) -> Optional[AiDigest]:
        """
        获取指定日期的日报

        Args:
            db: 数据库会话
            target_date: 目标日期

        Returns:
            Optional[AiDigest]: 日报对象，如果不存在返回 None
        """
        stmt = select(AiDigest).where(AiDigest.date == target_date)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession, skip: int = 0, limit: int = 10
    ) -> List[AiDigest]:
        """
        获取日报列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 返回数量

        Returns:
            List[AiDigest]: 日报列表
        """
        stmt = (
            select(AiDigest)
            .order_by(desc(AiDigest.date))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession, digest_id: int, data: AiDigestUpdate
    ) -> Optional[AiDigest]:
        """
        更新日报

        Args:
            db: 数据库会话
            digest_id: 日报 ID
            data: 更新数据

        Returns:
            Optional[AiDigest]: 更新后的日报对象，如果不存在返回 None
        """
        stmt = select(AiDigest).where(AiDigest.id == digest_id)
        result = await db.execute(stmt)
        digest = result.scalar_one_or_none()
        if not digest:
            return None

        # 更新字段
        if data.title is not None:
            digest.title = data.title
        if data.summary is not None:
            digest.summary = json.dumps(
                [item.model_dump() for item in data.summary], ensure_ascii=False
            )
        if data.content is not None:
            digest.content = json.dumps(data.content, ensure_ascii=False)  # 将字典转换为 JSON 字符串
        if data.total_items is not None:
            digest.total_items = data.total_items

        digest.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(digest)

        return digest

    @staticmethod
    async def delete(db: AsyncSession, digest_id: int) -> bool:
        """
        删除日报

        Args:
            db: 数据库会话
            digest_id: 日报 ID

        Returns:
            bool: 是否删除成功
        """
        stmt = select(AiDigest).where(AiDigest.id == digest_id)
        result = await db.execute(stmt)
        digest = result.scalar_one_or_none()
        if not digest:
            return False

        await db.delete(digest)
        await db.commit()

        return True

    @staticmethod
    async def count(db: AsyncSession) -> int:
        """
        获取日报总数

        Args:
            db: 数据库会话

        Returns:
            int: 日报总数
        """
        stmt = select(func.count()).select_from(AiDigest)
        result = await db.execute(stmt)
        return result.scalar_one() or 0
