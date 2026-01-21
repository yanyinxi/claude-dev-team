# 🤖 AI 日报系统使用指南

> 每天早上 9:00 自动整理最新、最有价值的 AI 资讯

---

## 📋 系统概述

AI 日报系统基于 **Celery Beat + Claude Code Skill** 实现，自动搜索并整理以下内容：

- 🤖 **AI Agent 技术** - 自主 Agent、多 Agent 系统、框架更新
- 🚀 **大模型进展** - GPT、Claude、Gemini 等新模型发布
- 📚 **AI 最新论文** - 顶会论文、arXiv 热门研究
- 🛠️ **AI 开源技术** - 新工具、框架、开源项目
- 💡 **突破性技术** - 算法创新、性能突破、新应用
- 💼 **行业动态** - 公司新闻、融资、政策法规

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install celery redis

# 安装 Redis（如果未安装）
# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server

# 启动 Redis
redis-server
```

### 2. 启动系统

```bash
# 一键启动
./scripts/start_ai_digest.sh
```

启动后会自动：
- ✅ 检查 Redis 服务
- ✅ 检查 Python 和 Celery
- ✅ 检查 Claude Code CLI
- ✅ 启动 Celery Worker
- ✅ 启动 Celery Beat（定时调度器）

### 3. 查看日报

```bash
# 查看今日日报
cat main/docs/ai_digest/$(date +%Y-%m-%d).md

# 查看最近 7 天日报
ls -lt main/docs/ai_digest/ | head -8
```

---

## 📅 定时任务配置

**执行时间**：每天早上 **9:00**（北京时间）

**任务流程**：
```
09:00:00 - Celery Beat 触发任务
    ↓
09:00:01 - 调用 Claude Code CLI
    ↓
09:00:02 - 执行 ai-digest Skill
    ↓
09:00:03 - WebSearch 搜索最新资讯
    ↓
09:05:00 - 内容筛选和分类
    ↓
09:08:00 - 生成 Markdown 文档
    ↓
09:10:00 - 任务完成，保存日报
```

**修改执行时间**：

编辑 `main/backend/tasks/ai_digest_task.py`：

```python
beat_schedule={
    "ai-daily-digest": {
        "task": "main.backend.tasks.ai_digest_task.run_ai_digest",
        "schedule": crontab(hour=9, minute=0),  # 修改这里
    },
}
```

---

## 🛠️ 手动执行

### 方式 1: 直接调用 Skill

```bash
claude -p "执行 /ai-digest"
```

### 方式 2: 通过 Celery 任务

```python
from main.backend.tasks.ai_digest_task import run_ai_digest

# 立即执行
result = run_ai_digest.delay()

# 查看结果
print(result.get())
```

### 方式 3: 测试任务

```bash
# 进入 Python 环境
python3

# 执行测试
from main.backend.tasks.ai_digest_task import test_task
result = test_task.delay()
print(result.get())
```

---

## 📊 监控和日志

### 查看日志

```bash
# Celery Worker 日志
tail -f logs/celery_worker.log

# Celery Beat 日志
tail -f logs/celery_beat.log

# AI 日报任务日志
tail -f logs/ai_digest_$(date +%Y%m%d).log
```

### 查看运行状态

```bash
# 查看 Celery 进程
ps aux | grep celery

# 查看任务队列
celery -A main.backend.tasks.ai_digest_task inspect active

# 查看定时任务
celery -A main.backend.tasks.ai_digest_task inspect scheduled
```

---

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置：

```bash
# Redis 配置
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# 时区配置
TIMEZONE=Asia/Shanghai

# Claude Code CLI 配置
CLAUDE_NO_INTERACTIVE=1
```

### Skill 配置

编辑 `.claude/skills/ai_daily_digest/SKILL.md` 可以：

- 修改搜索关键词
- 调整内容分类
- 自定义文档格式
- 修改筛选标准

---

## 🐛 故障排查

### 问题 1: Redis 连接失败

```bash
# 检查 Redis 是否运行
redis-cli ping

# 如果返回 PONG，说明正常
# 如果失败，启动 Redis
redis-server
```

### 问题 2: Celery 任务未执行

```bash
# 检查 Celery Beat 是否运行
ps aux | grep "celery.*beat"

# 重启 Celery Beat
./scripts/stop_ai_digest.sh
./scripts/start_ai_digest.sh
```

### 问题 3: Claude Code CLI 调用失败

```bash
# 检查 Claude Code 是否安装
claude --version

# 测试 Skill 是否可用
claude -p "执行 /ai-digest"
```

### 问题 4: 日报未生成

```bash
# 查看任务日志
tail -f logs/ai_digest_$(date +%Y%m%d).log

# 手动执行测试
claude -p "执行 /ai-digest"
```

---

## 🔄 停止系统

```bash
# 停止所有服务
./scripts/stop_ai_digest.sh
```

---

## 📁 文件结构

```
.
├── .claude/skills/ai_daily_digest/
│   └── SKILL.md                    # Skill 定义
├── main/backend/tasks/
│   ├── __init__.py
│   └── ai_digest_task.py           # Celery 任务
├── main/docs/ai_digest/
│   ├── README.md
│   └── YYYY-MM-DD.md               # 日报文件
├── scripts/
│   ├── start_ai_digest.sh          # 启动脚本
│   └── stop_ai_digest.sh           # 停止脚本
├── logs/
│   ├── celery_worker.log           # Worker 日志
│   ├── celery_beat.log             # Beat 日志
│   └── ai_digest_YYYYMMDD.log      # 任务日志
└── AI_DIGEST_GUIDE.md              # 本文档
```

---

## 🎯 最佳实践

1. **定期检查日志**
   - 每周查看一次任务执行日志
   - 确保没有错误和异常

2. **备份日报文件**
   - 定期备份 `main/docs/ai_digest/` 目录
   - 防止数据丢失

3. **优化搜索关键词**
   - 根据实际需求调整 Skill 中的搜索关键词
   - 提高内容质量

4. **监控系统资源**
   - 确保 Redis 有足够内存
   - 监控 Celery Worker 进程

---

## 📞 技术支持

如有问题，请查看：

1. **日志文件** - `logs/` 目录
2. **Skill 文档** - `.claude/skills/ai_daily_digest/SKILL.md`
3. **任务代码** - `main/backend/tasks/ai_digest_task.py`

---

**生成时间**: 2026-01-20
**版本**: 1.0.0
**维护者**: Claude Dev Team
