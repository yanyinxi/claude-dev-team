#!/bin/bash
# 测试自动反馈闭环系统（真实信号版）

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
export CLAUDE_PROJECT_DIR="$PROJECT_DIR"

SESSIONS_FILE="$PROJECT_DIR/.claude/logs/sessions.jsonl"
INVOCATIONS_FILE="$PROJECT_DIR/.claude/logs/agent-invocations.jsonl"
WEIGHTS_FILE="$PROJECT_DIR/.claude/strategy_weights.json"

echo "========================================="
echo "测试自动反馈闭环系统"
echo "项目目录: $PROJECT_DIR"
echo "========================================="
echo ""

mkdir -p "$PROJECT_DIR/.claude/logs"

before_sessions=0
before_invocations=0
[ -f "$SESSIONS_FILE" ] && before_sessions=$(wc -l < "$SESSIONS_FILE")
[ -f "$INVOCATIONS_FILE" ] && before_invocations=$(wc -l < "$INVOCATIONS_FILE")

echo "1. 测试 quality_evaluator.py..."
python3 "$PROJECT_DIR/.claude/lib/quality_evaluator.py" >/dev/null
echo "✅ quality_evaluator.py 测试通过"
echo ""

echo "2. 测试 auto_evolver.py（SubagentStop 记录）..."
echo '{"session_id":"test-auto-feedback","tool_input":{"subagent_type":"backend-developer"}}' \
  | python3 "$PROJECT_DIR/.claude/hooks/scripts/auto_evolver.py" >/dev/null
after_invocations=$(wc -l < "$INVOCATIONS_FILE")
if [ "$after_invocations" -le "$before_invocations" ]; then
  echo "❌ auto_evolver.py 未写入 agent-invocations.jsonl"
  exit 1
fi
echo "✅ auto_evolver.py 已记录 agent 调用事实"
echo ""

echo "3. 测试 session_evolver.py + strategy_updater.py（Stop 链路）..."
echo '{"session_id":"test-auto-feedback","stop_reason":"test"}' \
  | python3 "$PROJECT_DIR/.claude/hooks/scripts/session_evolver.py" >/dev/null
python3 "$PROJECT_DIR/.claude/hooks/scripts/strategy_updater.py" </dev/null >/dev/null

after_sessions=$(wc -l < "$SESSIONS_FILE")
if [ "$after_sessions" -le "$before_sessions" ]; then
  echo "❌ session_evolver.py 未写入 sessions.jsonl"
  exit 1
fi
if [ ! -f "$WEIGHTS_FILE" ]; then
  echo "❌ strategy_weights.json 不存在"
  exit 1
fi
echo "✅ Stop 链路写入成功（sessions + strategy_weights）"
echo ""

echo "4. 快速预览最新真实数据..."
echo "最近 2 条 sessions:" 
tail -n 2 "$SESSIONS_FILE" || true
echo ""
echo "策略权重文件前 20 行:"
python3 -m json.tool "$WEIGHTS_FILE" | head -20
echo ""

echo "========================================="
echo "✅ 自动反馈闭环测试完成"
echo "========================================="
