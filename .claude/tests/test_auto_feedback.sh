#!/bin/bash
# 测试自动化反馈闭环系统

# 设置项目根目录
PROJECT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
export CLAUDE_PROJECT_DIR="$PROJECT_DIR"

echo "========================================="
echo "测试自动化反馈闭环系统"
echo "项目目录: $PROJECT_DIR"
echo "========================================="
echo ""

# 测试 1: quality_evaluator.py
echo "1. 测试 quality_evaluator.py..."
python3 "$PROJECT_DIR/.claude/hooks/scripts/quality_evaluator.py"
if [ $? -eq 0 ]; then
    echo "✅ quality_evaluator.py 测试通过"
else
    echo "❌ quality_evaluator.py 测试失败"
fi
echo ""

# 测试 2: auto_evolver.py (模拟输入)
echo "2. 测试 auto_evolver.py..."
echo '{
  "tool_input": {
    "subagent_type": "backend-developer"
  },
  "tool_response": {
    "duration": 45,
    "files_modified": ["main/backend/api/routes/user_router.py", "main/backend/services/user_service.py"],
    "success": true,
    "parallel_execution": true
  }
}' | python3 "$PROJECT_DIR/.claude/hooks/scripts/auto_evolver.py"
if [ $? -eq 0 ]; then
    echo "✅ auto_evolver.py 测试通过"
else
    echo "❌ auto_evolver.py 测试失败"
fi
echo ""

# 测试 3: strategy_updater.py (模拟输入)
echo "3. 测试 strategy_updater.py..."
echo '{
  "session_data": {
    "strategy": "backend",
    "success": true,
    "parallel_execution": true
  }
}' | python3 "$PROJECT_DIR/.claude/hooks/scripts/strategy_updater.py"
if [ $? -eq 0 ]; then
    echo "✅ strategy_updater.py 测试通过"
else
    echo "❌ strategy_updater.py 测试失败"
fi
echo ""

# 测试 4: 检查生成的文件
echo "4. 检查生成的文件..."
if [ -f "$PROJECT_DIR/.claude/strategy_weights.json" ]; then
    echo "✅ strategy_weights.json 存在"
    echo "内容预览:"
    head -n 10 "$PROJECT_DIR/.claude/strategy_weights.json"
else
    echo "❌ strategy_weights.json 不存在"
fi
echo ""

if [ -f "$PROJECT_DIR/.claude/rules/backend.md" ]; then
    echo "✅ backend.md 已更新"
    echo "最后 10 行:"
    tail -n 10 "$PROJECT_DIR/.claude/rules/backend.md"
else
    echo "⚠️  backend.md 未找到（可能是首次运行）"
fi
echo ""

echo "========================================="
echo "测试完成"
echo "========================================="
