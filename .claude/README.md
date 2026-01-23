# Claude Code AI 开发团队协作系统

## 项目简介

这是一个基于 Claude Code 构建的 AI 开发团队协作系统，模拟真实软件开发团队的角色分工和协作流程。

## 核心特性

- ✅ 10 个专业 AI 代理角色（包括自进化引擎 + AlphaZero 自博弈系统）
- ✅ 6 个可复用技能包
- ✅ Claude Code 原生能力集成
- ✅ 动态任务分配
- ✅ 自进化系统（从经验中学习）
- ✅ **AlphaZero 风格自博弈学习**（策略选择 + 多变体评估 + 持续优化）
- ✅ 质量关卡控制

## 目录结构

```
.claude/
├── agents/              # 10个代理配置（符合官方文档标准）
│   ├── backend-developer.md
│   ├── code-reviewer.md
│   ├── evolver.md              # 自进化引擎
│   ├── frontend-developer.md
│   ├── orchestrator.md
│   ├── product-manager.md
│   ├── tech-lead.md
│   ├── test.md
│   ├── strategy-selector.md    # ⭐ 新增：策略选择器（AlphaZero）
│   └── self-play-trainer.md    # ⭐ 新增：自博弈训练器（AlphaZero）
├── skills/              # 6个技能
│   ├── api_design/
│   ├── architecture_design/
│   ├── code_quality/
│   ├── requirement_analysis/
│   ├── task_distribution/
│   └── testing/
├── hooks/               # Hook 脚本
│   ├── scripts/         # 质量门禁等脚本
│   ├── reward_evaluator.py      # ⭐ 新增：奖励评估器
│   └── strategy_learner.py       # ⭐ 新增：策略学习器
├── rules/               # ⭐ 新增：策略规则（学习成果）
│   ├── frontend.md
│   ├── backend.md
│   ├── collaboration.md
│   └── system-design.md      # ⭐ 新增：系统设计最佳实践
└── settings.json        # 配置文件（含 Hook 配置）
```

## 快速开始

直接开始使用，无需额外配置。

## 使用方法

### 自动委托（推荐）

直接描述你的需求，Claude 会自动选择合适的代理：

```
实现用户登录功能
→ Claude 自动调用 strategy-selector → 选择最优策略 → 自动分配 Agent

请分析这个需求并创建 PRD
→ Claude 自动调用 product-manager

审查代码安全问题
→ Claude 自动调用 code-reviewer
```

### 手动调用

使用 `/agents` 命令查看和调用：

```
/agents
```

### 直接指定

在对话中直接指定代理：

```
使用 backend-developer 代理实现用户认证 API
使用 frontend-developer 代理实现登录页面
使用 strategy-selector 优化任务分配策略
```

## 代理列表

| 代理 | 功能 | 使用场景 | 触发词 |
|------|------|---------|--------|
| **strategy-selector** | ⭐ 策略选择器 | 智能选择最优 Agent 分配策略 | 策略选择、智能分配、Agent 配置 |
| **self-play-trainer** | ⭐ 自博弈训练器 | 多策略对比，选择最优方案 | 自博弈、多策略对比、学习优化 |
| **evolver** | 自进化引擎 | 从执行结果中学习并更新系统配置 | 进化、更新、学习、改进 |
| **orchestrator** | 主协调器 | 协调整个开发流程，管理任务分配 | 协调、管理项目、整个流程 |
| **product-manager** | 产品经理 | 需求分析、PRD 生成、任务拆分 | 需求分析、PRD、产品需求 |
| **tech-lead** | 技术负责人 | 架构设计、技术选型、API 设计 | 架构设计、API 设计、技术选型 |
| **frontend-developer** | 前端开发 | React/Vue 组件、前端测试 | 前端、UI、组件、前端开发 |
| **backend-developer** | 后端开发 | API 实现、数据库操作、业务逻辑 | 后端、API、数据库、后端开发 |
| **test** | 测试工程师 | 测试计划、自动化测试、测试报告 | 测试、自动化测试、测试计划 |
| **code-reviewer** | 代码审查 | 代码质量、安全性、最佳实践审查 | 代码审查、PR 审查、代码质量 |

## 技能列表

| 技能 | 功能 |
|------|------|
| `requirement-analysis` | 需求分析、PRD 生成 |
| `architecture-design` | 系统架构设计 |
| `api-design` | RESTful API 设计 |
| `testing` | 测试规划和执行 |
| `code-quality` | 代码质量审查 |
| `task-distribution` | 任务拆分和分配 |

## AlphaZero 自博弈学习系统 ⭐

### 核心概念

借鉴 AlphaZero 的自博弈学习思想，但使用 Claude Code 原生能力实现：

| AlphaZero 概念 | Claude Code 实现 |
|----------------|------------------|
| 自我对弈生成数据 | 多策略变体并行执行 (background_task) |
| MCTS 搜索最优走法 | strategy-selector 选择最优策略 |
| 策略网络 | strategy-selector Agent |
| 价值网络 | reward_evaluator Hook |
| 迭代训练 | Evolver 持续提炼 + strategy_learner Hook |

### 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    AlphaZero-Style 学习系统                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  用户任务执行                                                    │
│      ↓                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  1. PostToolUse Hook: reward_evaluator.py               │   │
│  │     - 计算奖励分数 (0-10分)                              │   │
│  │     - 写入 experience_pool.json                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│      ↓                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  2. SubagentStop Hook: strategy_learner.py              │   │
│  │     - 分析策略效果                                       │   │
│  │     - 去重检查 (24小时内相同策略不重复)                  │   │
│  │     - 经验聚合 (多条相似经验合并)                        │   │
│  │     - 实时写入 .claude/rules/*.md                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│      ↓                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  3. Evolver (自动触发)                                   │   │
│  │     - 读取 .claude/rules/*.md                           │   │
│  │     - 提炼到 Agent/Skill/Standards                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│      ↓                                                          │
│  下次任务使用更新后的策略                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 优化机制

#### 1. 去重检查
相同策略在 24 小时内不重复更新，避免刷屏。

#### 2. 经验聚合
多条相似经验合并为一条，提高学习效率：
- 连续 2 次以上相同策略 → 合并为聚合经验
- 计算平均奖励分数
- 合并描述信息

### 使用示例

#### 示例 1：自动策略选择

```
用户：实现一个完整的电商系统

Claude：
→ strategy-selector 分析任务复杂度（8/10）
→ 选择"后端优先"策略 (backend×3, frontend×2)
→ 自动分配 Agent 并行开发
→ reward_evaluator 计算每次执行奖励
→ strategy_learner 写入 .claude/rules/
→ Evolver 提炼到 Agent 配置
```

#### 示例 2：自博弈训练

```
用户：使用 self-play-trainer 优化用户认证功能的分配策略

Claude：
→ self-play-trainer 生成 3 个变体
→ 并行执行，收集结果
→ 选择最佳变体（变体 1：8.5分）
→ 学到的最佳实践写入 .claude/rules/
```

## Hooks 系统

系统使用 Claude Code 原生 Hook 机制实现自动化：

| 事件 | 触发条件 | 执行脚本 | 作用 |
|------|---------|----------|------|
| **PostToolUse (Task)** | Task 工具调用后 | `reward_evaluator.py` | 计算奖励，积累经验 |
| **PostToolUse (Write\|Edit)** | 文件编辑后 | `quality-gate.sh` | 质量门禁检查 |
| **SubagentStop** | 子代理停止时 | `strategy_learner.py` | 分析策略，更新规则 |
| **PreToolUse (Bash)** | Bash 命令前 | `safety-check.sh` | 安全检查 |
| **UserPromptSubmit** | 用户提交消息时 | `context-enhancer.sh` | 上下文增强 |
| **Stop** | 任务结束时 | 提示信息 | 进化提醒 |

## 使用示例

### 示例 1：实现新功能

```
用户：实现一个待办事项功能

Claude：
→ strategy-selector 分析任务，选择策略
→ self-play-trainer 生成变体，选择最优
→ orchestrator 协调整个流程
→ product-manager 分析需求并创建 PRD
→ tech-lead 设计技术方案
→ frontend-developer 实现前端
→ backend-developer 实现后端 API
→ test 创建测试
→ code-reviewer 审查代码
→ reward_evaluator 计算奖励
→ strategy_learner 更新策略规则
→ evolver 提炼到全局知识库
```

### 示例 2：优化策略

```
用户：使用 self-play-trainer 优化用户登录功能的分配策略

Claude：
→ self-play-trainer 启动
→ 生成 3 个策略变体
→ 并行执行，对比评估
→ 选择最佳变体（得分 8.5/10）
→ 学到的经验写入 .claude/rules/collaboration.md
```

## 代理配置说明

所有代理配置文件符合 Claude Code 官方文档标准：

```yaml
---
name: agent-name
description: |
  代理描述
  使用场景：
  - 场景1
  - 场景2
  触发词：关键词1、关键词2
tools:
  - TodoWrite
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
skills:
  - skill-name
model: inherit
permissionMode: acceptEdits  # 或 default
---
```

### 配置字段说明

| 字段 | 说明 |
|------|------|
| `name` | 代理名称（小写字母和连字符） |
| `description` | 描述使用场景和触发词 |
| `tools` | 允许使用的工具列表 |
| `skills` | 代理可用的技能 |
| `model` | 使用 `inherit` 继承主对话模型 |
| `permissionMode` | `acceptEdits` 自动接受编辑，`default` 需要确认 |

## 工作流程

### 完整功能开发流程（含 AlphaZero 学习）

```
1. 用户提出需求
   ↓
2. strategy-selector 分析任务，选择最优策略
   ↓
3. self-play-trainer 生成变体，选择最佳方案
   ↓
4. product-manager 分析需求，创建 PRD
   ↓
5. tech-lead 设计技术方案
   ↓
6. 动态分配任务（frontend + backend）
   ↓
7. **并行开发**（前端 + 后端，使用 background_task()）
   ↓
8. test 创建测试
   ↓
9. code-reviewer 审查代码
   ↓
10. orchestrator 做最终决策
   ↓
11. **reward_evaluator** 计算奖励分数
   ↓
12. **strategy_learner** 更新 .claude/rules/
   ↓
13. **evolver** 提炼到全局知识库
   ↓
14. 系统学习和改进（越用越聪明）
```

## 自进化系统

### 工作原理

每次任务执行完成后，系统会自动进行学习和优化：

```
用户需求
    ↓
Agent 执行任务
    ↓
reward_evaluator 计算奖励 (PostToolUse)
    ↓
strategy_learner 更新策略规则 (SubagentStop)
    ↓
evolver 提炼到全局知识库
    ↓
下次任务使用更新后的配置
```

### 进化层次

| 层次 | 数据源 | 输出 |
|------|--------|------|
| 1 | experience_pool.json | 原始经验积累 |
| 2 | .claude/rules/*.md | 策略规则沉淀 |
| 3 | Agent 文件 | 最佳实践固化 |
| 4 | project_standards.md | 全局标准更新 |

### 查看学习成果

```bash
# 查看策略规则
cat .claude/rules/frontend.md
cat .claude/rules/backend.md
cat .claude/rules/collaboration.md

# 查看经验池
cat .claude/experience_pool.json | jq

# 查看 Agent 进化记录
grep -A 10 "进化记录" .claude/agents/frontend-developer.md
```

## 最佳实践

1. **清晰描述需求**：提供足够的上下文和约束
2. **使用触发词**：在描述中包含代理描述中的关键词
3. **指定代理**：复杂任务可以直接指定代理
4. **利用协调器**：跨多个领域的任务使用 orchestrator
5. **信任学习系统**：任务越多，系统越聪明
6. **定期查看进化记录**：了解系统学习到的最佳实践

## 并行任务执行

系统支持使用 `background_task()` 并行执行多个代理任务，显著提升开发效率。

### 并行开发流程

```
前端开发 + 后端开发（同时进行）
```

使用 `background_task()` 并行调用两个代理：

```python
# 并行启动前端和后端开发
frontend_task = background_task(
    agent="frontend-developer",
    prompt="请实现前端代码..."
)

backend_task = background_task(
    agent="backend-developer", 
    prompt="请实现后端代码..."
)

# 等待两者完成（并行执行）
frontend_result = background_output(task_id=frontend_task)
backend_result = background_output(task_id=backend_task)
```

**优势**：
- 前端和后端同时开发
- 节省约 40% 总开发时间
- 适合独立模块的并行开发

## 常见问题

### Q: AlphaZero 系统如何让系统变聪明？

每次任务执行后：
1. reward_evaluator 计算奖励分数
2. strategy_learner 记录有效的策略
3. evolver 将经验提炼到 Agent 配置

任务越多，积累的经验越丰富，策略选择越精准。

### Q: 去重机制是什么？

相同策略在 24 小时内不会重复更新，避免刷屏。但不同策略仍会正常记录。

### Q: 可以查看学习到的策略吗？

是的，策略保存在 `.claude/rules/` 目录下：
- `frontend.md` - 前端开发策略
- `backend.md` - 后端开发策略
- `collaboration.md` - 协作策略

### Q: 如何验证系统正常工作？

```bash
# 检查文件完整性
ls -la .claude/agents/strategy-selector.md
ls -la .claude/agents/self-play-trainer.md
ls -la .claude/hooks/reward_evaluator.py
ls -la .claude/hooks/strategy_learner.py
ls -la .claude/rules/

# 查看经验池
cat .claude/experience_pool.json
```

## 相关文档

- [Claude Code Skills 文档](https://code.claude.com/docs/zh-CN/skills)
- [Claude Code Sub-agents 文档](https://code.claude.com/docs/zh-CN/sub-agents)

## 许可证

MIT License
