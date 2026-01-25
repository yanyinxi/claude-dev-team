#!/bin/bash
# 测试运行脚本

set -e

echo "========================================="
echo "  系统进化能力集成测试"
echo "========================================="

# 切换到项目根目录
cd "$(dirname "$0")/../.."

# 检查依赖
echo "检查测试依赖..."
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "安装测试依赖..."
    pip3 install -r main/tests/requirements.txt
fi

# 运行集成测试
echo ""
echo "运行集成测试..."
python3 -m pytest main/tests/integration/test_system_evolution.py -v -s --tb=short

echo ""
echo "========================================="
echo "  测试完成"
echo "========================================="
