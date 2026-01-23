"""
AI 日报定时任务（每小时执行）

功能：
1. 每小时自动执行 AI 日报生成
2. 调用 Claude Code CLI 执行 ai-digest Skill
3. 智能去重和缓存机制
4. 记录执行结果和错误日志

依赖：
- Celery
- Redis/SQLite
- Claude Code CLI

使用方法：
1. 启动 Redis: redis-server（可选，默认使用 SQLite）
2. 启动 Celery Worker: celery -A main.backend.tasks.ai_digest_task worker --loglevel=info
3. 启动 Celery Beat: celery -A main.backend.tasks.ai_digest_task beat --loglevel=info
"""

import os
import subprocess
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from .schemas import AiDigestCreate, AiDigestSummaryItem
from .service import AiDigestService
from .config import config

# 日志配置
logger = get_task_logger(__name__)

# =====================================================
# Celery 应用初始化
# =====================================================
celery_app = Celery(
    "ai_digest_tasks",
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND,
)

# Celery 配置
celery_app.conf.update(
    timezone=config.TIMEZONE,
    enable_utc=True,
    result_expires=7 * 24 * 60 * 60,  # 结果保留 7 天
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule={
        "ai-hourly-digest": {
            "task": "main.backend.tasks.ai_digest_task.run_ai_digest",
            "schedule": crontab(minute=int(config.SCHEDULE_MINUTE)),  # 每小时执行一次
            "options": {
                "expires": config.TASK_EXPIRE,
            },
        },
    },
)

# =====================================================
# 工具函数
# =====================================================


def get_project_root() -> Path:
    """获取项目根目录"""
    return config.get_project_root()


def ensure_directories() -> tuple[Path, Path]:
    """
    确保必要的目录存在

    Returns:
        tuple: (文档目录, 日志目录)
    """
    docs_dir = config.get_docs_dir()
    log_dir = config.get_log_dir()

    docs_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    return docs_dir, log_dir


def get_cache_key() -> str:
    """
    生成缓存 key（基于当前小时）

    Returns:
        str: 缓存 key
    """
    now = datetime.now()
    cache_str = f"ai_digest_{now.year}_{now.month}_{now.day}_{now.hour}"
    return hashlib.md5(cache_str.encode()).hexdigest()


def check_cache(cache_key: str) -> Optional[Dict]:
    """
    检查缓存是否存在

    Args:
        cache_key: 缓存 key

    Returns:
        Optional[Dict]: 缓存的结果，如果不存在返回 None
    """
    if not config.CACHE_ENABLED:
        return None

    cache_file = config.get_log_dir() / f"cache_{cache_key}.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                # 检查缓存是否过期
                cache_time = datetime.fromisoformat(cache_data["timestamp"])
                if datetime.now() - cache_time < timedelta(seconds=config.CACHE_DURATION):
                    logger.info(f"✅ 使用缓存结果（{cache_time}）")
                    return cache_data
        except Exception as e:
            logger.warning(f"⚠️ 读取缓存失败: {e}")
    return None


def save_cache(cache_key: str, result: Dict) -> None:
    """
    保存结果到缓存

    Args:
        cache_key: 缓存 key
        result: 执行结果
    """
    if not config.CACHE_ENABLED:
        return

    cache_file = config.get_log_dir() / f"cache_{cache_key}.json"
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ 结果已缓存")
    except Exception as e:
        logger.warning(f"⚠️ 保存缓存失败: {e}")


def check_claude_cli() -> bool:
    """
    健康检查：验证 Claude CLI 是否可用

    Returns:
        bool: CLI 是否可用
    """
    if not config.HEALTH_CHECK_ENABLED:
        return True

    try:
        result = subprocess.run(
            [config.CLAUDE_CLI_COMMAND, "--version"],
            capture_output=True,
            text=True,
            timeout=config.HEALTH_CHECK_TIMEOUT,
        )
        if result.returncode == 0:
            logger.info(f"✅ Claude CLI 可用: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"❌ Claude CLI 不可用: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Claude CLI 健康检查失败: {e}")
        return False


def run_claude_command(project_root: Path) -> subprocess.CompletedProcess:
    """
    执行 Claude CLI 命令

    Args:
        project_root: 项目根目录

    Returns:
        subprocess.CompletedProcess: 执行结果
    """
    return subprocess.run(
        [
            config.CLAUDE_CLI_COMMAND,
            "-p",
            config.CLAUDE_PROMPT,
            "--output-format",
            "json",
        ],
        cwd=str(project_root),
        capture_output=True,
        text=True,
        timeout=config.TASK_TIMEOUT,
        env={**os.environ, "CLAUDE_NO_INTERACTIVE": "1"},
    )


def write_log(log_file: Path, start_time: datetime, result: subprocess.CompletedProcess = None, error: str = None) -> None:
    """
    统一的日志写入函数

    Args:
        log_file: 日志文件路径
        start_time: 开始时间
        result: subprocess 执行结果
        error: 错误信息
    """
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 80}\n")
        f.write(f"执行时间: {start_time}\n")

        if result:
            duration = (datetime.now() - start_time).total_seconds()
            f.write(f"耗时: {duration:.2f} 秒\n")
            f.write(f"返回码: {result.returncode}\n")
            f.write(f"\n--- STDOUT ---\n{result.stdout}\n")
            if result.stderr:
                f.write(f"\n--- STDERR ---\n{result.stderr}\n")

        if error:
            f.write(f"错误: {error}\n")


# =====================================================
# Celery 任务
# =====================================================


@celery_app.task(
    bind=True,
    name="main.backend.tasks.ai_digest_task.run_ai_digest",
    max_retries=config.MAX_RETRIES,
    default_retry_delay=config.RETRY_DELAY,
)
def run_ai_digest(self):
    """
    执行 AI 日报生成任务（每小时）

    核心流程：
    1. 健康检查 Claude CLI
    2. 检查缓存（避免重复生成）
    3. 执行 Claude CLI 命令
    4. 保存结果和日志
    5. 缓存结果

    Returns:
        dict: 执行结果
            - status: success/error/cached
            - timestamp: 执行时间
            - duration: 耗时（秒）
            - output: 输出内容
            - error: 错误信息（如果失败）
    """
    start_time = datetime.now()
    logger.info(f"[{start_time}] 开始执行 AI 日报任务（每小时）...")

    # 确保目录存在
    docs_dir, log_dir = ensure_directories()
    log_file = log_dir / f"ai_digest_{start_time.strftime('%Y%m%d_%H')}.log"

    # 健康检查
    if not check_claude_cli():
        error_msg = "Claude CLI 不可用，任务终止"
        logger.error(f"❌ {error_msg}")
        write_log(log_file, start_time, error=error_msg)
        return {
            "status": "error",
            "timestamp": start_time.isoformat(),
            "error": error_msg,
            "log_file": str(log_file),
        }

    # 检查缓存
    cache_key = get_cache_key()
    cached_result = check_cache(cache_key)
    if cached_result:
        return {
            **cached_result,
            "status": "cached",
        }

    try:
        # 执行 Claude CLI 命令
        logger.info("调用 Claude Code CLI...")
        result = run_claude_command(get_project_root())

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 记录日志
        write_log(log_file, start_time, result)

        if result.returncode == 0:
            logger.info(f"✅ AI 日报任务完成，耗时 {duration:.2f} 秒")

            # 构建返回结果
            task_result = {
                "status": "success",
                "timestamp": start_time.isoformat(),
                "duration": duration,
                "output": result.stdout,
                "log_file": str(log_file),
            }

            # 保存到缓存
            save_cache(cache_key, task_result)

            # 解析输出并保存到数据库（可选）
            try:
                output_data = json.loads(result.stdout)
                logger.info("⚠️ 数据库保存功能待实现")
                # TODO: 实现数据库保存逻辑
                # from main.backend.core.database import SessionLocal
                # db = SessionLocal()
                # try:
                #     digest_data = AiDigestCreate(...)
                #     AiDigestService.create(db, digest_data)
                # finally:
                #     db.close()
            except json.JSONDecodeError:
                logger.warning("⚠️ 输出不是有效的 JSON 格式")
            except Exception as e:
                logger.error(f"❌ 保存到数据库失败: {e}")

            return task_result
        else:
            error_msg = f"Claude Code CLI 执行失败: {result.stderr}"
            logger.error(f"❌ {error_msg}")
            raise self.retry(exc=Exception(error_msg))

    except subprocess.TimeoutExpired:
        error_msg = f"任务执行超时（{config.TASK_TIMEOUT} 秒）"
        logger.error(f"❌ {error_msg}")
        write_log(log_file, start_time, error=error_msg)

        return {
            "status": "error",
            "timestamp": start_time.isoformat(),
            "error": error_msg,
            "log_file": str(log_file),
        }

    except Exception as e:
        error_msg = f"任务执行异常: {str(e)}"
        logger.error(f"❌ {error_msg}")
        write_log(log_file, start_time, error=error_msg)
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
