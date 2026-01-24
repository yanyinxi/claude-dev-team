"""
数据库迁移：添加学习闹钟相关表

创建时间：2026-01-24
功能：添加 alarm_rules 和 alarm_sessions 两个表
"""

import sqlite3
from pathlib import Path


def get_db_path():
    """获取数据库文件路径"""
    # 从当前文件位置向上查找项目根目录
    current_file = Path(__file__).resolve()
    # current_file: .../main/backend/migrations/add_alarm_tables.py
    # parent: .../main/backend/migrations/
    # parent.parent: .../main/backend/
    # parent.parent.parent: .../main/
    # parent.parent.parent.parent: .../ (项目根目录)
    project_root = current_file.parent.parent.parent.parent
    db_path = project_root / "main" / "backend" / "db" / "ket_exam.db"
    return str(db_path)


def migrate():
    """执行数据库迁移"""
    db_path = get_db_path()
    print(f"连接数据库: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 创建 alarm_rules 表（闹钟规则表）
        print("创建 alarm_rules 表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alarm_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_type TEXT NOT NULL CHECK(rule_type IN ('global', 'personal')),
                student_nickname TEXT,
                study_duration INTEGER NOT NULL,
                rest_duration INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建 alarm_sessions 表（学习会话表）
        print("创建 alarm_sessions 表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alarm_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_type TEXT NOT NULL CHECK(session_type IN ('studying', 'resting')),
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                rule_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (rule_id) REFERENCES alarm_rules(id)
            )
        """)

        # 创建索引以提高查询性能
        print("创建索引...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_alarm_rules_type_nickname
            ON alarm_rules(rule_type, student_nickname)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_alarm_sessions_user_id
            ON alarm_sessions(user_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_alarm_sessions_end_time
            ON alarm_sessions(end_time)
        """)

        # 插入默认全局规则（学习 30 分钟，休息 10 分钟）
        print("插入默认全局规则...")
        cursor.execute("""
            INSERT INTO alarm_rules (rule_type, study_duration, rest_duration, is_active)
            SELECT 'global', 30, 10, 1
            WHERE NOT EXISTS (
                SELECT 1 FROM alarm_rules WHERE rule_type = 'global'
            )
        """)

        conn.commit()
        print("✅ 数据库迁移成功！")

    except Exception as e:
        conn.rollback()
        print(f"❌ 数据库迁移失败: {e}")
        raise

    finally:
        conn.close()


def rollback():
    """回滚数据库迁移"""
    db_path = get_db_path()
    print(f"连接数据库: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        print("删除 alarm_sessions 表...")
        cursor.execute("DROP TABLE IF EXISTS alarm_sessions")

        print("删除 alarm_rules 表...")
        cursor.execute("DROP TABLE IF EXISTS alarm_rules")

        conn.commit()
        print("✅ 数据库回滚成功！")

    except Exception as e:
        conn.rollback()
        print(f"❌ 数据库回滚失败: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback()
    else:
        migrate()
