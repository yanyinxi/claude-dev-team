# CLAUDE.md - Claude Dev Team 项目指南

> 💡 通用 Claude Code 规范见 @.claude/docs/claude-code-reference.md

## 项目概述

Claude Dev Team 是基于 Claude Code 原生能力构建的 AI 开发团队协作系统。通过 8 个专业 AI 代理和 6 个可复用技能，模拟真实软件开发团队的角色分工和协作流程，并配备自进化引擎从执行结果中持续学习。

**核心特性**：
- 🤖 8 个专业代理（orchestrator, product-manager, tech-lead, frontend/backend-developer, test, code-reviewer, evolver, progress-viewer）
- 🎯 6 个可复用技能（requirement-analysis, architecture-design, api-design, testing, code-quality, task-distribution）
- 🧠 自进化引擎（从执行结果中学习并更新配置）
- ⚡ 并行执行支持（background_task 实现多代理同时工作）

## 快速开始

### 示例项目

`examples/todo_app/` 目录包含完整的全栈示例：

```bash
cd examples/todo_app
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
```

### 健康检查

```bash
python3 .claude/scripts/verify_standards.py --verbose
```

## 架构设计

### Agent 系统 (.claude/agents/)

8 个专业代理通过 Task 工具协同工作：

#### orchestrator - 主协调器
- 管理完整开发生命周期
- 支持动态任务分配
- 通过 `background_task()` 实现并行执行
- 触发词：协调、管理流程、整个项目

#### product-manager - 需求分析
- 分析用户需求
- 生成 PRD 文档（保存到 `main/docs/prd/`）
- 拆分任务并评估优先级
- 触发词：需求分析、PRD、产品需求

#### tech-lead - 架构设计
- 系统架构设计
- 技术选型（参考 project_standards.md）
- API 规范制定
- 触发词：技术架构、API 设计、技术选型

#### frontend-developer - 前端开发
- React/Vue 组件实现
- 前端测试
- UI/UX 优化
- 触发词：前端、UI、组件

#### backend-developer - 后端开发
- API 端点实现
- 数据库操作
- 业务逻辑
- 触发词：后端、API、数据库

#### test - 测试工程师
- 测试计划
- 自动化测试（单元、集成、E2E）
- 测试报告
- 触发词：测试、测试计划

#### code-reviewer - 代码审查
- 代码质量审查
- 安全性检查
- 最佳实践验证
- 触发词：代码审查、PR 审查

#### evolver - 自进化引擎
- 分析执行结果
- 更新代理和 Skill 配置
- 记录进化历史
- 触发词：进化、更新、学习、改进

#### progress-viewer - 进度查询
- 任务进度跟踪
- 状态报告
- 触发词：进度、状态、查询

### Skills 系统 (.claude/skills/)

6 个可复用技能通过 Skill 工具调用：

- **requirement-analysis** - 需求分析和 PRD 生成
- **architecture-design** - 系统架构设计
- **api-design** - RESTful API 设计
- **testing** - 测试规划和执行
- **code-quality** - 代码质量审查
- **task-distribution** - 任务拆分和分配

### 自进化系统

任务完成后，代理自动调用 evolver 执行：

1. **分析执行结果** - 识别成功/失败模式
2. **提取经验** - 总结最佳实践和教训
3. **更新配置** - 使用 Write/Edit 更新代理和 Skill 文件
4. **记录进化** - 在 "📈 进化记录" 章节追加学习内容

进化记录格式：
```markdown
## 📈 进化记录（自动生成）

### 基于 [任务类型] 的学习

**执行时间**: YYYY-MM-DD HH:MM

**新增最佳实践**:
- **洞察标题**: 具体描述
  - 适用场景：...
  - 注意事项：...

**关键洞察**:
- [最重要的一条经验]
```

## 开发工作流

### 完整功能开发流程

```
用户需求
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
orchestrator (最终决策)
    ↓
evolver (系统进化)
```

### 并行执行示例

orchestrator 使用 `background_task()` 实现代理并行执行：

```python
# 启动并行任务
frontend_task = background_task(
    agent="frontend-developer",
    prompt="实现用户界面组件"
)
backend_task = background_task(
    agent="backend-developer",
    prompt="实现 API 端点"
)

# 等待完成
frontend_result = background_output(task_id=frontend_task)
backend_result = background_output(task_id=backend_task)
```

### Agent 调用方式

**自动调用（推荐）**：
Claude 根据请求关键词自动选择合适的代理。

**手动指定**：
```
使用 backend-developer 代理实现用户认证 API
使用 code-reviewer 代理审查代码
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
      "Edit(*)",
      "Grep(*)",
      "Glob(*)",
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
      "Read(**/.env)",
      "Write(**/.env)"
    ],
    "defaultMode": "acceptEdits"
  },
  "model": "sonnet"
}
```

### Hooks 自动化系统

项目使用 Hooks 系统实现自动化质量保障（配置位于 `.claude/settings.json`）：

#### PostToolUse Hook - 质量门禁
- **触发时机**: 使用 Write/Edit 工具修改文件后
- **验证内容**:
  - `project_standards.md` → 完整性验证（文件结构、路径变量、版本更新）
  - `.claude/agents/*.md` → Agent 文件格式验证
  - `.claude/skills/*/SKILL.md` → Skill 文件格式验证
- **脚本位置**: `.claude/hooks/scripts/quality-gate.sh`
- **验证脚本**: `.claude/scripts/verify_standards.py`

#### PreToolUse Hook - 安全检查
- **触发时机**: 执行 Bash 命令前
- **保护内容**: 阻止危险命令（rm -rf /、dd、fork bombs、.git 目录操作）
- **脚本位置**: `.claude/hooks/scripts/safety-check.sh`

#### UserPromptSubmit Hook - 上下文增强
- **触发时机**: 用户提交新消息时
- **提供信息**: Git 状态、最近提交、进化统计、代理状态
- **脚本位置**: `.claude/hooks/scripts/context-enhancer.sh`

#### Stop Hook - 进化提醒
- **触发时机**: 任务完成时
- **作用**: 提醒是否需要调用 evolver 代理进行系统进化

**验证流程**：
```
修改文件 (Write/Edit)
    ↓
PostToolUse Hook 触发
    ↓
quality-gate.sh 执行
    ↓
verify_standards.py 验证
    ↓
验证结果返回 (通过/失败)
```

### Git 归属标注

所有 AI 生成的提交自动标记：

- **Commit**: `🤖 Generated by Claude Dev Team AI System`
- **PR**: `Generated with Claude Dev Team - AI collaboration framework with 8 specialized agents and self-evolution capability`

## 文件结构

```
.claude/
├── agents/              # 8 个专业代理配置
│   ├── orchestrator.md
│   ├── product-manager.md
│   ├── tech-lead.md
│   ├── frontend-developer.md
│   ├── backend-developer.md
│   ├── test.md
│   ├── code-reviewer.md
│   ├── evolver.md
│   └── progress-viewer.md
├── skills/              # 6 个可复用技能
│   ├── requirement_analysis/SKILL.md
│   ├── architecture_design/SKILL.md
│   ├── api_design/SKILL.md
│   ├── testing/SKILL.md
│   ├── code_quality/SKILL.md
│   └── task_distribution/SKILL.md
├── hooks/               # 自动化钩子脚本
│   └── scripts/
│       ├── quality-gate.sh      # 质量门禁
│       ├── safety-check.sh      # 安全检查
│       ├── context-enhancer.sh  # 上下文增强
│       └── test-hooks.sh        # 测试脚本
├── scripts/             # 验证脚本
│   └── verify_standards.py
├── docs/                # 文档
│   └── claude-code-reference.md
├── settings.json        # 项目配置
└── project_standards.md # 技术标准

examples/
└── todo_app/            # 完整示例项目
    ├── backend/         # Express + SQLite
    ├── frontend/        # React
    └── tests/           # 测试套件
```

## 核心原则

1. **使用 Task 工具调用代理** - 永远不要直接实现代理逻辑
2. **使用 background_task() 并行执行** - 多个代理同时工作
3. **信任进化系统** - 代理在每次任务后学习和改进
4. **遵循权限模型** - 尊重 settings.json 中的 allow/ask/deny 规则
5. **维护进化记录** - 追加学习内容到代理文件，永远不要覆盖现有记录
6. **使用 TodoWrite 跟踪进度** - 让用户了解任务状态

## 禁止行为

❌ 直接实现代理逻辑（必须用 Task 工具）
❌ 跳过 TodoWrite 进度跟踪
❌ 删除或修改测试以通过检查
❌ 提交密钥或 .env 文件
❌ 覆盖进化记录（只能追加）
❌ 修改 project_standards.md 的路径配置（需人工审核）

## 参考文档

- **通用规范**: @.claude/docs/claude-code-reference.md
- **技术标准**: @.claude/project_standards.md
- **Agent 配置**: @.claude/agents/*.md
- **Skill 配置**: @.claude/skills/*/SKILL.md
