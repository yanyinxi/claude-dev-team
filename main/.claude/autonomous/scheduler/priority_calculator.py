#!/usr/bin/env python3
"""
优先级计算器
Priority Calculator

功能：
1. 计算任务优先级
2. 考虑多个因素（紧急度、影响力、依赖关系、资源可用性）
3. 动态调整优先级
4. 与策略权重集成
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core.logging_utils import get_logger


class PriorityCalculator:
    """优先级计算器"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化优先级计算器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
        """
        self.config = config
        self.logger = get_logger("priority_calculator", log_file=".claude/autonomous/logs/scheduler.log")

        # 加载策略权重
        self.strategy_weights = self._load_strategy_weights()

        # 优先级公式配置
        self.priority_formula = config.get("priority_formula", "base_priority * urgency_multiplier * resource_availability")

    def _load_strategy_weights(self) -> Dict[str, float]:
        """
        加载策略权重（从 AlphaZero 学习系统）

        Returns:
            Dict[str, float]: 策略权重
        """
        weights_file = Path(".claude/strategy_weights.json")

        if weights_file.exists():
            try:
                with open(weights_file, 'r', encoding='utf-8') as f:
                    weights = json.load(f)
                self.logger.info("Strategy weights loaded successfully")
                return weights
            except Exception as e:
                self.logger.error(f"Failed to load strategy weights: {e}")

        # 默认权重
        return {
            "frontend": 7.5,
            "backend": 7.6,
            "collaboration": 8.0,
            "testing": 7.0,
            "code-quality": 7.5,
            "evolution": 8.0,
            "general": 7.0
        }

    def calculate_priority(
        self,
        task: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        计算任务优先级

        Args:
            task: 任务信息
            context: 上下文信息（当前队列状态、资源可用性等）

        Returns:
            float: 计算后的优先级（0-10）
        """
        # 基础优先级
        base_priority = task.get("priority", 5)

        # 计算各个因素
        urgency_multiplier = self._calculate_urgency(task)
        impact_score = self._calculate_impact(task)
        dependency_score = self._calculate_dependency(task, context)
        resource_availability = self._calculate_resource_availability(task, context)
        strategy_weight = self._get_strategy_weight(task)

        # 综合计算
        final_priority = (
            base_priority * 0.3 +
            urgency_multiplier * 2.0 +
            impact_score * 1.5 +
            dependency_score * 1.0 +
            resource_availability * 0.5 +
            strategy_weight * 0.2
        )

        # 归一化到 0-10
        final_priority = max(0, min(10, final_priority))

        self.logger.debug(
            f"Priority calculated for task {task.get('task_id')}",
            context={
                "base_priority": base_priority,
                "urgency": urgency_multiplier,
                "impact": impact_score,
                "dependency": dependency_score,
                "resource": resource_availability,
                "strategy_weight": strategy_weight,
                "final_priority": final_priority
            }
        )

        return final_priority

    def _calculate_urgency(self, task: Dict[str, Any]) -> float:
        """
        计算紧急度

        Args:
            task: 任务信息

        Returns:
            float: 紧急度分数（0-3）
        """
        scheduled_at = task.get("scheduled_at")
        if not scheduled_at:
            return 1.0

        # 解析时间
        if isinstance(scheduled_at, str):
            scheduled_at = datetime.fromisoformat(scheduled_at)

        now = datetime.now()
        time_diff = (scheduled_at - now).total_seconds()

        # 已过期：最高紧急度
        if time_diff < 0:
            return 3.0

        # 1 小时内：高紧急度
        if time_diff < 3600:
            return 2.5

        # 1 天内：中等紧急度
        if time_diff < 86400:
            return 2.0

        # 1 周内：低紧急度
        if time_diff < 604800:
            return 1.5

        # 更远：最低紧急度
        return 1.0

    def _calculate_impact(self, task: Dict[str, Any]) -> float:
        """
        计算影响力

        Args:
            task: 任务信息

        Returns:
            float: 影响力分数（0-3）
        """
        task_type = task.get("task_type", "general")
        metadata = task.get("metadata", {})

        # 根据任务类型评估影响力
        impact_map = {
            "metric_based": 3.0,      # 指标触发：高影响（系统问题）
            "llm_driven": 2.5,        # LLM 驱动：中高影响（智能分析）
            "event_based": 2.0,       # 事件触发：中等影响（响应事件）
            "time_based": 1.5         # 时间触发：低影响（常规任务）
        }

        base_impact = impact_map.get(task_type, 2.0)

        # 根据元数据调整
        if metadata.get("critical", False):
            base_impact *= 1.5

        if metadata.get("affects_production", False):
            base_impact *= 1.3

        return min(3.0, base_impact)

    def _calculate_dependency(
        self,
        task: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        计算依赖关系分数

        Args:
            task: 任务信息
            context: 上下文信息

        Returns:
            float: 依赖分数（0-2）
        """
        if not context:
            return 1.0

        # 检查是否有其他任务依赖此任务
        blocked_tasks = context.get("blocked_tasks", [])
        task_id = task.get("task_id")

        # 如果有任务被此任务阻塞，提高优先级
        blocking_count = sum(1 for t in blocked_tasks if t.get("blocked_by") == task_id)

        if blocking_count > 0:
            return 2.0 + (blocking_count * 0.2)

        return 1.0

    def _calculate_resource_availability(
        self,
        task: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        计算资源可用性

        Args:
            task: 任务信息
            context: 上下文信息

        Returns:
            float: 资源可用性分数（0-2）
        """
        if not context:
            return 1.0

        # 检查当前运行的任务数
        running_tasks = context.get("running_tasks", 0)
        max_concurrent = context.get("max_concurrent_tasks", 3)

        # 如果资源充足，提高优先级
        if running_tasks < max_concurrent:
            availability = (max_concurrent - running_tasks) / max_concurrent
            return 1.0 + availability
        else:
            return 0.5

    def _get_strategy_weight(self, task: Dict[str, Any]) -> float:
        """
        获取策略权重（从 AlphaZero 学习系统）

        Args:
            task: 任务信息

        Returns:
            float: 策略权重（0-10）
        """
        task_type = task.get("task_type", "general")
        metadata = task.get("metadata", {})

        # 尝试从元数据获取策略类型
        strategy_type = metadata.get("strategy_type", task_type)

        # 从策略权重中获取
        weight = self.strategy_weights.get(strategy_type, 7.0)

        return weight

    def batch_calculate(
        self,
        tasks: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        批量计算任务优先级

        Args:
            tasks: 任务列表
            context: 上下文信息

        Returns:
            List[Dict[str, Any]]: 带有计算后优先级的任务列表
        """
        results = []

        for task in tasks:
            calculated_priority = self.calculate_priority(task, context)
            task_with_priority = task.copy()
            task_with_priority["calculated_priority"] = calculated_priority
            results.append(task_with_priority)

        # 按优先级排序
        results.sort(key=lambda t: t["calculated_priority"], reverse=True)

        return results

    def get_status(self) -> Dict[str, Any]:
        """
        获取计算器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "priority_formula": self.priority_formula,
            "strategy_weights_loaded": len(self.strategy_weights) > 0,
            "strategy_weights": self.strategy_weights
        }


def main():
    """测试优先级计算器"""
    print("🧪 Testing Priority Calculator...")

    # 模拟配置
    config = {
        "priority_formula": "base_priority * urgency_multiplier * resource_availability"
    }

    # 创建计算器
    calculator = PriorityCalculator(config)

    # 模拟任务
    tasks = [
        {
            "task_id": "task-1",
            "task_type": "time_based",
            "priority": 5,
            "scheduled_at": (datetime.now() - timedelta(hours=1)).isoformat(),
            "metadata": {}
        },
        {
            "task_id": "task-2",
            "task_type": "metric_based",
            "priority": 9,
            "scheduled_at": datetime.now().isoformat(),
            "metadata": {"critical": True}
        },
        {
            "task_id": "task-3",
            "task_type": "llm_driven",
            "priority": 7,
            "scheduled_at": (datetime.now() + timedelta(hours=2)).isoformat(),
            "metadata": {}
        }
    ]

    # 模拟上下文
    context = {
        "running_tasks": 1,
        "max_concurrent_tasks": 3,
        "blocked_tasks": [
            {"task_id": "task-4", "blocked_by": "task-2"}
        ]
    }

    # 批量计算优先级
    print(f"\n🎯 Calculating priorities...")
    results = calculator.batch_calculate(tasks, context)

    # 打印结果
    print(f"\n📊 Priority Calculation Results:")
    for i, task in enumerate(results, 1):
        print(f"  {i}. {task['task_id']}:")
        print(f"      Type: {task['task_type']}")
        print(f"      Base Priority: {task['priority']}")
        print(f"      Calculated Priority: {task['calculated_priority']:.2f}")

    # 获取状态
    status = calculator.get_status()
    print(f"\n📊 Calculator Status:")
    print(f"  Formula: {status['priority_formula']}")
    print(f"  Strategy Weights Loaded: {status['strategy_weights_loaded']}")
    print(f"  Strategy Weights: {status['strategy_weights']}")

    print("\n✅ Priority calculator test completed!")


if __name__ == "__main__":
    main()
