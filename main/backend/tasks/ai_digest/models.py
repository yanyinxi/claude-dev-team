"""
AI 日报数据库模型

表结构：
- id: 主键
- date: 日期（唯一索引）
- title: 标题
- summary: 摘要（今日最重要的 3 条）
- content: 完整内容（JSON 格式）
- created_at: 创建时间
- updated_at: 更新时间
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AiDigest(Base):
    """AI 日报模型"""

    __tablename__ = "ai_digests"

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 日期（唯一索引）
    date = Column(Date, unique=True, nullable=False, index=True, comment="日报日期")

    # 标题
    title = Column(String(200), nullable=False, comment="日报标题")

    # 摘要（今日最重要的 3 条）
    summary = Column(Text, nullable=False, comment="今日要闻摘要（JSON 数组）")

    # 完整内容（JSON 格式）
    content = Column(Text, nullable=False, comment="完整日报内容（JSON 格式）")

    # 统计信息
    total_items = Column(Integer, default=0, comment="资讯总数")

    # 时间戳
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False, comment="创建时间"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新时间",
    )

    # 索引
    __table_args__ = (
        Index("idx_date", "date"),
        Index("idx_created_at", "created_at"),
    )

    def __repr__(self):
        return f"<AiDigest(id={self.id}, date={self.date}, title={self.title})>"

    def to_dict(self):
        """转换为字典"""
        import json

        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "title": self.title,
            "summary": json.loads(self.summary) if self.summary else [],
            "content": self.content,  # content 是 JSON 字符串，直接返回
            "total_items": self.total_items,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
