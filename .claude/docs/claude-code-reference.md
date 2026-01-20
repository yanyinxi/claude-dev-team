# Claude Code 通用规范参考

> 本文档包含 Claude Code CLI 的通用使用规范，供项目开发参考。

## 核心原则

1. **使用 Task 工具** - 永远用 Task/background_task() 调用代理/工具
2. **并行执行** - 独立任务用 `background_task()` + `background_output()`
3. **TodoWrite 跟踪** - 多步骤任务必须有进度
4. **权限规则** - 遵循 settings.json 的 allow/deny/ask
5. **禁止** - 直接实现代理逻辑、删除测试过关、提交密钥

## 常用命令

```bash
# 启动
claude                    # 交互模式
claude "任务描述"          # 带提示启动
claude -p "query"         # 无头模式（编程使用）
claude -c                 # 继续最近对话
claude -r "session_id"    # 恢复指定会话

# 权限
claude --allowedTools "Bash,Read,Edit,Write"
claude --permission-mode plan  # 计划模式（只读）
claude --dangerously-skip-permissions

# 输出格式
claude -p "query" --output-format json        # JSON 输出
claude -p "query" --output-format stream-json # 流式 JSON
claude -p "query" --json-schema '{...}'       # 结构化验证

# 工具
/model sonnet             # 切换模型
/cost                     # 查看成本
/compact [instructions]   # 压缩对话
/rewind                   # 回退代码/对话
/memory                   # 编辑 CLAUDE.md
/hooks                    # 管理钩子
/agents                   # 管理子代理
/mcp                      # 管理 MCP
/config                   # 打开设置界面
/export [filename]        # 导出对话
/rename <name>            # 重命名会话
/statusline               # 设置状态行
```

## 快捷键

- `Ctrl+C` 取消 | `Ctrl+D` 退出 | `Esc+Esc` 回退代码/对话
- `Ctrl+B` 后台任务 | `\` + Enter 多行输入
- `Ctrl+O` 切换详细输出 | `Ctrl+L` 清除屏幕
- `Ctrl+K` 删除到行尾 | `Ctrl+U` 删除整行
- `Alt+B/F` 光标前后单词 | `Ctrl+R` 反向搜索历史
- `Option+T` / `Alt+T` 切换思考模式
- `Shift+Tab` / `Alt+M` 切换权限模式

## 思考模式

复杂问题用 `ultrathink:` 前缀：
```
ultrathink: 设计系统架构方案
```
- 最多 31,999 令牌思考
- 环境变量：`MAX_THINKING_TOKENS=10000` 自定义预算

## 权限配置 (settings.json)

```json
{
  "permissions": {
    "allow": ["Bash(npm run:*)", "Read(*)", "Edit(src/**)", "Task(Explore)"],
    "ask": ["Bash(git push:*)", "Bash(git commit:*)"],
    "deny": ["Bash(curl:*)", "Bash(wget:*)", "Read(.env)", "Read(secrets/**)"],
    "defaultMode": "acceptEdits"
  }
}
```

**规则顺序**：deny → ask → allow（第一个匹配生效）

**权限模式**：
- `default` - 标准（首次提示）
- `acceptEdits` - 自动接受编辑
- `plan` - 计划模式（只读）
- `dontAsk` - 自动拒绝
- `bypassPermissions` - 跳过检查

## 配置作用域（优先级）

| 优先级 | 作用域 | 位置 | 说明 |
|--------|--------|------|------|
| 1 | Managed | 系统级 `managed-settings.json` | IT 部署，不可覆盖 |
| 2 | 命令行 | CLI 参数 | 临时会话 |
| 3 | Local | `.claude/settings.local.json` | 仅本人/当前项目 |
| 4 | Project | `.claude/settings.json` | 团队共享 |
| 5 | User | `~/.claude/settings.json` | 跨项目本人 |

## Hooks 钩子

```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "..." }] }],
    "PostToolUse": [{ "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "npm run lint:fix" }] }],
    "Stop": [{ "hooks": [{ "type": "prompt", "prompt": "评估任务是否完成: $ARGUMENTS" }] }],
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "npm install" }] }],
    "SessionEnd": [{ "hooks": [{ "type": "command", "command": "npm run cleanup" }] }]
  }
}
```

**事件类型**：
- `PreToolUse` - 工具调用前
- `PostToolUse` - 工具成功后
- `Stop` - 主 agent 完成时
- `SubagentStop` - 子代理完成时
- `SessionStart` - 会话开始时
- `SessionEnd` - 会话结束时
- `UserPromptSubmit` - 用户提交提示时

## 子代理 Sub-Agents

**存储位置**（优先级）：
```
CLI --agents > .claude/agents/ > ~/.claude/agents/ > 插件 agents/
```

**配置格式**：
```markdown
---
name: code-reviewer
description: 专家代码审查者，代码修改后主动使用
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
model: sonnet
permissionMode: default
skills: pr-review, security-check
---

You are a senior code reviewer...
```

**Task 工具用法**：
```python
# 前台任务
task_id = background_task(agent="explore", prompt="查找认证相关代码")
result = background_output(task_id=task_id)

# 并行任务
t1 = background_task(agent="frontend", prompt="实现组件A")
t2 = background_task(agent="backend", prompt="实现 API")
r1 = background_output(task_id=t1)
r2 = background_output(task_id=t2)
```

## TodoWrite 任务跟踪

```python
from openai import OpenAI

client = OpenAI()

# 创建任务列表
todo = [
  {"id": "1", "content": "设计数据库模型", "status": "pending", "priority": "high"},
  {"id": "2", "content": "实现 API 接口", "status": "pending", "priority": "high"},
  {"id": "3", "content": "编写前端页面", "status": "pending", "priority": "medium"},
  {"id": "4", "content": "编写测试用例", "status": "pending", "priority": "medium"},
]

# 更新状态
todo_write(todos=todo)

# 标记完成
todo = [{"id": "1", "content": "设计数据库模型", "status": "completed", "priority": "high"}]
todo_write(todos=todo)
```

## 输出样式 (Output Styles)

```bash
/output-style default      # 默认（高效软件工程）
/output-style explanatory # 教育性见解
/output-style learning    # 协作式学习（添加 TODO(human)）
```

## MCP (Model Context Protocol)

```bash
# 安装 HTTP 服务器
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 安装 stdio 服务器
claude mcp add --transport stdio --env API_KEY=xxx airtable -- npx -y airtable-mcp-server

# 管理
claude mcp list    # 列出服务器
claude mcp get <name>   # 查看详情
claude mcp remove <name> # 删除

# 工具命名
mcp__<server>__<tool>

# 作用域：local > project > user

# 环境变量扩展
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "${API_URL:-https://api.example.com}/mcp",
      "headers": {"Authorization": "Bearer ${API_KEY}"}
    }
  }
}
```

## 内存系统 Memory

**分层优先级**（高→低）：
1. 企业策略 - 系统级 `/etc/claude-code/CLAUDE.md`
2. 项目内存 - `./CLAUDE.md` 或 `./.claude/CLAUDE.md`
3. 项目规则 - `./.claude/rules/*.md`（支持 Glob 路径限定）
4. 用户内存 - `~/.claude/CLAUDE.md`
5. 本地覆盖 - `./CLAUDE.local.md`

**导入语法**：
```markdown
参考 @README 了解项目概述
详细规范见 @docs/api-standards.md
```

**模块化规则**：
```markdown
---
paths: src/api/**/*.ts
---

# API 开发规范

- 所有接口必须包含输入验证
- 使用标准错误响应格式
```

## 斜杠命令

**自定义位置**：`.claude/commands/` | `~/.claude/commands/`

**参数**：`$ARGUMENTS`（全部）| `$1, $2`（位置）

**Bash 执行**（`!` 前缀）：
```markdown
---
description: 创建 git 提交
---
当前变更: !`git diff HEAD`

根据变更创建提交信息。
```

## Bash 模式

在提示开头使用 `!` 直接执行命令：
```
! npm test
! git status
! ls -la
```

## 检查点 Checkpointing

- 自动跟踪文件编辑，按 `Esc+Esc` 或 `/rewind` 回退
- 支持：**仅对话**、**仅代码**、**代码和对话**
- 30 天后自动清理
- **限制**：Bash 命令 (`rm`, `mv`, `cp`) 更改无法回退

## 插件系统 Plugin

**组件目录**：
- `commands/` - 斜杠命令
- `agents/` - 自定义代理
- `skills/` - 技能包（SKILL.md）
- `hooks/` - 钩子配置
- `.mcp.json` - MCP 服务器
- `.lsp.json` - LSP 服务器

**安装范围**：user | project | local | managed

## 关键环境变量

```bash
# 性能
export BASH_MAX_TIMEOUT_MS=600000
export MAX_THINKING_TOKENS=20000
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50

# MCP
export MCP_TIMEOUT=60000
export MAX_MCP_OUTPUT_TOKENS=50000

# 禁用功能
export DISABLE_PROMPT_CACHING=1
export DISABLE_TELEMETRY=1
export DISABLE_AUTOUPDATER=1

# API
export ANTHROPIC_API_KEY=xxx
export ANTHROPIC_MODEL=sonnet
```

## 状态行定制

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

输入 JSON 结构：
```json
{
  "session_id": "abc",
  "model": {"display_name": "Opus"},
  "workspace": {"current_dir": "/project"},
  "cost": {"total_cost_usd": 0.01},
  "context_window": {"total_input_tokens": 15000}
}
```
