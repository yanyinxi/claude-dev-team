"""
AI 日报定时任务

功能：
1. 每天早上 9:00 自动执行 AI 日报生成
2. 调用 Claude Code CLI 执行 ai-digest Skill
3. 记录执行结果和错误日志

依赖：
- Celery
- Redis
- Claude Code CLI

使用方法：
1. 启动 Redis: redis-server
2. 启动 Celery Worker: celery -A main.backend.tasks.ai_digest_task worker --loglevel=info
3. 启动 Celery Beat: celery -A main.backend.tasks.ai_digest_task beat --loglevel=info
"""

import os
import subprocess
import json
from datetime import datetime, date
from pathlib import Path

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session

from .schemas import AiDigestCreate, AiDigestSummaryItem
from .service import AiDigestService

# 配置日志
logger = get_task_logger(__name__)

# 创建 Celery 应用（不使用 Redis，使用数据库作为 broker）
celery_app = Celery(
    "ai_digest_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "sqla+sqlite:///celery.db"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "db+sqlite:///celery_results.db"),
)

# Celery 配置
celery_app.conf.update(
    # 时区设置
    timezone="Asia/Shanghai",
    enable_utc=True,
    # 任务结果过期时间（7 天）
    result_expires=7 * 24 * 60 * 60,
    # 任务序列化
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    # 定时任务配置
    beat_schedule={
        "ai-daily-digest": {
            "task": "main.backend.tasks.ai_digest_task.run_ai_digest",
            "schedule": crontab(hour=9, minute=0),  # 每天 9:00
            "options": {
                "expires": 3600,  # 任务 1 小时后过期
            },
        },
    },
)


@celery_app.task(
    bind=True,
    name="main.backend.tasks.ai_digest_task.run_ai_digest",
    max_retries=3,
    default_retry_delay=300,  # 5 分钟后重试
)
def run_ai_digest(self):
    """
    执行 AI 日报生成任务

    Returns:
        dict: 执行结果
            - status: success/error
            - timestamp: 执行时间
            - output: 输出内容
            - error: 错误信息（如果失败）
    """
    start_time = datetime.now()
    logger.info(f"[{start_time}] 开始执行 AI 日报任务...")

    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent.parent

    # 确保文档目录存在
    docs_dir = project_root / "main" / "docs" / "ai_digest"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # 日志目录
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"ai_digest_{start_time.strftime('%Y%m%d')}.log"

    try:
        # 调用 Claude Code CLI 执行 Skill
        logger.info("调用 Claude Code CLI...")

        result = subprocess.run(
            [
                "claude",
                "-p",
                "执行 /ai-digest 技能，生成今日 AI 日报",
                "--output-format",
                "json",
            ],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=600,  # 10 分钟超时
            env={**os.environ, "CLAUDE_NO_INTERACTIVE": "1"},
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 记录日志
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"执行时间: {start_time}\n")
            f.write(f"耗时: {duration:.2f} 秒\n")
            f.write(f"返回码: {result.returncode}\n")
            f.write(f"\n--- STDOUT ---\n{result.stdout}\n")
            if result.stderr:
                f.write(f"\n--- STDERR ---\n{result.stderr}\n")

        if result.returncode == 0:
            logger.info(f"✅ AI 日报任务完成，耗时 {duration:.2f} 秒")

            # 解析输出并保存到数据库
            try:
                # 从输出中提取 JSON 数据
                output_data = json.loads(result.stdout)

                # 创建数据库记录
                # TODO: 获取数据库会话
                # from main.backend.core.database import SessionLocal
                # db = SessionLocal()
                # try:
                #     digest_data = AiDigestCreate(
                #         date=date.fromisoformat(output_data["date"]),
                #         title=output_data["title"],
                #         summary=[AiDigestSummaryItem(**item) for item in output_data["summary"]],
                #         content=output_data["content"],
                #         total_items=output_data["total_items"]
                #     )
                #     AiDigestService.create(db, digest_data)
                #     logger.info("✅ 日报已保存到数据库")
                # finally:
                #     db.close()

                logger.info("⚠️ 数据库保存功能待实现")
            except Exception as e:
                logger.error(f"❌ 保存到数据库失败: {e}")

            return {
                "status": "success",
                "timestamp": start_time.isoformat(),
                "duration": duration,
                "output": result.stdout,
                "log_file": str(log_file),
            }
        else:
            error_msg = f"Claude Code CLI 执行失败: {result.stderr}"
            logger.error(f"❌ {error_msg}")

            # 重试任务
            raise self.retry(exc=Exception(error_msg))

    except subprocess.TimeoutExpired:
        error_msg = "任务执行超时（10 分钟）"
        logger.error(f"❌ {error_msg}")

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"执行时间: {start_time}\n")
            f.write(f"错误: {error_msg}\n")

        return {
            "status": "error",
            "timestamp": start_time.isoformat(),
            "error": error_msg,
            "log_file": str(log_file),
        }

    except Exception as e:
        error_msg = f"任务执行异常: {str(e)}"
        logger.error(f"❌ {error_msg}")

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"执行时间: {start_time}\n")
            f.write(f"异常: {error_msg}\n")

        # 重试任务
        raise self.retry(exc=e)


@celery_app.task(name="main.backend.tasks.ai_digest_task.test_task")
def test_task():
    """
    测试任务，用于验证 Celery 配置是否正确

    Returns:
        dict: 测试结果
    """
    logger.info("执行测试任务...")
    return {
        "status": "success",
        "message": "Celery 配置正常",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    # 用于测试
    print("测试 AI 日报任务...")
    result = run_ai_digest()
    print(f"结果: {result}")
