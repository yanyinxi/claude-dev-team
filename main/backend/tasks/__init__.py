"""
Celery 异步任务模块
"""

from .ai_digest.task import celery_app, run_ai_digest

__all__ = ["celery_app", "run_ai_digest"]
