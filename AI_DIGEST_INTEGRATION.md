# AI 日报集成说明

## 目录结构

所有 AI 日报相关代码位于 `main/backend/tasks/ai_digest/` 目录：

```
main/backend/tasks/ai_digest/
├── __init__.py          # 模块导出
├── models.py            # 数据库模型
├── schemas.py           # Pydantic Schema
├── service.py           # 业务逻辑
├── router.py            # API 路由
└── task.py              # Celery 定时任务
```

## 路由配置示例

在 Vue Router 配置文件中添加以下路由：

```typescript
// main/frontend/router/index.ts

import { createRouter, createWebHistory } from 'vue-router'
import AiDigestPage from '@/pages/AiDigestPage.vue'

const routes = [
  // ... 其他路由

  // AI 日报路由
  {
    path: '/ai-digest',
    name: 'AiDigest',
    component: AiDigestPage,
    meta: {
      title: 'AI 日报'
    }
  },
  {
    path: '/ai-digest/:date',
    name: 'AiDigestDetail',
    component: AiDigestPage,
    meta: {
      title: 'AI 日报详情'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

## 主页集成示例

在主页组件中引入 AI 日报卡片：

```vue
<!-- main/frontend/pages/HomePage.vue -->

<script setup lang="ts">
import AiDigestCard from '@/components/AiDigestCard.vue'
</script>

<template>
  <div class="home-page">
    <!-- 其他内容 -->

    <!-- AI 日报卡片 -->
    <AiDigestCard />

    <!-- 其他内容 -->
  </div>
</template>
```

## 导航栏集成示例

在导航栏中添加 AI 日报入口：

```vue
<!-- main/frontend/components/NavBar.vue -->

<template>
  <nav class="navbar">
    <router-link to="/">首页</router-link>
    <router-link to="/ai-digest">AI 日报</router-link>
    <router-link to="/docs">文档</router-link>
    <router-link to="/about">关于</router-link>
  </nav>
</template>
```

## 环境变量配置

在 `.env` 文件中配置 API 基础 URL：

```bash
# 开发环境
VITE_API_BASE_URL=http://localhost:8000

# 生产环境
VITE_API_BASE_URL=https://api.example.com
```

## 数据库迁移

创建数据库迁移文件：

```bash
# 使用 Alembic 创建迁移
alembic revision --autogenerate -m "Add ai_digest table"

# 执行迁移
alembic upgrade head
```

## 后端集成

在 FastAPI 主应用中注册路由：

```python
# main/backend/main.py

from fastapi import FastAPI
from main.backend.api.routes.ai_digest_router import router as ai_digest_router

app = FastAPI()

# 注册 AI 日报路由
app.include_router(ai_digest_router)
```

## 完整文件列表

### 后端文件（集中在 tasks/ai_digest/）
- `main/backend/tasks/ai_digest/__init__.py` - 模块导出
- `main/backend/tasks/ai_digest/models.py` - 数据库模型
- `main/backend/tasks/ai_digest/schemas.py` - Pydantic Schema
- `main/backend/tasks/ai_digest/service.py` - 业务逻辑
- `main/backend/tasks/ai_digest/router.py` - API 路由
- `main/backend/tasks/ai_digest/task.py` - Celery 定时任务

### 前端文件
- `main/frontend/services/aiDigestService.ts` - API 服务
- `main/frontend/components/AiDigestCard.vue` - 主页卡片组件
- `main/frontend/pages/AiDigestPage.vue` - 完整日报页面

### 配置文件
- `.claude/skills/ai_daily_digest/SKILL.md` - AI 日报 Skill
- `scripts/start_ai_digest.sh` - 启动脚本
- `scripts/stop_ai_digest.sh` - 停止脚本
- `AI_DIGEST_GUIDE.md` - 使用指南

## 下一步

1. **配置数据库连接**
   - 在 `main/backend/core/database.py` 中配置数据库连接
   - 实现 `get_db()` 依赖注入函数

2. **执行数据库迁移**
   - 创建 `ai_digests` 表
   - 添加必要的索引

3. **注册路由**
   - 在 FastAPI 主应用中注册 AI 日报路由

4. **配置前端路由**
   - 在 Vue Router 中添加 AI 日报路由

5. **集成到主页**
   - 在主页中引入 `AiDigestCard` 组件

6. **启动定时任务**
   - 运行 `./scripts/start_ai_digest.sh`

7. **测试功能**
   - 手动执行 `claude -p "执行 /ai-digest"`
   - 验证数据库保存
   - 验证前端展示
