#!/bin/bash
# cleanup-claude-artifacts.sh - 清理 .claude 目录下的运行时噪音文件

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$PROJECT_DIR"

echo "🧹 清理 .claude 运行时噪音..."

# Python 缓存
find .claude -type d -name '__pycache__' -prune -exec rm -rf {} +

# macOS 垃圾文件
find .claude -name '.DS_Store' -delete

# 已废弃日志
rm -f .claude/logs/evolution-log.jsonl

# 历史遗留目录（旧路径）
rm -rf .claude/hooks/execution_results
rm -f .claude/hooks/strategy_variants.json

echo "✅ 清理完成"
