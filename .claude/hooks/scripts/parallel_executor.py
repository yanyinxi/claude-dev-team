#!/usr/bin/env python3
"""
并行执行器 - AlphaZero 风格自博弈学习系统

功能：
1. 并行执行多个策略变体
2. 收集和对比执行结果
3. 选择最优策略
4. 更新策略权重
"""

import json
import asyncio
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class ParallelExecutor:
    """并行执行器 - 使用 asyncio 实现真正的并行"""

    def __init__(self):
        self.results_dir = Path(__file__).parent.parent / "execution_results"
        self.results_dir.mkdir(exist_ok=True)

    async def execute_variants(
        self,
        variants: List[Dict[str, Any]],
        task_description: str
    ) -> List[Dict[str, Any]]:
        """
        并行执行多个策略变体

        Args:
            variants: 策略变体列表
            task_description: 任务描述

        Returns:
            执行结果列表
        """
        print(f"\n🚀 开始并行执行 {len(variants)} 个策略变体...")
        print(f"📝 任务描述: {task_description}\n")

        # 创建并行任务
        tasks = []
        for i, variant in enumerate(variants):
            task = self._execute_single_variant(
                variant_id=i + 1,
                variant=variant,
                task_description=task_description
            )
            tasks.append(task)

        # 等待所有任务完成
        start_time = time.time()
        completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)
        total_duration = time.time() - start_time

        # 收集结果
        results = []
        for i, result in enumerate(completed_tasks):
            if isinstance(result, Exception):
                results.append({
                    "variant_id": i + 1,
                    "variant_name": variants[i]["name"],
                    "success": False,
                    "error": str(result),
                    "duration": 0,
                    "quality_score": 0
                })
            else:
                results.append(result)

        print(f"\n✅ 所有变体执行完成，总耗时: {total_duration:.2f}秒\n")

        # 保存结果
        self._save_results(results, task_description)

        return results

    async def _execute_single_variant(
        self,
        variant_id: int,
        variant: Dict[str, Any],
        task_description: str
    ) -> Dict[str, Any]:
        """
        执行单个策略变体

        Args:
            variant_id: 变体ID
            variant: 策略变体配置
            task_description: 任务描述

        Returns:
            执行结果
        """
        variant_name = variant["name"]
        print(f"🔄 变体 {variant_id} ({variant_name}) 开始执行...")

        start_time = time.time()

        try:
            # 模拟执行（实际应该调用 Claude Code 的 background_task API）
            result = await self._simulate_execution(variant, task_description)

            duration = time.time() - start_time

            # 计算质量分数
            quality_score = self._calculate_quality_score(result, variant)

            print(f"✅ 变体 {variant_id} ({variant_name}) 执行完成 - 得分: {quality_score:.1f}/10")

            return {
                "variant_id": variant_id,
                "variant_name": variant_name,
                "success": True,
                "duration": duration,
                "quality_score": quality_score,
                "result": result,
                "config": variant["config"]
            }

        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ 变体 {variant_id} ({variant_name}) 执行失败: {str(e)}")

            return {
                "variant_id": variant_id,
                "variant_name": variant_name,
                "success": False,
                "duration": duration,
                "quality_score": 0,
                "error": str(e)
            }

    async def _simulate_execution(
        self,
        variant: Dict[str, Any],
        task_description: str
    ) -> Dict[str, Any]:
        """
        模拟执行（实际应该调用 Claude Code API）

        Args:
            variant: 策略变体
            task_description: 任务描述

        Returns:
            执行结果
        """
        # 模拟执行时间（根据并行度调整）
        parallel_degree = variant.get("parallel_degree", "medium")
        if parallel_degree == "high":
            await asyncio.sleep(1.0)  # 高并行度，快速完成
        elif parallel_degree == "medium":
            await asyncio.sleep(1.5)  # 中等并行度
        elif parallel_degree == "low":
            await asyncio.sleep(2.0)  # 低并行度，慢速完成
        else:
            await asyncio.sleep(1.2)  # 自适应

        # 模拟执行结果
        return {
            "files_modified": 5,
            "tests_passed": 8,
            "tests_failed": 0,
            "code_quality": 8.5,
            "agent_coordination": 7.8,
            "task_completion": 9.0
        }

    def _calculate_quality_score(
        self,
        result: Dict[str, Any],
        variant: Dict[str, Any]
    ) -> float:
        """
        计算质量分数

        Args:
            result: 执行结果
            variant: 策略变体

        Returns:
            质量分数 (0-10)
        """
        # 权重配置
        weights = {
            "code_quality": 0.3,
            "task_completion": 0.3,
            "agent_coordination": 0.2,
            "test_pass_rate": 0.2
        }

        # 计算测试通过率
        tests_passed = result.get("tests_passed", 0)
        tests_failed = result.get("tests_failed", 0)
        total_tests = tests_passed + tests_failed
        test_pass_rate = (tests_passed / total_tests * 10) if total_tests > 0 else 8.0

        # 加权计算
        score = (
            result.get("code_quality", 8.0) * weights["code_quality"] +
            result.get("task_completion", 8.0) * weights["task_completion"] +
            result.get("agent_coordination", 7.0) * weights["agent_coordination"] +
            test_pass_rate * weights["test_pass_rate"]
        )

        # 根据并行度调整分数
        parallel_degree = variant.get("parallel_degree", "medium")
        if parallel_degree == "high":
            score *= 1.1  # 高并行度加分
        elif parallel_degree == "low":
            score *= 0.95  # 低并行度减分

        return min(10.0, max(0.0, score))

    def compare_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        对比结果，选择最优策略

        Args:
            results: 执行结果列表

        Returns:
            对比分析结果
        """
        print("\n📊 对比分析结果:\n")

        # 过滤成功的结果
        successful_results = [r for r in results if r["success"]]

        if not successful_results:
            return {
                "best_variant": None,
                "best_score": 0,
                "analysis": "所有变体执行失败",
                "all_results": results
            }

        # 找到最佳变体
        best_result = max(successful_results, key=lambda x: x["quality_score"])

        # 打印对比表格
        print("| 变体ID | 变体名称 | 得分 | 耗时(秒) | 状态 |")
        print("|--------|----------|------|----------|------|")
        for r in results:
            status = "✅" if r["success"] else "❌"
            print(f"| {r['variant_id']} | {r['variant_name'][:20]} | "
                  f"{r['quality_score']:.1f}/10 | {r['duration']:.2f} | {status} |")

        print(f"\n🏆 最佳变体: {best_result['variant_name']} (得分: {best_result['quality_score']:.1f}/10)")

        # 分析优势和劣势
        analysis = self._analyze_results(successful_results, best_result)

        return {
            "best_variant": best_result["variant_name"],
            "best_variant_id": best_result["variant_id"],
            "best_score": best_result["quality_score"],
            "analysis": analysis,
            "all_results": results
        }

    def _analyze_results(
        self,
        successful_results: List[Dict[str, Any]],
        best_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        分析结果

        Args:
            successful_results: 成功的结果列表
            best_result: 最佳结果

        Returns:
            分析结果
        """
        # 计算平均分数
        avg_score = sum(r["quality_score"] for r in successful_results) / len(successful_results)

        # 提取优势
        strengths = []
        if best_result["quality_score"] > avg_score + 1:
            strengths.append("质量显著高于平均水平")
        if best_result["duration"] < 2.0:
            strengths.append("执行速度快")

        # 提取劣势
        weaknesses = []
        if best_result["duration"] > 2.5:
            weaknesses.append("执行时间较长")

        # 提取最佳实践
        best_practices = []
        config = best_result.get("config", {})
        if config.get("max_parallel_agents", 0) >= 3:
            best_practices.append("适度并行提升效率")
        if config.get("task_granularity") == "fine":
            best_practices.append("细粒度任务分解提高质量")

        return {
            "avg_score": avg_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "best_practices": best_practices
        }

    def _save_results(self, results: List[Dict[str, Any]], task_description: str):
        """
        保存执行结果

        Args:
            results: 执行结果列表
            task_description: 任务描述
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"execution_{timestamp}.json"
        filepath = self.results_dir / filename

        data = {
            "timestamp": timestamp,
            "task_description": task_description,
            "results": results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"💾 结果已保存到: {filepath}")

    def update_strategy_weights(
        self,
        best_variant_name: str,
        best_score: float,
        weights_file: str = None
    ):
        """
        更新策略权重（指数移动平均）

        Args:
            best_variant_name: 最佳变体名称
            best_score: 最佳分数
            weights_file: 权重文件路径
        """
        if weights_file is None:
            weights_file = Path(__file__).parent.parent / "strategy_weights.json"

        # 读取现有权重
        if Path(weights_file).exists():
            with open(weights_file, 'r', encoding='utf-8') as f:
                weights = json.load(f)
        else:
            weights = {}

        # 提取策略类型（去掉 _default 后缀）
        strategy_type = best_variant_name.replace("_default", "").replace("default_", "")

        # 更新权重（指数移动平均，alpha=0.3）
        alpha = 0.3
        current_weight = weights.get(strategy_type, 5.0)
        new_weight = alpha * best_score + (1 - alpha) * current_weight

        weights[strategy_type] = round(new_weight, 2)
        weights["last_updated"] = datetime.now().isoformat()

        # 保存权重
        with open(weights_file, 'w', encoding='utf-8') as f:
            json.dump(weights, f, indent=2, ensure_ascii=False)

        print(f"\n📈 策略权重已更新:")
        print(f"  {strategy_type}: {current_weight:.2f} → {new_weight:.2f}")


async def main():
    """主函数"""
    executor = ParallelExecutor()

    # 示例变体
    variants = [
        {
            "name": "default_parallel_high",
            "parallel_degree": "high",
            "config": {"max_parallel_agents": 5}
        },
        {
            "name": "default_granular",
            "parallel_degree": "medium",
            "config": {"max_parallel_agents": 3, "task_granularity": "fine"}
        },
        {
            "name": "default_sequential",
            "parallel_degree": "low",
            "config": {"max_parallel_agents": 1}
        },
        {
            "name": "default_hybrid",
            "parallel_degree": "adaptive",
            "config": {"max_parallel_agents": 3, "task_granularity": "adaptive"}
        }
    ]

    # 执行
    results = await executor.execute_variants(variants, "实现用户登录功能")

    # 对比
    comparison = executor.compare_results(results)

    # 更新权重
    if comparison["best_variant"]:
        executor.update_strategy_weights(
            comparison["best_variant"],
            comparison["best_score"]
        )

    # 输出完整结果
    print("\n📋 完整对比结果:")
    print(json.dumps(comparison, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
