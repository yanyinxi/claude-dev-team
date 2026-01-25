#!/usr/bin/env python3
"""
基于指标的任务触发器
Metric-Based Task Trigger

功能：
1. 系统指标监控
2. 阈值检测
3. 异常识别
4. 任务生成和入队
"""

import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable
import threading

from ..core.logging_utils import get_logger
from ..core.task_queue import TaskQueue
from ..database.init_db import DatabaseManager, TaskRepository, MetricsRepository


class MetricBasedTrigger:
    """基于指标的任务触发器"""

    def __init__(
        self,
        config: Dict[str, Any],
        task_queue: TaskQueue,
        db_manager: DatabaseManager
    ):
        """
        初始化指标触发器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            task_queue: 任务队列实例
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.task_queue = task_queue
        self.task_repo = TaskRepository(db_manager)
        self.metrics_repo = MetricsRepository(db_manager)
        self.logger = get_logger("metric_based_trigger", log_file=".claude/autonomous/logs/triggers.log")

        # 解析配置
        self.enabled = config.get("enabled", True)
        self.thresholds = config.get("thresholds", [])
        self.check_interval = 60  # 检查间隔（秒）

        # 运行状态
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # 触发历史（防止重复触发）
        self.last_triggered: Dict[str, datetime] = {}
        self.cooldown_period = timedelta(minutes=5)  # 冷却期

        # 操作符映射
        self.operators: Dict[str, Callable] = {
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
        }

    def start(self):
        """启动指标触发器"""
        if not self.enabled:
            self.logger.info("Metric-based trigger is disabled")
            return

        if self.running:
            self.logger.warning("Metric-based trigger is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

        self.logger.info(
            "Metric-based trigger started",
            context={"thresholds_count": len(self.thresholds)}
        )

    def stop(self):
        """停止指标触发器"""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

        self.logger.info("Metric-based trigger stopped")

    def _monitor_loop(self):
        """监控循环：检查指标并触发任务"""
        while self.running:
            try:
                # 检查每个阈值配置
                for threshold_config in self.thresholds:
                    self._check_threshold(threshold_config)

                # 休眠后再检查
                time.sleep(self.check_interval)

            except Exception as e:
                self.logger.exception(
                    "Error in metric-based trigger loop",
                    context={"error": str(e)}
                )
                time.sleep(self.check_interval)

    def _check_threshold(self, threshold_config: Dict[str, Any]):
        """
        检查阈值

        Args:
            threshold_config: 阈值配置
        """
        name = threshold_config["name"]
        metric_name = threshold_config["metric"]
        threshold_value = threshold_config["threshold"]
        operator = threshold_config["operator"]
        description = threshold_config["description"]
        priority = threshold_config["priority"]

        try:
            # 获取最近的指标值
            recent_metrics = self.metrics_repo.get_recent_metrics(metric_name, days=1)

            if not recent_metrics:
                self.logger.debug(
                    f"No recent metrics found for {metric_name}",
                    context={"metric_name": metric_name}
                )
                return

            # 获取最新值
            latest_metric = recent_metrics[0]
            current_value = latest_metric["metric_value"]

            # 检查阈值
            operator_func = self.operators.get(operator)
            if not operator_func:
                self.logger.error(
                    f"Invalid operator: {operator}",
                    context={"operator": operator, "threshold_name": name}
                )
                return

            if operator_func(current_value, threshold_value):
                # 阈值触发
                self._trigger_threshold_task(
                    threshold_config,
                    current_value,
                    threshold_value
                )

        except Exception as e:
            self.logger.exception(
                f"Failed to check threshold {name}",
                context={"threshold_name": name, "error": str(e)}
            )

    def _trigger_threshold_task(
        self,
        threshold_config: Dict[str, Any],
        current_value: float,
        threshold_value: float
    ):
        """
        触发阈值任务

        Args:
            threshold_config: 阈值配置
            current_value: 当前值
            threshold_value: 阈值
        """
        name = threshold_config["name"]
        metric_name = threshold_config["metric"]
        operator = threshold_config["operator"]
        description = threshold_config["description"]
        priority = threshold_config["priority"]

        # 检查冷却期
        now = datetime.now()
        last_triggered = self.last_triggered.get(name)
        if last_triggered and (now - last_triggered) < self.cooldown_period:
            self.logger.debug(
                f"Threshold {name} in cooldown period",
                context={
                    "threshold_name": name,
                    "last_triggered": last_triggered.isoformat()
                }
            )
            return

        # 生成任务 ID
        task_id = f"metric-{name}-{now.strftime('%Y%m%d%H%M%S')}"

        try:
            # 创建任务元数据
            metadata = {
                "trigger_type": "metric_based",
                "threshold_name": name,
                "metric_name": metric_name,
                "current_value": current_value,
                "threshold_value": threshold_value,
                "operator": operator,
                "triggered_at": now.isoformat()
            }

            # 添加到数据库
            success = self.task_repo.create_task(
                task_id=task_id,
                task_type="metric_based",
                description=f"{description} (current: {current_value}, threshold: {threshold_value})",
                priority=priority,
                scheduled_at=now,
                metadata=metadata
            )

            if success:
                # 添加到内存队列
                self.task_queue.add_task(
                    task_id=task_id,
                    task_type="metric_based",
                    description=f"{description} (current: {current_value}, threshold: {threshold_value})",
                    priority=priority,
                    scheduled_at=now,
                    metadata=metadata
                )

                # 更新触发历史
                self.last_triggered[name] = now

                self.logger.info(
                    f"Threshold task triggered: {task_id}",
                    context={
                        "task_id": task_id,
                        "threshold_name": name,
                        "current_value": current_value,
                        "threshold_value": threshold_value,
                        "priority": priority
                    }
                )
            else:
                self.logger.error(
                    f"Failed to create task in database: {task_id}",
                    context={"task_id": task_id, "threshold_name": name}
                )

        except Exception as e:
            self.logger.exception(
                f"Failed to trigger threshold task for {name}",
                context={"threshold_name": name, "error": str(e)}
            )

    def record_metric(self, metric_name: str, metric_value: float, metadata: Optional[Dict] = None):
        """
        记录指标值

        Args:
            metric_name: 指标名称
            metric_value: 指标值
            metadata: 额外元数据
        """
        try:
            success = self.metrics_repo.record_metric(
                metric_name=metric_name,
                metric_value=metric_value,
                metadata=metadata
            )

            if success:
                self.logger.debug(
                    f"Metric recorded: {metric_name}",
                    context={
                        "metric_name": metric_name,
                        "metric_value": metric_value
                    }
                )
            else:
                self.logger.error(
                    f"Failed to record metric: {metric_name}",
                    context={"metric_name": metric_name}
                )

        except Exception as e:
            self.logger.exception(
                f"Failed to record metric {metric_name}",
                context={"metric_name": metric_name, "error": str(e)}
            )

    def get_status(self) -> Dict[str, Any]:
        """
        获取触发器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "enabled": self.enabled,
            "running": self.running,
            "thresholds_count": len(self.thresholds),
            "check_interval": self.check_interval,
            "last_triggered": {
                name: timestamp.isoformat()
                for name, timestamp in self.last_triggered.items()
            }
        }


def main():
    """测试指标触发器"""
    print("🧪 Testing Metric-Based Trigger...")

    # 模拟配置
    config = {
        "enabled": True,
        "thresholds": [
            {
                "name": "high_error_rate",
                "metric": "error_rate",
                "threshold": 0.05,
                "operator": ">",
                "description": "错误率过高",
                "priority": 9
            },
            {
                "name": "slow_response_time",
                "metric": "response_time_ms",
                "threshold": 500,
                "operator": ">",
                "description": "响应时间过慢",
                "priority": 7
            }
        ]
    }

    # 创建依赖
    task_queue = TaskQueue()
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建触发器
    trigger = MetricBasedTrigger(config, task_queue, db_manager)

    # 记录一些测试指标
    print(f"\n📊 Recording test metrics...")
    trigger.record_metric("error_rate", 0.02)  # 正常
    trigger.record_metric("error_rate", 0.08)  # 超过阈值
    trigger.record_metric("response_time_ms", 300)  # 正常
    trigger.record_metric("response_time_ms", 600)  # 超过阈值

    # 启动触发器
    trigger.start()

    # 获取状态
    status = trigger.get_status()
    print(f"\n📊 Trigger Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Running: {status['running']}")
    print(f"  Thresholds: {status['thresholds_count']}")

    # 等待检查
    print(f"\n⏳ Waiting for threshold checks...")
    time.sleep(5)

    # 检查队列
    print(f"\n📋 Task Queue Status:")
    stats = task_queue.get_statistics()
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Ready tasks: {stats['ready_tasks']}")

    # 停止触发器
    trigger.stop()

    print("\n✅ Metric-based trigger test completed!")


if __name__ == "__main__":
    main()
