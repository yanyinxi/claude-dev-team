"""
数据库连接和会话管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from typing import AsyncGenerator

from core.config import settings
from models.db import Base, User, Question, Achievement
from tasks.ai_digest.models import AiDigest


# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in settings.DATABASE_URL else None,
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """初始化数据库"""
    from core.security import get_password_hash

    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

    # 初始化示例数据
    async with AsyncSessionLocal() as session:
        # 检查是否已有数据
        from sqlalchemy import select
        result = await session.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            return  # 已有数据，跳过初始化

        # 创建管理员账号
        admin = User(
            nickname="管理员",
            role="admin",
            password_hash=get_password_hash(settings.ADMIN_PASSWORD),
            total_score=0
        )
        session.add(admin)

        # 创建示例题目
        sample_questions = [
            Question(
                module="vocabulary",
                difficulty=1,
                question_text="What is the meaning of 'happy'?",
                option_a="快乐的",
                option_b="悲伤的",
                option_c="生气的",
                option_d="害怕的",
                correct_answer="A",
                explanation="happy表示快乐的、高兴的"
            ),
            Question(
                module="vocabulary",
                difficulty=1,
                question_text="What is the meaning of 'cat'?",
                option_a="狗",
                option_b="猫",
                option_c="鸟",
                option_d="鱼",
                correct_answer="B",
                explanation="cat表示猫"
            ),
            Question(
                module="vocabulary",
                difficulty=2,
                question_text="What is the meaning of 'beautiful'?",
                option_a="丑陋的",
                option_b="美丽的",
                option_c="普通的",
                option_d="奇怪的",
                correct_answer="B",
                explanation="beautiful表示美丽的"
            ),
            Question(
                module="grammar",
                difficulty=1,
                question_text="I ___ a student.",
                option_a="am",
                option_b="is",
                option_c="are",
                option_d="be",
                correct_answer="A",
                explanation="主语是I，be动词用am"
            ),
            Question(
                module="grammar",
                difficulty=2,
                question_text="She ___ to school every day.",
                option_a="go",
                option_b="goes",
                option_c="going",
                option_d="went",
                correct_answer="B",
                explanation="主语是第三人称单数，动词要加s"
            ),
            Question(
                module="reading",
                difficulty=2,
                question_text="Tom likes apples. What does Tom like?",
                option_a="Bananas",
                option_b="Apples",
                option_c="Oranges",
                option_d="Grapes",
                correct_answer="B",
                explanation="文中说Tom likes apples"
            ),
            Question(
                module="vocabulary",
                difficulty=1,
                question_text="What is the meaning of 'dog'?",
                option_a="猫",
                option_b="狗",
                option_c="鸟",
                option_d="鱼",
                correct_answer="B",
                explanation="dog表示狗"
            ),
            Question(
                module="vocabulary",
                difficulty=2,
                question_text="What is the meaning of 'friend'?",
                option_a="敌人",
                option_b="朋友",
                option_c="老师",
                option_d="学生",
                correct_answer="B",
                explanation="friend表示朋友"
            ),
            Question(
                module="grammar",
                difficulty=1,
                question_text="They ___ playing football.",
                option_a="am",
                option_b="is",
                option_c="are",
                option_d="be",
                correct_answer="C",
                explanation="主语是They，be动词用are"
            ),
            Question(
                module="reading",
                difficulty=1,
                question_text="The cat is black. What color is the cat?",
                option_a="White",
                option_b="Black",
                option_c="Brown",
                option_d="Yellow",
                correct_answer="B",
                explanation="文中说The cat is black"
            ),
        ]

        for question in sample_questions:
            session.add(question)

        # 创建成就
        achievements = [
            Achievement(
                name="初学者",
                description="完成第1道题目",
                badge_icon="/badges/beginner.png",
                requirement_type="total_questions",
                requirement_value=1
            ),
            Achievement(
                name="勤奋学习",
                description="完成10道题目",
                badge_icon="/badges/diligent.png",
                requirement_type="total_questions",
                requirement_value=10
            ),
            Achievement(
                name="连击高手",
                description="连续答对5题",
                badge_icon="/badges/streak.png",
                requirement_type="streak",
                requirement_value=5
            ),
            Achievement(
                name="学霸",
                description="完成50道题目",
                badge_icon="/badges/master.png",
                requirement_type="total_questions",
                requirement_value=50
            ),
        ]

        for achievement in achievements:
            session.add(achievement)

        await session.commit()
        print("数据库初始化完成！")
