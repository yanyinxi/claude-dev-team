#!/bin/bash
# AlphaZero 自博弈学习系统测试脚本

echo "=========================================="
echo "AlphaZero 自博弈学习系统测试"
echo "=========================================="
echo ""

# 测试 1: 策略变体生成
echo "📊 测试 1: 策略变体生成"
echo "------------------------------------------"
python3 .claude/hooks/scripts/strategy_generator.py
echo ""

# 测试 2: 任务复杂度分析
echo "📊 测试 2: 任务复杂度分析"
echo "------------------------------------------"
python3 .claude/hooks/scripts/strategy_generator.py "实现用户认证和权限管理系统，包括JWT Token、角色管理、权限控制"
echo ""

# 测试 3: 并行执行器
echo "📊 测试 3: 并行执行器"
echo "------------------------------------------"
python3 .claude/hooks/scripts/parallel_executor.py
echo ""

# 测试 4: 查看生成的文件
echo "📊 测试 4: 查看生成的文件"
echo "------------------------------------------"
echo "策略变体文件:"
ls -lh .claude/hooks/strategy_variants.json
echo ""
echo "策略权重文件:"
ls -lh .claude/strategy_weights.json
echo ""
echo "执行结果目录:"
ls -lh .claude/hooks/execution_results/
echo ""

# 测试 5: 验证文件内容
echo "📊 测试 5: 验证文件内容"
echo "------------------------------------------"
echo "策略权重内容:"
cat .claude/strategy_weights.json | python3 -m json.tool | head -20
echo ""

echo "=========================================="
echo "✅ 所有测试完成！"
echo "=========================================="
echo ""
echo "📁 生成的文件:"
echo "  - .claude/hooks/strategy_variants.json"
echo "  - .claude/strategy_weights.json"
echo "  - .claude/hooks/execution_results/*.json"
echo ""
echo "📖 查看文档:"
echo "  - .claude/hooks/scripts/README_ALPHAZERO.md"
echo "  - .claude/agents/strategy-selector.md"
echo "  - .claude/agents/self-play-trainer.md"
echo ""
