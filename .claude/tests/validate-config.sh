#!/bin/bash
# validate-config.sh - 验证当前 .claude 配置与 hooks 引用是否一致

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"

echo "🔍 验证 .claude 配置..."
echo "📁 项目目录: $PROJECT_DIR"

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "❌ 未找到配置文件: $SETTINGS_FILE"
    exit 1
fi

# 1) 校验 JSON 结构
python3 -m json.tool "$SETTINGS_FILE" >/dev/null
echo "✅ settings.json 是合法 JSON"

# 2) 校验关键配置字段存在
if ! python3 - "$SETTINGS_FILE" <<'PY'
import json, sys
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
assert "llm_driven_config" in cfg
hooks = cfg.get("hooks", {})
assert "Stop" in hooks and hooks["Stop"]
assert "SubagentStop" in hooks and hooks["SubagentStop"]

stop_cmds = [h.get("command", "") for item in hooks["Stop"] for h in item.get("hooks", [])]
sub_cmds = [h.get("command", "") for item in hooks["SubagentStop"] for h in item.get("hooks", [])]

assert any("session_evolver.py" in c for c in stop_cmds)
assert any("strategy_updater.py" in c for c in stop_cmds)
assert any("auto_evolver.py" in c for c in sub_cmds)
print("ok")
PY
then
    echo "❌ Hooks 配置缺失或不匹配当前实现"
    exit 1
fi
echo "✅ hooks 关键命令校验通过"

# 3) 校验关键 skill 文件存在
if [ ! -f "$PROJECT_DIR/.claude/skills/llm-driven-collaboration/SKILL.md" ]; then
    echo "❌ 缺少 Skill: .claude/skills/llm-driven-collaboration/SKILL.md"
    exit 1
fi
if [ ! -f "$PROJECT_DIR/.claude/docs/directory-governance.md" ]; then
    echo "❌ 缺少目录治理文档: .claude/docs/directory-governance.md"
    exit 1
fi
echo "✅ Skill 与治理文档存在"

# 4) 校验能力清单与文档声明
if ! python3 "$PROJECT_DIR/.claude/tests/verify_capabilities.py"; then
    echo "❌ capabilities 校验失败"
    exit 1
fi
echo "✅ capabilities 校验通过"

echo "🎉 配置验证通过"
