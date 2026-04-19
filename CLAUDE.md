# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目定位

**Claude Dev Team 是一个"会自己进化的 AI 开发团队"**。

核心产品是 `.claude/` 目录下的多代理协作 + 自进化系统。`main/` 下的 KET 后端和前端是**练习场**，用来让代理在真实项目上协作，从协作中采集真实数据反哺进化系统。

**不要把这个项目理解为 KET 考试应用**——那只是代理的"靶场"。真正的产品是：代理怎样协作、怎样从协作中学习、怎样把学到的东西沉淀到规则与策略权重里。

## 自进化系统架构

进化系统的核心原则：**只学习可验证的真实信号，不编造数据**。

```text
┌─────────────────────────────────────────────────────────────┐
│ 数据采集（真实信号）                                         │
│  SubagentStop → auto_evolver.py                             │
│     → 记录 agent 调用事实到 agent-invocations.jsonl         │
│  Stop → session_evolver.py                                  │
│     → 采集 git diff/log 的真实指标到 sessions.jsonl         │
├─────────────────────────────────────────────────────────────┤
│ 评分与更新                                                   │
│  Stop → strategy_updater.py                                 │
│     → 读 sessions.jsonl 最新记录                            │
│     → 基于真实 signals（生产力、测试比例、协作度、规模）打分 │
│     → EMA 更新 strategy_weights.json（alpha=0.3）           │
├─────────────────────────────────────────────────────────────┤
│ 知识沉淀                                                     │
│  rules/*.md                                                 │
│     → 人工编写的最佳实践和反模式                            │
│     → 统计数据由进化系统从真实数据累积，不手工编写           │
└─────────────────────────────────────────────────────────────┘
```

## 开发命令

### 后端（FastAPI + Python）

```bash
cd main/backend
pip install -r requirements.txt
cp .env.example .env                 # 务必修改 SECRET_KEY 和 ADMIN_PASSWORD
uvicorn main:app --reload            # http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 前端（Vue 3 + TypeScript）

```bash
cd main/frontend
npm install
npm run dev
npm run build
npm run lint
```

### 测试

```bash
# 后端单元测试
pytest main/tests/backend -v

# 前端测试
cd main/frontend && npm run test:run

# 集成测试
bash main/tests/run_tests.sh

# .claude/ 配置自检
python3 .claude/tests/verify_hook_references.py
python3 .claude/tests/verify_standards.py --verbose
```

### 查看进化数据

```bash
# 查看最近几次会话采集的真实指标
tail -5 .claude/logs/sessions.jsonl | python3 -m json.tool

# 查看当前策略权重
cat .claude/strategy_weights.json

# 查看本次会话中被调用过的 agent
grep "$(date +%Y-%m-%d)" .claude/logs/agent-invocations.jsonl
```

## 目录结构

| 路径 | 职责 |
|------|------|
| `.claude/agents/` | 10 个专业 AI 代理的定义 |
| `.claude/skills/` | 可复用技能（可跨 agent 使用） |
| `.claude/hooks/` | Claude Code 自动执行的钩子脚本 |
| `.claude/lib/` | **agent 按需调用的库代码**（不自动执行） |
| `.claude/rules/` | 分领域的最佳实践与反模式 |
| `.claude/tests/` | `.claude/` 自身的自检脚本 |
| `.claude/docs/` | 当前架构文档（历史文档归档在 `docs/history/`） |
| `.claude/logs/` | 进化系统采集的真实数据 |
| `main/backend/` | FastAPI 练习场（KET 考试系统） |
| `main/frontend/` | Vue 3 练习场 |
| `main/tests/` | **所有**测试文件的唯一位置 |

## 代理系统

10 个代理通过 `Task` 工具协同，根据关键词自动触发：

| 代理 | 职责 | 触发词 |
|------|------|--------|
| `product-manager` | 需求分析、PRD | 需求分析、PRD |
| `tech-lead` | 架构设计、API 契约 | 架构设计、技术选型 |
| `frontend-developer` | 前端实现 | 前端、UI、组件 |
| `backend-developer` | 后端实现 | 后端、API、数据库 |
| `test` | 测试规划与执行 | 测试 |
| `code-reviewer` | 代码审查 | 代码审查、PR |
| `orchestrator` | 多 agent 协调 | 协调、整个项目 |
| `evolver` | 进化规则维护 | 进化、学习 |
| `strategy-selector` | 任务分配策略 | 策略选择 |
| `self-play-trainer` | 多策略对比 | 自博弈 |

**硬性规则**：
- 永远用 `Task` 工具调用代理，不要自己实现代理逻辑
- 独立任务并行执行（多个 Task 调用放在同一条消息中）
- 多步骤任务使用 `TodoWrite` 跟踪
- 不要手工编写 `.claude/rules/*.md` 的统计数字——让进化系统累积

## Hooks（自动执行）

定义在 `.claude/settings.json`，每个事件都是**真实有效的**：

| 事件 | 脚本 | 作用 |
|------|------|------|
| `PreToolUse` (Write\|Edit) | `path_validator.py` | 拦截违规文件路径 |
| `PreToolUse` (Bash) | `safety-check.sh` | 拦截危险命令（rm -rf /、curl\|sh 等） |
| `PostToolUse` (Write\|Edit) | `quality-gate.sh` | JSON/Python 语法验证 |
| `UserPromptSubmit` | `context-enhancer.sh` | 注入项目状态上下文 |
| `SubagentStop` | `auto_evolver.py` | 记录 agent 调用事实 |
| `Stop` | `session_evolver.py` + `strategy_updater.py` | 采集真实数据并更新策略权重 |
| `SessionStart` | `setup_env.sh` | 配置环境变量 |

## 强制目录约束（由 path_validator.py 自动执行）

| 内容 | 必须位置 |
|------|---------|
| 所有测试文件 | `main/tests/` |
| API 路由 | `main/backend/api/routes/` |
| 业务逻辑 | `main/backend/services/` |
| 脚本 | `main/backend/scripts/` |
| 文档 | `main/docs/` |
| 前端组件 | `main/frontend/components/` |
| Claude 配置 | `.claude/` |

## 典型工作流

```text
用户需求 → strategy-selector 选择策略
       → product-manager 写 PRD
       → tech-lead 定义 API 契约
       → [frontend-developer] + [backend-developer] 并行实现
       → test 编写测试
       → code-reviewer 审查
       → (Stop hook 自动采集真实数据 → strategy_updater 更新权重)
       → evolver 基于多次执行结果更新 rules/*.md
```

## 关键配置文件

- `.claude/settings.json` — 权限规则 + hooks 注册（JSON，无注释）
- `.claude/settings-guide.md` — settings.json 的说明文档
- `.claude/strategy_weights.json` — 策略权重（由 strategy_updater 自动更新）
- `.claude/project_standards.md` — 技术标准（单一事实来源）

## 安全

- **生产部署前必须**：通过环境变量或 `.env` 文件覆盖 `SECRET_KEY` 和 `ADMIN_PASSWORD`
- `DEBUG` 默认 `False`，开发时显式设置 `DEBUG=true`
- 请求日志已启用（见 `main/backend/utils/middleware.py`）
