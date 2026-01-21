# AI 日报目录结构重构说明

## 新的目录结构

所有 AI 日报相关代码已整合到 `main/backend/tasks/ai_digest/` 目录：

```
main/backend/tasks/ai_digest/
├── __init__.py          # 模块导出
├── models.py            # 数据库模型（原 models/ai_digest.py）
├── schemas.py           # Pydantic Schema（原 models/ai_digest_schema.py）
├── service.py           # 业务逻辑（原 services/ai_digest_service.py）
├── router.py            # API 路由（原 api/routes/ai_digest_router.py）
└── task.py              # Celery 定时任务（原 tasks/ai_digest_task.py）
```

## 导入路径变更

### 旧路径
```python
from models.ai_digest import AiDigest
from models.ai_digest_schema import AiDigestCreate
from services.ai_digest_service import AiDigestService
from api.routes.ai_digest_router import router
```

### 新路径
```python
from tasks.ai_digest.models import AiDigest
from tasks.ai_digest.schemas import AiDigestCreate
from tasks.ai_digest.service import AiDigestService
from tasks.ai_digest.router import router
```

### 或使用模块导入
```python
from tasks.ai_digest import (
    AiDigest,
    AiDigestCreate,
    AiDigestService,
    router
)
```

## 已更新的文件

1. `main/backend/main.py` - 更新路由导入
2. `main/backend/core/database.py` - 更新模型导入
3. `main/backend/tasks/ai_digest/service.py` - 更新内部导入
4. `main/backend/tasks/ai_digest/router.py` - 更新内部导入
5. `main/backend/tasks/ai_digest/task.py` - 更新内部导入

## 需要删除的旧文件

```bash
# 删除旧文件
rm main/backend/models/ai_digest.py
rm main/backend/models/ai_digest_schema.py
rm main/backend/services/ai_digest_service.py
rm main/backend/api/routes/ai_digest_router.py
rm main/backend/tasks/ai_digest_task.py
```

## 启动命令（无变化）

```bash
# 进入后端目录
cd main/backend

# 启动服务
uvicorn main:app --reload
```

## 优势

1. **模块化** - 所有相关代码集中在一个目录
2. **易维护** - 清晰的文件组织结构
3. **易扩展** - 可以轻松添加新功能
4. **独立性** - 可以作为独立模块使用或移除
