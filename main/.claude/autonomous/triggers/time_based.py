#!/usr/bin/env python3
"""
基于时间的任务触发器
Time-Based Task Trigger

功能：
1. Cron 表达式解析
2. 定时任务调度
3. 任务生成和入队
4. 与配置文件集成
"""

import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from croniter import croniter
import threading
import time

from ..core.logging_utils import get_logger
from ..core.task_queue import TaskQueue
from ..database.init_db import DatabaseManager, TaskRepository


class TimeBasedTrigger:
    """基于时间的任务触发器"""

    def __init__(
        self,
        config: Dict[str, Any],
        task_queue: TaskQueue,
        db_manager: DatabaseManager
    ):
        """
        初始化时间触发器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            task_queue: 任务队列实例
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.task_queue = task_queue
        self.task_repo = TaskRepository(db_manager)
        self.logger = get_logger("time_based_trigger", log_file=".claude/autonomous/logs/triggers.log")

        # 解析配置
        self.enabled = config.get("enabled", True)
        self.schedules = config.get("schedules", [])

        # 调度状态
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.next_run_times: Dict[str, datetime] = {}

        # 初始化下次运行时间
        self._initialize_next_run_times()

    def _initialize_next_run_times(self):
        """初始化所有任务的下次运行时间"""
        now = datetime.now()
        for schedule in self.schedules:
            name = schedule["name"]
            cron = schedule["cron"]

            try:
                cron_iter = croniter(cron, now)
                next_run = cron_iter.get_next(datetime)
                self.next_run_times[name] = next_run

                self.logger.info(
                    f"Initialized schedule: {name}",
                    context={
                        "name": name,
                        "cron": cron,
                        "next_run": next_run.isoformat()
                    }
                )
            except Exception as e:
                self.logger.error(
                    f"Failed to parse cron expression for {name}",
                    context={"name": name, "cron": cron, "error": str(e)}
                )

    def start(self):
        """启动时间触发器"""
        if not self.enabled:
            self.logger.info("Time-based trigger is disabled")
            return

        if self.running:
            self.logger.warning("Time-based trigger is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

        self.logger.info(
            "Time-based trigger started",
            context={"schedules_count": len(self.schedules)}
        )

    def stop(self):
        """停止时间触发器"""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

        self.logger.info("Time-based trigger stopped")

    def _run_loop(self):
        """主循环：检查并触发到期任务"""
        while self.running:
            try:
                now = datetime.now()

                # 检查每个调度任务
                for schedule in self.schedules:
                    name = schedule["name"]
                    next_run = self.next_run_times.get(name)

                    if next_run and now >= next_run:
                        # 触发任务
                        self._trigger_task(schedule)

                        # 更新下次运行时间
                        cron = schedule["cron"]
                        cron_iter = croniter(cron, now)
                        self.next_run_times[name] = cron_iter.get_next(datetime)

                # 休眠 1 分钟后再检查
                time.sleep(60)

            except Exception as e:
                self.logger.exception(
                    "Error in time-based trigger loop",
                    context={"error": str(e)}
                )
                time.sleep(60)

    def _trigger_task(self, schedule: Dict[str, Any]):
        """
        触发任务

        Args:
            schedule: 调度配置
        """
        name = schedule["name"]
        description = schedule["description"]
        priority = schedule["priority"]

        # 生成任务 ID
        task_id = f"time-{name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        try:
            # 创建任务元数据
            metadata = {
                "trigger_type": "time_based",
                "schedule_name": name,
                "cron": schedule["cron"],
                "triggered_at": datetime.now().isoformat()
            }

            # 添加到数据库
            success = self.task_repo.create_task(
                task_id=task_id,
                task_type="time_based",
                description=description,
                priority=priority,
                scheduled_at=datetime.now(),
                metadata=metadata
            )

            if success:
                # 添加到内存队列
                self.task_queue.add_task(
                    task_id=task_id,
                    task_type="time_based",
                    description=description,
                    priority=priority,
                    scheduled_at=datetime.now(),
                    metadata=metadata
                )

                self.logger.info(
                    f"Task triggered: {task_id}",
                    context={
                        "task_id": task_id,
                        "schedule_name": name,
                        "priority": priority
                    }
                )
            else:
                self.logger.error(
                    f"Failed to create task in database: {task_id}",
                    context={"task_id": task_id, "schedule_name": name}
                )

        except Exception as e:
            self.logger.exception(
                f"Failed to trigger task for schedule {name}",
                context={"schedule_name": name, "error": str(e)}
            )

    def get_next_run_times(self) -> Dict[str, str]:
        """
        获取所有调度任务的下次运行时间

        Returns:
            Dict[str, str]: 任务名称 -> 下次运行时间（ISO 格式）
        """
        return {
            name: next_run.isoformat()
            for name, next_run in self.next_run_times.items()
        }

    def get_status(self) -> Dict[str, Any]:
        """
        获取触发器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "enabled": self.enabled,
            "running": self.running,
            "schedules_count": len(self.schedules),
            "next_run_times": self.get_next_run_times()
        }


def main():
    """测试时间触发器"""
    print("🧪 Testing Time-Based Trigger...")

    # 模拟配置
    config = {
        "enabled": True,
        "schedules": [
            {
                "name": "test_every_minute",
                "cron": "* * * * *",  # 每分钟
                "description": "Test task every minute",
                "priority": 5
            },
            {
                "name": "test_every_5_minutes",
                "cron": "*/5 * * * *",  # 每 5 分钟
                "description": "Test task every 5 minutes",
                "priority": 7
            }
        ]
    }

    # 创建依赖
    task_queue = TaskQueue()
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建触发器
    trigger = TimeBasedTrigger(config, task_queue, db_manager)

    # 获取状态
    status = trigger.get_status()
    print(f"\n📊 Trigger Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Running: {status['running']}")
    print(f"  Schedules: {status['schedules_count']}")
    print(f"\n⏰ Next Run Times:")
    for name, next_run in status['next_run_times'].items():
        print(f"  - {name}: {next_run}")

    # 启动触发器（测试模式：运行 2 分钟后停止）
    print(f"\n🚀 Starting trigger for 2 minutes...")
    trigger.start()

    try:
        time.sleep(120)  # 运行 2 分钟
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")

    # 停止触发器
    trigger.stop()

    # 检查队列
    print(f"\n📋 Task Queue Status:")
    stats = task_queue.get_statistics()
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Ready tasks: {stats['ready_tasks']}")

    print("\n✅ Time-based trigger test completed!")


if __name__ == "__main__":
    main()
