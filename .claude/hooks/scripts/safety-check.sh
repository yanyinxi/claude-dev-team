#!/bin/bash
# 安全检查：阻止危险的 Bash 命令

TOOL_NAME="$1"
COMMAND_INPUT="$2"

# 只检查 Bash 命令
if [[ "$TOOL_NAME" != "Bash" ]]; then
    exit 0
fi

# 危险命令模式列表
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \*"
    "> /dev/sda"
    "dd if="
    "mkfs"
    ":(){ :|:& };:"
)

# 检查危险模式
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ "$COMMAND_INPUT" == *"$pattern"* ]]; then
        cat << EOF >&2
🚨 安全警告：检测到危险命令模式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模式: $pattern
命令: $COMMAND_INPUT

此操作已被阻止以保护系统安全。
如果这是合法操作，请手动执行或修改安全规则。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
        exit 2  # 阻止操作
    fi
done

# 检查是否尝试删除 .git 目录
if [[ "$COMMAND_INPUT" == *"rm"* ]] && [[ "$COMMAND_INPUT" == *".git"* ]]; then
    cat << EOF >&2
⚠️ 警告：尝试删除 .git 相关文件
此操作已被阻止以保护版本控制历史。
EOF
    exit 2
fi

exit 0
