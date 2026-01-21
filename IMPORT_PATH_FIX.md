# 导入路径修复说明

## 问题原因

在 `main/backend/` 目录下运行时，Python 的模块搜索路径是从 `main/backend/` 开始的，不应该使用 `main.backend` 前缀。

## 已修复的文件

1. `main/backend/api/routes/ai_digest_router.py`
   - 修改前：`from main.backend.models.ai_digest_schema import ...`
   - 修改后：`from models.ai_digest_schema import ...`

2. `main/backend/services/ai_digest_service.py`
   - 修改前：`from main.backend.models.ai_digest import ...`
   - 修改后：`from models.ai_digest import ...`

3. `main/backend/tasks/ai_digest_task.py`
   - 修改前：`from main.backend.models.ai_digest_schema import ...`
   - 修改后：`from models.ai_digest_schema import ...`

## 启动命令

```bash
# 进入后端目录
cd main/backend

# 启动服务
uvicorn main:app --reload
```

## Redis 问题

如果看到 "Redis 未运行" 错误，需要先启动 Redis：

```bash
# macOS
brew services start redis

# 或直接运行
redis-server
```

## 验证步骤

1. 启动 Redis
2. 启动后端服务
3. 访问 http://127.0.0.1:8000/docs 查看 API 文档
4. 测试 AI 日报 API 端点
