"""
添加抢答模式数据表
"""
import sqlite3
import os

def migrate():
    """执行迁移"""
    # 连接数据库
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ket_exam.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建 speed_quiz_battles 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS speed_quiz_battles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            difficulty INTEGER NOT NULL,
            module VARCHAR(20) NOT NULL,
            total_questions INTEGER NOT NULL,
            user_correct INTEGER DEFAULT 0,
            ai_correct INTEGER DEFAULT 0,
            user_wins INTEGER DEFAULT 0,
            ai_wins INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 创建 speed_quiz_details 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS speed_quiz_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            battle_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            user_answer VARCHAR(1),
            user_time INTEGER,
            ai_answer VARCHAR(1) NOT NULL,
            ai_time INTEGER NOT NULL,
            correct_answer VARCHAR(1) NOT NULL,
            winner VARCHAR(10) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (battle_id) REFERENCES speed_quiz_battles(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_speed_quiz_battles_user_id ON speed_quiz_battles(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_speed_quiz_battles_created_at ON speed_quiz_battles(created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_speed_quiz_details_battle_id ON speed_quiz_details(battle_id)')

    conn.commit()
    conn.close()

    print("✅ 抢答模式数据表创建成功")
    print("  - speed_quiz_battles")
    print("  - speed_quiz_details")
    print("  - 相关索引")

if __name__ == "__main__":
    migrate()
