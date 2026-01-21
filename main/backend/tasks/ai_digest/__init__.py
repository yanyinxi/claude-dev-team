"""
AI 日报模块

包含：
- models.py: 数据库模型
- schemas.py: Pydantic Schema
- service.py: 业务逻辑
- task.py: Celery 定时任务
"""

from .models import AiDigest
from .schemas import (
    AiDigestCreate,
    AiDigestUpdate,
    AiDigestResponse,
    AiDigestListItem,
    AiDigestSummaryItem,
)
from .service import AiDigestService
from .task import celery_app, run_ai_digest
# Don't import router here to avoid circular import

__all__ = [
    "AiDigest",
    "AiDigestCreate",
    "AiDigestUpdate",
    "AiDigestResponse",
    "AiDigestListItem",
    "AiDigestSummaryItem",
    "AiDigestService",
    "celery_app",
    "run_ai_digest",
]
