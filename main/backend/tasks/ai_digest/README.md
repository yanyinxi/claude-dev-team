# AI 日报定时任务

## 概述

自动化 AI 日报生成系统，每小时执行一次，支持智能缓存和去重机制。

## 核心特性

- ✅ **每小时执行**：从每天 9:00 改为每小时整点执行
- ✅ **智能缓存**：1 小时内避免重复生成相同内容
- ✅ **健康检查**：任务开始前验证 Claude CLI 可用性
- ✅ **配置化管理**：所有参数支持环境变量覆盖
- ✅ **代码优化**：简化逻辑，提取工具函数，提高可维护性
- ✅ **超时优化**：从 10 分钟降低到 5 分钟（hourly 任务更快）

## 文件结构

```
main/backend/tasks/ai_digest/
├── task.py          # 主任务文件（优化后）
├── config.py        # 配置管理（新增）
├── schemas.py       # 数据模型
├── service.py       # 业务服务
└── README.md        # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install celery redis sqlalchemy
```

### 2. 启动 Redis（可选）

```bash
# 使用 Redis 作为 broker（推荐生产环境）
redis-server

# 或使用 SQLite（默认，无需额外配置）
```

### 3. 启动 Celery Worker

```bash
celery -A main.backend.tasks.ai_digest_task worker --loglevel=info
```

### 4. 启动 Celery Beat（定时任务调度器）

```bash
celery -A main.backend.tasks.ai_digest_task beat --loglevel=info
```

### 5. 测试任务

```bash
# 手动触发任务
python -c "from main.backend.tasks.ai_digest.task import run_ai_digest; run_ai_digest()"

# 或使用 Celery 命令
celery -A main.backend.tasks.ai_digest_task call main.backend.tasks.ai_digest_task.run_ai_digest
```

## 配置说明

所有配置支持环境变量覆盖，默认值见 `config.py`。

### 任务执行配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `AI_DIGEST_TIMEOUT` | `300` | 任务超时时间（秒） |
| `AI_DIGEST_EXPIRE` | `1800` | 任务过期时间（秒） |
| `AI_DIGEST_RETRY_DELAY` | `180` | 重试延迟（秒） |
| `AI_DIGEST_MAX_RETRIES` | `2` | 最大重试次数 |

### 缓存配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `AI_DIGEST_CACHE_ENABLED` | `true` | 是否启用缓存 |
| `AI_DIGEST_CACHE_DURATION` | `3600` | 缓存有效期（秒） |

### 定时任务配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `AI_DIGEST_SCHEDULE_HOUR` | `*` | 执行小时（* 表示每小时） |
| `AI_DIGEST_SCHEDULE_MINUTE` | `0` | 执行分钟（0 表示整点） |

### Celery 配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `CELERY_BROKER_URL` | `sqla+sqlite:///celery.db` | Celery broker URL |
| `CELERY_RESULT_BACKEND` | `db+sqlite:///celery_results.db` | 结果存储后端 |
| `TIMEZONE` | `Asia/Shanghai` | 时区 |

### Claude CLI 配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `CLAUDE_CLI_COMMAND` | `claude` | Claude CLI 命令 |
| `AI_DIGEST_PROMPT` | `执行 /ai-digest 技能，生成今日 AI 日报` | 执行提示 |

### 健康检查配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `AI_DIGEST_HEALTH_CHECK` | `true` | 是否启用健康检查 |
| `AI_DIGEST_HEALTH_CHECK_TIMEOUT` | `5` | 健康检查超时（秒） |

### 数据库配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `AI_DIGEST_DB_SAVE` | `false` | 是否保存到数据库 |

## 配置示例

### 开发环境（.env）

```bash
# 使用 SQLite，快速启动
CELERY_BROKER_URL=sqla+sqlite:///celery.db
CELERY_RESULT_BACKEND=db+sqlite:///celery_results.db

# 每小时执行
AI_DIGEST_SCHEDULE_MINUTE=0

# 启用缓存
AI_DIGEST_CACHE_ENABLED=true
AI_DIGEST_CACHE_DURATION=3600

# 健康检查
AI_DIGEST_HEALTH_CHECK=true
```

### 生产环境（.env.production）

```bash
# 使用 Redis，高性能
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# 每 2 小时执行（节省资源）
AI_DIGEST_SCHEDULE_MINUTE=0

# 启用缓存
AI_DIGEST_CACHE_ENABLED=true
AI_DIGEST_CACHE_DURATION=7200

# 启用数据库保存
AI_DIGEST_DB_SAVE=true

# 健康检查
AI_DIGEST_HEALTH_CHECK=true
```

## 优化内容

### 1. 定时任务频率调整

**变更前**：
```python
"schedule": crontab(hour=9, minute=0),  # 每天 9:00
```

**变更后**：
```python
"schedule": crontab(minute=0),  # 每小时整点
```

### 2. 超时时间优化

**变更前**：
```python
timeout=600  # 10 分钟超时
```

**变更后**：
```python
timeout=300  # 5 分钟超时（hourly 任务应该更快）
```

### 3. 任务过期时间调整

**变更前**：
```python
"expires": 3600,  # 任务 1 小时后过期
```

**变更后**：
```python
"expires": 1800,  # 任务 30 分钟后过期
```

### 4. 代码简化

#### 提取工具函数

- `get_project_root()` - 获取项目根目录
- `ensure_directories()` - 确保目录存在
- `get_cache_key()` - 生成缓存 key
- `check_cache()` - 检查缓存
- `save_cache()` - 保存缓存
- `check_claude_cli()` - 健康检查
- `run_claude_command()` - 执行 Claude CLI
- `write_log()` - 统一日志写入

#### 配置集中管理

所有配置提取到 `config.py`，支持环境变量覆盖。

#### 移除冗余代码

- 删除注释掉的数据库保存代码（第 141-155 行）
- 简化日志记录逻辑
- 合并相似的异常处理

### 5. 智能优化

#### 缓存机制

```python
# 基于当前小时生成缓存 key
cache_key = get_cache_key()  # ai_digest_2026_01_23_14

# 检查缓存
cached_result = check_cache(cache_key)
if cached_result:
    return {"status": "cached", ...}

# 保存缓存
save_cache(cache_key, task_result)
```

#### 健康检查

```python
# 任务开始前检查 Claude CLI
if not check_claude_cli():
    return {"status": "error", "error": "Claude CLI 不可用"}
```

#### 去重机制

通过缓存实现，1 小时内不会重复生成相同内容。

## 日志和监控

### 日志文件

```
logs/
├── ai_digest_20260123_09.log  # 每小时一个日志文件
├── ai_digest_20260123_10.log
├── cache_abc123.json          # 缓存文件
└── cache_def456.json
```

### 日志格式

```
================================================================================
执行时间: 2026-01-23 09:00:00
耗时: 45.23 秒
返回码: 0

--- STDOUT ---
{"date": "2026-01-23", "title": "AI 日报", ...}

--- STDERR ---
(如果有错误)
```

### 监控指标

- 任务执行时间
- 成功/失败率
- 缓存命中率
- 重试次数

## 故障排查

### 问题 1：任务不执行

**原因**：Celery Beat 未启动

**解决**：
```bash
celery -A main.backend.tasks.ai_digest_task beat --loglevel=info
```

### 问题 2：Claude CLI 不可用

**原因**：Claude CLI 未安装或不在 PATH 中

**解决**：
```bash
# 检查 Claude CLI
claude --version

# 如果未安装，参考官方文档安装
```

### 问题 3：任务超时

**原因**：网络慢或任务复杂

**解决**：
```bash
# 增加超时时间
export AI_DIGEST_TIMEOUT=600
```

### 问题 4：缓存不生效

**原因**：缓存被禁用或过期

**解决**：
```bash
# 启用缓存
export AI_DIGEST_CACHE_ENABLED=true

# 增加缓存时长
export AI_DIGEST_CACHE_DURATION=7200
```

## 测试

### 单元测试

```bash
pytest main/backend/tasks/ai_digest/test_task.py
```

### 集成测试

```bash
# 测试任务执行
celery -A main.backend.tasks.ai_digest_task call main.backend.tasks.ai_digest_task.test_task

# 测试 AI 日报任务
celery -A main.backend.tasks.ai_digest_task call main.backend.tasks.ai_digest_task.run_ai_digest
```

### 配置验证

```python
from main.backend.tasks.ai_digest.config import config

# 验证配置
config.validate()

# 打印配置
config.print_config()
```

## 性能优化建议

### 1. 使用 Redis

生产环境建议使用 Redis 作为 broker，性能更好。

```bash
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

### 2. 调整并发数

```bash
# 启动多个 worker
celery -A main.backend.tasks.ai_digest_task worker --concurrency=4
```

### 3. 启用结果压缩

```python
celery_app.conf.update(
    result_compression='gzip',
)
```

### 4. 定期清理日志

```bash
# 删除 7 天前的日志
find logs/ -name "ai_digest_*.log" -mtime +7 -delete
```

## 未来改进

- [ ] 支持多种 AI 模型
- [ ] 添加 Prometheus 监控指标
- [ ] 支持分布式任务调度
- [ ] 添加 Web 管理界面
- [ ] 支持任务优先级
- [ ] 添加任务依赖管理

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
