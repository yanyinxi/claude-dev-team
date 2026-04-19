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
from typing import Dict, List, Any


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
        提取有实质价值的洞察。
        只记录非常规情况：失败、并行执行、大量文件修改、特定文件类型。
        避免把「成功」「快速」这类无意义的默认状态写入规则文件。
        """
        insights = []

        # 失败情况：值得记录以便分析
        if not result.get("success", True):
            insights.append("任务执行失败，需要分析原因")

        # 并行执行：有实际意义的执行模式
        if result.get("parallel_execution"):
            insights.append("并行执行模式验证有效")

        # 大量文件修改（超过5个）：值得记录规模
        files_modified = result.get("files_modified", [])
        if len(files_modified) > 5:
            insights.append(f"大规模修改：{len(files_modified)} 个文件")

        # Agent 特定洞察：基于实际修改的文件类型
        if agent_name == "backend-developer":
            api_files = [f for f in files_modified if "api" in f.lower() or "route" in f.lower()]
            if api_files:
                insights.append(f"API 路由开发：{', '.join(api_files[:2])}")

        if agent_name == "frontend-developer":
            comp_files = [
                f for f in files_modified
                if "component" in f.lower() or ".vue" in f.lower()
            ]
            if comp_files:
                insights.append(f"组件开发：{', '.join(comp_files[:2])}")

        # 耗时过长（超过5分钟）：可能存在优化空间
        duration = result.get("duration", 0)
        if duration > 300:
            insights.append(f"执行耗时 {duration}s，超过5分钟，建议分析瓶颈")

        return insights

    def categorize_insight(self, insight: str) -> str:
        """
        分类洞察类型

        返回：Best_Practice, Improvement, Collaboration, Efficiency
        """
        if any(keyword in insight for keyword in ["成功", "快速", "并行", "组件", "API"]):
            return "Best_Practice"
        if any(keyword in insight for keyword in ["需要", "改进", "优化"]):
            return "Improvement"
        if any(keyword in insight for keyword in ["协作", "配合", "沟通"]):
            return "Collaboration"
        if any(keyword in insight for keyword in ["效率", "提升", "加速"]):
            return "Efficiency"
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

        # 追加新的洞察（跳过空洞察，防止写入无意义内容）
        new_insights_section = self._format_insights(agent_name, quality_score, insights)
        if not new_insights_section:
            return rules_file

        # 防止重复：检查同样内容是否已存在
        for insight in insights:
            if insight in content:
                return rules_file

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

    def _format_insights(self, agent_name: str, _quality_score: float, insights: List[str]) -> str:
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
        raw = sys.stdin.read().strip()
        input_data = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(0)

    # SubagentStop 实际可用字段：tool_input.subagent_type，其余字段不可靠
    tool_input = input_data.get("tool_input", {})
    agent_name = tool_input.get("subagent_type", "unknown")

    # SubagentStop hook 不提供 duration/files_modified/success 等字段
    # 仅能从 tool_input.subagent_type 获取 agent 名称，暂无法提取有价值洞察
    project_root = Path.cwd()
    evolver = AutoEvolver(project_root)
    insights = evolver.extract_insights({}, agent_name)

    if insights:
        rules_file = evolver.update_rules_file(agent_name, 0.0, insights)
        print(f"✅ Auto-evolution completed: {agent_name}")
        print(f"📝 Updated: {rules_file}")
    else:
        print(f"ℹ️  No significant insights for {agent_name}")

    sys.exit(0)


if __name__ == "__main__":
    main()
