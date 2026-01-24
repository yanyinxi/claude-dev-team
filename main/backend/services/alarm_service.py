"""
闹钟服务 - 学习闹钟业务逻辑
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload

from models.db import AlarmRule, AlarmSession, User
from models.schema import AlarmRuleCreate, AlarmRuleUpdate, AlarmRuleResponse, AlarmStatusResponse, AlarmValidateResponse


class AlarmService:
    """闹钟服务类"""

    @staticmethod
    async def get_effective_rule(user_id: int, db: AsyncSession) -> Optional[AlarmRule]:
        """
        获取生效的规则（个性化优先于全局）

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            生效的规则，如果没有则返回 None
        """
        # 获取用户信息
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return None

        # 优先查找个性化规则
        result = await db.execute(
            select(AlarmRule).where(
                and_(
                    AlarmRule.rule_type == "personal",
                    AlarmRule.student_nickname == user.nickname,
                    AlarmRule.is_active == True
                )
            )
        )
        personal_rule = result.scalar_one_or_none()
        if personal_rule:
            return personal_rule

        # 查找全局规则
        result = await db.execute(
            select(AlarmRule).where(
                and_(
                    AlarmRule.rule_type == "global",
                    AlarmRule.is_active == True
                )
            )
        )
        global_rule = result.scalar_one_or_none()
        return global_rule

    @staticmethod
    async def start_session(user_id: int, db: AsyncSession) -> AlarmSession:
        """
        开始学习会话

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            创建的学习会话

        业务流程：
        1. 获取生效的规则
        2. 创建 studying 会话
        3. 自动创建下一个 resting 会话
        """
        # 获取生效的规则
        rule = await AlarmService.get_effective_rule(user_id, db)
        if not rule:
            raise ValueError("没有找到生效的闹钟规则")

        # 使用服务器时间
        now = datetime.utcnow()

        # 创建学习会话
        study_session = AlarmSession(
            user_id=user_id,
            session_type="studying",
            start_time=now,
            end_time=now + timedelta(minutes=rule.study_duration),
            rule_id=rule.id
        )
        db.add(study_session)

        # 创建休息会话
        rest_session = AlarmSession(
            user_id=user_id,
            session_type="resting",
            start_time=now + timedelta(minutes=rule.study_duration),
            end_time=now + timedelta(minutes=rule.study_duration + rule.rest_duration),
            rule_id=rule.id
        )
        db.add(rest_session)

        await db.commit()
        await db.refresh(study_session)

        return study_session

    @staticmethod
    async def get_current_status(user_id: int, db: AsyncSession) -> AlarmStatusResponse:
        """
        获取当前学习状态

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            当前状态响应
        """
        now = datetime.utcnow()

        # 查找当前时间段的会话
        result = await db.execute(
            select(AlarmSession).where(
                and_(
                    AlarmSession.user_id == user_id,
                    AlarmSession.start_time <= now,
                    AlarmSession.end_time > now
                )
            ).options(selectinload(AlarmSession.rule))
        )
        current_session = result.scalar_one_or_none()

        if not current_session:
            # 没有进行中的会话
            return AlarmStatusResponse(
                session_type="idle",
                start_time=None,
                end_time=None,
                remaining_seconds=0,
                is_blocked=False,
                rule=None
            )

        # 计算剩余秒数
        remaining_seconds = int((current_session.end_time - now).total_seconds())

        # 判断是否被阻止操作
        is_blocked = current_session.session_type == "resting"

        return AlarmStatusResponse(
            session_type=current_session.session_type,
            start_time=current_session.start_time,
            end_time=current_session.end_time,
            remaining_seconds=max(0, remaining_seconds),
            is_blocked=is_blocked,
            rule=AlarmRuleResponse.model_validate(current_session.rule) if current_session.rule else None
        )

    @staticmethod
    async def validate_operation(user_id: int, db: AsyncSession) -> AlarmValidateResponse:
        """
        验证是否可以操作

        Args:
            user_id: 用户ID
            db: 数据库会话

        Returns:
            验证响应
        """
        status = await AlarmService.get_current_status(user_id, db)

        if status.is_blocked:
            return AlarmValidateResponse(
                can_operate=False,
                reason=f"休息时间，请等待 {status.remaining_seconds} 秒后再继续学习",
                remaining_seconds=status.remaining_seconds
            )

        return AlarmValidateResponse(
            can_operate=True,
            reason=None,
            remaining_seconds=0
        )

    @staticmethod
    async def create_rule(rule_data: AlarmRuleCreate, db: AsyncSession) -> AlarmRule:
        """
        创建闹钟规则

        Args:
            rule_data: 规则数据
            db: 数据库会话

        Returns:
            创建的规则
        """
        # 验证个性化规则必须有学生昵称
        if rule_data.rule_type == "personal" and not rule_data.student_nickname:
            raise ValueError("个性化规则必须指定学生昵称")

        # 创建规则
        rule = AlarmRule(
            rule_type=rule_data.rule_type,
            student_nickname=rule_data.student_nickname,
            study_duration=rule_data.study_duration,
            rest_duration=rule_data.rest_duration,
            is_active=True
        )
        db.add(rule)
        await db.commit()
        await db.refresh(rule)

        return rule

    @staticmethod
    async def update_rule(rule_id: int, rule_data: AlarmRuleUpdate, db: AsyncSession) -> AlarmRule:
        """
        更新闹钟规则

        Args:
            rule_id: 规则ID
            rule_data: 规则数据
            db: 数据库会话

        Returns:
            更新后的规则
        """
        result = await db.execute(select(AlarmRule).where(AlarmRule.id == rule_id))
        rule = result.scalar_one_or_none()
        if not rule:
            raise ValueError("规则不存在")

        # 更新字段
        if rule_data.study_duration is not None:
            rule.study_duration = rule_data.study_duration
        if rule_data.rest_duration is not None:
            rule.rest_duration = rule_data.rest_duration
        if rule_data.is_active is not None:
            rule.is_active = rule_data.is_active

        rule.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(rule)

        return rule

    @staticmethod
    async def delete_rule(rule_id: int, db: AsyncSession) -> None:
        """
        删除闹钟规则

        Args:
            rule_id: 规则ID
            db: 数据库会话
        """
        result = await db.execute(select(AlarmRule).where(AlarmRule.id == rule_id))
        rule = result.scalar_one_or_none()
        if not rule:
            raise ValueError("规则不存在")

        await db.delete(rule)
        await db.commit()

    @staticmethod
    async def toggle_rule(rule_id: int, db: AsyncSession) -> AlarmRule:
        """
        启用/禁用规则

        Args:
            rule_id: 规则ID
            db: 数据库会话

        Returns:
            更新后的规则
        """
        result = await db.execute(select(AlarmRule).where(AlarmRule.id == rule_id))
        rule = result.scalar_one_or_none()
        if not rule:
            raise ValueError("规则不存在")

        rule.is_active = not rule.is_active
        rule.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(rule)

        return rule

    @staticmethod
    async def get_all_rules(db: AsyncSession) -> list[AlarmRule]:
        """
        获取所有规则

        Args:
            db: 数据库会话

        Returns:
            规则列表
        """
        result = await db.execute(select(AlarmRule).order_by(AlarmRule.created_at.desc()))
        rules = result.scalars().all()
        return list(rules)
