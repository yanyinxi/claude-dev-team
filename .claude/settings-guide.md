# settings.json 配置说明

> settings.json 是 Claude Code 的严格 schema 文件，不支持任何注释语法。
> 所有字段说明统一维护在本文档。

## permissions 权限配置

| 分区 | 含义 |
|------|------|
| `allow` | 自动允许，无需用户确认 |
| `ask`   | 执行前弹窗询问用户确认 |
| `deny`  | 始终拒绝，不可绕过 |
| `defaultMode` | `acceptEdits` = 自动接受文件编辑 |

### allow 规则说明

| 规则 | 说明 |
|------|------|
| `Bash(npm run *)` | 允许运行 npm 脚本 |
| `Bash(git status/diff/log)` | 允许只读 git 操作 |
| `Read(*)` | 允许读取所有文件 |
| `Write(main/**)` | 仅允许写入 main/ 下各子目录 |
| `Edit(*)` | 允许编辑所有文件 |
| `Skill(*) / Task(*)` | 允许调用所有技能和代理 |

### ask 规则说明（需确认）

| 规则 | 说明 |
|------|------|
| `Bash(git add/commit/push)` | git 提交类操作需确认 |
| `Bash(rm:*)` | 删除文件需确认 |
| `Bash(docker:*)` | Docker 操作需确认 |

### deny 规则说明（永久禁止）

| 规则 | 说明 |
|------|------|
| `Bash(curl/wget:*)` | 禁止网络下载（安全） |
| `Read/Write(.git/**)` | 禁止直接操作 .git 目录 |
| `Read/Write(**/.env*)` | 禁止读写环境变量文件 |

---

## hooks 执行时机

| 事件 | 触发时机 | 执行脚本 |
|------|----------|----------|
| `PostToolUse` (Write\|Edit) | 写/编辑文件后 | `quality-gate.sh`（质量检查，30s超时）|
| `PreToolUse` (Write\|Edit) | 写/编辑文件前 | `path_validator.py`（路径合规验证，5s超时）|
| `PreToolUse` (Bash) | 执行 Bash 前 | `safety-check.sh`（危险命令拦截，5s超时）|
| `UserPromptSubmit` | 用户每次提交 | `context-enhancer.sh`（注入项目上下文，10s超时）|
| `Stop` | 主 Agent 完成时 | LLM战略分析(35s) + `strategy_updater.py`(30s) |
| `SubagentStop` | 子 Agent 完成时 | LLM智能分析(25s) + `auto_evolver.py`(25s) |
| `SessionStart` | 会话启动时 | `setup_env.sh`（初始化环境，10s超时）|

---

## llm_driven_config 高级功能开关

| 字段 | 说明 |
|------|------|
| `intelligent_analysis_enabled` | 启用 LLM 智能分析 |
| `autonomous_evolution_enabled` | 启用自主进化引擎 |
| `real_time_collaboration_enabled` | 启用实时协作机制 |
| `predictive_optimization_enabled` | 启用预测优化 |
| `context_driven_learning` | 启用上下文驱动学习 |
