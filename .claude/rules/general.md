# General Development Rules

**更新时间**: 2026-01-24
**策略关键词**: general, best-practices, code-quality

## 全局规则

此规则适用于所有开发场景，无路径限制。

## 最佳实践

### ✅ 遵循项目标准
- **描述**: 严格遵守 project_standards.md 中的技术标准和规范
- **证据**: 项目标准强制约束
- **适用场景**: 所有开发任务
- **关键标准**:
  - 目录结构规范
  - 命名约定
  - API 规范
  - 错误处理规范
  - Git 提交规范

### ✅ 代码注释规范
- **描述**: 为核心逻辑添加必要的中文注释
- **证据**: 项目标准要求（参考 project_standards.md）
- **适用场景**: 所有代码文件
- **注释级别**:
  - **必要注释**: 函数/方法、类、复杂逻辑
  - **重要注释**: 业务逻辑、算法、配置
  - **核心注释**: 关键流程、边界情况、hack 方案

### ✅ 使用 Task 工具调用 Agent
- **描述**: 永远使用 Task 工具调用 Agent，不要直接实现 Agent 逻辑
- **证据**: 项目标准强制约束（参考 CLAUDE.md）
- **适用场景**: 所有需要调用 Agent 的场景
- **示例**:
  ```python
  # ✅ 正确：使用 Task 工具
  task(agent="backend-developer", prompt="实现用户登录 API")

  # ❌ 错误：直接实现 Agent 逻辑
  # 不要自己写代码实现 backend-developer 的工作
  ```

### ✅ Git 提交规范
- **描述**: 使用规范的 Git 提交信息格式
- **证据**: 项目标准要求（参考 project_standards.md）
- **适用场景**: 所有 Git 提交
- **格式**: `<type>(<scope>): <description>`
- **类型**:
  - `feat` - 新功能
  - `fix` - 修复 Bug
  - `docs` - 文档更新
  - `style` - 代码格式
  - `refactor` - 重构代码
  - `test` - 添加测试
  - `chore` - 工具/配置

### ✅ 错误处理规范
- **描述**: 使用统一的错误处理机制
- **证据**: 项目标准要求（参考 project_standards.md）
- **适用场景**: 所有错误处理场景
- **后端**: 使用 `AppException` 及其子类
- **前端**: 使用统一的错误提示组件

## 反模式

### ⚠️ 直接实现 Agent 逻辑
- **问题**: 不使用 Task 工具，直接实现 Agent 逻辑
- **正确做法**: 使用 Task 工具调用 Agent
- **原因**: 保持系统架构一致性
- **影响**: 破坏系统架构，难以维护

### ⚠️ 缺少代码注释
- **问题**: 核心逻辑缺少中文注释
- **正确做法**: 为核心逻辑添加必要的中文注释
- **原因**: 提高代码可读性和可维护性
- **影响**: 代码难以理解，维护困难

### ⚠️ 不规范的 Git 提交
- **问题**: Git 提交信息不规范
- **正确做法**: 使用规范的 Git 提交信息格式
- **原因**: 便于代码审查和版本管理
- **影响**: 提交历史混乱，难以追踪变更

### ⚠️ 违反目录结构约束
- **问题**: 在错误位置创建文件
- **正确做法**: 遵守项目目录结构约束
- **原因**: 保持项目结构清晰
- **影响**: 项目结构混乱，难以维护

## 相关文档

- **项目标准**: `.claude/project_standards.md`
- **通用规范**: `.claude/docs/claude-code-reference.md`
- **项目指南**: `CLAUDE.md`
- **Git 提交规范**: `.claude/project_standards.md` → Git 提交规范

## 真实执行数据

此规则文件的统计数据不再手工编造。真实执行指标由以下机制累积：

- 每次会话结束时，`session_evolver.py` 采集 git diff / agent 调用等真实数据到 `.claude/logs/sessions.jsonl`
- `strategy_updater.py` 基于真实指标做 EMA 更新到 `.claude/strategy_weights.json`
- 查看最近会话信号：`tail -n 5 .claude/logs/sessions.jsonl`
- 查看最新策略权重：`cat .claude/strategy_weights.json`
