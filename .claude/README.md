# AI 开发团队协作系统

## 项目简介

这是一个基于 Claude Code 构建的 AI 开发团队协作系统，模拟真实软件开发团队的角色分工和协作流程。

## 核心特性

- ✅ 6 个专业 AI 代理角色
- ✅ 8 个可复用技能包
- ✅ 3 种标准化工作流
- ✅ 动态开发者数量（LLM 智能决定）
- ✅ 并行任务执行
- ✅ 质量关卡控制
- ✅ 完整的协作记录

## 目录结构

```
.claude/
├── agents/              # 6个代理配置
├── skills/              # 8个技能（Claude Code 原生）
├── workflows/           # 3个工作流（Claude Code 原生）
├── slashcommands/       # 4个快捷命令
├── schemas/             # JSON Schema
└── settings.toml        # 系统配置
```

## 快速开始

1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

2. 复制配置文件
   ```bash
   cp .env.example .env
   ```

3. 使用快捷命令
   ```
   /develop "实现用户登录功能"
   ```

## 核心代理

| 代理 | 职责 |
|------|------|
| Product Manager | 需求分析、PRD 生成 |
| Tech Lead | 架构设计、技术选型、任务分配 |
| Frontend Developer | 前端开发 |
| Backend Developer | 后端开发 |
| Test | 测试保证 |
| Code Reviewer | 代码审查 |

## 核心技能

| 技能 | 说明 |
|------|------|
| requirement-analysis | 需求分析 |
| architecture-design | 架构设计 |
| api-design | API 设计 |
| testing | 测试 |
| code-quality | 代码质量 |
| task-distribution | 动态任务分配 |
| git-workflow | Git 工作流 |
| report-generation | 报告生成 |

## 工作流

| 工作流 | 说明 |
|--------|------|
| feature_development | 新功能开发（支持动态开发者） |
| bug_fix | Bug 修复 |
| code_review | 代码审查 |

## 配置

### 开发者数量

系统支持动态决定开发者数量：

- **前端**: 1-5 人（LLM 根据复杂度决定）
- **后端**: 1-5 人（LLM 根据复杂度决定）

可通过以下方式配置：

1. **settings.toml**:
   ```toml
   [developers.max]
   frontend = 5
   backend = 5
   ```

2. **环境变量**:
   ```bash
   MAX_FRONTEND_WORKERS=5
   MAX_BACKEND_WORKERS=5
   ```

3. **命令行参数**:
   ```bash
   --max-frontend-workers 5 --max-backend-workers 5
   ```

## 文档

- [AGENTS.md](AGENTS.md) - 代理详细说明
- [SKILLS.md](SKILLS.md) - 技能详细说明
- [WORKFLOWS.md](WORKFLOWS.md) - 工作流详细说明
- [OUTPUT_STRUCTURE.md](OUTPUT_STRUCTURE.md) - 输出结构
- [ERROR_HANDLING.md](ERROR_HANDLING.md) - 错误处理
- [RESOURCE_MANAGEMENT.md](RESOURCE_MANAGEMENT.md) - 资源管理

## 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](../../CONTRIBUTING.md)

## 许可证

MIT License
