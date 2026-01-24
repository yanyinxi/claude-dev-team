#!/bin/bash
# =====================================================
# 测试所有 Hooks 脚本
# =====================================================

set -e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
echo "📊 测试 Claude Dev Team Hooks 系统"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 测试 1: SessionStart Hook
echo "🧪 测试 1: SessionStart Hook (setup_env.sh)"
CLAUDE_ENV_FILE=/tmp/test_env.sh CLAUDE_PROJECT_DIR="$PROJECT_DIR" "$PROJECT_DIR/.claude/hooks/scripts/setup_env.sh"
if [ -f /tmp/test_env.sh ]; then
  echo "✅ SessionStart Hook 测试通过"
  rm /tmp/test_env.sh
else
  echo "❌ SessionStart Hook 测试失败"
fi
echo ""

# 测试 2: PreToolUse Hook - Path Validator
echo "🧪 测试 2: PreToolUse Hook (path_validator.py)"
if python3 "$PROJECT_DIR/.claude/hooks/path_validator.py" --help > /dev/null 2>&1; then
  echo "✅ Path Validator 测试通过"
else
  echo "⚠️  Path Validator 需要参数"
fi
echo ""

# 测试 3: PreToolUse Hook - Safety Check
echo "🧪 测试 3: PreToolUse Hook (safety-check.sh)"
if [ -x "$PROJECT_DIR/.claude/hooks/scripts/safety-check.sh" ]; then
  echo "✅ Safety Check 脚本可执行"
else
  echo "❌ Safety Check 脚本不可执行"
fi
echo ""

# 测试 4: PostToolUse Hook - Quality Gate
echo "🧪 测试 4: PostToolUse Hook (quality-gate.sh)"
if [ -x "$PROJECT_DIR/.claude/hooks/scripts/quality-gate.sh" ]; then
  echo "✅ Quality Gate 脚本可执行"
else
  echo "❌ Quality Gate 脚本不可执行"
fi
echo ""

# 测试 5: UserPromptSubmit Hook - Context Enhancer
echo "🧪 测试 5: UserPromptSubmit Hook (context-enhancer.sh)"
"$PROJECT_DIR/.claude/hooks/scripts/context-enhancer.sh" > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ Context Enhancer 测试通过"
else
  echo "❌ Context Enhancer 测试失败"
fi
echo ""

# 测试 6: 验证 settings.json 格式
echo "🧪 测试 6: 验证 settings.json 格式"
if python3 -m json.tool "$PROJECT_DIR/.claude/settings.json" > /dev/null 2>&1; then
  echo "✅ settings.json 格式正确"
else
  echo "❌ settings.json 格式错误"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 所有 Hooks 测试完成"
