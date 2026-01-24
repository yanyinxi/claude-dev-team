#!/usr/bin/env python3
"""
Strategy Updater - Stop Hook Script
策略更新器：在会话结束时分析整体策略有效性并更新权重
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class StrategyUpdater:
    """策略更新器"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.weights_file = project_root / ".claude" / "strategy_weights.json"
        self.rules_dir = project_root / ".claude" / "rules"

    def analyze_strategy_effectiveness(self, session_data: Dict[str, Any]) -> Dict[str, float]:
        """
        分析策略有效性

        基于会话数据评估：
        - 整体完成质量
        - 协作效率
        - 执行速度
        - 创新程度
        """
        scores = {
            "overall_score": 7.5,
            "collaboration_quality": 8.0,
            "efficiency": 7.0,
            "innovation": 7.5
        }

        # 从会话数据中提取指标
        # 这里可以根据实际的会话数据结构进行调整
        if session_data.get("success", True):
            scores["overall_score"] += 1.0

        if session_data.get("parallel_execution", False):
            scores["efficiency"] += 1.0
            scores["collaboration_quality"] += 0.5

        # 归一化到 0-10 范围
        for key in scores:
            scores[key] = min(10.0, max(0.0, scores[key]))

        return scores

    def update_strategy_weights(self, strategy_name: str, scores: Dict[str, float]):
        """
        更新策略权重

        使用指数移动平均（EMA）更新权重
        """
        # 读取现有权重
        if self.weights_file.exists():
            with open(self.weights_file, "r", encoding="utf-8") as f:
                weights = json.load(f)
        else:
            weights = {}

        # 更新权重（指数移动平均，alpha=0.1）
        current_weight = weights.get(strategy_name, 5.0)
        new_weight = current_weight * 0.9 + scores["overall_score"] * 0.1
        weights[strategy_name] = round(new_weight, 2)

        # 添加元数据
        if "metadata" not in weights:
            weights["metadata"] = {}

        weights["metadata"][strategy_name] = {
            "last_updated": datetime.now().isoformat(),
            "scores": scores,
            "execution_count": weights["metadata"].get(strategy_name, {}).get("execution_count", 0) + 1
        }

        # 保存
        with open(self.weights_file, "w", encoding="utf-8") as f:
            json.dump(weights, f, indent=2, ensure_ascii=False)

    def generate_evolution_report(self, strategy_name: str, scores: Dict[str, float]) -> str:
        """生成进化报告"""
        report = f"""
📊 策略进化报告
================

策略名称: {strategy_name}
评估时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

评分详情:
- 整体质量: {scores['overall_score']:.1f}/10
- 协作质量: {scores['collaboration_quality']:.1f}/10
- 执行效率: {scores['efficiency']:.1f}/10
- 创新程度: {scores['innovation']:.1f}/10

平均分数: {sum(scores.values()) / len(scores):.1f}/10
"""
        return report

    def update_aggregated_insights(self, strategy_name: str, scores: Dict[str, float]):
        """
        更新聚合洞察

        在对应的 Rules 文件中更新聚合经验章节
        """
        rules_file = self.rules_dir / f"{strategy_name}.md"

        if not rules_file.exists():
            return

        # 读取现有内容
        with open(rules_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 查找聚合经验章节
        if "## 聚合经验 (基于多次执行)" not in content:
            # 添加章节
            content += "\n\n## 聚合经验 (基于多次执行)\n\n"

        # 提取现有的执行次数
        match = re.search(r"基于 (\d+) 次执行", content)
        execution_count = int(match.group(1)) + 1 if match else 1

        # 计算平均奖励
        avg_reward = scores["overall_score"]

        # 更新聚合洞察
        aggregated_section = f"""### 📊 聚合洞察 (基于 {execution_count} 次执行)

- **平均奖励**: {avg_reward:.1f}/10
- **策略**: {strategy_name}
- **描述**: 持续优化中

"""

        # 替换或添加聚合洞察
        if "### 📊 聚合洞察" in content:
            content = re.sub(
                r"### 📊 聚合洞察.*?(?=\n##|\Z)",
                aggregated_section,
                content,
                flags=re.DOTALL
            )
        else:
            content = content.replace(
                "## 聚合经验 (基于多次执行)\n",
                f"## 聚合经验 (基于多次执行)\n\n{aggregated_section}"
            )

        # 保存
        with open(rules_file, "w", encoding="utf-8") as f:
            f.write(content)


def main():
    """主函数：处理 Stop Hook 输入"""
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(0)

    # 提取会话数据
    session_data = input_data.get("session_data", {})
    strategy_name = session_data.get("strategy", "general")

    # 获取项目根目录
    project_root = Path.cwd()

    # 创建策略更新器
    updater = StrategyUpdater(project_root)

    # 分析策略有效性
    scores = updater.analyze_strategy_effectiveness(session_data)

    # 更新策略权重
    updater.update_strategy_weights(strategy_name, scores)

    # 更新聚合洞察
    updater.update_aggregated_insights(strategy_name, scores)

    # 生成报告
    report = updater.generate_evolution_report(strategy_name, scores)
    print(report)

    print(f"✅ Strategy updated: {strategy_name} - overall score {scores['overall_score']:.1f}/10")

    sys.exit(0)


if __name__ == "__main__":
    main()
