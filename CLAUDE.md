# CLAUDE.md - Claude Dev Team 项目指南

> 💡 通用 Claude Code 规范见 @.claude/docs/claude-code-reference.md

## 项目概述

Claude Dev Team 是基于 Claude Code 原生能力构建的 AI 开发团队协作系统。通过 8 个专业 AI 代理和 6 个可复用技能，模拟真实软件开发团队的角色分工和协作流程，并配备自进化引擎从执行结果中持续学习。

**核心特性**：
- 🤖 10 个专业代理（8 个基础 + 2 个 AlphaZero）
- 🎯 6 个可复用技能（requirement-analysis, architecture-design, api-design, testing, code-quality, task-distribution）
- 🧠 自进化引擎（从执行结果中学习并更新配置）
- ⚡ 并行执行支持（background_task 实现多代理同时工作）
- 🎯 AlphaZero 自博弈学习系统（strategy-selector + self-play-trainer）

## 快速开始

### 示例项目

`main/examples/todo_app/` 目录包含完整的全栈示例：

```bash
cd main/examples/todo_app
npm install              # 安装依赖
npm run init-db          # 初始化数据库
npm start                # 启动服务器 (http://localhost:3000)
npm test                 # 运行所有测试
npm run test:backend     # 仅运行后端测试
npm run test:frontend    # 仅运行前端测试
```

### 常用代理调用

Claude 会根据关键词自动选择合适的代理：

```
"需求分析" / "PRD"           → product-manager
"架构设计" / "技术选型"       → tech-lead
"前端" / "UI" / "组件"       → frontend-developer
"后端" / "API" / "数据库"    → backend-developer
"测试"                      → test
"代码审查" / "PR 审查"       → code-reviewer
"协调" / "整个项目"          → orchestrator
"进化" / "学习" / "改进"     → evolver
"进度" / "状态"             → progress-viewer
"策略选择" / "策略配置"      → strategy-selector
"自博弈" / "多策略对比"      → self-play-trainer
```

### 健康检查

```bash
python3 .claude/hooks/scripts/verify_standards.py --verbose
```

## 架构设计

### Agent 系统 (.claude/agents/)

10 个专业代理通过 Task 工具协同工作：

| 代理 | 功能 | 触发词 |
|------|------|--------|
| **strategy-selector** | AlphaZero 策略选择 | 策略选择、智能分配 |
| **self-play-trainer** | AlphaZero 自博弈训练 | 自博弈、多策略对比 |
| **orchestrator** | 主协调器 | 协调、管理流程 |
| **product-manager** | 需求分析 | 需求分析、PRD |
| **tech-lead** | 架构设计 | 架构设计、技术选型 |
| **frontend-developer** | 前端开发 | 前端、UI、组件 |
| **backend-developer** | 后端开发 | 后端、API、数据库 |
| **test** | 测试工程师 | 测试、测试计划 |
| **code-reviewer** | 代码审查 | 代码审查、PR 审查 |
| **evolver** | 自进化引擎 | 进化、学习、改进 |
| **progress-viewer** | 进度查询 | 进度、状态 |

### Skills 系统 (.claude/skills/)

6 个可复用技能通过 Skill 工具调用：

- `requirement-analysis` - 需求分析和 PRD 生成
- `architecture-design` - 系统架构设计
- `api-design` - RESTful API 设计
- `testing` - 测试规划和执行
- `code-quality` - 代码质量审查
- `task-distribution` - 任务拆分和分配

### AlphaZero 自博弈学习系统

借鉴 AlphaZero 的自博弈学习思想，使用 Claude Code 原生能力实现：

| AlphaZero 概念 | Claude Code 实现 |
|----------------|------------------|
| 自我对弈生成数据 | 多策略变体并行执行 (background_task) |
| MCTS 搜索最优走法 | strategy-selector 选择最优策略 |
| 策略网络 | strategy-selector Agent |
| 价值网络 | reward_evaluator Hook |
| 迭代训练 | Evolver 持续提炼 + strategy_learner Hook |

## 开发工作流

### 完整功能开发流程

```
用户需求
    ↓
strategy-selector (选择最优策略)
    ↓
self-play-trainer (生成并评估变体)
    ↓
product-manager (PRD)
    ↓
tech-lead (架构设计)
    ↓
并行开发 (前端 + 后端通过 background_task())
    ↓
test (测试)
    ↓
code-reviewer (审查)
    ↓
reward_evaluator (计算奖励)
    ↓
strategy_learner (更新策略规则)
    ↓
evolver (提炼到全局知识库)
```

## 项目配置

### 权限配置 (.claude/settings.json)

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Read(*)",
      "Write(main/docs/**)",
      "Write(main/backend/**)",
      "Write(main/frontend/**)",
      "Write(main/tests/**)",
      "Write(main/examples/**)",
      "Edit(*)",
      "Grep(*)",
      "Glob(*)",
      "Skill(*)",
      "Task(*)",
      "TodoWrite"
    ],
    "ask": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(rm:*)",
      "Bash(docker:*)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Read(.git/**)",
      "Write(.git/**)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Write(**/.env)",
      "Write(**/.env.*)"
    ],
    "defaultMode": "acceptEdits"
  },
  "model": "sonnet"
}
```

## 🚨 强制目录结构约束（必须遵守！）

### 禁止行为（违反将导致任务失败）

| ❌ 禁止 | ✅ 正确做法 |
|--------|------------|
| 在根目录创建 `tests/` | 放 `main/tests/` |
| 在任何非 `main/tests/` 位置创建测试文件 | **所有测试必须放 `main/tests/`** |
| 在根目录创建 `scripts/` | 放 `main/backend/scripts/` |
| 在根目录创建 `src/` | 放 `main/backend/` 或 `main/frontend/` |
| 在根目录创建 `backend/` 或 `frontend/` | 放 `main/` 子目录下 |
| 随机创建目录 | 参考项目结构，在合适位置创建 |
| 在后端根目录放脚本文件 | 放 `main/backend/scripts/` |

### ⚠️ 测试文件强制约束（已配置 Hook 自动检查）

**规则**：所有测试文件（`test_*.py`, `*.test.ts`, `*.spec.js` 等）**必须且只能**放在 `main/tests/` 目录下。

**测试目录结构**：
```
main/tests/                # 唯一允许的测试目录
├── backend/              # 后端测试
│   ├── test_auth.py
│   ├── test_api.py
│   └── test_services.py
├── frontend/             # 前端测试
│   ├── components.test.ts
│   └── services.spec.ts
├── integration/          # 集成测试
│   └── test_e2e.py
└── conftest.py           # Pytest 配置
```

**自动检查**：
- PreToolUse Hook 会自动验证所有文件路径
- 如果尝试在错误位置创建测试文件，操作会被阻止
- 错误示例：`backend/test_api.py` ❌
- 正确示例：`main/tests/backend/test_api.py` ✅

### 后端目录结构（main/backend/）

```
main/backend/               # 后端代码根目录
├── api/                   # API 路由层（必须）
│   └── routes/            # 路由文件（必须）
│       ├── auth_router.py
│       ├── question_router.py
│       ├── answer_router.py
│       ├── progress_router.py
│       ├── admin_router.py
│       ├── speed_quiz_router.py
│       └── monitor_router.py    # AlphaZero 监控
├── core/                  # 核心配置（必须）
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库连接
│   ├── security.py        # 安全认证
│   └── exceptions.py      # 异常定义
├── models/                # 数据模型层（必须）
│   ├── db.py              # SQLAlchemy 模型
│   └── schema.py          # Pydantic 模型
├── services/              # 业务逻辑层（必须）
│   ├── auth_service.py
│   ├── question_service.py
│   ├── progress_service.py
│   └── ...
├── tasks/                 # 定时任务（可选）
│   └── ai_digest/         # AI 日报任务
│       ├── router.py
│       ├── service.py
│       ├── models.py
│       └── schemas.py
├── scripts/               # 脚本文件（必须）
│   ├── create_admin.py    # 创建管理员
│   └── alphazero-status.py # AlphaZero 监控脚本
├── migrations/            # 数据库迁移（可选）
│   ├── add_speed_quiz_tables.py
│   └── add_ai_digest_table.py
├── main.py                # 应用入口（根目录）
└── requirements.txt       # 依赖文件（根目录）
```

### 目录归属规则（必须遵守）

| 内容类型 | 必须放在 | 禁止放在 |
|----------|----------|----------|
| **API 路由** | `main/backend/api/routes/` | 根目录 |
| **业务逻辑** | `main/backend/services/` | 根目录 |
| **数据模型** | `main/backend/models/` | 根目录 |
| **核心配置** | `main/backend/core/` | 根目录 |
| **定时任务** | `main/backend/tasks/` | 根目录 |
| **脚本文件** | `main/backend/scripts/` | 根目录 |
| **数据库迁移** | `main/backend/migrations/` | 根目录 |
| **应用入口** | `main/backend/main.py` | 其他位置 |
| **测试文件** | `main/tests/` | **任何其他位置（强制约束）** |

### 前端目录结构（main/frontend/）

```
main/frontend/
├── src/
│   ├── components/        # 组件
│   ├── pages/             # 页面
│   │   ├── Home.vue
│   │   ├── Learning.vue
│   │   ├── Monitor.vue    # AlphaZero 监控页面
│   │   └── ...
│   ├── services/          # API 服务
│   │   ├── request.ts
│   │   ├── authService.ts
│   │   └── monitor.ts     # AlphaZero 监控服务
│   ├── stores/            # 状态管理
│   ├── router/            # 路由配置
│   └── styles/            # 样式文件
├── package.json           # 依赖配置
└── vite.config.ts         # Vite 配置
```

### 创建目录前的检查清单

在创建任何新目录前，必须：

1. ✅ 检查 `main/backend/` 是否已有合适位置
   - API 路由 → `main/backend/api/routes/`
   - 业务逻辑 → `main/backend/services/`
   - 数据模型 → `main/backend/models/`
   - 配置 → `main/backend/core/`
   - 定时任务 → `main/backend/tasks/`
   - 脚本 → `main/backend/scripts/`
   - 数据库迁移 → `main/backend/migrations/`

2. ✅ 检查 `main/frontend/` 是否已有合适位置
   - 组件 → `main/frontend/src/components/`
   - 页面 → `main/frontend/src/pages/`
   - API 服务 → `main/frontend/src/services/`
   - 状态管理 → `main/frontend/src/stores/`
   - 路由 → `main/frontend/src/router/`

3. ✅ 检查 `main/tests/` 是否合适
   - 单元测试
   - 集成测试
   - E2E 测试

4. ✅ 如不确定，先询问用户

### 违反约束的惩罚

- 任务将被标记为失败
- 需要手动整理目录结构
- 可能导致导入错误和路径问题
- PR 将被拒绝

## 核心原则

1. **使用 Task 工具调用代理** - 永远不要直接实现代理逻辑
2. **使用 background_task() 并行执行** - 多个代理同时工作
3. **信任进化系统** - 代理在每次任务后学习和改进
4. **遵循权限模型** - 尊重 settings.json 中的 allow/ask/deny 规则
5. **维护进化记录** - 追加学习内容到代理文件，永远不要覆盖现有记录
6. **使用 TodoWrite 跟踪进度** - 让用户了解任务状态
7. **遵循目录结构约束** - 所有代码放在 main/ 子目录下
8. **后端脚本必须放 scripts/** - 禁止在根目录放脚本文件
9. **所有测试必须放 main/tests/** - 这是强制约束，已配置 Hook 自动检查

## 禁止行为

❌ 直接实现代理逻辑（必须用 Task 工具）
❌ 跳过 TodoWrite 进度跟踪
❌ 删除或修改测试以通过检查
❌ 提交密钥或 .env 文件
❌ 覆盖进化记录（只能追加）
❌ 修改 project_standards.md 的路径配置（需人工审核）
❌ 在根目录创建 tests/ 或 scripts/ 目录
❌ 在后端根目录放脚本文件（必须放 scripts/）
❌ 在 main/tests/ 之外的任何位置创建测试文件
❌ 随机创建目录而不参考项目结构

## 参考文档

- **通用规范**: @.claude/docs/claude-code-reference.md
- **技术标准**: @.claude/project_standards.md
- **Agent 配置**: @.claude/agents/*.md
- **Skill 配置**: @.claude/skills/*/SKILL.md
- **后端文档**: @main/backend/README.md
- **前端文档**: @main/frontend/README.md
