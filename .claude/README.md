# Claude Code AI 开发团队协作系统

## 项目简介

这是一个基于 Claude Code 构建的 AI 开发团队协作系统，模拟真实软件开发团队的角色分工和协作流程。

## 核心特性

- ✅ 7 个专业 AI 代理角色
- ✅ 6 个可复用技能包
- ✅ Claude Code 原生能力集成
- ✅ 动态任务分配
- ✅ 并行任务执行
- ✅ 质量关卡控制

## 目录结构

```
.claude/
├── agents/              # 7个代理配置（符合官方文档标准）
│   ├── backend-developer.md
│   ├── code-reviewer.md
│   ├── frontend-developer.md
│   ├── orchestrator.md
│   ├── product-manager.md
│   ├── tech-lead.md
│   └── test.md
├── skills/              # 6个技能
│   ├── api_design/
│   ├── architecture_design/
│   ├── code_quality/
│   ├── requirement_analysis/
│   ├── task_distribution/
│   └── testing/
```

## 快速开始

直接开始使用，无需额外配置。

## 使用方法

### 自动委托（推荐）

直接描述你的需求，Claude 会自动选择合适的代理：

```
实现用户登录功能
→ Claude 自动调用 orchestrator → tech-lead → backend-developer

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
使用 code-reviewer 代理审查我的代码
```

## 代理列表

| 代理 | 功能 | 使用场景 | 触发词 |
|------|------|---------|--------|
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

## 使用示例

### 示例 1：实现新功能

```
用户：实现一个待办事项功能

Claude：
→ orchestrator 协调整个流程
→ product-manager 分析需求并创建 PRD
→ tech-lead 设计技术方案
→ frontend-developer 实现前端
→ backend-developer 实现后端 API
→ test 创建测试
→ code-reviewer 审查代码
```

### 示例 2：代码审查

```
用户：使用 code-reviewer 代理审查最近的代码变更

Claude：
→ code-reviewer 开始工作
→ 分析变更
→ 识别问题
→ 生成审查报告
```

### 示例 3：需求分析

```
用户：请用 product-manager 代理分析这个需求

Claude：
→ product-manager 接收需求
→ 提取功能需求
→ 创建 PRD 文档
→ 拆分任务
→ 估算优先级
```

### 示例 4：快速开发

```
用户：用 backend-developer 实现用户登录 API

Claude：
→ backend-developer 启动
→ 设计 API 端点
→ 实现业务逻辑
→ 添加数据库操作
→ 编写测试
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
| `allowed-tools` | 允许使用的工具列表 |
| `skills` | 代理可用的技能 |
| `model` | 使用 `inherit` 继承主对话模型 |
| `permissionMode` | `acceptEdits` 自动接受编辑，`default` 需要确认 |

## 工作流程

### 完整功能开发流程

```
1. 用户提出需求
   ↓
2. product-manager 分析需求，创建 PRD
   ↓
3. tech-lead 设计技术方案
   ↓
4. 动态分配任务（frontend + backend）
   ↓
5. 并行开发（前端 + 后端）
   ↓
6. test 创建测试
   ↓
7. code-reviewer 审查代码
   ↓
8. orchestrator 做最终决策
```

### 快速修复流程

```
1. 用户报告问题
   ↓
2. orchestrator 分析问题
   ↓
3. 分配给相应代理
   ↓
4. 修复并测试
   ↓
5. 代码审查
```

## 最佳实践

1. **清晰描述需求**：提供足够的上下文和约束
2. **使用触发词**：在描述中包含代理描述中的关键词
3. **指定代理**：复杂任务可以直接指定代理
4. **利用协调器**：跨多个领域的任务使用 orchestrator
5. **审查代码**：重要变更使用 code-reviewer

## 常见问题

### Q: 如何查看可用代理？

运行 `/agents` 命令查看所有代理。

### Q: 代理会自动选择吗？

是的，Claude 会根据你的需求描述自动选择合适的代理。

### Q: 可以手动指定代理吗？

可以，直接在对话中指定代理名称。

### Q: 代理可以链式调用吗？

是的，orchestrator 可以协调多个代理按顺序工作。

### Q: 如何验证代理是否生效？

运行 `/agents` 检查代理列表，或直接描述需求观察响应。

## 相关文档

- [Claude Code Skills 文档](https://code.claude.com/docs/zh-CN/skills)
- [Claude Code Sub-agents 文档](https://code.claude.com/docs/zh-CN/sub-agents)

## 许可证

MIT License
