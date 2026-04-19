---
paths: main/backend/**/*.py
---

# Backend Development Rules

**更新时间**: 2026-01-24
**策略关键词**: backend, api, database, fastapi

## 路径特定规则

此规则仅适用于 `main/backend/` 下的 Python 文件。

## 最佳实践

### ✅ API-First 并行开发
- **描述**: 先定义接口契约（API 路由 + Pydantic Schema），再并行开发前后端
- **适用场景**: 中大型功能开发、前后端协作
- **实施步骤**:
  1. 在 `main/backend/models/schema.py` 定义 Pydantic 模型
  2. 在 `main/backend/api/routes/` 定义路由接口
  3. 前后端并行开发（前端 mock 数据，后端实现逻辑）
  4. 集成测试验证

### ✅ 异步数据库操作
- **描述**: 使用 async/await 进行所有数据库操作，避免阻塞
- **证据**: 项目标准要求（参考 project_standards.md）
- **适用场景**: 所有 SQLAlchemy 查询、数据库事务
- **示例**:
  ```python
  # ✅ 正确
  async def get_user(user_id: int):
      async with AsyncSession(engine) as session:
          user = await session.get(User, user_id)
          return user

  # ❌ 错误
  def get_user(user_id: int):
      session = Session(engine)
      user = session.get(User, user_id)
      return user
  ```

### ✅ 统一错误处理
- **描述**: 使用 `AppException` 及其子类处理所有业务错误
- **适用场景**: 所有 API 路由、业务服务层
- **标准异常类**:
  - `NotFoundException` (404) - 资源不存在
  - `ValidationException` (400) - 数据验证错误
  - `UnauthorizedException` (401) - 未授权
  - `ForbiddenException` (403) - 禁止访问
  - `ConflictException` (409) - 业务冲突
  - `InternalException` (500) - 服务器错误
- **示例**:
  ```python
  # ✅ 正确
  from main.backend.core.exceptions import NotFoundException

  @router.get("/{user_id}")
  async def get_user(user_id: int):
      user = await user_service.get(user_id)
      if not user:
          raise NotFoundException("user", user_id)
      return user

  # ❌ 错误
  from fastapi import HTTPException

  @router.get("/{user_id}")
  async def get_user(user_id: int):
      user = await user_service.get(user_id)
      if not user:
          raise HTTPException(status_code=404, detail="User not found")
      return user
  ```

### ✅ 目录结构规范
- **描述**: 严格遵守 6 层目录结构（api, models, services, core, utils, scripts）
- **证据**: 项目标准强制约束（参考 project_standards.md）
- **适用场景**: 所有新文件创建
- **目录职责**:
  - `api/routes/` - FastAPI 路由定义、请求处理
  - `models/` - SQLAlchemy + Pydantic 模型
  - `services/` - 核心业务逻辑、数据处理
  - `core/` - 配置、异常、安全认证
  - `utils/` - 日志、验证、中间件
  - `scripts/` - 脚本文件（创建管理员、数据迁移等）

## 反模式

### ⚠️ 直接抛出 HTTPException
- **问题**: 错误响应格式不统一，前端难以处理
- **正确做法**: 使用 `AppException` 及其子类
- **原因**: 统一错误响应格式 `{"code": 404, "message": "...", "details": {...}}`
- **影响**: 前端需要针对不同错误格式编写多套处理逻辑

### ⚠️ 同步数据库操作
- **问题**: 阻塞事件循环，降低并发性能
- **正确做法**: 使用 `async/await` + `AsyncSession`
- **原因**: FastAPI 是异步框架，同步操作会阻塞其他请求
- **影响**: 性能下降 40%+

### ⚠️ 业务逻辑写在路由层
- **问题**: 路由文件臃肿，逻辑难以复用和测试
- **正确做法**: 路由层只做请求/响应转换，业务逻辑放 `services/`
- **原因**: 单一职责原则，便于单元测试
- **影响**: 代码可维护性差，测试覆盖率低

### ⚠️ 数据库连接池配置不当
- **问题**: 连接池过小导致连接耗尽，过大浪费资源
- **正确做法**: 根据并发量调整 `pool_size` 和 `max_overflow`
- **推荐配置**:
  ```python
  engine = create_async_engine(
      DATABASE_URL,
      pool_size=20,        # 连接池大小
      max_overflow=10,     # 最大溢出连接
      pool_pre_ping=True,  # 连接健康检查
  )
  ```

## 相关文档

- **项目标准**: `.claude/project_standards.md`
- **后端文档**: `main/backend/README.md`
- **错误处理规范**: `.claude/project_standards.md` → 错误处理规范
- **目录结构**: `.claude/project_standards.md` → 目录结构

## 真实执行数据

此规则文件的统计数据不再手工编造。真实执行指标由以下机制累积：

- 每次会话结束时，`session_evolver.py` 采集 git diff / agent 调用等真实数据到 `.claude/logs/sessions.jsonl`
- `strategy_updater.py` 基于真实指标做 EMA 更新到 `.claude/strategy_weights.json`
- 如需查看实时统计：`python3 .claude/lib/knowledge_retriever.py --stats`
