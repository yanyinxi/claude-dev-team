#!/usr/bin/env python3
"""
策略变体生成器 - AlphaZero 风格自博弈学习系统

功能：
1. 根据基础策略生成多个变体
2. 支持不同的并行度和任务粒度
3. 自动生成策略配置
"""

import json
import sys
from typing import List, Dict, Any
from pathlib import Path


class StrategyGenerator:
    """策略变体生成器"""

    def __init__(self):
        self.weights_file = Path(__file__).parent.parent / "strategy_weights.json"
        self.variant_types = [
            "parallel_high",      # 高并行度
            "granular",           # 细粒度任务分解
            "sequential",         # 顺序执行
            "hybrid"              # 混合策略
        ]
        self.domain_keywords = {
            "backend": ["后端", "api", "数据库", "db", "服务", "service", "鉴权", "认证", "权限"],
            "frontend": ["前端", "ui", "页面", "组件", "vue", "react", "样式", "交互"],
            "tests": ["测试", "test", "单测", "集成测试", "e2e", "回归"],
            "docs": ["文档", "docs", "说明", "readme", "规范"],
            "config": ["配置", "config", "设置", "settings", "hook", "脚本"],
        }

    def generate_variants(self, base_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成策略变体

        Args:
            base_strategy: 基础策略配置

        Returns:
            策略变体列表
        """
        variants = []

        # 变体 1: 高并行度策略
        variants.append(self._create_parallel_high_variant(base_strategy))

        # 变体 2: 细粒度任务分解策略
        variants.append(self._create_granular_variant(base_strategy))

        # 变体 3: 顺序执行策略
        variants.append(self._create_sequential_variant(base_strategy))

        # 变体 4: 混合策略
        variants.append(self._create_hybrid_variant(base_strategy))

        return variants

    def _create_parallel_high_variant(self, base: Dict[str, Any]) -> Dict[str, Any]:
        """创建高并行度变体"""
        return {
            "name": f"{base.get('name', 'default')}_parallel_high",
            "parallel_degree": "high",
            "description": "高并行度策略 - 最大化并行执行，适合独立任务多的场景",
            "config": {
                **base.get("config", {}),
                "max_parallel_agents": 5,
                "task_granularity": "coarse",
                "agent_distribution": {
                    "frontend-developer": 2,
                    "backend-developer": 3
                },
                "execution_mode": "parallel",
                "timeout": 300,
                "retry_count": 2
            },
            "advantages": [
                "执行速度快",
                "资源利用率高",
                "适合独立任务"
            ],
            "disadvantages": [
                "协调成本高",
                "可能出现冲突",
                "资源消耗大"
            ]
        }

    def _create_granular_variant(self, base: Dict[str, Any]) -> Dict[str, Any]:
        """创建细粒度任务分解变体"""
        return {
            "name": f"{base.get('name', 'default')}_granular",
            "parallel_degree": "medium",
            "description": "细粒度任务分解策略 - 更小的任务单元，便于控制和调试",
            "config": {
                **base.get("config", {}),
                "max_parallel_agents": 3,
                "task_granularity": "fine",
                "agent_distribution": {
                    "frontend-developer": 2,
                    "backend-developer": 2,
                    "test": 1
                },
                "execution_mode": "mixed",
                "timeout": 400,
                "retry_count": 3
            },
            "advantages": [
                "任务可控性强",
                "易于调试",
                "质量更高"
            ],
            "disadvantages": [
                "执行时间较长",
                "任务切换开销",
                "协调复杂度中等"
            ]
        }

    def _create_sequential_variant(self, base: Dict[str, Any]) -> Dict[str, Any]:
        """创建顺序执行变体"""
        return {
            "name": f"{base.get('name', 'default')}_sequential",
            "parallel_degree": "low",
            "description": "顺序执行策略 - 确保依赖关系，适合强依赖任务",
            "config": {
                **base.get("config", {}),
                "max_parallel_agents": 1,
                "task_granularity": "medium",
                "agent_distribution": {
                    "tech-lead": 1,
                    "frontend-developer": 1,
                    "backend-developer": 1,
                    "test": 1
                },
                "execution_mode": "sequential",
                "timeout": 600,
                "retry_count": 3
            },
            "advantages": [
                "依赖关系清晰",
                "冲突最少",
                "质量稳定"
            ],
            "disadvantages": [
                "执行时间最长",
                "资源利用率低",
                "不适合大型任务"
            ]
        }

    def _create_hybrid_variant(self, base: Dict[str, Any]) -> Dict[str, Any]:
        """创建混合策略变体"""
        return {
            "name": f"{base.get('name', 'default')}_hybrid",
            "parallel_degree": "adaptive",
            "description": "混合策略 - 根据任务复杂度动态调整，平衡速度和质量",
            "config": {
                **base.get("config", {}),
                "max_parallel_agents": 3,
                "task_granularity": "adaptive",
                "agent_distribution": {
                    "frontend-developer": 2,
                    "backend-developer": 2,
                    "test": 1
                },
                "execution_mode": "adaptive",
                "timeout": 450,
                "retry_count": 3,
                "adaptive_rules": {
                    "complexity_threshold": 7,
                    "parallel_if_independent": True,
                    "sequential_if_dependent": True
                }
            },
            "advantages": [
                "灵活性高",
                "平衡速度和质量",
                "适应性强"
            ],
            "disadvantages": [
                "决策复杂",
                "需要更多上下文",
                "可能不够极致"
            ]
        }

    def analyze_task_complexity(self, task_description: str) -> int:
        """
        分析任务复杂度

        Args:
            task_description: 任务描述

        Returns:
            复杂度分数 (1-10)
        """
        complexity = 5  # 默认中等复杂度

        # 关键词权重
        high_complexity_keywords = [
            "架构", "重构", "迁移", "集成", "分布式",
            "性能优化", "安全", "多模块", "复杂业务"
        ]
        medium_complexity_keywords = [
            "功能", "API", "数据库", "认证", "权限"
        ]
        low_complexity_keywords = [
            "修复", "样式", "文案", "配置", "简单"
        ]

        # 计算复杂度
        for keyword in high_complexity_keywords:
            if keyword in task_description:
                complexity += 1

        for keyword in medium_complexity_keywords:
            if keyword in task_description:
                complexity += 0.5

        for keyword in low_complexity_keywords:
            if keyword in task_description:
                complexity -= 1

        # 限制范围
        return max(1, min(10, int(complexity)))

    def recommend_strategy(self, task_description: str, complexity: int = None) -> str:
        """
        基于复杂度推荐策略（不含历史反馈）

        Args:
            task_description: 任务描述
            complexity: 任务复杂度（可选）

        Returns:
            推荐的策略名称
        """
        if complexity is None:
            complexity = self.analyze_task_complexity(task_description)

        # 根据复杂度推荐策略
        if complexity <= 3:
            return "sequential"  # 简单任务，顺序执行即可
        elif complexity <= 6:
            return "granular"    # 中等任务，细粒度分解
        elif complexity <= 8:
            return "hybrid"      # 复杂任务，混合策略
        else:
            return "parallel_high"  # 超复杂任务，高并行度

    def _infer_task_domain(self, task_description: str) -> str:
        """
        根据任务描述推断主要领域。
        """
        text = task_description.lower()
        scores = {k: 0 for k in self.domain_keywords}

        for domain, keywords in self.domain_keywords.items():
            for kw in keywords:
                if kw in text:
                    scores[domain] += 1

        best_domain = max(scores, key=scores.get)
        return best_domain if scores[best_domain] > 0 else "config"

    def _load_domain_weights(self, weights_file: Path = None) -> Dict[str, float]:
        """
        读取领域权重（由 Stop hook 的 EMA 维护）。
        """
        wf = weights_file or self.weights_file
        if not wf.exists():
            return {}

        try:
            with open(wf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return {}

        domain_weights: Dict[str, float] = {}
        for key in ("backend", "frontend", "tests", "docs", "config"):
            value = data.get(key)
            if isinstance(value, (int, float)):
                domain_weights[key] = float(value)
        return domain_weights

    def _upgrade_strategy(self, strategy: str) -> str:
        order = ["sequential", "granular", "hybrid", "parallel_high"]
        idx = order.index(strategy)
        return order[min(idx + 1, len(order) - 1)]

    def _downgrade_strategy(self, strategy: str) -> str:
        order = ["sequential", "granular", "hybrid", "parallel_high"]
        idx = order.index(strategy)
        return order[max(idx - 1, 0)]

    def recommend_strategy_with_feedback(
        self,
        task_description: str,
        complexity: int = None,
        weights_file: Path = None
    ) -> Dict[str, Any]:
        """
        在复杂度基线推荐上叠加 EMA 历史反馈，输出最终策略。
        """
        if complexity is None:
            complexity = self.analyze_task_complexity(task_description)

        base_strategy = self.recommend_strategy(task_description, complexity)
        domain = self._infer_task_domain(task_description)
        domain_weights = self._load_domain_weights(weights_file)
        domain_weight = domain_weights.get(domain, 5.0)
        final_strategy = base_strategy
        reason = "复杂度基线策略"

        # 反馈偏置：高权重时更积极，低权重时更保守
        if domain_weight >= 6.5 and complexity >= 5:
            final_strategy = self._upgrade_strategy(base_strategy)
            reason = f"{domain} 领域历史表现较强（{domain_weight:.2f}），策略上调一级"
        elif domain_weight <= 4.5 and complexity <= 8:
            final_strategy = self._downgrade_strategy(base_strategy)
            reason = f"{domain} 领域历史表现偏弱（{domain_weight:.2f}），策略下调一级"

        return {
            "complexity": complexity,
            "domain": domain,
            "domain_weight": round(domain_weight, 2),
            "base_strategy": base_strategy,
            "final_strategy": final_strategy,
            "reason": reason,
            "weights_file": str((weights_file or self.weights_file)),
        }

    def export_to_json(self, variants: List[Dict[str, Any]], output_path: str = None):
        """
        导出变体到 JSON 文件

        Args:
            variants: 策略变体列表
            output_path: 输出文件路径
        """
        if output_path is None:
            output_path = Path(__file__).parent.parent / "strategy_variants.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(variants, f, indent=2, ensure_ascii=False)

        print(f"✅ 策略变体已导出到: {output_path}")


def main():
    """主函数"""
    generator = StrategyGenerator()

    # 基础策略
    base_strategy = {
        "name": "default",
        "config": {
            "timeout": 300,
            "retry_count": 3
        }
    }

    # 生成变体
    print("🔄 正在生成策略变体...")
    variants = generator.generate_variants(base_strategy)

    # 输出到控制台
    print("\n📊 生成的策略变体:\n")
    print(json.dumps(variants, indent=2, ensure_ascii=False))

    # 导出到文件
    generator.export_to_json(variants)

    # 示例：分析任务并推荐策略（复杂度 + EMA 反馈）
    if len(sys.argv) > 1:
        task_description = " ".join(sys.argv[1:])
        recommendation = generator.recommend_strategy_with_feedback(task_description)

        print(f"\n🎯 任务分析:")
        print(f"  任务描述: {task_description}")
        print(f"  复杂度: {recommendation['complexity']}/10")
        print(f"  任务领域: {recommendation['domain']}")
        print(f"  领域权重: {recommendation['domain_weight']}")
        print(f"  基线策略: {recommendation['base_strategy']}")
        print(f"  最终策略: {recommendation['final_strategy']}")
        print(f"  调整原因: {recommendation['reason']}")


if __name__ == "__main__":
    main()
