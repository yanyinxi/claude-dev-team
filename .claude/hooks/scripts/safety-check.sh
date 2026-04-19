#!/bin/bash
# 安全检查：阻止危险的 Bash 命令
# Claude Code PreToolUse Hook - 从 stdin 读取 JSON 输入

# 从 stdin 读取 JSON
INPUT=$(cat)

# 只处理 Bash 工具调用
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null)
if [[ "$TOOL_NAME" != "Bash" ]]; then
    exit 0
fi

# 提取命令内容
COMMAND_INPUT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

if [[ -z "$COMMAND_INPUT" ]]; then
    exit 0
fi

block() {
    local pattern="$1"
    local reason="🚨 安全警告：检测到危险命令模式「${pattern}」\n命令：${COMMAND_INPUT}\n\n此操作已被阻止。如需执行，请手动运行或在 settings.json 中调整规则。"
    python3 -c "
import json, sys
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'deny',
        'permissionDecisionReason': sys.argv[1]
    }
}, ensure_ascii=False))
" "$reason"
    exit 2
}

# ── 系统破坏类 ──
[[ "$COMMAND_INPUT" =~ rm[[:space:]]+-rf[[:space:]]+/ ]]       && block "rm -rf /"
[[ "$COMMAND_INPUT" =~ rm[[:space:]]+-rf[[:space:]]+~ ]]       && block "rm -rf ~"
[[ "$COMMAND_INPUT" =~ rm[[:space:]]+-rf[[:space:]]+\* ]]      && block "rm -rf *"
[[ "$COMMAND_INPUT" =~ \>[[:space:]]*/dev/sda ]]               && block "> /dev/sda"
[[ "$COMMAND_INPUT" =~ dd[[:space:]]+if= ]]                    && block "dd if= (磁盘写入)"
[[ "$COMMAND_INPUT" =~ mkfs ]]                                 && block "mkfs (格式化)"
[[ "$COMMAND_INPUT" =~ shutdown|reboot|halt|poweroff ]]        && block "系统关机/重启命令"

# ── Fork Bomb ──
[[ "$COMMAND_INPUT" =~ :\(\)\{.*:\|:.*\} ]]                   && block "fork bomb (:|:&)"

# ── 代码注入类 ──
[[ "$COMMAND_INPUT" =~ \beval\b.*\$ ]]                         && block "eval 变量注入"
[[ "$COMMAND_INPUT" =~ curl.*\|.*sh ]]                         && block "curl | sh (远程代码执行)"
[[ "$COMMAND_INPUT" =~ curl.*\|.*bash ]]                       && block "curl | bash (远程代码执行)"
[[ "$COMMAND_INPUT" =~ wget.*\|.*sh ]]                         && block "wget | sh (远程代码执行)"
[[ "$COMMAND_INPUT" =~ wget.*-O.*\|.*sh ]]                     && block "wget -O | sh (远程代码执行)"

# ── 权限提升类 ──
[[ "$COMMAND_INPUT" =~ \bsudo\b ]]                             && block "sudo 权限提升"
[[ "$COMMAND_INPUT" =~ chmod[[:space:]]+(777|a\+rwx) ]]        && block "chmod 777/a+rwx (危险权限)"
[[ "$COMMAND_INPUT" =~ chown.*root ]]                          && block "chown root (权限变更)"

# ── .git 目录保护 ──
if [[ "$COMMAND_INPUT" =~ \brm\b ]] && [[ "$COMMAND_INPUT" =~ \.git ]]; then
    block "rm .git (版本控制目录)"
fi

# ── 敏感文件保护 ──
if [[ "$COMMAND_INPUT" =~ \>[[:space:]]*/etc/ ]] || [[ "$COMMAND_INPUT" =~ \>[[:space:]]*/etc/(passwd|shadow|sudoers|hosts) ]]; then
    block "覆写系统配置文件 /etc/"
fi

exit 0
