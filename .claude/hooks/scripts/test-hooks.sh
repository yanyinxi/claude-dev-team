#!/bin/bash
# Hooks 测试脚本

echo "🧪 测试 Claude Dev Team Hooks 配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

PROJECT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
export CLAUDE_PROJECT_DIR="$PROJECT_DIR"

echo "📁 项目目录: $PROJECT_DIR"
echo ""

# 测试 1: 质量门禁
echo "测试 1: 质量门禁 (quality-gate.sh)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$PROJECT_DIR/.claude/hooks/scripts/quality-gate.sh" "Write" "$PROJECT_DIR/.claude/project_standards.md"
echo ""

# 测试 2: 上下文增强
echo "测试 2: 上下文增强 (context-enhancer.sh)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$PROJECT_DIR/.claude/hooks/scripts/context-enhancer.sh"
echo ""

# 测试 3: 安全检查 - 正常命令
echo "测试 3: 安全检查 - 正常命令"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$PROJECT_DIR/.claude/hooks/scripts/safety-check.sh" "Bash" "ls -la"
if [ $? -eq 0 ]; then
    echo "✅ 正常命令通过"
else
    echo "❌ 正常命令被阻止（不应该）"
fi
echo ""

# 测试 4: 安全检查 - 危险命令
echo "测试 4: 安全检查 - 危险命令"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$PROJECT_DIR/.claude/hooks/scripts/safety-check.sh" "Bash" "rm -rf /"
if [ $? -eq 2 ]; then
    echo "✅ 危险命令被正确阻止"
else
    echo "❌ 危险命令未被阻止（应该阻止）"
fi
echo ""

# 测试 5: 检查脚本权限
echo "测试 5: 检查脚本权限"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for script in "$PROJECT_DIR/.claude/hooks/scripts/"*.sh; do
    if [ -x "$script" ]; then
        echo "✅ $(basename "$script") 可执行"
    else
        echo "❌ $(basename "$script") 不可执行"
    fi
done
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Hooks 测试完成"
echo ""
echo "💡 提示："
echo "  • Hooks 会在 Claude Code 运行时自动触发"
echo "  • 使用 'claude --debug' 可以看到 hooks 执行日志"
echo "  • 查看 .claude/logs/ 目录了解 hooks 执行历史"
