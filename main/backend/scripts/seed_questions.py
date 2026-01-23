import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到 python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.db import Question
from core.config import settings


async def seed_questions():
    print(f"Connecting to database: {settings.DATABASE_URL}")

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
        if "sqlite" in settings.DATABASE_URL
        else {},
    )

    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with AsyncSessionLocal() as session:
        print("Start seeding questions...")

        # 预定义一些题目模板
        modules = ["vocabulary", "grammar", "reading"]
        difficulties = [1, 2, 3, 4, 5]

        new_questions = []

        for module in modules:
            for diff in difficulties:
                # 每个组合添加 5 道题
                for i in range(5):
                    q = None
                    if module == "vocabulary":
                        q = Question(
                            module=module,
                            difficulty=diff,
                            question_text=f"[Level {diff}] What implies the word 'Test_{diff}_{i}'?",
                            option_a="Option A",
                            option_b="Option B",
                            option_c="Option C",
                            option_d="Option D",
                            correct_answer="A",
                            explanation=f"This is a vocabulary question for level {diff}.",
                        )
                    elif module == "grammar":
                        q = Question(
                            module=module,
                            difficulty=diff,
                            question_text=f"[Level {diff}] She _____ to the store yesterday (Test_{i}).",
                            option_a="go",
                            option_b="went",
                            option_c="gone",
                            option_d="going",
                            correct_answer="B",
                            explanation=f"This is a grammar question for level {diff}.",
                        )
                    elif module == "reading":
                        q = Question(
                            module=module,
                            difficulty=diff,
                            question_text=f"[Level {diff}] Read the text: 'The sun rises in the east.' Question {i}: Where does the sun rise?",
                            option_a="West",
                            option_b="North",
                            option_c="East",
                            option_d="South",
                            correct_answer="C",
                            explanation=f"This is a reading question for level {diff}.",
                        )

                    if q:
                        new_questions.append(q)

        session.add_all(new_questions)
        await session.commit()
        print(f"Successfully added {len(new_questions)} questions covering all levels!")


if __name__ == "__main__":
    asyncio.run(seed_questions())
