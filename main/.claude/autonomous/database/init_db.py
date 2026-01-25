#!/usr/bin/env python3
"""
数据库初始化脚本
Database Initialization Script

功能：
1. 创建 SQLite 数据库
2. 执行 schema.sql 创建表和视图
3. 提供数据库连接和操作工具函数
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


class DatabaseManager:
    """数据库管理器"""

    def __init__(self, db_path: Optional[str] = None):
        """
        初始化数据库管理器

        Args:
            db_path: 数据库文件路径，默认使用配置文件中的路径
        """
        if db_path is None:
            # 默认路径：.claude/autonomous/database/autonomous.db
            db_path = Path(__file__).parent / "autonomous.db"

        self.db_path = Path(db_path)
        self.schema_path = Path(__file__).parent / "schema.sql"

    def initialize(self) -> bool:
        """
        初始化数据库

        Returns:
            bool: 初始化是否成功
        """
        try:
            # 确保数据库目录存在
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # 读取 schema.sql
            if not self.schema_path.exists():
                print(f"❌ Schema file not found: {self.schema_path}")
                return False

            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            # 创建数据库并执行 schema
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 执行 schema（支持多条 SQL 语句）
            cursor.executescript(schema_sql)

            conn.commit()
            conn.close()

            print(f"✅ Database initialized successfully: {self.db_path}")
            return True

        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False

    def get_connection(self) -> sqlite3.Connection:
        """
        获取数据库连接

        Returns:
            sqlite3.Connection: 数据库连接对象
        """
        conn = sqlite3.connect(self.db_path)
        # 启用外键约束
        conn.execute("PRAGMA foreign_keys = ON")
        # 返回字典格式的行
        conn.row_factory = sqlite3.Row
        return conn

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        执行查询并返回结果

        Args:
            query: SQL 查询语句
            params: 查询参数

        Returns:
            List[Dict]: 查询结果列表
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # 将 Row 对象转换为字典
        results = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return results

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        执行更新操作（INSERT, UPDATE, DELETE）

        Args:
            query: SQL 更新语句
            params: 更新参数

        Returns:
            int: 受影响的行数
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        affected_rows = cursor.rowcount
        conn.close()

        return affected_rows


class TaskRepository:
    """任务数据访问层"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_task(
        self,
        task_id: str,
        task_type: str,
        description: str,
        priority: int,
        scheduled_at: Optional[datetime] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        创建新任务

        Args:
            task_id: 任务 ID
            task_type: 任务类型（time_based, event_based, metric_based, llm_driven）
            description: 任务描述
            priority: 优先级（1-10）
            scheduled_at: 计划执行时间
            metadata: 额外元数据

        Returns:
            bool: 创建是否成功
        """
        try:
            query = """
                INSERT INTO tasks (id, type, description, priority, status, scheduled_at, metadata)
                VALUES (?, ?, ?, ?, 'pending', ?, ?)
            """
            params = (
                task_id,
                task_type,
                description,
                priority,
                scheduled_at.isoformat() if scheduled_at else None,
                json.dumps(metadata) if metadata else None
            )

            self.db.execute_update(query, params)
            return True

        except Exception as e:
            print(f"❌ Failed to create task: {e}")
            return False

    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """
        获取所有活跃任务（pending 或 running）

        Returns:
            List[Dict]: 任务列表
        """
        query = "SELECT * FROM v_active_tasks"
        return self.db.execute_query(query)

    def update_task_status(
        self,
        task_id: str,
        status: str,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ) -> bool:
        """
        更新任务状态

        Args:
            task_id: 任务 ID
            status: 新状态（pending, running, completed, failed, cancelled）
            started_at: 开始时间
            completed_at: 完成时间

        Returns:
            bool: 更新是否成功
        """
        try:
            query = """
                UPDATE tasks
                SET status = ?,
                    started_at = COALESCE(?, started_at),
                    completed_at = COALESCE(?, completed_at)
                WHERE id = ?
            """
            params = (
                status,
                started_at.isoformat() if started_at else None,
                completed_at.isoformat() if completed_at else None,
                task_id
            )

            affected = self.db.execute_update(query, params)
            return affected > 0

        except Exception as e:
            print(f"❌ Failed to update task status: {e}")
            return False


class ExecutionHistoryRepository:
    """执行历史数据访问层"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def record_execution(
        self,
        execution_id: str,
        task_id: str,
        status: str,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        started_at: datetime = None,
        completed_at: datetime = None
    ) -> bool:
        """
        记录任务执行结果

        Args:
            execution_id: 执行 ID
            task_id: 任务 ID
            status: 执行状态（success, failure, timeout, cancelled）
            result: 执行结果数据
            error: 错误信息
            started_at: 开始时间
            completed_at: 完成时间

        Returns:
            bool: 记录是否成功
        """
        try:
            # 计算执行时长
            duration = None
            if started_at and completed_at:
                duration = (completed_at - started_at).total_seconds()

            query = """
                INSERT INTO execution_history
                (id, task_id, status, result, error, started_at, completed_at, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                execution_id,
                task_id,
                status,
                json.dumps(result) if result else None,
                error,
                started_at.isoformat() if started_at else None,
                completed_at.isoformat() if completed_at else None,
                duration
            )

            self.db.execute_update(query, params)
            return True

        except Exception as e:
            print(f"❌ Failed to record execution: {e}")
            return False


class MetricsRepository:
    """指标数据访问层"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def record_metric(
        self,
        metric_name: str,
        metric_value: float,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        记录系统指标

        Args:
            metric_name: 指标名称
            metric_value: 指标值
            metadata: 额外元数据

        Returns:
            bool: 记录是否成功
        """
        try:
            query = """
                INSERT INTO metrics (metric_name, metric_value, metadata)
                VALUES (?, ?, ?)
            """
            params = (
                metric_name,
                metric_value,
                json.dumps(metadata) if metadata else None
            )

            self.db.execute_update(query, params)
            return True

        except Exception as e:
            print(f"❌ Failed to record metric: {e}")
            return False

    def get_recent_metrics(self, metric_name: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        获取最近的指标数据

        Args:
            metric_name: 指标名称
            days: 天数

        Returns:
            List[Dict]: 指标数据列表
        """
        query = """
            SELECT * FROM metrics
            WHERE metric_name = ?
            AND timestamp >= datetime('now', ? || ' days')
            ORDER BY timestamp DESC
        """
        params = (metric_name, f'-{days}')
        return self.db.execute_query(query, params)


class AuditLogRepository:
    """审计日志数据访问层"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def log_event(
        self,
        event_type: str,
        description: str,
        user: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        记录审计事件

        Args:
            event_type: 事件类型
            description: 事件描述
            user: 触发用户
            metadata: 额外元数据

        Returns:
            bool: 记录是否成功
        """
        try:
            query = """
                INSERT INTO audit_log (event_type, description, user, metadata)
                VALUES (?, ?, ?, ?)
            """
            params = (
                event_type,
                description,
                user,
                json.dumps(metadata) if metadata else None
            )

            self.db.execute_update(query, params)
            return True

        except Exception as e:
            print(f"❌ Failed to log audit event: {e}")
            return False


def main():
    """主函数：初始化数据库"""
    print("🚀 Initializing Autonomous Evolution System Database...")

    # 创建数据库管理器
    db_manager = DatabaseManager()

    # 初始化数据库
    if db_manager.initialize():
        print("✅ Database initialization completed successfully!")

        # 测试数据库连接
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        # 检查表是否创建成功
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Created tables: {', '.join(tables)}")

        # 检查视图是否创建成功
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = [row[0] for row in cursor.fetchall()]
        print(f"📈 Created views: {', '.join(views)}")

        conn.close()

        return True
    else:
        print("❌ Database initialization failed!")
        return False


if __name__ == "__main__":
    main()
