# Claude Dev Team Hooks 系统文档

## 概述

Hooks 系统是 Claude Dev Team 的自动化核心，通过在关键时刻自动执行脚本和 LLM 分析，实现智能化的开发流程。

## Hooks 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Hooks 生命周期                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SessionStart (会话开始)                                     │
│  └─ setup_env.sh - 持久化环境变量                           │
│                                                             │
│  UserPromptSubmit (用户提交提示)                             │
│  └─ context-enhancer.sh - 添加项目上下文                    │
│                                                             │
│  PreToolUse (工具调用前)                                     │
│  ├─ path_validator.py - 验证文件路径                        │
│  └─ safety-check.sh - 安全检查                              │
│                                                             │
│  PostToolUse (工具调用后)                                    │
│  └─ quality-gate.sh - 代码质量检查                          │
│                                                             │
│  SubagentStop (子代理完成)                                   │
│  └─ LLM 智能分析 - 评估执行质量                             │
│                                                             │
│  Stop (主代理完成)                                           │
│  └─ LLM 战略分析 - 制定进化战略                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Hooks 详细说明

### 1. SessionStart Hook

**触发时机**: 会话开始时

**脚本**: `.claude/hooks/scripts/setup_env.sh`

**功能**:
- 持久化项目根目录环境变量
- 配置 Python 虚拟环境
- 配置 Node.js 环境
- 设置常用别名（cdp, cdb, cdf）

**环境变量**:
```bash
export PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
export PYTHONPATH="$CLAUDE_PROJECT_DIR/main/backend:$PYTHONPATH"
export PATH="$CLAUDE_PROJECT_DIR/main/frontend/node_modules/.bin:$PATH"
```

**别名**:
```bash
alias cdp='cd "$CLAUDE_PROJECT_DIR"'      # 跳转到项目根目录
alias cdb='cd "$CLAUDE_PROJECT_DIR/main/backend"'  # 跳转到后端目录
alias cdf='cd "$CLAUDE_PROJECT_DIR/main/frontend"' # 跳转到前端目录
```

---

### 2. UserPromptSubmit Hook

**触发时机**: 用户提交提示时

**脚本**: `.claude/hooks/scripts/context-enhancer.sh`

**功能**:
- 显示当前 Git 状态
- 显示最近提交
- 统计进化记录
- 显示代理和技能数量

**输出示例**:
```
📊 Claude Dev Team 项目状态 (2026-01-24 17:31)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Git 状态:
M main/backend/main.py
M main/backend/models/db.py

📝 最近提交:
d14029b 🚀 功能: 监控系统中文本地化与功能增强

🧠 进化统计:
  • Agents 进化记录: 8 个
  • Skills 进化记录: 6 个

🎯 代理状态:
  • 总代理数: 10
  • 总技能数: 6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 3. PreToolUse Hook - Path Validator

**触发时机**: Write/Edit 工具调用前

**脚本**: `.claude/hooks/path_validator.py`

**功能**:
- 验证文件路径是否符合项目结构规范
- 阻止在错误位置创建文件
- 提供正确的路径建议

**验证规则**:
```python
FORBIDDEN_NESTED_PATHS = [
    r"^main/backend/main/",   # 禁止 main/backend/main/
    r"^main/frontend/main/",  # 禁止 main/frontend/main/
    r"^main/backend/docs/",   # 禁止 main/backend/docs/
    r"^main/frontend/docs/",  # 禁止 main/frontend/docs/
]
```

**错误提示示例**:
```
❌ 路径违规: main/backend/docs/api.md

原因: 文档应统一放在 main/docs/ 目录
正确做法: 将文件移动到 main/docs/ 对应子目录

详细说明: 参考 .claude/project_standards.md 的「目录结构强制约束」章节
```

---

### 4. PreToolUse Hook - Safety Check

**触发时机**: Bash 命令执行前

**脚本**: `.claude/hooks/scripts/safety-check.sh`

**功能**:
- 检查危险命令（rm -rf, curl, wget 等）
- 验证命令安全性
- 阻止潜在的破坏性操作

---

### 5. PostToolUse Hook - Quality Gate

**触发时机**: Write/Edit 工具调用后

**脚本**: `.claude/hooks/scripts/quality-gate.sh`

**功能**:
- 代码格式检查
- 语法验证
- 自动格式化（可选）

---

### 6. SubagentStop Hook

**触发时机**: 子代理完成任务时

**类型**: LLM Prompt

**功能**:
- 全面质量评估
- 模式智能识别
- 团队协作洞察
- 进化策略生成
- 知识自主沉淀

**评估维度**:
- 任务理解深度
- 执行策略有效性
- 协作质量评估
- 结果质量判断
- 学习机会识别

---

### 7. Stop Hook

**触发时机**: 主代理完成任务时

**类型**: LLM Prompt

**功能**:
- 会话质量综合评估
- 系统性问题识别
- 进化机会优先级排序
- 战略进化路线图
- 创新方向探索

**战略输出**:
- 团队成熟度评估
- 执行质量趋势
- 协作效率分析
- 创新采纳情况
- 学习加速度

---

## 配置文件

所有 Hooks 配置在 `.claude/settings.json` 中：

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/setup_env.sh",
        "timeout": 10
      }]
    }],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/path_validator.py",
          "timeout": 5
        }]
      },
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/safety-check.sh",
          "timeout": 5
        }]
      }
    ],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/quality-gate.sh",
        "timeout": 30
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/context-enhancer.sh",
        "timeout": 10
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "LLM 智能分析提示...",
        "timeout": 25
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "LLM 战略分析提示...",
        "timeout": 35
      }]
    }]
  }
}
```

## 测试 Hooks

运行测试脚本验证所有 Hooks 是否正常工作：

```bash
.claude/hooks/scripts/test-all-hooks.sh
```

## 自定义 Hooks

### 添加新的 Hook

1. 在 `.claude/hooks/scripts/` 创建脚本
2. 添加执行权限：`chmod +x script.sh`
3. 在 `.claude/settings.json` 中注册
4. 测试脚本是否正常工作

### Hook 脚本规范

- 使用 `#!/bin/bash` 或 `#!/usr/bin/env python3` shebang
- 返回 0 表示成功，非 0 表示失败
- 输出清晰的错误信息
- 设置合理的 timeout

## 常见问题

### Q: Hook 执行失败怎么办？

A: 检查以下几点：
1. 脚本是否有执行权限
2. 脚本路径是否正确
3. 环境变量是否设置
4. timeout 是否足够

### Q: 如何禁用某个 Hook？

A: 在 `.claude/settings.json` 中注释或删除对应的 Hook 配置。

### Q: Hook 可以访问哪些环境变量？

A: 常用环境变量：
- `$CLAUDE_PROJECT_DIR` - 项目根目录
- `$CLAUDE_ENV_FILE` - 环境变量文件路径
- `$AGENT_NAME` - 当前代理名称（SubagentStop）
- `$RESULT` - 执行结果（SubagentStop）
- `$ARGUMENTS` - 会话参数（Stop）

## 最佳实践

1. **保持脚本简洁**: 每个 Hook 只做一件事
2. **快速执行**: 避免长时间运行的操作
3. **清晰输出**: 提供有用的错误信息
4. **优雅失败**: 不要因为 Hook 失败而阻塞主流程
5. **测试充分**: 在添加新 Hook 前充分测试

## 进化记录

- **2026-01-24**: 添加 SessionStart Hook，实现环境变量持久化
- **2026-01-23**: 完善 PreToolUse Hook，添加路径验证
- **2026-01-20**: 初始化 Hooks 系统，添加基础 Hooks

---

**维护者**: Claude Dev Team
**最后更新**: 2026-01-24
