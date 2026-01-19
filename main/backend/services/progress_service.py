"""
进度服务 - 处理答题和进度统计
"""
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from models.db import User, Question, UserProgress, Achievement, UserAchievement, WrongQuestion
from models.schema import AnswerRequest, AnswerResponse, AchievementResponse
from core.exceptions import NotFoundException


class ProgressService:
    """进度服务类"""

    @staticmethod
    async def submit_answer(
        request: AnswerRequest,
        user: User,
        db: AsyncSession
    ) -> AnswerResponse:
        """
        提交答案并计算得分、连击、成就
        """
        # 获取题目
        result = await db.execute(
            select(Question).where(Question.id == request.question_id)
        )
        question = result.scalar_one_or_none()

        if not question:
            raise NotFoundException("question", request.question_id)

        # 判断答案是否正确
        is_correct = request.answer == question.correct_answer

        # 记录答题进度
        progress = UserProgress(
            user_id=user.id,
            question_id=question.id,
            is_correct=is_correct,
            answer_time=request.answer_time
        )
        db.add(progress)

        # 计算连击
        streak = await ProgressService._calculate_streak(user.id, is_correct, db)

        # 计算得分
        score = 0
        if is_correct:
            score = ProgressService._calculate_score(request.answer_time, streak)
            # 更新用户总分
            user.total_score += score
        else:
            # 记录错题
            await ProgressService._record_wrong_question(user.id, question.id, db)

        # 检查成就
        new_achievements = await ProgressService._check_achievements(user.id, streak, db)

        # 生成鼓励语
        encouragement = ProgressService._generate_encouragement(is_correct, streak, score)

        await db.commit()

        return AnswerResponse(
            is_correct=is_correct,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            score=score,
            streak=streak,
            new_achievements=[AchievementResponse.model_validate(a) for a in new_achievements],
            encouragement=encouragement
        )

    @staticmethod
    async def _calculate_streak(user_id: int, is_correct: bool, db: AsyncSession) -> int:
        """
        计算连击数
        如果答对，连击+1；如果答错，连击归零
        """
        if not is_correct:
            return 0

        # 获取最近的答题记录（按时间倒序）
        result = await db.execute(
            select(UserProgress)
            .where(UserProgress.user_id == user_id)
            .order_by(UserProgress.answered_at.desc())
            .limit(100)  # 限制查询数量
        )
        recent_progress = result.scalars().all()

        # 计算连续答对的题目数
        streak = 1  # 当前这题答对了，至少是1
        for p in recent_progress:
            if p.is_correct:
                streak += 1
            else:
                break

        return streak

    @staticmethod
    def _calculate_score(answer_time: int, streak: int) -> int:
        """
        计算得分
        基础分 = 10分
        连击加成:
          - 连击2-5: x1.5
          - 连击6-10: x2.0
          - 连击11+: x2.5
        速度加成: 答题时间 < 10秒 ? 5分 : 0分
        """
        base_score = 10

        # 连击加成
        if streak >= 11:
            multiplier = 2.5
        elif streak >= 6:
            multiplier = 2.0
        elif streak >= 2:
            multiplier = 1.5
        else:
            multiplier = 1.0

        # 速度加成
        speed_bonus = 5 if answer_time < 10 else 0

        total_score = int(base_score * multiplier) + speed_bonus
        return total_score

    @staticmethod
    async def _record_wrong_question(user_id: int, question_id: int, db: AsyncSession):
        """记录错题"""
        # 查询是否已存在
        result = await db.execute(
            select(WrongQuestion).where(
                and_(
                    WrongQuestion.user_id == user_id,
                    WrongQuestion.question_id == question_id
                )
            )
        )
        wrong_question = result.scalar_one_or_none()

        if wrong_question:
            # 已存在，增加错误次数
            wrong_question.wrong_count += 1
            wrong_question.last_wrong_at = datetime.utcnow()
        else:
            # 不存在，创建新记录
            wrong_question = WrongQuestion(
                user_id=user_id,
                question_id=question_id,
                wrong_count=1
            )
            db.add(wrong_question)

    @staticmethod
    async def _check_achievements(
        user_id: int,
        streak: int,
        db: AsyncSession
    ) -> List[Achievement]:
        """
        检查是否解锁新成就
        """
        new_achievements = []

        # 获取所有成就
        result = await db.execute(select(Achievement))
        all_achievements = result.scalars().all()

        # 获取用户已解锁的成就
        result = await db.execute(
            select(UserAchievement.achievement_id).where(UserAchievement.user_id == user_id)
        )
        unlocked_ids = set(result.scalars().all())

        # 获取用户统计数据
        result = await db.execute(
            select(func.count(UserProgress.id))
            .where(UserProgress.user_id == user_id)
        )
        total_questions = result.scalar() or 0

        # 检查每个成就
        for achievement in all_achievements:
            # 如果已解锁，跳过
            if achievement.id in unlocked_ids:
                continue

            # 检查是否满足条件
            is_unlocked = False
            if achievement.requirement_type == "total_questions":
                is_unlocked = total_questions >= achievement.requirement_value
            elif achievement.requirement_type == "streak":
                is_unlocked = streak >= achievement.requirement_value

            # 解锁成就
            if is_unlocked:
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                db.add(user_achievement)
                new_achievements.append(achievement)

        return new_achievements

    @staticmethod
    def _generate_encouragement(is_correct: bool, streak: int, score: int) -> str:
        """生成鼓励语"""
        if not is_correct:
            return "没关系，继续加油！错题会记录在错题本中哦~"

        if streak >= 10:
            return f"太厉害了！连续答对{streak}题！你是学霸！🌟"
        elif streak >= 5:
            return f"太棒了！连续答对{streak}题！继续保持！⭐"
        elif streak >= 3:
            return f"很好！连续答对{streak}题！加油！✨"
        else:
            return f"答对了！获得{score}分！💪"
