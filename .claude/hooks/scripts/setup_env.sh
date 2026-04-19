#!/bin/bash
# SessionStart Hook - 持久化环境变量（幂等：重复执行不会重复追加）

set -e

if [ -z "$CLAUDE_ENV_FILE" ]; then
  echo "⚠️  CLAUDE_ENV_FILE 未设置，跳过环境变量持久化"
  exit 0
fi

if [ -z "$CLAUDE_PROJECT_DIR" ]; then
  echo "⚠️  CLAUDE_PROJECT_DIR 未设置，跳过环境变量持久化"
  exit 0
fi

echo "🔧 正在设置 Claude Dev Team 环境变量..."

# 幂等追加：只在内容不存在时才写入
append_once() {
  local line="$1"
  local marker="$2"  # 用于去重检测的唯一标识字符串
  if ! grep -qF "$marker" "$CLAUDE_ENV_FILE" 2>/dev/null; then
    echo "$line" >> "$CLAUDE_ENV_FILE"
  fi
}

append_once "export PROJECT_ROOT=\"\$CLAUDE_PROJECT_DIR\""        "PROJECT_ROOT="
append_once "export PYTHONPATH=\"\$CLAUDE_PROJECT_DIR/main/backend:\$PYTHONPATH\""  "main/backend:\$PYTHONPATH"
append_once "alias cdp='cd \"\$CLAUDE_PROJECT_DIR\"'"             "alias cdp="
append_once "alias cdb='cd \"\$CLAUDE_PROJECT_DIR/main/backend\"'"  "alias cdb="
append_once "alias cdf='cd \"\$CLAUDE_PROJECT_DIR/main/frontend\"'" "alias cdf="

if [ -f "$CLAUDE_PROJECT_DIR/venv/bin/activate" ]; then
  append_once "source \"\$CLAUDE_PROJECT_DIR/venv/bin/activate\""  "venv/bin/activate"
  echo "✅ Python 虚拟环境已配置"
fi

if [ -d "$CLAUDE_PROJECT_DIR/main/frontend/node_modules" ]; then
  append_once "export PATH=\"\$CLAUDE_PROJECT_DIR/main/frontend/node_modules/.bin:\$PATH\""  "node_modules/.bin:\$PATH"
  echo "✅ Node.js 环境已配置"
fi

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

exit 0
