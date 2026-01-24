#!/usr/bin/env python3
"""
Auto Evolver - SubagentStop Hook Script
自动进化引擎：在每个 Agent 任务完成后自动评估质量并更新知识库
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple


class AutoEvolver:
    """自动进化引擎"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.rules_dir = project_root / ".claude" / "rules"
        self.rules_dir.mkdir(parents=True, exist_ok=True)

    def evaluate_quality(self, result: Dict[str, Any]) -> float:
        """
        评估任务质量（0-10分）

        评估维度：
        - 执行时间（快速完成加分）
        - 文件修改数（有产出加分）
        - 成功率（成功加分，失败扣分）
        - 并行执行（并行加分）
        """
        score = 7.0  # 基础分

        # 基于执行时间调整
        duration = result.get("duration", 0)
        if duration < 60:
            score += 1.5  # 快速完成
        elif duration < 180:
            score += 0.5  # 正常速度
        elif duration > 300:
            score -= 0.5  # 耗时较长

        # 基于文件修改数调整
        files_modified = len(result.get("files_modified", []))
        if files_modified > 0:
            score += 0.5
        if files_modified > 3:
            score += 0.5  # 多文件修改

        # 基于成功率调整
        if result.get("success", True):
            score += 1.0
        else:
            score -= 2.0

        # 基于并行执行调整
        if result.get("parallel_execution", False):
            score += 0.5

        return min(10.0, max(0.0, score))

    def extract_insights(self, result: Dict[str, Any], agent_name: str) -> List[str]:
        """
        提取关键洞察

        分析执行结果，提取最佳实践和改进建议
        """
        insights = []

        # 成功模式
        if result.get("success"):
            insights.append("任务成功完成")

        # 并行执行
        if result.get("parallel_execution"):
            insights.append("并行执行提升效率")

        # 快速完成
        duration = result.get("duration", 0)
        if duration < 60:
            insights.append("快速响应")

        # 多文件修改
        files_modified = len(result.get("files_modified", []))
        if files_modified > 3:
            insights.append(f"修改了{files_modified}个文件")

        # Agent 特定洞察
        if agent_name == "frontend-developer":
            if any("component" in f.lower() for f in result.get("files_modified", [])):
                insights.append("组件开发")
        elif agent_name == "backend-developer":
            if any("api" in f.lower() or "router" in f.lower() for f in result.get("files_modified", [])):
                insights.append("API开发")

        return insights

    def categorize_insight(self, insight: str) -> str:
        """
        分类洞察类型

        返回：Best_Practice, Improvement, Collaboration, Efficiency
        """
        if any(keyword in insight for keyword in ["成功", "快速", "并行", "组件", "API"]):
            return "Best_Practice"
        elif any(keyword in insight for keyword in ["需要", "改进", "优化"]):
            return "Improvement"
        elif any(keyword in insight for keyword in ["协作", "配合", "沟通"]):
            return "Collaboration"
        elif any(keyword in insight for keyword in ["效率", "提升", "加速"]):
            return "Efficiency"
        else:
            return "Best_Practice"

    def map_agent_to_strategy(self, agent_name: str) -> str:
        """
        将 Agent 名称映射到策略关键词
        """
        mapping = {
            "frontend-developer": "frontend",
            "backend-developer": "backend",
            "orchestrator": "collaboration",
            "product-manager": "requirement-analysis",
            "tech-lead": "architecture-design",
            "test": "testing",
            "code-reviewer": "code-quality",
            "evolver": "evolution",
        }
        return mapping.get(agent_name, "unknown")

    def update_rules_file(
        self,
        agent_name: str,
        quality_score: float,
        insights: List[str]
    ) -> Path:
        """
        更新 Rules 文件

        追加新的经验记录到对应的策略规则文件
        """
        strategy = self.map_agent_to_strategy(agent_name)
        rules_file = self.rules_dir / f"{strategy}.md"

        # 如果文件不存在，创建初始文件
        if not rules_file.exists():
            self._create_initial_rules_file(rules_file, strategy)

        # 读取现有内容
        with open(rules_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查是否有"新学到的洞察"章节
        if "## 新学到的洞察" not in content:
            # 在文件开头添加章节
            header = f"""# {strategy.title()} Strategy Rules

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**策略关键词**: {strategy}

## 新学到的洞察

"""
            content = header + content

        # 追加新的洞察
        new_insights_section = self._format_insights(agent_name, quality_score, insights)

        # 在"新学到的洞察"章节后插入
        content = content.replace(
            "## 新学到的洞察\n",
            f"## 新学到的洞察\n\n{new_insights_section}"
        )

        # 更新时间戳
        content = re.sub(
            r"\*\*更新时间\*\*: .*",
            f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            content
        )

        # 保存
        with open(rules_file, "w", encoding="utf-8") as f:
            f.write(content)

        return rules_file

    def _create_initial_rules_file(self, rules_file: Path, strategy: str):
        """创建初始 Rules 文件"""
        content = f"""# {strategy.title()} Strategy Rules

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**策略关键词**: {strategy}

## 新学到的洞察

## 聚合经验 (基于多次执行)

"""
        with open(rules_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _format_insights(self, agent_name: str, quality_score: float, insights: List[str]) -> str:
        """格式化洞察为 Markdown"""
        if not insights:
            return ""

        sections = []
        for insight in insights:
            category = self.categorize_insight(insight)
            sections.append(f"### {category}\n\n- **Agent**: {agent_name}\n- **描述**: {insight}\n")

        return "\n".join(sections)


def main():
    """主函数：处理 SubagentStop Hook 输入"""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(0)

    # 提取关键信息
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})
    agent_name = tool_input.get("subagent_type", "unknown")

    # 构建结果数据
    result = {
        "duration": tool_response.get("duration", 0),
        "files_modified": tool_response.get("files_modified", []),
        "success": tool_response.get("success", True),
        "parallel_execution": tool_response.get("parallel_execution", False)
    }

    # 获取项目根目录
    project_root = Path.cwd()

    # 创建进化引擎
    evolver = AutoEvolver(project_root)

    # 评估质量
    quality_score = evolver.evaluate_quality(result)

    # 提取洞察
    insights = evolver.extract_insights(result, agent_name)

    # 更新 Rules 文件
    if insights:
        rules_file = evolver.update_rules_file(agent_name, quality_score, insights)
        print(f"✅ Auto-evolution completed: {agent_name} scored {quality_score:.1f}/10")
        print(f"📝 Updated: {rules_file}")
    else:
        print(f"ℹ️  No significant insights extracted for {agent_name}")

    sys.exit(0)


if __name__ == "__main__":
    main()
