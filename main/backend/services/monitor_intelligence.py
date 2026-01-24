"""
监控系统 - 智能水平计算服务

功能：
1. 计算系统智能水平总分
2. 统计策略权重
3. 统计知识丰富度
4. 统计质量趋势
5. 统计进化频率
6. 识别学习路径里程碑

数据来源：
- .claude/rules/*.md (策略规则)
- .claude/agents/*.md (Agent 配置)
- .claude/skills/*/SKILL.md (技能知识)
- .claude/project_standards.md (最佳实践)
- main/docs/reviews/*.md (代码审查记录)
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List

from models.monitor_schema import IntelligenceScore, Milestone


class IntelligenceCalculator:
    """
    智能水平计算器

    计算公式：
    intelligence_score = (
        strategy_weight * 0.3 +
        knowledge_richness * 0.25 +
        quality_trend * 0.25 +
        evolution_frequency * 0.2
    ) * 10
    """

    def __init__(self):
        """初始化计算器"""
        self.project_root = Path(__file__).parent.parent.parent.parent

    def calculate_intelligence_score(self) -> IntelligenceScore:
        """
        计算智能水平总分

        Returns:
            IntelligenceScore: 智能水平分数对象
        """
        # 计算各项指标
        strategy_weight = self._calculate_strategy_weight()
        knowledge_richness = self._calculate_knowledge_richness()
        quality_trend = self._calculate_quality_trend()
        evolution_frequency = self._calculate_evolution_frequency()

        # 计算总分
        intelligence_score = (
            strategy_weight * 0.3 +
            knowledge_richness * 0.25 +
            quality_trend * 0.25 +
            evolution_frequency * 0.2
        ) * 10

        return IntelligenceScore(
            timestamp=datetime.now(),
            intelligence_score=round(intelligence_score, 2),
            strategy_weight=round(strategy_weight, 2),
            knowledge_richness=round(knowledge_richness, 2),
            quality_trend=round(quality_trend, 2),
            evolution_frequency=round(evolution_frequency, 2)
        )

    def _calculate_strategy_weight(self) -> float:
        """
        计算策略权重 (0-1)

        数据来源: .claude/rules/*.md 文件
        计算方法: (策略规则数量 / 100) × (平均奖励分数 / 10)

        Returns:
            float: 策略权重分数
        """
        rules_dir = self.project_root / ".claude" / "rules"
        if not rules_dir.exists():
            return 0.0

        total_rules = 0
        total_reward = 0.0
        file_count = 0

        for rule_file in rules_dir.glob("*.md"):
            try:
                content = rule_file.read_text(encoding="utf-8")

                # 解析规则数量（统计洞察章节）
                insights = re.findall(r"###.*洞察", content)
                total_rules += len(insights)

                # 解析平均奖励
                reward_matches = re.findall(r"平均奖励.*?(\d+\.?\d*)/10", content)
                if reward_matches:
                    avg_reward = sum(float(r) for r in reward_matches) / len(reward_matches)
                    total_reward += avg_reward
                    file_count += 1

            except Exception:
                continue

        if total_rules == 0:
            return 0.0

        # 规则数量得分（最多 100 条规则）
        rule_score = min(total_rules / 100, 1.0)

        # 奖励得分（平均奖励 / 10）
        reward_score = (total_reward / file_count / 10) if file_count > 0 else 0.0

        # 综合得分
        return (rule_score + reward_score) / 2

    def _calculate_knowledge_richness(self) -> float:
        """
        计算知识丰富度 (0-1)

        数据来源:
        - .claude/agents/*.md (Agent 配置)
        - .claude/skills/*/SKILL.md (技能知识)
        - .claude/project_standards.md (最佳实践)

        计算方法: (Agent数量×10 + Skill数量×20 + 最佳实践数量×5) / 500

        Returns:
            float: 知识丰富度分数
        """
        # 统计 Agent 数量
        agents_dir = self.project_root / ".claude" / "agents"
        agents_count = len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0

        # 统计 Skill 数量
        skills_dir = self.project_root / ".claude" / "skills"
        skills_count = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0

        # 统计最佳实践数量
        standards_file = self.project_root / ".claude" / "project_standards.md"
        best_practices = 0
        if standards_file.exists():
            try:
                content = standards_file.read_text(encoding="utf-8")
                best_practices = len(re.findall(r"###.*最佳实践", content))
            except Exception:
                pass

        # 计算知识丰富度
        knowledge_score = (
            agents_count * 10 +
            skills_count * 20 +
            best_practices * 5
        ) / 500

        return min(knowledge_score, 1.0)

    def _calculate_quality_trend(self) -> float:
        """
        计算质量趋势 (0-1)

        数据来源:
        - main/docs/reviews/*.md (代码审查记录)
        - 测试覆盖率报告（暂时使用默认值）

        计算方法: (代码审查通过率×0.6 + 测试覆盖率×0.4)

        Returns:
            float: 质量趋势分数
        """
        # 统计代码审查通过率
        reviews_dir = self.project_root / "main" / "docs" / "reviews"
        if not reviews_dir.exists():
            return 0.5  # 默认值

        total_reviews = 0
        passed_reviews = 0

        for review_file in reviews_dir.glob("*.md"):
            try:
                content = review_file.read_text(encoding="utf-8")
                total_reviews += 1
                # 检查是否通过（包含"通过"或"LGTM"关键词）
                if "通过" in content or "LGTM" in content or "✅" in content:
                    passed_reviews += 1
            except Exception:
                continue

        # 计算审查通过率
        review_pass_rate = passed_reviews / total_reviews if total_reviews > 0 else 0.5

        # 测试覆盖率（暂时使用默认值，实际应从测试报告解析）
        test_coverage = 0.75

        # 综合质量趋势
        return review_pass_rate * 0.6 + test_coverage * 0.4

    def _calculate_evolution_frequency(self) -> float:
        """
        计算进化频率 (0-1)

        数据来源: .claude/rules/*.md 文件的更新时间
        计算方法: 最近 7 天的进化记录数量 / 50

        Returns:
            float: 进化频率分数
        """
        rules_dir = self.project_root / ".claude" / "rules"
        if not rules_dir.exists():
            return 0.0

        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_updates = 0

        for rule_file in rules_dir.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(rule_file.stat().st_mtime)
                if mtime > seven_days_ago:
                    recent_updates += 1
            except Exception:
                continue

        return min(recent_updates / 50, 1.0)

    def identify_milestones(self) -> List[Milestone]:
        """
        识别学习路径里程碑

        里程碑定义：
        - 智能水平突破 8.0
        - 新增重要功能（如 AlphaZero 系统）
        - 重大架构升级

        Returns:
            List[Milestone]: 里程碑列表
        """
        milestones = []

        # 从 project_standards.md 解析进化历史
        standards_file = self.project_root / ".claude" / "project_standards.md"
        if standards_file.exists():
            try:
                content = standards_file.read_text(encoding="utf-8")

                # 解析进化记录
                evolution_pattern = r"### (\d{4}-\d{2}-\d{2}) v([\d.]+)\n- \*\*(.+?)\*\*: (.+)"
                matches = re.findall(evolution_pattern, content)

                for date_str, version, change_type, description in matches:
                    # 识别重要里程碑
                    if any(keyword in description for keyword in ["AlphaZero", "架构", "重大", "升级"]):
                        try:
                            milestone_date = datetime.strptime(date_str, "%Y-%m-%d")
                            milestones.append(Milestone(
                                timestamp=milestone_date,
                                event=f"{change_type}: {description[:50]}...",
                                intelligence_score=8.0  # 默认分数
                            ))
                        except Exception:
                            continue

            except Exception:
                pass

        return milestones
