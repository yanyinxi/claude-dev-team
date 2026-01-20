#!/bin/bash
# 上下文增强：自动添加项目状态信息

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# 输出项目状态信息
cat << EOF

📊 Claude Dev Team 项目状态 ($(date '+%Y-%m-%d %H:%M'))
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Git 状态:
$(cd "$PROJECT_DIR" && git status --short 2>/dev/null | head -5 || echo "  无变更")

📝 最近提交:
$(cd "$PROJECT_DIR" && git log -1 --oneline 2>/dev/null || echo "  无提交历史")

🧠 进化统计:
  • Agents 进化记录: $(grep -r "📈 进化记录" "$PROJECT_DIR/.claude/agents/" 2>/dev/null | wc -l | tr -d ' ') 个
  • Skills 进化记录: $(grep -r "📈 进化记录" "$PROJECT_DIR/.claude/skills/" 2>/dev/null | wc -l | tr -d ' ') 个

🎯 代理状态:
  • 总代理数: $(ls -1 "$PROJECT_DIR/.claude/agents/"*.md 2>/dev/null | wc -l | tr -d ' ')
  • 总技能数: $(find "$PROJECT_DIR/.claude/skills/" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF

exit 0
