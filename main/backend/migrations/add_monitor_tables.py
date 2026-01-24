"""
数据库迁移脚本 - 添加监控系统表

功能：
1. 创建 monitor_intelligence 表（智能水平历史记录）
2. 创建 monitor_diagnosis 表（诊断记录）
3. 创建 monitor_agent_performance 表（Agent 性能记录）

执行方式：
python main/backend/migrations/add_monitor_tables.py
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "main" / "backend"))

from sqlalchemy import create_engine, text
from core.config import settings


def create_monitor_tables():
    """创建监控系统相关表"""

    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL.replace("+aiosqlite", ""))

    with engine.connect() as conn:
        # 1. 创建 monitor_intelligence 表（智能水平历史记录）
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS monitor_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                intelligence_score REAL NOT NULL,           -- 智能水平总分 (0-10)
                strategy_weight REAL NOT NULL,              -- 策略权重 (0-1)
                knowledge_richness REAL NOT NULL,           -- 知识丰富度 (0-1)
                quality_trend REAL NOT NULL,                -- 质量趋势 (0-1)
                evolution_frequency REAL NOT NULL,          -- 进化频率 (0-1)
                milestone_event TEXT,                       -- 里程碑事件（可选）
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # 创建索引
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_intelligence_timestamp
            ON monitor_intelligence(timestamp)
        """))

        print("✅ 创建表: monitor_intelligence")

        # 2. 创建 monitor_diagnosis 表（诊断记录）
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS monitor_diagnosis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnosis_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                issue_id VARCHAR(50) NOT NULL UNIQUE,       -- 问题唯一标识
                severity VARCHAR(20) NOT NULL,              -- Critical/Important/Suggestion
                category VARCHAR(50) NOT NULL,              -- performance/security/quality/architecture
                title VARCHAR(200) NOT NULL,                -- 问题标题
                description TEXT NOT NULL,                  -- 问题描述
                location VARCHAR(500),                      -- 文件位置
                suggestion TEXT,                            -- 修复建议
                auto_fixable BOOLEAN DEFAULT 0,             -- 是否可自动修复
                fix_code TEXT,                              -- 修复代码
                status VARCHAR(20) DEFAULT 'open',          -- open/fixed/ignored
                fixed_at DATETIME,                          -- 修复时间
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # 创建索引
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_diagnosis_severity
            ON monitor_diagnosis(severity)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_diagnosis_status
            ON monitor_diagnosis(status)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_diagnosis_time
            ON monitor_diagnosis(diagnosis_time)
        """))

        print("✅ 创建表: monitor_diagnosis")

        # 3. 创建 monitor_agent_performance 表（Agent 性能记录）
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS monitor_agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name VARCHAR(100) NOT NULL,           -- Agent 名称
                agent_type VARCHAR(50) NOT NULL,            -- developer/reviewer/tester/orchestrator
                task_id VARCHAR(100),                       -- 任务 ID
                status VARCHAR(20) NOT NULL,                -- working/completed/failed
                progress INTEGER DEFAULT 0,                 -- 进度 (0-100)
                duration_seconds INTEGER,                   -- 任务耗时（秒）
                success BOOLEAN,                            -- 是否成功
                error_message TEXT,                         -- 错误信息
                started_at DATETIME NOT NULL,               -- 开始时间
                completed_at DATETIME,                      -- 完成时间
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # 创建索引
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_agent_name
            ON monitor_agent_performance(agent_name)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_agent_status
            ON monitor_agent_performance(status)
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_monitor_agent_started
            ON monitor_agent_performance(started_at)
        """))

        print("✅ 创建表: monitor_agent_performance")

        # 提交事务
        conn.commit()

    print("\n🎉 监控系统表创建成功！")
    print("\n表结构：")
    print("1. monitor_intelligence - 智能水平历史记录")
    print("2. monitor_diagnosis - 诊断记录")
    print("3. monitor_agent_performance - Agent 性能记录")


if __name__ == "__main__":
    try:
        create_monitor_tables()
    except Exception as e:
        print(f"\n❌ 创建表失败: {e}")
        sys.exit(1)
