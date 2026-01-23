# 数据库文件目录

此目录统一存放项目的所有 SQLite 数据库文件。

## 目录结构

```
main/backend/db/
├── ket_exam.db          # 主数据库（生产/开发）
├── test.db              # 测试数据库
├── .gitignore           # Git 忽略规则
└── README.md            # 本文档
```

## 数据库文件说明

### ket_exam.db
- **用途**: 主数据库，存储所有业务数据
- **表结构**:
  - `users` - 用户表
  - `questions` - 题目表
  - `achievements` - 成就表
  - `user_achievements` - 用户成就关联表
  - `user_progress` - 用户进度表
  - `wrong_questions` - 错题记录表
  - `speed_quiz_battles` - 抢答对战记录表
  - `speed_quiz_details` - 抢答详情表
  - `ai_digests` - AI 日报表（可选）

### test.db
- **用途**: 测试数据库，用于单元测试和集成测试
- **特点**: 可以随时删除和重建

## 配置说明

### 数据库连接配置

在 `main/backend/core/config.py` 中配置：

```python
# 开发环境（默认）
DATABASE_URL = "sqlite+aiosqlite:///main/backend/db/ket_exam.db"

# 测试环境
DATABASE_URL = "sqlite+aiosqlite:///main/backend/db/test.db"

# 生产环境（推荐使用 PostgreSQL）
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
```

### 环境变量配置

可以通过环境变量覆盖默认配置：

```bash
# .env 文件
DATABASE_URL=sqlite+aiosqlite:///main/backend/db/ket_exam.db
```

## 数据库初始化

### 自动初始化

首次启动应用时，会自动创建数据库和示例数据：

```bash
cd main/backend
python main.py
```

### 手动初始化

使用脚本手动初始化：

```bash
# 创建管理员账号
python main/backend/scripts/create_admin.py

# 添加示例题目
python main/backend/scripts/seed_questions.py
```

## 数据库迁移

### 执行迁移

```bash
# 添加抢答模式表
python main/backend/migrations/add_speed_quiz_tables.py

# 添加 AI 日报表
python main/backend/migrations/add_ai_digest_table.py
```

## 备份与恢复

### 备份数据库

```bash
# 备份主数据库
cp main/backend/db/ket_exam.db backup/ket_exam_$(date +%Y%m%d).db

# 或使用 SQLite 命令
sqlite3 main/backend/db/ket_exam.db ".backup backup/ket_exam_$(date +%Y%m%d).db"
```

### 恢复数据库

```bash
# 从备份恢复
cp backup/ket_exam_20260123.db main/backend/db/ket_exam.db
```

## 数据库维护

### 查看表结构

```bash
sqlite3 main/backend/db/ket_exam.db ".schema"
```

### 查看数据

```bash
# 查看所有表
sqlite3 main/backend/db/ket_exam.db "SELECT name FROM sqlite_master WHERE type='table';"

# 查看用户数据
sqlite3 main/backend/db/ket_exam.db "SELECT * FROM users;"
```

### 清理数据库

```bash
# 删除所有数据（保留表结构）
sqlite3 main/backend/db/ket_exam.db "DELETE FROM users; DELETE FROM questions;"

# 重建数据库（删除并重新创建）
rm main/backend/db/ket_exam.db
python main.py
```

## 注意事项

1. **版本控制**: 数据库文件已添加到 `.gitignore`，不会提交到 Git
2. **路径配置**: 使用相对路径，确保从项目根目录运行
3. **生产环境**: 建议使用 PostgreSQL 替代 SQLite
4. **备份策略**: 定期备份生产数据库
5. **权限管理**: 确保数据库文件有正确的读写权限

## 故障排查

### 数据库文件不存在

```bash
# 检查文件是否存在
ls -lh main/backend/db/ket_exam.db

# 如果不存在，重新初始化
python main/backend/main.py
```

### 数据库连接失败

```bash
# 检查配置
python3 -c "from main.backend.core.config import settings; print(settings.DATABASE_URL)"

# 检查文件权限
chmod 644 main/backend/db/ket_exam.db
```

### 数据库损坏

```bash
# 检查数据库完整性
sqlite3 main/backend/db/ket_exam.db "PRAGMA integrity_check;"

# 如果损坏，从备份恢复
cp backup/ket_exam_latest.db main/backend/db/ket_exam.db
```

## 相关文档

- [后端 README](../README.md)
- [项目技术标准](../../../.claude/project_standards.md)
- [数据库迁移指南](../migrations/README.md)
