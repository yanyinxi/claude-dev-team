#!/bin/bash
# Stop Hook 验证测试脚本

echo "🧪 测试 Stop Hook 配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROJECT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"

echo "📁 项目目录: $PROJECT_DIR"
echo ""

# 测试 1: 验证 settings.json 格式
echo "测试 1: 验证 settings.json JSON 格式"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 -c "import json; json.loads(open('$PROJECT_DIR/.claude/settings.json').read())" 2>/dev/null; then
    echo "✅ settings.json 是有效的 JSON 格式"
else
    echo "❌ settings.json JSON 格式错误"
    exit 1
fi
echo ""

# 测试 2: 检查 Stop hook 配置
echo "测试 2: 检查 Stop hook 配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HOOK_TYPE=$(python3 -c "import json; data=json.loads(open('$PROJECT_DIR/.claude/settings.json').read()); print(data['hooks']['Stop'][0]['hooks'][0]['type'])" 2>/dev/null)
if [ "$HOOK_TYPE" = "command" ]; then
    echo "✅ Stop hook 类型正确: command"
else
    echo "❌ Stop hook 类型错误: $HOOK_TYPE (应该是 command)"
    exit 1
fi
echo ""

# 测试 3: 执行 Stop hook 命令
echo "测试 3: 执行 Stop hook 命令"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HOOK_COMMAND=$(python3 -c "import json; data=json.loads(open('$PROJECT_DIR/.claude/settings.json').read()); print(data['hooks']['Stop'][0]['hooks'][0]['command'])" 2>/dev/null)
if eval "$HOOK_COMMAND" 2>/dev/null; then
    echo "✅ Stop hook 命令执行成功"
else
    echo "❌ Stop hook 命令执行失败"
    exit 1
fi
echo ""

# 测试 4: 验证不再使用 prompt 类型
echo "测试 4: 验证不再使用 prompt 类型"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if grep -q '"type": "prompt"' "$PROJECT_DIR/.claude/settings.json"; then
    echo "⚠️  警告: settings.json 中仍然存在 prompt 类型的 hook"
else
    echo "✅ 已移除所有 prompt 类型的 Stop hook"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Stop Hook 验证测试完成"
echo ""
echo "💡 说明："
echo "  • Stop hook 已从 prompt 类型改为 command 类型"
echo "  • 不再要求返回 JSON 格式"
echo "  • 使用 echo 命令输出简单提示信息"
echo "  • 下次任务完成时将自动触发，不会再出现 JSON validation failed 错误"
