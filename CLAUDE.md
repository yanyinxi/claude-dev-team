# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Claude Dev Team 是基于 Claude Code 原生能力构建的 AI 开发团队协作系统。核心特性：10 个专业 AI 代理、6 个可复用技能、自进化引擎、AlphaZero 自博弈学习系统。

## 开发命令

### 后端（FastAPI + Python）

```bash
cd main/backend
pip install -r requirements.txt     # 安装依赖
uvicorn main:app --reload           # 启动开发服务器 (http://localhost:8000)
python main.py                      # 直接运行
# API 文档: http://localhost:8000/docs
```

### 前端（Vue 3 + TypeScript）

```bash
cd main/frontend
npm install                         # 安装依赖
npm run dev                         # 启动开发服务器
npm run build                       # 构建生产版本
npm run lint                        # ESLint 检查
npm run format                      # Prettier 格式化
```

### 测试

```bash
# 后端测试
cd main/backend && python -m pytest main/tests/backend/ -v
python -m pytest main/tests/backend/test_auth.py -v   # 单个文件

# 前端测试
cd main/frontend && npm test        # 监听模式
npm run test:run                    # 单次运行
npm run test:ui                     # 可视化界面

# 集成测试
bash main/tests/run_tests.sh

# 健康检查
python3 .claude/tests/verify_standards.py --verbose
```

### 示例项目（Todo App）

```bash
cd main/examples/todo_app
npm install && npm run init-db && npm start  # http://localhost:3000
```

## 架构概述

### 代理系统（.claude/agents/）

10 个专业代理通过 `Task` 工具协同，根据关键词自动触发：

| 代理 | 触发词 |
|------|--------|
| `product-manager` | 需求分析、PRD |
| `tech-lead` | 架构设计、技术选型 |
| `frontend-developer` | 前端、UI、组件 |
| `backend-developer` | 后端、API、数据库 |
| `test` | 测试、测试计划 |
| `code-reviewer` | 代码审查、PR 审查 |
| `orchestrator` | 协调、整个项目 |
| `evolver` | 进化、学习、改进 |
| `strategy-selector` | 策略选择、智能分配 |
| `self-play-trainer` | 自博弈、多策略对比 |

**重要**：永远使用 `Task` 工具调用代理，不要直接实现代理逻辑。

### Hooks 自动执行（.claude/settings.json）

- **PreToolUse**：`path_validator.py` 验证文件路径合规性；`safety-check.sh` 拦截危险命令
- **PostToolUse**：`quality-gate.sh` 在写/编辑操作后检查质量
- **SubagentStop**：`auto_evolver.py` 从代理执行结果中学习并更新规则
- **Stop**：`strategy_updater.py` 更新策略权重

### 技术栈

- **后端**：Python FastAPI + SQLAlchemy（异步）+ SQLite + JWT 认证
- **前端**：Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS
- **测试**：pytest（后端）+ Vitest（前端）

## 强制目录结构约束

**已配置 Hook 自动拦截违规操作**：

| 内容类型 | 必须放在 | 禁止放在 |
|----------|----------|----------|
| 所有测试文件 | `main/tests/` | 任何其他位置 |
| API 路由 | `main/backend/api/routes/` | 根目录 |
| 业务逻辑 | `main/backend/services/` | 根目录 |
| 脚本文件 | `main/backend/scripts/` | 后端根目录 |
| 文档 | `main/docs/` | `main/backend/docs/` 等 |
| 前端组件 | `main/frontend/src/components/` | 其他位置 |

## 开发工作流

### 完整功能开发流程

```
用户需求 → strategy-selector → product-manager (PRD) → tech-lead (API 契约)
    → 并行开发 [frontend-developer + backend-developer] (使用 background_task())
    → test → code-reviewer → evolver (学习并更新规则)
```

### 关键原则

- **并行执行**：独立任务用 `background_task()` 并行运行，不要串行
- **API 契约先行**：前后端并行开发前必须先由 tech-lead 定义 API 契约
- **进度跟踪**：多步骤任务使用 `TodoWrite` 跟踪状态
- **维护进化记录**：只追加到代理文件，不覆盖现有记录

## 配置文件

- **权限配置**：`.claude/settings.json`（allow/ask/deny 规则）
- **技术标准**：`.claude/project_standards.md`（单一事实来源）
- **规则文件**：`.claude/rules/`（collaboration.md, general.md, system-design.md）
- **策略权重**：`.claude/strategy_weights.json`（AlphaZero 学习结果）
