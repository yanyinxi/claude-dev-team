"""
应用配置管理
"""

from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""

    # 获取项目根目录（向上查找直到找到 .git 或 CLAUDE.md）
    @staticmethod
    def get_project_root() -> Path:
        """
        智能查找项目根目录

        策略：
        1. 从当前文件向上查找，直到找到 .git 或 CLAUDE.md
        2. 如果找不到，使用当前文件向上 3 级（backend/core/config.py -> backend -> main -> root）

        Returns:
            Path: 项目根目录的绝对路径
        """
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            if (parent / '.git').exists() or (parent / 'CLAUDE.md').exists():
                return parent
        # 如果找不到，使用当前文件向上 3 级
        return Path(__file__).resolve().parent.parent.parent

    # 数据库配置 - 使用绝对路径（智能解析）
    @property
    def DATABASE_URL(self) -> str:
        """
        数据库连接 URL

        使用绝对路径，确保从任何目录运行都能正确找到数据库文件
        """
        db_path = self.get_project_root() / "main" / "backend" / "db" / "ket_exam.db"
        return f"sqlite+aiosqlite:///{db_path}"

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    # 管理员账号
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    # 应用配置
    APP_NAME: str = "KET备考系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
