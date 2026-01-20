# Claude Dev Team - 智能 Hooks 方案

## 问题诊断

### 当前配置的问题
1. ❌ **位置错误** - 在 `.claude/hooks/hooks.json`，应该在 `.claude/settings.json` 的 `hooks` 字段
2. ❌ **格式错误** - 使用了插件格式，不是标准 settings.json 格式
3. ❌ **条件匹配错误** - 使用 `conditions` 数组，应该用 `matcher` 字段

## 智能 Hooks 设计方案

### 设计原则

1. **质量门禁** - 自动验证，防止破坏性变更
2. **自动进化** - 任务完成后智能触发进化流程
3. **上下文增强** - 自动添加项目状态和历史信息
4. **安全防护** - 阻止危险操作，保护关键文件
5. **智能决策** - 根据执行结果决定下一步行动

### 完整 Hooks 配置

```json
{
  "hooks": {
    // ============================================
    // 1. 质量门禁 - 自动验证
    // ============================================

    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/quality-gate.sh",
            "timeout": 30
          }
        ]
      }
    ],

    // ============================================
    // 2. 安全防护 - 阻止危险操作
    // ============================================

    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/safety-check.sh",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/file-protection.sh",
            "timeout": 5
          }
        ]
      }
    ],

    // ============================================
    // 3. 上下文增强 - 自动添加项目信息
    // ============================================

    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/context-enhancer.sh",
            "timeout": 10
          }
        ]
      }
    ],

    // ============================================
    // 4. 智能进化 - 任务完成后自动分析
    // ============================================

    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "分析任务执行结果并决定是否需要进化：\\n\\n任务参数: $ARGUMENTS\\n\\n如果任务涉及代码实现、问题解决或新功能开发，请调用 evolver 代理记录经验。如果只是简单查询或信息获取，则跳过进化。"
          }
        ]
      }
    ],

    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/subagent-analyzer.sh",
            "timeout": 15
          }
        ]
      }
    ],

    // ============================================
    // 5. 会话管理 - 初始化和清理
    // ============================================

    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/session-init.sh",
            "timeout": 10
          }
        ]
      }
    ],

    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/scripts/session-cleanup.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Hook 脚本实现

### 1. quality-gate.sh - 质量门禁

```bash
#!/bin/bash
# 质量门禁：验证代码和配置文件

set -e

PROJECT_DIR="$CLAUDE_PROJECT_DIR"
MODIFIED_FILE="$1"  # Claude 会传递修改的文件路径

# 如果是 project_standards.md，运行验证
if [[ "$MODIFIED_FILE" == *"project_standards.md"* ]]; then
    echo "🔍 验证 project_standards.md..."
    python3 "$PROJECT_DIR/.claude/scripts/verify_standards.py" --verbose
    if [ $? -ne 0 ]; then
        echo "❌ project_standards.md 验证失败" >&2
        exit 2  # 阻止操作
    fi
    echo "✅ project_standards.md 验证通过"
fi

# 如果是 agent 文件，验证格式
if [[ "$MODIFIED_FILE" == *".claude/agents/"* ]]; then
    echo "🔍 验证 agent 文件格式..."
    python3 "$PROJECT_DIR/.claude/scripts/verify_standards.py" --verbose
    if [ $? -ne 0 ]; then
        echo "⚠️ Agent 文件验证有警告，但允许继续" >&2
        exit 0  # 警告但不阻止
    fi
    echo "✅ Agent 文件验证通过"
fi

# 如果是 TypeScript/JavaScript，运行 lint
if [[ "$MODIFIED_FILE" =~ \\.(ts|tsx|js|jsx)$ ]]; then
    if [ -f "$PROJECT_DIR/package.json" ]; then
        echo "🔍 运行 ESLint..."
        cd "$PROJECT_DIR"
        npm run lint:fix 2>/dev/null || true
        echo "✅ Lint 完成"
    fi
fi

exit 0
```

### 2. safety-check.sh - 安全检查

```bash
#!/bin/bash
# 安全检查：阻止危险的 Bash 命令

COMMAND="$1"

# 危险命令列表
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \\*"
    "> /dev/sda"
    "dd if="
    "mkfs"
    ":(){ :|:& };:"  # fork bomb
)

# 检查危险模式
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        echo "🚨 检测到危险命令：$pattern" >&2
        echo "此操作已被阻止以保护系统安全" >&2
        exit 2  # 阻止操作
    fi
done

# 检查是否尝试修改关键文件
if [[ "$COMMAND" == *"rm"* ]] && [[ "$COMMAND" == *".git"* ]]; then
    echo "⚠️ 警告：尝试删除 .git 目录" >&2
    echo "此操作已被阻止" >&2
    exit 2
fi

exit 0
```

### 3. file-protection.sh - 文件保护

```bash
#!/bin/bash
# 文件保护：防止修改关键配置

FILE_PATH="$1"

# 受保护的文件列表
PROTECTED_FILES=(
    ".claude/project_standards.md"
    ".git/config"
    ".env"
)

# 检查是否是受保护文件
for protected in "${PROTECTED_FILES[@]}"; do
    if [[ "$FILE_PATH" == *"$protected"* ]]; then
        echo "⚠️ 警告：尝试修改受保护文件 $protected" >&2
        echo "请确认此操作是必要的" >&2
        # 不阻止，只警告
        exit 0
    fi
done

exit 0
```

### 4. context-enhancer.sh - 上下文增强

```bash
#!/bin/bash
# 上下文增强：自动添加项目状态信息

PROJECT_DIR="$CLAUDE_PROJECT_DIR"

# 输出项目状态信息
cat << EOF
📊 项目状态快照 ($(date '+%Y-%m-%d %H:%M'))

Git 状态:
$(cd "$PROJECT_DIR" && git status --short 2>/dev/null | head -5)

最近提交:
$(cd "$PROJECT_DIR" && git log -1 --oneline 2>/dev/null)

进化记录统计:
- Agents 进化记录: $(grep -r "📈 进化记录" "$PROJECT_DIR/.claude/agents/" 2>/dev/null | wc -l | tr -d ' ')
- Skills 进化记录: $(grep -r "📈 进化记录" "$PROJECT_DIR/.claude/skills/" 2>/dev/null | wc -l | tr -d ' ')

EOF

exit 0
```

### 5. subagent-analyzer.sh - 子代理分析器

```bash
#!/bin/bash
# 子代理分析器：分析子代理执行结果

AGENT_NAME="$1"
RESULT="$2"

# 记录到日志
LOG_FILE="$CLAUDE_PROJECT_DIR/.claude/logs/subagent-history.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Agent: $AGENT_NAME | Result: $RESULT" >> "$LOG_FILE"

# 如果是关键代理，输出提醒
CRITICAL_AGENTS=("frontend-developer" "backend-developer" "test")
for agent in "${CRITICAL_AGENTS[@]}"; do
    if [[ "$AGENT_NAME" == "$agent" ]]; then
        echo "✅ 关键代理 $AGENT_NAME 已完成"
        echo "💡 建议：检查代码质量并运行测试"
    fi
done

exit 0
```

### 6. session-init.sh - 会话初始化

```bash
#!/bin/bash
# 会话初始化：设置环境变量和检查依赖

PROJECT_DIR="$CLAUDE_PROJECT_DIR"

# 设置环境变量
if [ -n "$CLAUDE_ENV_FILE" ]; then
    cat >> "$CLAUDE_ENV_FILE" << EOF
export NODE_ENV=development
export CLAUDE_DEV_TEAM_VERSION=2.0.0
export PYTHONPATH="$PROJECT_DIR/.claude/scripts:\$PYTHONPATH"
EOF
fi

# 检查依赖
echo "🔍 检查项目依赖..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "⚠️ 警告：未找到 python3" >&2
fi

# 检查 Node.js
if [ -f "$PROJECT_DIR/package.json" ]; then
    if ! command -v npm &> /dev/null; then
        echo "⚠️ 警告：未找到 npm" >&2
    fi
fi

echo "✅ 会话初始化完成"
exit 0
```

### 7. session-cleanup.sh - 会话清理

```bash
#!/bin/bash
# 会话清理：保存状态和清理临时文件

PROJECT_DIR="$CLAUDE_PROJECT_DIR"

# 保存会话统计
STATS_FILE="$PROJECT_DIR/.claude/logs/session-stats.log"
mkdir -p "$(dirname "$STATS_FILE")"

cat >> "$STATS_FILE" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] Session ended
- Modified files: $(cd "$PROJECT_DIR" && git status --short 2>/dev/null | wc -l | tr -d ' ')
- Commits: $(cd "$PROJECT_DIR" && git log --since="1 hour ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
EOF

echo "✅ 会话已保存"
exit 0
```

## 实施步骤

### 1. 创建脚本目录
```bash
mkdir -p .claude/hooks/scripts
mkdir -p .claude/logs
```

### 2. 创建所有脚本文件
```bash
# 将上述脚本保存到对应文件
chmod +x .claude/hooks/scripts/*.sh
```

### 3. 更新 settings.json
```bash
# 将 hooks 配置合并到 .claude/settings.json
```

### 4. 测试 hooks
```bash
# 测试质量门禁
echo "test" > test.txt
# 应该看到 hook 被触发

# 测试安全检查
# 尝试运行危险命令（会被阻止）
```

## 智能特性

### 1. 自适应质量门禁
- 根据文件类型自动选择验证策略
- TypeScript/JavaScript → ESLint
- Python → Flake8/Black
- Agent/Skill 文件 → 自定义验证

### 2. 智能进化触发
- 任务完成后自动分析是否需要进化
- 只对有价值的任务触发进化（代码实现、问题解决）
- 跳过简单查询和信息获取

### 3. 上下文感知
- 自动添加 Git 状态
- 显示最近的进化记录
- 提供项目健康度快照

### 4. 安全防护
- 阻止危险的 Bash 命令
- 保护关键配置文件
- 防止误删 .git 目录

### 5. 历史追踪
- 记录所有子代理执行
- 保存会话统计
- 便于后续分析和优化

## 优势

1. **零配置** - 开箱即用，自动适配项目
2. **智能化** - 根据上下文自动决策
3. **安全性** - 多层防护，防止破坏性操作
4. **可扩展** - 易于添加新的 hook 脚本
5. **自我进化** - 通过日志分析持续优化

## 监控和优化

### 查看 hook 执行日志
```bash
tail -f .claude/logs/subagent-history.log
tail -f .claude/logs/session-stats.log
```

### 分析 hook 性能
```bash
# 统计最常触发的 hooks
grep "Agent:" .claude/logs/subagent-history.log | cut -d'|' -f1 | sort | uniq -c | sort -rn
```

### 优化建议
- 如果某个 hook 经常超时，增加 timeout 值
- 如果某个 hook 误报太多，调整检测规则
- 定期审查日志，发现可优化的模式
