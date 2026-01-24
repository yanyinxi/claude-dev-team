#!/bin/bash
# =====================================================
# SessionStart Hook - 持久化环境变量
# =====================================================
# 功能：在会话开始时自动设置项目环境变量
# 依赖：CLAUDE_ENV_FILE 环境变量
# =====================================================

set -e

# 检查是否存在 CLAUDE_ENV_FILE
if [ -z "$CLAUDE_ENV_FILE" ]; then
  echo "⚠️  CLAUDE_ENV_FILE 未设置，跳过环境变量持久化"
  exit 0
fi

# 检查是否存在 CLAUDE_PROJECT_DIR
if [ -z "$CLAUDE_PROJECT_DIR" ]; then
  echo "⚠️  CLAUDE_PROJECT_DIR 未设置，跳过环境变量持久化"
  exit 0
fi

echo "🔧 正在设置 Claude Dev Team 环境变量..."

# 持久化项目根目录
echo "export PROJECT_ROOT=\"\$CLAUDE_PROJECT_DIR\"" >> "$CLAUDE_ENV_FILE"

# 持久化 Python 路径
echo "export PYTHONPATH=\"\$CLAUDE_PROJECT_DIR/main/backend:\$PYTHONPATH\"" >> "$CLAUDE_ENV_FILE"

# 持久化 Python 虚拟环境（如果存在）
if [ -f "$CLAUDE_PROJECT_DIR/venv/bin/activate" ]; then
  echo "source \"\$CLAUDE_PROJECT_DIR/venv/bin/activate\"" >> "$CLAUDE_ENV_FILE"
  echo "✅ Python 虚拟环境已配置"
fi

# 持久化 Node.js 环境（如果存在）
if [ -d "$CLAUDE_PROJECT_DIR/main/frontend/node_modules" ]; then
  echo "export PATH=\"\$CLAUDE_PROJECT_DIR/main/frontend/node_modules/.bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
  echo "✅ Node.js 环境已配置"
fi

# 持久化常用别名
echo "alias cdp='cd \"\$CLAUDE_PROJECT_DIR\"'" >> "$CLAUDE_ENV_FILE"
echo "alias cdb='cd \"\$CLAUDE_PROJECT_DIR/main/backend\"'" >> "$CLAUDE_ENV_FILE"
echo "alias cdf='cd \"\$CLAUDE_PROJECT_DIR/main/frontend\"'" >> "$CLAUDE_ENV_FILE"

echo "✅ 环境变量持久化完成"
echo ""
echo "📋 已设置的环境变量："
echo "  • PROJECT_ROOT: \$CLAUDE_PROJECT_DIR"
echo "  • PYTHONPATH: \$CLAUDE_PROJECT_DIR/main/backend"
echo ""
echo "📋 已设置的别名："
echo "  • cdp: 跳转到项目根目录"
echo "  • cdb: 跳转到后端目录"
echo "  • cdf: 跳转到前端目录"
echo ""

exit 0
