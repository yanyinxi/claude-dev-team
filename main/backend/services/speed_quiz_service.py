"""
抢答模式业务逻辑
"""
import random
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from models.db import SpeedQuizBattle, SpeedQuizDetail, Question
from models.schema import (
    SpeedQuizStartRequest,
    SpeedQuizSubmitRequest,
    SpeedQuizStartResponse,
    SpeedQuizSubmitResponse,
    SpeedQuizStatsResponse,
    SpeedQuizHistoryResponse,
    SpeedQuizBattleResponse,
    QuestionResponse
)


class SpeedQuizService:
    """抢答服务"""

    @staticmethod
    def calculate_ai_time(difficulty: int) -> int:
        """计算 AI 答题时间（毫秒）"""
        base_times = {
            1: (5000, 8000),
            2: (6000, 10000),
            3: (8000, 15000),
            4: (12000, 18000),
            5: (15000, 20000)
        }
        min_time, max_time = base_times.get(difficulty, (8000, 15000))
        base = random.randint(min_time, max_time)
        variation = random.uniform(0.8, 1.2)
        return int(base * variation)

    @staticmethod
    def ai_should_answer_correct(difficulty: int) -> bool:
        """判断 AI 是否答对"""
        accuracy_rates = {
            1: 0.90,
            2: 0.85,
            3: 0.80,
            4: 0.70,
            5: 0.65
        }
        rate = accuracy_rates.get(difficulty, 0.75)
        return random.random() < rate

    @staticmethod
    def get_ai_answer(correct_answer: str, should_correct: bool) -> str:
        """获取 AI 答案"""
        if should_correct:
            return correct_answer
        options = ['A', 'B', 'C', 'D']
        options.remove(correct_answer)
        return random.choice(options)

    @staticmethod
    def determine_winner(
        user_answer: str,
        user_time: int,
        ai_answer: str,
        ai_time: int,
        correct_answer: str
    ) -> str:
        """判定胜负"""
        user_correct = user_answer == correct_answer
        ai_correct = ai_answer == correct_answer

        if user_correct and not ai_correct:
            return "user"
        elif ai_correct and not user_correct:
            return "ai"
        elif user_correct and ai_correct:
            return "user" if user_time < ai_time else "ai"
        else:
            return "tie"

    async def start_battle(
        self,
        db: AsyncSession,
        user_id: int,
        request: SpeedQuizStartRequest
    ) -> SpeedQuizStartResponse:
        """开始抢答"""
        # 创建对战记录
        battle = SpeedQuizBattle(
            user_id=user_id,
            difficulty=request.difficulty,
            module=request.module,
            total_questions=request.rounds
        )
        db.add(battle)
        await db.commit()
        await db.refresh(battle)

        # 获取第一题
        question = await self._get_random_question(db, request.difficulty, request.module)
        if not question:
            raise ValueError("No questions available")

        return SpeedQuizStartResponse(
            battle_id=battle.id,
            question=QuestionResponse.from_orm(question)
        )

    async def submit_answer(
        self,
        db: AsyncSession,
        user_id: int,
        request: SpeedQuizSubmitRequest
    ) -> SpeedQuizSubmitResponse:
        """提交答案"""
        # 验证对战
        query = select(SpeedQuizBattle).where(
            SpeedQuizBattle.id == request.battle_id,
            SpeedQuizBattle.user_id == user_id
        )
        result = await db.execute(query)
        battle = result.scalar_one_or_none()
        if not battle:
            raise ValueError("Battle not found")

        # 获取题目
        query = select(Question).where(Question.id == request.question_id)
        result = await db.execute(query)
        question = result.scalar_one_or_none()
        if not question:
            raise ValueError("Question not found")

        # AI 答题
        should_correct = self.ai_should_answer_correct(question.difficulty)
        ai_answer = self.get_ai_answer(question.correct_answer, should_correct)
        ai_time = self.calculate_ai_time(question.difficulty)

        # 判定胜负
        winner = self.determine_winner(
            request.answer,
            request.answer_time,
            ai_answer,
            ai_time,
            question.correct_answer
        )

        # 记录详情
        detail = SpeedQuizDetail(
            battle_id=battle.id,
            question_id=question.id,
            user_answer=request.answer,
            user_time=request.answer_time,
            ai_answer=ai_answer,
            ai_time=ai_time,
            correct_answer=question.correct_answer,
            winner=winner
        )
        db.add(detail)

        # 更新对战统计
        if request.answer == question.correct_answer:
            battle.user_correct += 1
        if ai_answer == question.correct_answer:
            battle.ai_correct += 1
        if winner == "user":
            battle.user_wins += 1
        elif winner == "ai":
            battle.ai_wins += 1

        await db.commit()

        # 获取下一题
        count_query = select(func.count()).select_from(SpeedQuizDetail).where(
            SpeedQuizDetail.battle_id == battle.id
        )
        result = await db.execute(count_query)
        answered_count = result.scalar()

        next_question = None
        if answered_count < battle.total_questions:
            next_q = await self._get_random_question(db, battle.difficulty, battle.module)
            if next_q:
                next_question = QuestionResponse.from_orm(next_q)

        return SpeedQuizSubmitResponse(
            is_correct=request.answer == question.correct_answer,
            ai_answer=ai_answer,
            ai_time=ai_time,
            correct_answer=question.correct_answer,
            winner=winner,
            next_question=next_question
        )

    async def get_stats(self, db: AsyncSession, user_id: int) -> SpeedQuizStatsResponse:
        """获取战绩统计"""
        query = select(SpeedQuizBattle).where(SpeedQuizBattle.user_id == user_id)
        result = await db.execute(query)
        battles = result.scalars().all()

        total_battles = len(battles)
        wins = sum(1 for b in battles if b.user_wins > b.ai_wins)
        losses = sum(1 for b in battles if b.user_wins < b.ai_wins)
        win_rate = wins / total_battles if total_battles > 0 else 0.0

        # 最快答题时间
        battle_ids = [b.id for b in battles]
        if battle_ids:
            fastest_query = select(func.min(SpeedQuizDetail.user_time)).where(
                SpeedQuizDetail.battle_id.in_(battle_ids),
                SpeedQuizDetail.user_answer == SpeedQuizDetail.correct_answer
            )
            result = await db.execute(fastest_query)
            fastest_time = result.scalar() or 0
        else:
            fastest_time = 0

        # 最长连胜
        max_streak = self._calculate_max_streak(battles)

        return SpeedQuizStatsResponse(
            total_battles=total_battles,
            wins=wins,
            losses=losses,
            win_rate=round(win_rate, 2),
            fastest_time=fastest_time,
            max_streak=max_streak
        )

    async def get_history(
        self,
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
    ) -> SpeedQuizHistoryResponse:
        """获取历史记录"""
        query = select(SpeedQuizBattle).where(
            SpeedQuizBattle.user_id == user_id
        ).order_by(desc(SpeedQuizBattle.created_at))

        # 获取总数
        count_query = select(func.count()).select_from(SpeedQuizBattle).where(
            SpeedQuizBattle.user_id == user_id
        )
        result = await db.execute(count_query)
        total = result.scalar()

        # 分页查询
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        battles = result.scalars().all()

        return SpeedQuizHistoryResponse(
            battles=[SpeedQuizBattleResponse.from_orm(b) for b in battles],
            total=total,
            page=page,
            page_size=page_size
        )

    async def _get_random_question(
        self,
        db: AsyncSession,
        difficulty: int,
        module: str
    ) -> Optional[Question]:
        """随机获取题目"""
        query = select(Question).where(
            Question.difficulty == difficulty,
            Question.module == module
        )
        result = await db.execute(query)
        questions = result.scalars().all()
        return random.choice(questions) if questions else None

    def _calculate_max_streak(self, battles: list) -> int:
        """计算最长连胜"""
        max_streak = 0
        current_streak = 0
        for battle in sorted(battles, key=lambda b: b.created_at):
            if battle.user_wins > battle.ai_wins:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak
