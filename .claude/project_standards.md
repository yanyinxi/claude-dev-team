---
name: project-standards
description: 项目技术标准索引，定义项目的技术栈规范、代码规范和架构约定。此文件由 Evolver 自动维护更新。
---

# 项目技术标准

> ⚡ 项目技术规范的唯一事实来源。

## 项目信息

| 字段 | 值 |
|------|-----|
| 版本 | 2.0.0 |

## 🚀 进化机制

> 此文件支持自动进化，Evolver Agent 会根据任务执行结果自动更新以下章节。

### 可进化章节

| 章节 | 进化触发条件 | 更新频率 | 自动化级别 |
|------|-------------|---------|-----------|
| 技术栈版本 | 依赖版本变化 | 按需 | 🤖 自动 |
| 常用命令 | 工具链变化 | 按需 | 🤖 自动 |
| 最佳实践 | 任务成功/失败经验 | 每次 | 🤖 自动 |
| 代码示例 | 代码优化发现 | 按需 | 🤖 自动 |
| 错误处理规范 | 新错误类型 | 按需 | 🤖 自动 |
| 模式模板 | 新设计模式 | 按需 | 🤖 自动 |
| 进化记录 | 版本更新 | 每次 | 🤖 自动 |

### ❌ 禁止自动更新的章节

以下章节需要人工审核后才能更新：

| 章节 | 原因 | 处理方式 |
|------|------|---------|
| 路径配置 | 涉及项目结构重大变更 | 标记为待审核，人工确认 |
| 命名约定 | 影响所有代码命名 | 标记为待审核，人工确认 |
| API 规范 | 影响接口一致性 | 标记为待审核，人工确认 |

### 进化流程

```
任务执行完成
    │
    ▼
┌─────────────────────┐
│  Evolver Agent      │
│  - 分析执行结果     │
│  - 提取最佳实践     │
│  - 识别改进空间     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  判断进化类型        │
└──────────┬──────────┘
           │
           ├─── 技术栈/命令/最佳实践/代码示例/错误处理 ───┐
           │                                              │
           ▼                                              ▼
┌─────────────────────┐                    ┌─────────────────────┐
│  自动更新           │                    │  标记为待审核       │
│  - 更新文件         │                    │  - 添加审核标记     │
│  - 验证完整性       │                    │  - 发送告警通知     │
│  - 记录进化         │                    │  - 等待人工确认     │
└─────────────────────┘                    └─────────────────────┘
```

### 进化记录格式

```markdown
### [日期] v[版本号]
- **变更类型**: [技术栈/最佳实践/错误处理/其他]
- **变更内容**: [具体描述]
- **变更原因**: [为什么需要变更]
- **影响范围**: [哪些文件/功能受影响]
```

### 验证清单

每次进化后会自动验证以下项目：

- ✅ 文件结构完整性（必需章节存在）
- ✅ 代码块平衡（无未闭合的代码块标记）
- ✅ 路径变量一致性（定义与使用匹配）
- ✅ 版本号格式正确（v1.x.x）
- ✅ 进化记录已更新

### 进化历史

| 日期 | 版本 | 变更类型 | 主要变更 |
|------|------|---------|---------|
| 2026-01-19 | 2.0.0 | 路径 | 修复项目结构，移除多余的 `src/` 层级，改为 `main/frontend/` 和 `main/backend/` |
| 2026-01-19 | 1.9.0 | 路径 | 修复前端路径 `{FRONTEND_ROOT}` 为 `main/src/frontend/` |
| 2026-01-19 | 1.7.0 | 规范 | 新增中文代码注释规范（必要/重要/核心三级） |
| 2026-01-18 | 1.6.0 | 机制 | 新增自动进化机制 |
| 2026-01-18 | 1.5.0 | 路径 | Agent 文件统一使用路径变量 |
| 2026-01-18 | 1.4.0 | 结构 | 统一使用 main/src/backend/ 和 main/src/frontend/ |

---

## 📂 路径配置 (单一事实来源)

> ⚠️ **重要**: 所有代码路径以此配置为准，修改此处即修改全局路径约定
>
> **LLM 提示**: 使用路径时，请根据下方的 `路径变量` 列替换 `{VARIABLE}` 占位符

### 项目根路径变量

| 变量 | 值 (当前项目) | 说明 |
|------|--------------|------|
| `{PROJECT_ROOT}` | `main/` | 项目源码根目录 |
| `{BACKEND_ROOT}` | `main/backend/` | 后端代码根目录 |
| `{FRONTEND_ROOT}` | `main/frontend/` | **前端代码根目录** |

### 测试目录变量

| 变量 | 值 (当前项目) | 说明 |
|------|--------------|------|
| `{TESTS_ROOT}` | `main/tests/` | 测试根目录 |
| `{BACKEND_TESTS}` | `main/tests/backend/` | 后端测试目录 |
| `{FRONTEND_TESTS}` | `main/tests/frontend/` | 前端测试目录 |

### 文档目录变量

| 变量 | 值 (当前项目) | 说明 |
|------|--------------|------|
| `{DOCS_ROOT}` | `main/docs/` | 文档根目录 |
| `{PRD_DIR}` | `main/docs/prds/` | PRD 文档目录 |
| `{TECH_DESIGN_DIR}` | `main/docs/tech_designs/` | 技术设计目录 |
| `{API_DIR}` | `main/docs/api/` | API 规范目录 |
| `{REVIEW_DIR}` | `main/docs/reviews/` | 代码审查目录 |
| `{TEST_REPORT_DIR}` | `main/docs/test_reports/` | 测试报告目录 |
| `{BUG_REPORT_DIR}` | `main/docs/bug_reports/` | Bug 报告目录 |
| `{TASK_DIST_DIR}` | `main/docs/task_distribution/` | 任务分配目录 |

### 后端目录结构

| 目录 | 完整路径 | 职责 |
|------|---------|------|
| API 路由 | `{BACKEND_ROOT}/api/routes/` | FastAPI 路由定义、请求处理 |
| 业务服务 | `{BACKEND_ROOT}/services/` | 核心业务逻辑、数据处理 |
| 数据模型 | `{BACKEND_ROOT}/models/` | SQLAlchemy + Pydantic 模型 |
| 核心配置 | `{BACKEND_ROOT}/core/` | 配置、异常、安全认证 |
| 工具函数 | `{BACKEND_ROOT}/utils/` | 日志、验证、中间件 |

### 前端目录结构

| 目录 | 完整路径 | 职责 |
|------|---------|------|
| UI 组件 | `{FRONTEND_ROOT}/components/` | Vue 组件（通用 + 业务） |
| 页面容器 | `{FRONTEND_ROOT}/pages/` | 页面级别根容器组件 |
| 状态管理 | `{FRONTEND_ROOT}/stores/` | Pinia 全局状态 |
| API 服务 | `{FRONTEND_ROOT}/services/` | HTTP 请求、数据转换 |
| 工具函数 | `{FRONTEND_ROOT}/utils/` | 通用函数、类型定义 |
| 路由配置 | `{FRONTEND_ROOT}/router/` | Vue Router 路由配置 |
| 样式资源 | `{FRONTEND_ROOT}/styles/` | 全局样式、主题配置 |
| 入口文件 | `{FRONTEND_ROOT}/main.ts` | 应用入口文件 |
| 根组件 | `{FRONTEND_ROOT}/App.vue` | 应用根组件 |
| 样式资源 | `{FRONTEND_ROOT}/styles/` | 全局样式、主题配置 |

### 路径使用示例

```python
# 后端示例
from {BACKEND_ROOT}.services.user_service import UserService
from {BACKEND_ROOT}.api.routes.user_router import router as user_router

# 前端示例
import {FRONTEND_ROOT}.services.userService from '@/services/userService'
import {FRONTEND_ROOT}.stores.userStore from '@/stores/userStore'
```

### 路径配置变更记录

| 日期 | 版本 | 变更内容 | 原因 |
|------|------|---------|------|
| 2026-01-18 | 1.6.0 | 新增自动进化机制，添加进化流程和验证清单 | 实现 project_standards.md 自动进化能力 |
| 2026-01-18 | 1.5.0 | Agent 文件统一使用路径变量，移除硬编码路径 | 消除重复定义，确保单一事实来源 |
| 2026-01-18 | 1.4.0 | 统一使用 `main/src/backend/` 和 `main/src/frontend/` | 项目结构调整 |

---

## ⚡ 快速参考

### 📚 按任务类型查找

| 任务类型 | 查找章节 | 关键模式 |
|---------|---------|---------|
| 创建新 API 端点 | API 规范 | `POST/PUT/PATCH/DELETE /api/v1/xxx` |
| 添加前端页面 | 目录结构 → 前端 | `{FRONTEND_ROOT}/pages/xxx.vue` |
| 添加后端服务 | 目录结构 → 后端 | `{BACKEND_ROOT}/services/xxx_service.py` |
| 修复 Bug | Git 提交规范 | `fix(scope): description` |
| 添加新功能 | Git 提交规范 | `feat(scope): description` |
| 添加依赖 | 常用命令 | `poetry add xxx` / `npm install xxx` |
| 添加数据库模型 | 目录结构 → 后端 | `{BACKEND_ROOT}/models/` |
| 添加工具函数 | 目录结构 → 后端 | `{BACKEND_ROOT}/utils/xxx.py` |
| 错误处理 | 错误处理规范 | `raise AppException` |

### 🔧 常用命令速查

| 场景 | 前端命令 | 后端命令 |
|------|---------|---------|
| 安装依赖 | `npm install` | `poetry install` |
| 开发启动 | `npm run dev` | `uvicorn {BACKEND_ROOT}.main:app --reload` |
| 运行测试 | `npm run test` | `pytest` |
| 代码检查 | `npm run lint` | `ruff check {BACKEND_ROOT}/` |
| 代码格式化 | `npm run format` | `ruff format {BACKEND_ROOT}/` |
| 构建生产 | `npm run build` | N/A |

### 🌳 快速决策

```
需要新增功能？
├─ 需要 UI 界面？
│   ├─ 是 → 前端: {FRONTEND_ROOT}/pages/xxx.vue + {FRONTEND_ROOT}/components/xxx.vue
│   └─ 否 → 仅后端逻辑
├─ 需要数据库操作？
│   ├─ 是 → 后端: {BACKEND_ROOT}/services/xxx_service.py + {BACKEND_ROOT}/models/
│   └─ 否 → 仅工具函数: {BACKEND_ROOT}/utils/xxx.py
└─ 需要暴露 API？
    └─ API 路由: {BACKEND_ROOT}/api/routes/xxx_router.py
```

---

## 项目信息
| 更新 | 2026-01-18 |
| 维护 | Evolver |

## 技术栈

### 前端
**核心特性**：
- ✨ **快速开发** - Vite 极速 HMR，毫秒级热更新
- 🎯 **类型安全** - TypeScript 5.x 完整类型支持
- 📦 **状态管理** - Pinia 轻量级状态管理（比 Vuex 更简单）
- 🚀 **路由系统** - Vue Router 4.x 灵活的路由管理
- 🤖 **AI 友好** - 自动导入和自动组件注册，减少模板代码
- 🧪 **测试完整** - Vitest 单元测试 + Playwright E2E 测试
- 💄 **样式框架** - Tailwind CSS 原子类 + PostCSS

**技术选型理由**：
1. **Vue 3** - 比 React 更轻量，API 更直观，学习曲线平缓
2. **Vite** - 比 Webpack 快 10 倍以上，国内最受欢迎的构建工具
3. **Pinia** - 官方推荐，API 更简洁，TypeScript 支持更好
4. **unplugin** - 自动导入减少重复代码，AI 更容易理解项目结构
5. **Tailwind** - 函数式 CSS，团队协作更高效
| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.x | UI 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 5.x | 构建工具 |
| Pinia | 2.x | 状态管理 |
| Vue Router | 4.x | 路由 |
| Axios | 1.x | HTTP 客户端 |
| Tailwind CSS | 3.x | CSS 框架 |
| unplugin-auto-import | 0.x | 自动导入 |
| unplugin-vue-components | 0.x | 自动组件 |
| Vitest | 1.x | 单元测试 |
| Playwright | 1.x | E2E 测试 |
| ESLint + Prettier | 9.x | 代码质量 |

### 后端 (Python + FastAPI + LangChain)

**核心特性**：
- 🚀 **异步优先** - FastAPI 异步架构，比 Flask 快 10 倍
- 🤖 **AI 生态** - LangChain 完整的大模型应用框架
- 📊 **向量检索** - Qdrant 本地向量数据库，完美支持 RAG
- 💾 **灵活存储** - SQLite (开发) + PostgreSQL (生产)
- ⚡ **多层缓存** - Redis + FastAPI Cache2 + 内存缓存
- 📝 **自动文档** - FastAPI 自动生成 Swagger/OpenAPI 文档
- ⏱️ **后台任务** - Celery + Redis 分布式任务处理
- 🧪 **测试完整** - Pytest 单元测试 + 覆盖率报告

**技术选型理由**：
1. **Python 3.10+** - AI/ML 生态最成熟，LangChain 原生支持
2. **FastAPI** - 比 Flask/Django 快 10 倍，完美支持异步
3. **LangChain + Qdrant** - 大模型应用框架 + 开源向量数据库（自托管友好）
4. **SQLAlchemy 2.x** - Python ORM 最强大，支持 SQLite 和 PostgreSQL
5. **Pydantic 2.x** - 数据验证标准库，自动生成 JSON Schema
6. **Redis** - 缓存 + 消息队列 + 会话存储
7. **FastAPI Cache2** - 装饰器式缓存，开发便捷

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 编程语言 |
| FastAPI | 0.100+ | Web 框架 |
| Uvicorn | 0.23+ | ASGI 服务器 |
| LangChain | 0.1+ | LLM 应用框架 |
| LangChain-Qdrant | 最新 | Qdrant 集成 |
| SQLAlchemy | 2.x | ORM 框架 |
| Alembic | 1.x | 数据库迁移 |
| Pydantic | 2.x | 数据验证 |
| Qdrant-Client | 2.x | 向量数据库客户端 |
| SQLite | 3.x | 本地开发数据库 |
| PostgreSQL | 16 | 生产关系数据库 |
| AsyncPG | 0.28+ | PostgreSQL 异步驱动 |
| Redis | 7.x | 缓存 + 消息队列 |
| FastAPI-Cache2 | 0.2+ | API 响应缓存 |
| Celery | 5.x | 异步任务队列 |
| NumPy | 1.x | 数值计算 |
| Sentence-Transformers | 2.x | 文本向量化 |
| Pytest | 7.x | 单元测试 |
| Ruff | 0.x | 代码质量检查 |
| Poetry | 1.x | 包管理工具 |

## 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| Python 文件 | snake_case | `user_service.py` |
| 类名 | PascalCase | `UserService` |
| 函数/变量 | snake_case | `get_user_data()` |
| 常量 | UPPER_SNAKE | `MAX_RETRY` |
| 路由 | kebab-case | `/api/v1/user-profiles` |
| 表名 | snake_case 复数 | `user_accounts` |
| Vue 组件 | PascalCase | `UserProfile.vue` |
| Composable | use + PascalCase | `useUserData.ts` |

## 📁 文件命名速查表

| 目录 | 文件类型 | 命名模式 | ✅ 正确示例 | ❌ 错误示例 |
|------|---------|---------|-----------|-----------|
| **后端 (FastAPI)** |
| `{BACKEND_ROOT}/api/routes/` | 路由文件 | `{resource}_router.py` | `user_router.py` | `UserRouter.py`, `users-router.py` |
| `{BACKEND_ROOT}/services/` | 服务文件 | `{resource}_service.py` | `user_service.py` | `UserService.py`, `userSvc.py` |
| `{BACKEND_ROOT}/models/` | 数据库模型 | `db.py` | `db.py` | `database.py`, `models.py` |
| `{BACKEND_ROOT}/models/` | Pydantic 模式 | `{resource}_schema.py` | `user_schema.py` | `UserModel.py`, `userModels.py` |
| `{BACKEND_ROOT}/utils/` | 工具函数 | `{purpose}.py` | `logger.py`, `validators.py` | `util.py`, `HelperFunctions.py` |
| `{BACKEND_ROOT}/core/` | 配置文件 | `{purpose}.py` | `config.py`, `exceptions.py` | `settings.py`, `CoreConfig.py` |
| **前端 (Vue)** |
| `{FRONTEND_ROOT}/components/` | Vue 组件 | `{PascalCase}.vue` | `UserCard.vue` | `user-card.vue`, `UserCard.ts` |
| `{FRONTEND_ROOT}/pages/` | 页面组件 | `{PascalCase}.vue` | `UserList.vue` | `user-list.vue`, `page_user.py` |
| `{FRONTEND_ROOT}/stores/` | Pinia store | `{camelCase}Store.ts` | `userStore.ts` | `UserStore.ts`, `user-store.js` |
| `{FRONTEND_ROOT}/services/` | API 服务 | `{camelCase}Service.ts` | `userService.ts` | `UserService.ts`, `api_user.js` |
| `{FRONTEND_ROOT}/composables/` | Composable | `use{camelCase}.ts` | `useUserData.ts` | `userData.ts`, `UseUserData.ts` |
| `{FRONTEND_ROOT}/utils/` | 工具函数 | `{camelCase}.ts` | `formatDate.ts` | `FormatDate.ts`, `utils.js` |
| `{FRONTEND_ROOT}/types/` | 类型定义 | `{PascalCase}.ts` | `UserTypes.ts` | `userTypes.js`, `types.ts` |

### 前缀/后缀约定

| 类型 | 前缀/后缀 | 示例 |
|------|----------|------|
| Service 类 | `{Resource}Service` | `UserService`, `PaymentService` |
| Router 文件 | `_router.py` | `user_router.py`, `order_router.py` |
| Service 文件 | `_service.py` | `user_service.py`, `order_service.py` |
| Schema 文件 | `_schema.py` | `user_schema.py`, `order_schema.py` |
| Pinia Store | `Store` | `userStore`, `cartStore` |
| Composable | `use` | `useAuth`, `useFetch` |
| 工具函数 | 无特殊后缀 | `formatDate`, `validateEmail` |

### 常量命名

| 类型 | 规则 | 示例 |
|------|------|------|
| 配置常量 | UPPER_SNAKE | `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE` |
| 环境变量 | UPPER_SNAKE | `DATABASE_URL`, `REDIS_HOST` |
| 状态码 | UPPER_SNAKE | `HTTP_STATUS_OK`, `ERROR_CODE_NOT_FOUND` |

---

## 📝 代码注释规范

> ⚠️ **重要**: 所有代码必须添加必要的中文注释，尤其是核心逻辑和关键实现。

### 注释级别

| 级别 | 说明 | 场景 |
|------|------|------|
| **必要注释** | 必须添加，不加扣分 | 函数/方法、类、复杂逻辑 |
| **重要注释** | 强烈建议添加 | 业务逻辑、算法、配置 |
| **核心注释** | 必须详细说明 | 关键流程、边界情况、hack 方案 |

### Python 注释规范

```python
# =====================================================
# 核心注释：模块功能说明
# =====================================================
# 用户认证服务 - 处理用户登录、注册、Token 生成与验证
# 依赖：JWT 加密、bcrypt 密码加密
# =====================================================

from datetime import datetime, timedelta


class AuthService:
    """
    认证服务类 - 核心业务逻辑

    功能：
    1. 用户登录验证
    2. JWT Token 生成与刷新
    3. 密码加密与验证

    使用示例：
        service = AuthService()
        token = service.login("user@example.com", "password")
    """

    # 重要注释：常量定义
    TOKEN_EXPIRE_HOURS = 24  # Token 过期时间（小时）
    REFRESH_EXPIRE_DAYS = 7  # 刷新 Token 过期时间（天）

    def __init__(self, secret_key: str):
        """
        初始化认证服务

        Args:
            secret_key: JWT 加密密钥，生产环境从环境变量读取
        """
        self.secret_key = secret_key

    async def login(self, email: str, password: str) -> dict:
        """
        用户登录 - 核心业务方法

        Args:
            email: 用户邮箱
            password: 原始密码（未加密）

        Returns:
            dict: 包含 access_token 和 refresh_token

        Raises:
            ValidationException: 参数验证失败
            UnauthorizedException: 账号或密码错误

        业务流程：
        1. 校验邮箱格式
        2. 从数据库获取用户
        3. 验证密码（bcrypt）
        4. 生成 JWT Token
        5. 记录登录日志
        """
        # 必要注释：校验邮箱格式
        if not self._validate_email(email):
            raise ValidationException([{"field": "email", "error": "邮箱格式不正确"}])

        # 重要注释：查询用户（使用 N+1 优化后的批量查询）
        user = await self.user_repo.get_by_email(email)
        if not user:
            # 核心注释：安全考虑，不提示具体错误信息
            raise UnauthorizedException("账号或密码错误")

        # 必要注释：验证密码
        if not self._verify_password(password, user.hashed_password):
            raise UnauthorizedException("账号或密码错误")

        # 核心注释：生成 Token，封装敏感信息
        access_token = self._generate_token(
            user_id=user.id,
            email=user.email,
            role=user.role
        )

        # 记录登录日志
        await self._log_login(user.id, "success")

        return {
            "access_token": access_token,
            "refresh_token": self._generate_refresh_token(user.id),
            "token_type": "Bearer"
        }

    def _generate_token(self, user_id: int, email: str, role: str) -> str:
        """
        生成 JWT Token - 核心加密逻辑

        Args:
            user_id: 用户 ID
            email: 用户邮箱
            role: 用户角色

        Returns:
            str: JWT Token 字符串

        核心实现：
        - 使用 HS256 算法加密
        -  payload 包含用户基本信息
        - 设置过期时间防止 Token 泄露
        """
        # 必要注释：构建 payload
        payload = {
            "sub": str(user_id),  # subject: 用户标识
            "email": email,
            "role": role,
            "iat": datetime.utcnow(),  # issued at: 签发时间
            "exp": datetime.utcnow() + timedelta(hours=self.TOKEN_EXPIRE_HOURS)
        }

        # 核心注释：JWT 加密编码
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token
```

### Vue/TypeScript 注释规范

```typescript
// =====================================================
// 核心注释：组件功能说明
// =====================================================
// 用户登录表单组件
// 功能：邮箱/密码登录、记住我、忘记密码链接
// 依赖：userStore、validationUtils
// =====================================================

import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { validateEmail, validatePassword } from '@/utils/validationUtils'

// 重要注释：Props 类型定义
interface Props {
  /** 是否显示记住我复选框 */
  showRememberMe?: boolean
  /** 登录成功后的回调函数 */
  onSuccess?: (user: User) => void
  /** 自定义登录 API 地址 */
  loginApiUrl?: string
}

/**
 * 用户登录表单组件 - 核心业务组件

 * 使用示例：
 * <UserLoginForm
 *   :show-remember-me="true"
 *   :on-success="handleLoginSuccess"
 * />
 */
const UserLoginForm = (props: Props) => {
  // =====================================================
  // 必要注释：响应式数据定义
  // =====================================================
  const email = ref('')           // 用户邮箱
  const password = ref('')        // 用户密码
  const loading = ref(false)      // 加载状态
  const errorMessage = ref('')    // 错误信息
  const rememberMe = ref(false)   // 记住我

  // =====================================================
  // 核心注释：计算属性
  // =====================================================
  const isFormValid = computed(() => {
    // 校验逻辑：邮箱和密码都不为空
    return validateEmail(email.value) && password.value.length >= 6
  })

  // =====================================================
  // 必要注释：方法定义
  // =====================================================

  /**
   * 处理登录 - 核心业务方法

   * 业务流程：
   * 1. 表单校验
   * 2. 显示加载状态
   * 3. 调用登录 API
   * 4. 处理成功/失败结果
   */
  const handleLogin = async () => {
    // 必要注释：表单校验
    if (!isFormValid.value) {
      errorMessage.value = '请输入正确的邮箱和密码'
      return
    }

    try {
      loading.value = true
      errorMessage.value = ''

      // 核心注释：调用登录 API
      const response = await fetch(props.loginApiUrl || '/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.value,
          password: password.value,
          remember: rememberMe.value
        })
      })

      // 重要注释：处理响应
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || '登录失败')
      }

      const data = await response.json()

      // 核心注释：存储用户信息到 Pinia
      const userStore = useUserStore()
      userStore.setToken(data.access_token)
      userStore.setUser(data.user)

      // 重要注释：记住我功能 - 存储到 localStorage
      if (rememberMe.value) {
        localStorage.setItem('remember_email', email.value)
      } else {
        localStorage.removeItem('remember_email')
      }

      // 回调通知
      props.onSuccess?.(data.user)

    } catch (error) {
      // 核心注释：错误处理 - 不暴露敏感信息
      errorMessage.value = error instanceof Error ? error.message : '登录失败，请稍后重试'
    } finally {
      loading.value = false
    }
  }

  // =====================================================
  // 必要注释：生命周期钩子
  // =====================================================

  /**
   * 组件挂载时检查记住的邮箱
   */
  onMounted(() => {
    const savedEmail = localStorage.getItem('remember_email')
    if (savedEmail && props.showRememberMe) {
      email.value = savedEmail
      rememberMe.value = true
    }
  })

  return {
    // 模板需要使用的变量和方法
    email,
    password,
    loading,
    errorMessage,
    rememberMe,
    isFormValid,
    handleLogin
  }
}

export default UserLoginForm
```

### 注释检查清单

| 检查项 | 描述 |
|--------|------|
| ✅ 文件头注释 | 每个文件必须有功能说明、作者、创建时间 |
| ✅ 类注释 | 每个类必须有用途说明和使用示例 |
| ✅ 函数注释 | 每个函数必须有参数、返回值、异常说明 |
| ✅ 核心逻辑注释 | 关键算法、业务流程必须有中文注释 |
| ✅ 边界情况注释 | 特殊输入、异常处理必须有说明 |
| ✅ TODO 注释 | 未完成的代码必须有 TODO 说明 |

### 不需要注释的情况

| 情况 | 说明 |
|------|------|
| 简单 Getter/Setter | `getName() { return this.name }` |
| 显而易见的变量 | `const items = []` |
| 通用模板代码 | Vue 组件的基本结构 |
| 第三方库调用 | 遵循原库文档即可 |

---

## API 规范

```
GET    /api/v1/users          # 列表
GET    /api/v1/users/:id      # 详情
POST   /api/v1/users          # 创建
PATCH  /api/v1/users/:id      # 更新
DELETE /api/v1/users/:id      # 删除（软删除）
```

响应格式：
```json
{ "code": 200, "message": "success", "data": {} }
```

## 目录结构

### 前端 (Vue 3 + Vite) - `{FRONTEND_ROOT}` 下的结构

```
{FRONTEND_ROOT}/
├── components/      # UI 组件库
│                    # 职责：所有 Vue 组件（通用 + 业务）
│                    # 边界：纯 UI 渲染，不含业务逻辑
│
├── pages/          # 页面容器
│                    # 职责：页面级别的根容器组件
│                    # 边界：组织 components + composables
│
├── services/       # API & 业务服务
│                    # 职责：HTTP 请求、外部 API 调用、数据转换
│                    # 边界：不涉及 UI 状态，只处理数据流
│
├── stores/         # Pinia 状态管理
│                    # 职责：应用全局状态、缓存状态、跨页面通信
│                    # 边界：只存储需要多处使用的状态
│
├── utils/          # 工具函数库
│                    # 职责：通用函数、类型定义、常量、helpers
│                    # 边界：无依赖、纯函数、可复用代码
│
├── styles/         # 样式 & 资源
│                    # 职责：全局样式、资源文件 (assets)、主题配置
│                    # 边界：只放样式和静态资源，不放逻辑代码
│
├── router/         # 路由配置
│                    # 职责：Vue Router 路由定义
│                    # 边界：路由规则，不涉及业务逻辑
│
├── main.ts         # 应用入口
│                    # 职责：Vue 应用初始化
│
├── App.vue         # 根组件
│                    # 职责：应用顶层组件
│
├── index.html      # HTML 入口
│                    # 职责：页面骨架，挂载 Vue 应用
│
├── package.json    # 项目配置
│                    # 职责：依赖管理、脚本命令
│
├── vite.config.ts  # Vite 配置
│                    # 职责：构建工具配置
│
└── tsconfig.json   # TypeScript 配置
                    # 职责：类型检查、编译选项
```

### 后端 (Python FastAPI) - 6 个目录

```
src/
├── api/            # 路由层
│                    # 职责：FastAPI 路由定义、请求处理、响应返回
│                    # 边界：只做请求/响应转换，业务逻辑委托给 services
│                    # 内容：routes/users.py, routes/products.py ...
│
├── models/         # 数据模型
│                    # 职责：数据库模型 + Pydantic 模型
│                    # 边界：定义数据结构，不含业务逻辑
│                    # 内容：db.py (SQLAlchemy) + schema.py (Pydantic)
│
├── services/       # 业务逻辑层
│                    # 职责：核心业务逻辑、数据处理、LLM 调用、RAG、任务
│                    # 边界：与数据库交互，处理复杂业务流程
│                    # 内容：user_svc.py, llm_svc.py, rag_svc.py 等
│
├── core/           # 核心配置
│                    # 职责：环境配置、异常定义、安全认证、依赖注入
│                    # 边界：项目全局的静态配置和工具类
│                    # 内容：config.py, exceptions.py, security.py
│
├── utils/          # 工具函数库
│                    # 职责：日志、验证、中间件、helpers、缓存工具
│                    # 边界：无业务逻辑的工具代码，可复用
│                    # 内容：logger.py, validators.py, middleware/ 等
│
└── tests/          # 测试用例
                    # 职责：单元测试、集成测试、测试工具
                    # 边界：测试代码专区，不影响生产代码
                    # 内容：test_api/, test_services/, conftest.py
```

**补充说明**：
- 项目根目录：`main.py`、`requirements.txt`、`pyproject.toml`、`.env.example`、`alembic/`

## 🌳 决策树

### 新功能开发决策

```
需要新增功能？
│
├─ 需要 UI 界面？
│   ├─ 是 → 前端开发
│   │   ├─ 通用 UI 组件 → `{FRONTEND_ROOT}/components/`
│   │   │   └─ 命名: PascalCase (e.g., UserCard.vue)
│   │   │
│   │   ├─ 页面级别 → `{FRONTEND_ROOT}/pages/`
│   │   │   └─ 命名: PascalCase (e.g., UserList.vue)
│   │   │
│   │   ├─ 跨页面状态 → `{FRONTEND_ROOT}/stores/`
│   │   │   └─ 命名: camelCase + Store (e.g., userStore.ts)
│   │   │
│   │   └─ API 调用 → `{FRONTEND_ROOT}/services/`
│   │       └─ 命名: camelCase + Service (e.g., userService.ts)
│   │
│   └─ 否 → 仅后端逻辑
│
├─ 需要数据库操作？
│   ├─ 是 → 后端开发
│   │   ├─ 数据模型 → `{BACKEND_ROOT}/models/`
│   │   │   ├─ db.py (SQLAlchemy models)
│   │   │   └─ schema.py (Pydantic models)
│   │   │
│   │   ├─ 业务逻辑 → `{BACKEND_ROOT}/services/`
│   │   │   └─ 命名: snake_case + _service (e.g., user_service.py)
│   │   │
│   │   └─ API 路由 → `{BACKEND_ROOT}/api/routes/`
│   │       └─ 命名: snake_case + _router (e.g., user_router.py)
│   │
│   └─ 否 → 仅工具函数
│       └─ → `{BACKEND_ROOT}/utils/`
│           └─ 命名: snake_case (e.g., logger.py, validators.py)
│
└─ 需要暴露 API？
    └─ → `{BACKEND_ROOT}/api/routes/xxx_router.py`
```

### 错误处理决策

```
发生错误？
│
├─ 输入验证错误 (400) → raise ValidationException
│
├─ 资源不存在 (404) → raise NotFoundException
│
├─ 未授权 (401) → raise UnauthorizedException
│
├─ 禁止访问 (403) → raise ForbiddenException
│
├─ 业务冲突 (409) → raise ConflictException
│
└─ 服务器错误 (500) → raise InternalException
```

### Git Commit 决策

```
代码变更类型？
│
├─ 新功能 → feat(scope): description
│   └─ 示例: feat(user): add login API
│
├─ 修复 Bug → fix(scope): description
│   └─ 示例: fix(auth): resolve token expiration bug
│
├─ 文档更新 → docs(scope): description
│   └─ 示例: docs(readme): update installation guide
│
├─ 代码格式 → style(scope): description
│   └─ 示例: style(api): format code with ruff
│
├─ 重构代码 → refactor(scope): description
│   └─ 示例: refactor(utils): optimize validation logic
│
├─ 添加测试 → test(scope): description
│   └─ 示例: test(service): add user creation test
│
└─ 工具/配置 → chore(scope): description
    └─ 示例: chore(ci): update github workflow
```

---

## 🚨 错误处理规范

### HTTP 状态码

| 场景 | 状态码 | 错误码 |
|------|--------|--------|
| 成功 | 200 | `success` |
| 创建成功 | 201 | `created` |
| 客户端错误 | 400 | `bad_request` |
| 未授权 | 401 | `unauthorized` |
| 资源不存在 | 404 | `not_found` |
| 禁止访问 | 403 | `forbidden` |
| 冲突 | 409 | `conflict` |
| 服务器错误 | 500 | `internal_error` |

### 错误响应格式

```json
{
  "code": 404,
  "message": "User not found",
  "details": {
    "resource": "user",
    "resource_id": 123
  }
}
```

### 异常类定义

```python
# 📁 {BACKEND_ROOT}/core/exceptions.py

from fastapi import HTTPException, status


class AppException(HTTPException):
    """基础异常类"""
    def __init__(self, code: str, message: str, details: dict = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(status_code=status_code, detail=message)


class NotFoundException(AppException):
    """资源不存在 (404)"""
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            code="not_found",
            message=f"{resource} with id {resource_id} not found",
            details={"resource": resource, "resource_id": resource_id},
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationException(AppException):
    """数据验证错误 (400)"""
    def __init__(self, field_errors: list):
        super().__init__(
            code="validation_error",
            message="Validation failed",
            details={"field_errors": field_errors},
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UnauthorizedException(AppException):
    """未授权 (401)"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            code="unauthorized",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ForbiddenException(AppException):
    """禁止访问 (403)"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            code="forbidden",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


class ConflictException(AppException):
    """业务冲突 (409)"""
    def __init__(self, message: str):
        super().__init__(
            code="conflict",
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )


class InternalException(AppException):
    """服务器错误 (500)"""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            code="internal_error",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

### 使用示例

```python
# 📁 {BACKEND_ROOT}/api/routes/users.py

from {BACKEND_ROOT}.core.exceptions import NotFoundException, ValidationException


@router.get("/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    user = await user_service.get(user_id)
    if not user:
        raise NotFoundException("user", user_id)
    return user


@router.post("")
async def create_user(data: UserCreate) -> UserResponse:
    # 验证数据
    if not data.email:
        raise ValidationException([{"field": "email", "error": "Email is required"}])
    
    # 创建用户
    return await user_service.create(data)
```

---

## 🔧 模式模板

### API CRUD 模板

```python
# 📁 {BACKEND_ROOT}/api/routes/{resource}_router.py

from fastapi import APIRouter, HTTPException, status
from {BACKEND_ROOT}.models.schema import {Resource}Create, {Resource}Update, {Resource}Response
from {BACKEND_ROOT}.services.{resource}_service import {Resource}Service
from {BACKEND_ROOT}.core.exceptions import NotFoundException

router = APIRouter(prefix="/api/v1/{resources}", tags=["{Resources}"])


@router.get("", response_model=list[{Resource}Response])
async def list_{resources}() -> list[{Resource}Response]:
    """列出所有 {resources}"""
    return await {Resource}Service.list()


@router.get("/{id}", response_model={Resource}Response)
async def get_{resource}(id: int) -> {Resource}Response:
    """获取单个 {resource}"""
    resource = await {Resource}Service.get(id)
    if not resource:
        raise NotFoundException("{resource}", id)
    return resource


@router.post("", response_model={Resource}Response, status_code=status.HTTP_201_CREATED)
async def create_{resource}(data: {Resource}Create) -> {Resource}Response:
    """创建 {resource}"""
    return await {Resource}Service.create(data)


@router.patch("/{id}", response_model={Resource}Response)
async def update_{resource}(id: int, data: {Resource}Update) -> {Resource}Response:
    """更新 {resource}"""
    return await {Resource}Service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{resource}(id: int):
    """删除 {resource} (软删除)"""
    await {Resource}Service.soft_delete(id)
```

### Service 模板

```python
# 📁 {BACKEND_ROOT}/services/{resource}_service.py

from typing import Optional, list
from {BACKEND_ROOT}.models.schema import {Resource}Create, {Resource}Update, {Resource}Response


class {Resource}Service:
    """{Resource} 服务层"""
    
    @staticmethod
    async def list() -> list[{Resource}Response]:
        """列出所有资源"""
        ...
    
    @staticmethod
    async def get(id: int) -> Optional[{Resource}Response]:
        """获取单个资源"""
        ...
    
    @staticmethod
    async def create(data: {Resource}Create) -> {Resource}Response:
        """创建资源"""
        ...
    
    @staticmethod
    async def update(id: int, data: {Resource}Update) -> {Resource}Response:
        """更新资源"""
        ...
    
    @staticmethod
    async def soft_delete(id: int) -> None:
        """软删除资源"""
        ...
```

### Vue 组件模板

```vue
<!-- 📁 {FRONTEND_ROOT}/components/{PascalCase}.vue -->

<script setup lang="ts">
// 导入类型和 props
interface Props {
  // 定义 props
}

const props = defineProps<Props>()

// 导入 composables
// const { xxx } = useXxx()

// 定义 emits
// const emit = defineEmits<{ xxx: [value: type] }>()

// 响应式数据
// const count = ref(0)

// 计算属性
// const doubleCount = computed(() => count.value * 2)

// 方法
// const handleClick = () => { ... }

// 生命周期
// onMounted(() => { ... })
</script>

<template>
  <div class="{kebab-case}">
    <!-- 模板内容 -->
  </div>
</template>

<style scoped>
.{kebab-case} {
  /* 样式 */
}
</style>
```

### Pydantic Schema 模板

```python
# 📁 {BACKEND_ROOT}/models/schema.py

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class {Resource}Base(BaseModel):
    """基础模型"""
    ...


class {Resource}Create({Resource}Base):
    """创建模型"""
    ...


class {Resource}Update(BaseModel):
    """更新模型"""
    ...


class {Resource}Response({Resource}Base):
    """响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## 最佳实践

### 数据库策略

| 环境 | 数据库 | 适用场景 |
|------|------|--------|
| 开发 | PostgreSQL | 本地开发、快速测试、演示 |
| 测试 | PostgreSQL | 单元测试、集成测试 |
| 生产 | PostgreSQL | 并发处理、事务、数据安全 |

### 缓存分层策略

```
L1 缓存（最快）: 内存缓存 (FastAPI Cache2)
    └─ 单服务器进程级
    └─ 适合：同进程内的频繁数据
    
L2 缓存（快）: Redis
    └─ 分布式、跨服务器
    └─ 适合：热点数据、会话、状态
    
L3 缓存（完整）: 数据库
    └─ 持久化存储
    └─ 适合：所有数据
```

### FastAPI Cache2 使用示例

```python
# 📁 {BACKEND_ROOT}/api/endpoints/cache_example.py

from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend
from fastapi_cache2.decorators import cache

# 简单缓存 60 秒
@app.get("/users/{user_id}")
@cache(expire=60)
async def get_user(user_id: int):
    return await db.get_user(user_id)

# 自定义缓存 key
@app.get("/search")
@cache(expire=300, namespace="search")
async def search(q: str):
    return await db.search(q)
```

### 向量数据库 (Qdrant) 与 LangChain 集成

```python
# 📁 {BACKEND_ROOT}/services/rag_service.py

from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

# 初始化嵌入模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 连接 Qdrant
client = QdrantClient(
    host="localhost",
    port=6333,
    # 或使用内存模式：path="./qdrant_storage"
)

# 创建向量存储
vector_store = Qdrant(
    client=client,
    collection_name="my_collection",
    embeddings=embeddings,
)

# RAG 应用
documents = ["文本 1", "文本 2", "文本 3"]
vector_store.add_texts(documents)

# 向量检索
results = vector_store.similarity_search("查询文本", k=3)
```

### 异步数据库连接

```python
# 📁 {BACKEND_ROOT}/core/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# PostgreSQL 异步连接
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/dbname",
    echo=False,
    pool_size=20,
    max_overflow=0,
)

# SQLite 异步连接
engine = create_async_engine(
    "sqlite+aiosqlite:///./test.db",
)

# 异步查询
async with AsyncSession(engine) as session:
    user = await session.get(User, user_id)
```

### 后台任务 (Celery)

```python
# 📁 {BACKEND_ROOT}/tasks/embedding_tasks.py

from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379",
    backend="redis://localhost:6379"
)

# 异步任务
@celery_app.task
def process_embedding(text: str):
    # 长流程任务
    embedding = model.encode(text)
    return embedding

# 在 FastAPI 中调用
@app.post("/process")
async def process(text: str):
    task = process_embedding.delay(text)
    return {"task_id": task.id}
```

## Git 提交规范

```
feat: 新功能
fix: 修复
docs: 文档
style: 格式
refactor: 重构
test: 测试
chore: 工具
```

## 常用命令

### 前端 (Vue 3 + Vite + TypeScript)

```bash
# 创建新项目
npm create vite@latest my-app -- --template vue-ts

# 安装依赖
npm install

# 开发环境启动
npm run dev

# 生产构建
npm run build

# 预览构建结果
npm run preview

# 运行测试
npm run test

# 代码检查
npm run lint

# 格式化代码
npm run format
```

### 初始化 package.json 依赖

```bash
npm install vue@3 pinia vue-router axios
npm install -D typescript vite @vitejs/plugin-vue
npm install -D unplugin-auto-import unplugin-vue-components
npm install -D vitest @vitest/ui playwright
npm install -D eslint prettier eslint-plugin-vue
npm install -D tailwindcss postcss autoprefixer
```

### 后端 (Python FastAPI + LangChain)

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 使用 Poetry 创建项目
poetry new backend

# 使用 Poetry 安装依赖
poetry install

# 运行开发服务器
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 数据库初始化
alembic init alembic

# 创建迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head

# 运行单元测试
pytest

# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 代码质量检查
ruff check src/

# 代码格式化
ruff format src/

# 启动 Celery worker
celery -A src.tasks worker --loglevel=info

# 启动 Celery beat (定时任务)
celery -A src.tasks beat --loglevel=info
```

### 初始化 Python 依赖 (Poetry)

```bash
# 创建项目
poetry new backend
cd backend

# 核心依赖
poetry add fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic
poetry add langchain langchain-core langchain-community

# LLM 和向量处理
poetry add langchain-qdrant qdrant-client
poetry add sentence-transformers numpy scikit-learn

# 数据库驱动
poetry add asyncpg           # PostgreSQL 异步驱动
poetry add psycopg2-binary   # PostgreSQL 同步驱动（备用）

# 缓存和队列
poetry add redis
poetry add fastapi-cache2
poetry add celery

# 安全和认证
poetry add python-dotenv PyJWT passlib python-multipart
poetry add pyjwt cryptography

# HTTP 和网络
poetry add httpx aiohttp requests

# 日志和监控
poetry add python-json-logger

# 开发依赖
poetry add -G dev pytest pytest-cov pytest-asyncio
poetry add -G dev black ruff mypy
poetry add -G dev httpx  # 测试 HTTP 客户端
poetry add -G dev pytest-mock  # Mock 支持
```

### 数据库配置示例

```python
# 📁 {BACKEND_ROOT}/core/config.py

# 开发环境：SQLite
DATABASE_URL = "sqlite:///./test.db"

# 生产环境：PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# 向量数据库：Qdrant
QDRANT_URL = "http://localhost:6333"
# 或使用内存模式（开发）
QDRANT_PATH = "./qdrant_storage"
```

### Qdrant 快速启动

```bash
# Docker 启动 Qdrant
docker run -p 6333:6333 qdrant/qdrant

# 使用内存模式（开发，无需 Docker）
# 在代码中使用：from qdrant_client import QdrantClient
# client = QdrantClient(path="./qdrant_storage")
```

### 快速启动脚本 (start.sh)

```bash
#!/bin/bash
# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
alembic upgrade head

# 启动服务
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 进化记录

### 2026-01-19 v2.0.0
- **修复项目结构**: 移除多余的 `main/src/` 层级
- 将 `main/src/frontend/` 移动到 `main/frontend/`
- 将 `main/src/backend/` 移动到 `main/backend/`
- 更新所有路径变量配置：`{PROJECT_ROOT}` = `main/`, `{FRONTEND_ROOT}` = `main/frontend/`, `{BACKEND_ROOT}` = `main/backend/`

### 2026-01-19 v1.9.0
- **修复前端路径配置**: `{FRONTEND_ROOT}` 从 `main/src/frontend/src/` 改为 `main/src/frontend/`
- 更新前端目录结构，添加更多子目录说明（router, styles, 配置文件等）
- 更新 frontend-developer.md 示例路径

### 2026-01-19 v1.7.0
- **新增中文代码注释规范**: 定义必要、重要、核心三级注释标准
- 添加 Python 和 Vue/TypeScript 完整注释示例
- 包含注释检查清单，明确哪些情况需要/不需要注释

### 2026-01-18 v1.6.0
- **新增自动进化机制**: Evolver Agent 现在可以自动更新 project_standards.md
- **添加进化流程图**: 明确自动更新与人工审核的边界
- **定义可进化章节**: 技术栈版本、最佳实践、代码示例、错误处理规范等
- **添加禁止自动更新列表**: 路径配置、命名约定、API 规范需要人工审核
- **新增验证清单**: 文件结构、路径变量、版本格式等自动验证

### 2026-01-18 v1.5.0
- **数据库架构优化**：明确 SQLite (开发) + PostgreSQL (生产) 策略
- **向量数据库升级**：Pinecone/Weaviate → Qdrant (开源自托管友好)
- 添加 LangChain-Qdrant 集成
- **多层缓存策略**：FastAPI Cache2 + Redis + 内存缓存
- 集成 AsyncPG 异步 PostgreSQL 驱动
- 添加 Sentence-Transformers 文本向量化
- 补充完整的最佳实践指南（数据库、缓存、向量检索、异步）
- 提供代码示例：FastAPI Cache2、Qdrant 集成、异步 ORM、Celery 任务

### 2026-01-18 v1.2.0
- **后端升级**：NestJS (Node.js) → Python FastAPI + LangChain
- 引入 LangChain 完整的大模型应用框架
- 替换 ORM：Prisma → SQLAlchemy 2.x
- 添加 Pydantic 数据验证（自动生成 JSON Schema）
- 集成 Celery 异步任务队列
- 支持向量数据库（Pinecone、Weaviate）
- 添加 Poetry 包管理工具
- 集成 Pytest 单元测试
- 更新后端目录结构和命名规范
- 补充完整的 Python 初始化命令

### 2026-01-18 v1.1.0
- **前端升级**：React → Vue 3 + Vite
- 引入 Pinia 状态管理（替代 Zustand）
- 添加 Vue Router 路由管理
- 集成 unplugin 自动导入系统
- 添加 Playwright E2E 测试
- 更新前端目录结构和命名规范
- 补充完整的初始化命令

### 2026-01-18 v1.0.0
- 初始化项目技术标准
- 定义前后端技术栈
- 统一命名约定和 API 规范
