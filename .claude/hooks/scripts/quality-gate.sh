#!/bin/bash
# 质量门禁：验证代码和配置文件

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
TOOL_NAME="$1"
FILE_PATH="$2"

# 如果是 project_standards.md，运行验证
if [[ "$FILE_PATH" == *"project_standards.md"* ]]; then
    echo "🔍 验证 project_standards.md..."
    if python3 "$PROJECT_DIR/.claude/scripts/verify_standards.py" --verbose 2>&1; then
        echo "✅ project_standards.md 验证通过"
    else
        echo "❌ project_standards.md 验证失败" >&2
        exit 2  # 阻止操作
    fi
fi

# 如果是 agent 文件，验证格式
if [[ "$FILE_PATH" == *".claude/agents/"* ]]; then
    echo "🔍 验证 agent 文件格式..."
    if python3 "$PROJECT_DIR/.claude/scripts/verify_standards.py" --verbose 2>&1; then
        echo "✅ Agent 文件验证通过"
    else
        echo "⚠️ Agent 文件验证有警告，但允许继续"
    fi
fi

# 如果是 Skill 文件，验证格式
if [[ "$FILE_PATH" == *".claude/skills/"* ]]; then
    echo "🔍 验证 Skill 文件格式..."
    # 检查是否有进化记录章节
    if grep -q "📈 进化记录" "$FILE_PATH" 2>/dev/null; then
        echo "✅ Skill 文件包含进化记录章节"
    else
        echo "⚠️ Skill 文件缺少进化记录章节"
    fi
fi

exit 0
