#!/bin/bash
# validate-config.sh - 验证LLM驱动配置是否正确

echo "🔍 验证LLM驱动配置..."

# 检查settings.json是否存在关键配置
if ! grep -q "llm_driven_config" settings.json; then
    echo "❌ 缺少llm_driven_config配置"
    exit 1
fi

# 检查SubagentStop Hook
if ! grep -q "llm_driven_assessment" settings.json; then
    echo "❌ SubagentStop Hook配置不正确"
    exit 1
fi

# 检查Stop Hook
if ! grep -q "strategic_session_assessment" settings.json; then
    echo "❌ Stop Hook配置不正确"
    exit 1
fi

# 检查新Skill是否存在
if [ ! -f "skills/llm-driven-collaboration/SKILL.md" ]; then
    echo "❌ llm-driven-collaboration Skill不存在"
    exit 1
fi

# 检查测试文件
if [ ! -f "tests/llm-driven-tests.md" ]; then
    echo "❌ 测试用例文件不存在"
    exit 1
fi

echo "✅ 配置验证通过"
echo "🎉 LLM驱动智能协作团队v3.0配置完成！"
