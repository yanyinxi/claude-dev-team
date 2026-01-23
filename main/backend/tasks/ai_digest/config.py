"""
AI 日报任务配置文件

所有可配置的参数集中管理，支持环境变量覆盖
"""

import os
from pathlib import Path


class AiDigestConfig:
    """AI 日报任务配置类"""

    # =====================================================
    # 任务执行配置
    # =====================================================
    TASK_TIMEOUT: int = int(os.getenv("AI_DIGEST_TIMEOUT", "300"))  # 5 分钟超时
    TASK_EXPIRE: int = int(os.getenv("AI_DIGEST_EXPIRE", "1800"))  # 任务 30 分钟后过期
    RETRY_DELAY: int = int(os.getenv("AI_DIGEST_RETRY_DELAY", "180"))  # 3 分钟后重试
    MAX_RETRIES: int = int(os.getenv("AI_DIGEST_MAX_RETRIES", "2"))  # 最多重试 2 次

    # =====================================================
    # 缓存配置
    # =====================================================
    CACHE_ENABLED: bool = os.getenv("AI_DIGEST_CACHE_ENABLED", "true").lower() == "true"
    CACHE_DURATION: int = int(os.getenv("AI_DIGEST_CACHE_DURATION", "3600"))  # 缓存 1 小时

    # =====================================================
    # Celery 配置
    # =====================================================
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "sqla+sqlite:///celery.db")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "db+sqlite:///celery_results.db")
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Shanghai")

    # =====================================================
    # 定时任务配置
    # =====================================================
    # 支持 cron 表达式配置
    SCHEDULE_HOUR: str = os.getenv("AI_DIGEST_SCHEDULE_HOUR", "*")  # 每小时
    SCHEDULE_MINUTE: str = os.getenv("AI_DIGEST_SCHEDULE_MINUTE", "0")  # 整点执行

    # =====================================================
    # 路径配置
    # =====================================================
    @staticmethod
    def get_project_root() -> Path:
        """获取项目根目录"""
        return Path(__file__).parent.parent.parent.parent.parent

    @staticmethod
    def get_docs_dir() -> Path:
        """获取文档目录"""
        return AiDigestConfig.get_project_root() / "main" / "docs" / "ai_digest"

    @staticmethod
    def get_log_dir() -> Path:
        """获取日志目录"""
        return AiDigestConfig.get_project_root() / "logs"

    # =====================================================
    # Claude CLI 配置
    # =====================================================
    CLAUDE_CLI_COMMAND: str = os.getenv("CLAUDE_CLI_COMMAND", "claude")
    CLAUDE_PROMPT: str = os.getenv(
        "AI_DIGEST_PROMPT",
        "执行 /ai-digest 技能，生成今日 AI 日报"
    )

    # =====================================================
    # 数据库配置
    # =====================================================
    DB_SAVE_ENABLED: bool = os.getenv("AI_DIGEST_DB_SAVE", "false").lower() == "true"

    # =====================================================
    # 健康检查配置
    # =====================================================
    HEALTH_CHECK_ENABLED: bool = os.getenv("AI_DIGEST_HEALTH_CHECK", "true").lower() == "true"
    HEALTH_CHECK_TIMEOUT: int = int(os.getenv("AI_DIGEST_HEALTH_CHECK_TIMEOUT", "5"))

    @classmethod
    def validate(cls) -> bool:
        """
        验证配置是否有效

        Returns:
            bool: 配置是否有效
        """
        try:
            # 验证超时时间
            assert cls.TASK_TIMEOUT > 0, "TASK_TIMEOUT 必须大于 0"
            assert cls.TASK_EXPIRE > cls.TASK_TIMEOUT, "TASK_EXPIRE 必须大于 TASK_TIMEOUT"

            # 验证重试配置
            assert cls.MAX_RETRIES >= 0, "MAX_RETRIES 必须大于等于 0"
            assert cls.RETRY_DELAY > 0, "RETRY_DELAY 必须大于 0"

            # 验证缓存配置
            assert cls.CACHE_DURATION > 0, "CACHE_DURATION 必须大于 0"

            # 验证路径
            assert cls.get_project_root().exists(), "项目根目录不存在"

            return True
        except AssertionError as e:
            print(f"❌ 配置验证失败: {e}")
            return False

    @classmethod
    def print_config(cls):
        """打印当前配置（用于调试）"""
        print("=" * 80)
        print("AI 日报任务配置")
        print("=" * 80)
        print(f"任务超时: {cls.TASK_TIMEOUT} 秒")
        print(f"任务过期: {cls.TASK_EXPIRE} 秒")
        print(f"重试延迟: {cls.RETRY_DELAY} 秒")
        print(f"最大重试: {cls.MAX_RETRIES} 次")
        print(f"缓存启用: {cls.CACHE_ENABLED}")
        print(f"缓存时长: {cls.CACHE_DURATION} 秒")
        print(f"时区: {cls.TIMEZONE}")
        print(f"定时: 每小时 {cls.SCHEDULE_MINUTE} 分")
        print(f"项目根目录: {cls.get_project_root()}")
        print(f"文档目录: {cls.get_docs_dir()}")
        print(f"日志目录: {cls.get_log_dir()}")
        print(f"Claude CLI: {cls.CLAUDE_CLI_COMMAND}")
        print(f"健康检查: {cls.HEALTH_CHECK_ENABLED}")
        print(f"数据库保存: {cls.DB_SAVE_ENABLED}")
        print("=" * 80)


# 创建全局配置实例
config = AiDigestConfig()

# 验证配置
if not config.validate():
    raise ValueError("AI 日报任务配置无效，请检查环境变量")
