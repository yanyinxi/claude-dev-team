#!/usr/bin/env python3
"""
触发器管理器
Trigger Manager

功能：
1. 统一管理所有触发器
2. 启动/停止所有触发器
3. 状态监控和报告
4. 配置加载和验证
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .time_based import TimeBasedTrigger
from .event_based import EventBasedTrigger
from .metric_based import MetricBasedTrigger
from .llm_driven import LLMDrivenTrigger
from ..core.logging_utils import get_logger, AuditLogger
from ..core.task_queue import TaskQueue
from ..database.init_db import DatabaseManager


class TriggerManager:
    """触发器管理器"""

    def __init__(self, config_path: str = ".claude/autonomous/config/autonomous_config.yaml"):
        """
        初始化触发器管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.logger = get_logger("trigger_manager", log_file=".claude/autonomous/logs/manager.log")
        self.audit_logger = AuditLogger()

        # 加载配置
        self.config = self._load_config()

        # 初始化依赖
        self.db_manager = DatabaseManager()
        self.db_manager.initialize()
        self.task_queue = TaskQueue()

        # 初始化触发器
        self.triggers: Dict[str, Any] = {}
        self._initialize_triggers()

    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件

        Returns:
            Dict[str, Any]: 配置字典
        """
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                self.logger.error(f"Config file not found: {self.config_path}")
                return {}

            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            self.logger.info(
                "Configuration loaded successfully",
                context={"config_path": self.config_path}
            )

            return config

        except Exception as e:
            self.logger.exception(
                "Failed to load configuration",
                context={"config_path": self.config_path, "error": str(e)}
            )
            return {}

    def _initialize_triggers(self):
        """初始化所有触发器"""
        task_generation_config = self.config.get("task_generation", {})

        # 初始化时间触发器
        time_based_config = task_generation_config.get("time_based", {})
        if time_based_config.get("enabled", False):
            try:
                self.triggers["time_based"] = TimeBasedTrigger(
                    config=time_based_config,
                    task_queue=self.task_queue,
                    db_manager=self.db_manager
                )
                self.logger.info("Time-based trigger initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize time-based trigger: {e}")

        # 初始化事件触发器
        event_based_config = task_generation_config.get("event_based", {})
        if event_based_config.get("enabled", False):
            try:
                self.triggers["event_based"] = EventBasedTrigger(
                    config=event_based_config,
                    task_queue=self.task_queue,
                    db_manager=self.db_manager
                )
                self.logger.info("Event-based trigger initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize event-based trigger: {e}")

        # 初始化指标触发器
        metric_based_config = task_generation_config.get("metric_based", {})
        if metric_based_config.get("enabled", False):
            try:
                self.triggers["metric_based"] = MetricBasedTrigger(
                    config=metric_based_config,
                    task_queue=self.task_queue,
                    db_manager=self.db_manager
                )
                self.logger.info("Metric-based trigger initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize metric-based trigger: {e}")

        # 初始化 LLM 触发器
        llm_driven_config = task_generation_config.get("llm_driven", {})
        if llm_driven_config.get("enabled", False):
            try:
                self.triggers["llm_driven"] = LLMDrivenTrigger(
                    config=llm_driven_config,
                    task_queue=self.task_queue,
                    db_manager=self.db_manager
                )
                self.logger.info("LLM-driven trigger initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize LLM-driven trigger: {e}")

        self.logger.info(
            "All triggers initialized",
            context={"triggers_count": len(self.triggers)}
        )

    def start_all(self):
        """启动所有触发器"""
        self.logger.info("Starting all triggers...")
        self.audit_logger.log_event(
            event_type="system_started",
            description="Autonomous evolution system started"
        )

        for trigger_name, trigger in self.triggers.items():
            try:
                trigger.start()
                self.logger.info(f"Started trigger: {trigger_name}")
            except Exception as e:
                self.logger.error(f"Failed to start trigger {trigger_name}: {e}")

        self.logger.info(
            "All triggers started",
            context={"triggers_count": len(self.triggers)}
        )

    def stop_all(self):
        """停止所有触发器"""
        self.logger.info("Stopping all triggers...")
        self.audit_logger.log_event(
            event_type="system_stopped",
            description="Autonomous evolution system stopped"
        )

        for trigger_name, trigger in self.triggers.items():
            try:
                trigger.stop()
                self.logger.info(f"Stopped trigger: {trigger_name}")
            except Exception as e:
                self.logger.error(f"Failed to stop trigger {trigger_name}: {e}")

        self.logger.info(
            "All triggers stopped",
            context={"triggers_count": len(self.triggers)}
        )

    def get_trigger(self, trigger_name: str) -> Optional[Any]:
        """
        获取指定触发器

        Args:
            trigger_name: 触发器名称

        Returns:
            Optional[Any]: 触发器实例
        """
        return self.triggers.get(trigger_name)

    def get_status(self) -> Dict[str, Any]:
        """
        获取所有触发器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "triggers": {},
            "task_queue": self.task_queue.get_statistics()
        }

        for trigger_name, trigger in self.triggers.items():
            try:
                status["triggers"][trigger_name] = trigger.get_status()
            except Exception as e:
                self.logger.error(f"Failed to get status for {trigger_name}: {e}")
                status["triggers"][trigger_name] = {"error": str(e)}

        return status

    def get_task_queue(self) -> TaskQueue:
        """
        获取任务队列实例

        Returns:
            TaskQueue: 任务队列
        """
        return self.task_queue

    def get_db_manager(self) -> DatabaseManager:
        """
        获取数据库管理器实例

        Returns:
            DatabaseManager: 数据库管理器
        """
        return self.db_manager


def main():
    """测试触发器管理器"""
    print("🧪 Testing Trigger Manager...")

    # 创建管理器
    manager = TriggerManager()

    # 获取状态
    status = manager.get_status()
    print(f"\n📊 System Status:")
    print(f"  Timestamp: {status['timestamp']}")
    print(f"\n🎯 Triggers:")
    for trigger_name, trigger_status in status["triggers"].items():
        print(f"  - {trigger_name}:")
        print(f"      Enabled: {trigger_status.get('enabled', False)}")
        print(f"      Running: {trigger_status.get('running', False)}")

    print(f"\n📋 Task Queue:")
    queue_stats = status["task_queue"]
    print(f"  Total tasks: {queue_stats['total_tasks']}")
    print(f"  Ready tasks: {queue_stats['ready_tasks']}")

    # 启动所有触发器
    print(f"\n🚀 Starting all triggers...")
    manager.start_all()

    # 等待一段时间
    import time
    print(f"\n⏳ Running for 10 seconds...")
    time.sleep(10)

    # 获取更新后的状态
    status = manager.get_status()
    print(f"\n📊 Updated Status:")
    print(f"  Task Queue:")
    queue_stats = status["task_queue"]
    print(f"    Total tasks: {queue_stats['total_tasks']}")
    print(f"    Ready tasks: {queue_stats['ready_tasks']}")

    # 停止所有触发器
    print(f"\n🛑 Stopping all triggers...")
    manager.stop_all()

    print("\n✅ Trigger manager test completed!")


if __name__ == "__main__":
    main()
