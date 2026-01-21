"""
添加 AI 日报表

创建时间: 2026-01-20
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


def upgrade(engine):
    """创建 ai_digests 表"""
    from sqlalchemy import MetaData, Table

    metadata = MetaData()

    # 创建 ai_digests 表
    ai_digests = Table(
        'ai_digests',
        metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('date', Date, unique=True, nullable=False, index=True, comment='日报日期'),
        Column('title', String(200), nullable=False, comment='日报标题'),
        Column('summary', Text, nullable=False, comment='今日要闻摘要（JSON 数组）'),
        Column('content', Text, nullable=False, comment='完整日报内容（JSON 格式）'),
        Column('total_items', Integer, default=0, comment='资讯总数'),
        Column('created_at', DateTime, default=datetime.utcnow, nullable=False, comment='创建时间'),
        Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间'),
        Index('idx_date', 'date'),
        Index('idx_created_at', 'created_at'),
    )

    metadata.create_all(engine)
    print("✅ ai_digests 表创建成功")


def downgrade(engine):
    """删除 ai_digests 表"""
    from sqlalchemy import MetaData, Table

    metadata = MetaData()
    metadata.reflect(bind=engine)

    if 'ai_digests' in metadata.tables:
        Table('ai_digests', metadata, autoload_with=engine).drop(engine)
        print("✅ ai_digests 表删除成功")


if __name__ == "__main__":
    # 测试迁移
    from sqlalchemy import create_engine
    import os

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    engine = create_engine(DATABASE_URL)

    print("执行迁移...")
    upgrade(engine)
    print("迁移完成！")
