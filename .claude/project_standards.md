---
name: project-standards
description: 项目技术标准索引，定义项目的技术栈规范、代码规范和架构约定。此文件由 Evolver 自动维护更新。
---

# 项目技术标准

> ⚡ 项目技术规范的唯一事实来源。版本 2.2.0

---

## 📂 路径配置（单一事实来源）

| 变量 | 值 | 说明 |
|------|-----|------|
| `{PROJECT_ROOT}` | `main/` | 项目源码根目录 |
| `{BACKEND_ROOT}` | `main/backend/` | 后端代码根目录 |
| `{FRONTEND_ROOT}` | `main/frontend/` | 前端代码根目录 |
| `{TESTS_ROOT}` | `main/tests/` | 测试根目录（唯一允许的测试位置） |
| `{DOCS_ROOT}` | `main/docs/` | 文档根目录 |

### 后端目录

| 目录 | 路径 | 职责 |
|------|------|------|
| API 路由 | `main/backend/api/routes/` | FastAPI 路由 |
| 业务服务 | `main/backend/services/` | 核心业务逻辑 |
| 数据模型 | `main/backend/models/` | SQLAlchemy + Pydantic |
| 核心配置 | `main/backend/core/` | 配置、异常、安全 |
| 工具函数 | `main/backend/utils/` | 日志、验证、中间件 |
| 脚本文件 | `main/backend/scripts/` | 管理脚本 |
| 数据库文件 | `main/backend/db/` | SQLite 文件 |

### 前端目录

| 目录 | 路径 | 职责 |
|------|------|------|
| UI 组件 | `main/frontend/src/components/` | Vue 组件 |
| 页面 | `main/frontend/src/pages/` | 页面容器 |
| 状态管理 | `main/frontend/src/stores/` | Pinia |
| API 服务 | `main/frontend/src/services/` | HTTP 请求 |
| 路由 | `main/frontend/src/router/` | Vue Router |

---

## 🚨 目录结构强制约束

> 已配置 PreToolUse Hook 自动检查，违规操作将被阻止

### 禁止的路径

| ❌ 禁止 | ✅ 正确 |
|---------|---------|
| `tests/`（根目录） | `main/tests/` |
| `scripts/`（根目录） | `main/backend/scripts/` |
| `backend/`（根目录） | `main/backend/` |
| `frontend/`（根目录） | `main/frontend/` |
| `main/backend/docs/` | `main/docs/` |
| `main/frontend/docs/` | `main/docs/` |
| `main/backend/main/`（嵌套） | `main/` |

### 测试文件强制规则

所有测试文件（`test_*.py`, `*.test.ts`, `*.spec.js`）**必须且只能**放在 `main/tests/` 下：
- 后端测试 → `main/tests/backend/`
- 前端测试 → `main/tests/frontend/`
- 集成测试 → `main/tests/integration/`

---

## 命名约定

| 类型 | 规则 | 示例 |
|------|------|------|
| Python 文件 | snake_case | `user_service.py` |
| 类名 | PascalCase | `UserService` |
| 函数/变量 | snake_case | `get_user_data()` |
| 常量 | UPPER_SNAKE | `MAX_RETRY` |
| 路由文件 | `{resource}_router.py` | `user_router.py` |
| 服务文件 | `{resource}_service.py` | `user_service.py` |
| Vue 组件 | PascalCase.vue | `UserProfile.vue` |
| Pinia Store | `{camelCase}Store.ts` | `userStore.ts` |
| Composable | `use{PascalCase}.ts` | `useUserData.ts` |
| API 服务 | `{camelCase}Service.ts` | `userService.ts` |

---

## 技术栈

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.x | UI 框架 |
| TypeScript | 5.x | 类型安全 |
| Vite | 5.x | 构建工具 |
| Pinia | 2.x | 状态管理 |
| Vue Router | 4.x | 路由 |
| Axios | 1.x | HTTP 客户端 |
| Tailwind CSS | 3.x | CSS 框架 |
| Vitest | 1.x | 单元测试 |

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 编程语言 |
| FastAPI | 0.100+ | Web 框架 |
| SQLAlchemy | 2.x | ORM |
| Pydantic | 2.x | 数据验证 |
| SQLite/PostgreSQL | — | 数据库 |
| Redis | 7.x | 缓存 |
| Pytest | 7.x | 测试 |
| Ruff | 0.x | 代码质量 |

---

## API 规范

```
GET    /api/v1/{resources}        # 列表
GET    /api/v1/{resources}/:id    # 详情
POST   /api/v1/{resources}        # 创建
PATCH  /api/v1/{resources}/:id    # 更新
DELETE /api/v1/{resources}/:id    # 删除（软删除）
```

响应格式：`{ "code": 200, "message": "success", "data": {} }`

### HTTP 状态码

| 场景 | 状态码 | 异常类 |
|------|--------|--------|
| 成功 | 200/201 | — |
| 客户端错误 | 400 | `ValidationException` |
| 未授权 | 401 | `UnauthorizedException` |
| 禁止访问 | 403 | `ForbiddenException` |
| 资源不存在 | 404 | `NotFoundException` |
| 冲突 | 409 | `ConflictException` |
| 服务器错误 | 500 | `InternalException` |

> 异常类定义：`main/backend/core/exceptions.py`

---

## Git 提交规范

```
feat(scope): 新功能
fix(scope): 修复 Bug
docs(scope): 文档更新
style(scope): 代码格式
refactor(scope): 重构代码
test(scope): 添加测试
chore(scope): 工具/配置
```

---

## 代码注释规范

所有核心逻辑必须有中文注释，分三级：
- **必要注释**：函数/方法、类、复杂逻辑
- **重要注释**：业务逻辑、算法、配置
- **核心注释**：关键流程、边界情况

---

## 数据库策略

| 环境 | 数据库 |
|------|--------|
| 开发 | SQLite（`main/backend/db/ket_exam.db`） |
| 测试 | SQLite（`main/backend/db/test.db`） |
| 生产 | PostgreSQL |

---

## 进化机制

Evolver Agent 可根据任务执行结果提出更新建议，由人工确认后更新技术栈版本、最佳实践、错误处理规范。

**禁止自动更新**：路径配置、命名约定、API 规范（需人工审核）。

### 进化历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-01-23 | 2.2.0 | 新增三层防护体系最佳实践 |
| 2026-01-19 | 2.0.0 | 修复项目结构，移除多余 src/ 层级 |
| 2026-01-18 | 1.6.0 | 新增自动进化机制 |

> 详细代码模板、最佳实践和命令速查见 `.claude/docs/` 目录。
