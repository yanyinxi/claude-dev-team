#!/usr/bin/env python3
"""
资源管理器
Resource Manager

功能：
1. 管理并发任务数量
2. 执行速率限制
3. 跟踪资源可用性
4. 与优先级计算器和冲突检测器集成
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import deque
import threading

from ..core.logging_utils import get_logger


class ResourceManager:
    """资源管理器"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化资源管理器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
        """
        self.config = config
        self.logger = get_logger("resource_manager", log_file=".claude/autonomous/logs/scheduler.log")

        # 并发控制配置
        self.max_concurrent_tasks = config.get("max_concurrent_tasks", 3)
        self.max_tasks_per_hour = config.get("max_tasks_per_hour", 5)
        self.max_tasks_per_day = config.get("max_tasks_per_day", 20)

        # 运行状态
        self.running_tasks: Dict[str, Dict[str, Any]] = {}  # task_id -> task_info
        self.task_history: deque = deque(maxlen=1000)  # 最近 1000 个任务历史
        self.lock = threading.Lock()

        # 速率限制窗口
        self.hourly_window: deque = deque()  # 最近 1 小时的任务
        self.daily_window: deque = deque()   # 最近 24 小时的任务

    def can_execute_task(self, task: Dict[str, Any]) -> tuple[bool, str]:
        """
        检查是否可以执行任务

        Args:
            task: 任务信息

        Returns:
            tuple[bool, str]: (是否可以执行, 原因)
        """
        with self.lock:
            # 检查并发限制
            if len(self.running_tasks) >= self.max_concurrent_tasks:
                return False, f"Concurrent task limit reached ({self.max_concurrent_tasks})"

            # 检查小时速率限制
            self._cleanup_windows()
            if len(self.hourly_window) >= self.max_tasks_per_hour:
                return False, f"Hourly rate limit reached ({self.max_tasks_per_hour})"

            # 检查每日速率限制
            if len(self.daily_window) >= self.max_tasks_per_day:
                return False, f"Daily rate limit reached ({self.max_tasks_per_day})"

            # 检查资源可用性
            resource_check = self._check_resource_availability(task)
            if not resource_check[0]:
                return False, resource_check[1]

            return True, "Resources available"

    def acquire_resources(self, task: Dict[str, Any]) -> bool:
        """
        获取任务执行所需的资源

        Args:
            task: 任务信息

        Returns:
            bool: 是否成功获取资源
        """
        with self.lock:
            task_id = task.get("task_id")

            # 再次检查是否可以执行
            can_execute, reason = self.can_execute_task(task)
            if not can_execute:
                self.logger.warning(
                    f"Cannot acquire resources for task {task_id}",
                    context={"reason": reason}
                )
                return False

            # 记录任务开始
            now = datetime.now()
            self.running_tasks[task_id] = {
                "task": task,
                "started_at": now,
                "agent_type": task.get("agent_type"),
                "priority": task.get("priority_score", 0)
            }

            # 更新速率限制窗口
            self.hourly_window.append(now)
            self.daily_window.append(now)

            self.logger.info(
                f"Resources acquired for task {task_id}",
                context={
                    "running_tasks": len(self.running_tasks),
                    "hourly_count": len(self.hourly_window),
                    "daily_count": len(self.daily_window)
                }
            )

            return True

    def release_resources(self, task_id: str, result: Dict[str, Any]):
        """
        释放任务占用的资源

        Args:
            task_id: 任务 ID
            result: 任务执行结果
        """
        with self.lock:
            if task_id not in self.running_tasks:
                self.logger.warning(f"Task {task_id} not found in running tasks")
                return

            # 获取任务信息
            task_info = self.running_tasks.pop(task_id)
            ended_at = datetime.now()
            duration = (ended_at - task_info["started_at"]).total_seconds()

            # 记录到历史
            self.task_history.append({
                "task_id": task_id,
                "agent_type": task_info["agent_type"],
                "started_at": task_info["started_at"].isoformat(),
                "ended_at": ended_at.isoformat(),
                "duration_seconds": duration,
                "status": result.get("status"),
                "success": result.get("success", False)
            })

            self.logger.info(
                f"Resources released for task {task_id}",
                context={
                    "duration_seconds": duration,
                    "status": result.get("status"),
                    "running_tasks": len(self.running_tasks)
                }
            )

    def get_available_slots(self) -> int:
        """
        获取可用的任务槽位数

        Returns:
            int: 可用槽位数
        """
        with self.lock:
            return max(0, self.max_concurrent_tasks - len(self.running_tasks))

    def get_running_tasks(self) -> List[Dict[str, Any]]:
        """
        获取当前运行的任务列表

        Returns:
            List[Dict[str, Any]]: 运行中的任务列表
        """
        with self.lock:
            return [
                {
                    "task_id": task_id,
                    "agent_type": info["agent_type"],
                    "priority": info["priority"],
                    "started_at": info["started_at"].isoformat(),
                    "duration_seconds": (datetime.now() - info["started_at"]).total_seconds()
                }
                for task_id, info in self.running_tasks.items()
            ]

    def get_resource_stats(self) -> Dict[str, Any]:
        """
        获取资源使用统计

        Returns:
            Dict[str, Any]: 资源统计信息
        """
        with self.lock:
            self._cleanup_windows()

            # 计算平均任务时长
            recent_tasks = list(self.task_history)[-100:]  # 最近 100 个任务
            if recent_tasks:
                avg_duration = sum(t["duration_seconds"] for t in recent_tasks) / len(recent_tasks)
                success_rate = sum(1 for t in recent_tasks if t["success"]) / len(recent_tasks)
            else:
                avg_duration = 0
                success_rate = 0

            return {
                "concurrent": {
                    "current": len(self.running_tasks),
                    "max": self.max_concurrent_tasks,
                    "available": self.get_available_slots()
                },
                "rate_limits": {
                    "hourly": {
                        "current": len(self.hourly_window),
                        "max": self.max_tasks_per_hour,
                        "remaining": max(0, self.max_tasks_per_hour - len(self.hourly_window))
                    },
                    "daily": {
                        "current": len(self.daily_window),
                        "max": self.max_tasks_per_day,
                        "remaining": max(0, self.max_tasks_per_day - len(self.daily_window))
                    }
                },
                "performance": {
                    "avg_duration_seconds": avg_duration,
                    "success_rate": success_rate,
                    "total_tasks_executed": len(self.task_history)
                },
                "running_tasks": self.get_running_tasks()
            }

    def _cleanup_windows(self):
        """清理过期的速率限制窗口"""
        now = datetime.now()

        # 清理小时窗口（保留最近 1 小时）
        hour_ago = now - timedelta(hours=1)
        while self.hourly_window and self.hourly_window[0] < hour_ago:
            self.hourly_window.popleft()

        # 清理每日窗口（保留最近 24 小时）
        day_ago = now - timedelta(days=1)
        while self.daily_window and self.daily_window[0] < day_ago:
            self.daily_window.popleft()

    def _check_resource_availability(self, task: Dict[str, Any]) -> tuple[bool, str]:
        """
        检查资源可用性

        Args:
            task: 任务信息

        Returns:
            tuple[bool, str]: (是否可用, 原因)
        """
        # 检查是否有相同 agent 类型的任务正在运行
        agent_type = task.get("agent_type")
        same_agent_tasks = [
            t for t in self.running_tasks.values()
            if t["agent_type"] == agent_type
        ]

        # 限制同一 agent 类型的并发数（最多 2 个）
        if len(same_agent_tasks) >= 2:
            return False, f"Too many concurrent tasks for agent {agent_type}"

        # 检查是否有高优先级任务正在运行
        task_priority = task.get("priority_score", 0)
        high_priority_tasks = [
            t for t in self.running_tasks.values()
            if t["priority"] > 8.0
        ]

        # 如果有高优先级任务运行，低优先级任务需要等待
        if high_priority_tasks and task_priority < 7.0:
            return False, "High priority tasks are running"

        return True, "Resources available"

    def wait_for_slot(self, timeout_seconds: int = 300) -> bool:
        """
        等待可用的任务槽位

        Args:
            timeout_seconds: 超时时间（秒）

        Returns:
            bool: 是否成功获取槽位
        """
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout_seconds:
            if self.get_available_slots() > 0:
                return True
            # 等待 5 秒后重试
            import time
            time.sleep(5)

        return False

    def get_estimated_wait_time(self) -> Optional[int]:
        """
        估算等待时间（秒）

        Returns:
            Optional[int]: 估算的等待时间，None 表示无法估算
        """
        with self.lock:
            if self.get_available_slots() > 0:
                return 0

            # 基于当前运行任务的平均时长估算
            if not self.running_tasks:
                return None

            # 计算最近任务的平均时长
            recent_tasks = list(self.task_history)[-50:]
            if not recent_tasks:
                return None

            avg_duration = sum(t["duration_seconds"] for t in recent_tasks) / len(recent_tasks)

            # 估算最快完成的任务还需要多久
            running_durations = [
                (datetime.now() - info["started_at"]).total_seconds()
                for info in self.running_tasks.values()
            ]

            if running_durations:
                max_running_duration = max(running_durations)
                estimated_remaining = max(0, avg_duration - max_running_duration)
                return int(estimated_remaining)

            return None

    def get_status(self) -> Dict[str, Any]:
        """
        获取资源管理器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        stats = self.get_resource_stats()
        estimated_wait = self.get_estimated_wait_time()

        return {
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
            "estimated_wait_seconds": estimated_wait,
            "config": {
                "max_concurrent_tasks": self.max_concurrent_tasks,
                "max_tasks_per_hour": self.max_tasks_per_hour,
                "max_tasks_per_day": self.max_tasks_per_day
            }
        }


def main():
    """测试资源管理器"""
    print("🧪 Testing Resource Manager...")

    # 模拟配置
    config = {
        "max_concurrent_tasks": 3,
        "max_tasks_per_hour": 5,
        "max_tasks_per_day": 20
    }

    # 创建资源管理器
    manager = ResourceManager(config)

    # 模拟任务
    tasks = [
        {
            "task_id": f"task-{i}",
            "agent_type": "frontend-developer" if i % 2 == 0 else "backend-developer",
            "priority_score": 7.0 + i * 0.5
        }
        for i in range(5)
    ]

    print(f"\n📊 Initial Status:")
    status = manager.get_status()
    print(f"  Available Slots: {status['stats']['concurrent']['available']}")
    print(f"  Hourly Remaining: {status['stats']['rate_limits']['hourly']['remaining']}")
    print(f"  Daily Remaining: {status['stats']['rate_limits']['daily']['remaining']}")

    # 尝试获取资源
    print(f"\n🔄 Acquiring resources for tasks...")
    for task in tasks[:4]:  # 尝试执行 4 个任务（超过并发限制）
        can_execute, reason = manager.can_execute_task(task)
        print(f"\n  Task {task['task_id']}:")
        print(f"    Can Execute: {can_execute}")
        print(f"    Reason: {reason}")

        if can_execute:
            success = manager.acquire_resources(task)
            print(f"    Acquired: {success}")

    # 查看运行中的任务
    print(f"\n🏃 Running Tasks:")
    running = manager.get_running_tasks()
    for task in running:
        print(f"  - {task['task_id']} ({task['agent_type']}) - Priority: {task['priority']}")

    # 释放一个任务
    print(f"\n✅ Releasing task-0...")
    manager.release_resources("task-0", {"status": "completed", "success": True})

    # 再次检查状态
    print(f"\n📊 Updated Status:")
    status = manager.get_status()
    print(f"  Available Slots: {status['stats']['concurrent']['available']}")
    print(f"  Running Tasks: {status['stats']['concurrent']['current']}")
    print(f"  Estimated Wait: {status['estimated_wait_seconds']} seconds")

    # 获取资源统计
    print(f"\n📈 Resource Stats:")
    stats = manager.get_resource_stats()
    print(f"  Total Tasks Executed: {stats['performance']['total_tasks_executed']}")
    print(f"  Success Rate: {stats['performance']['success_rate']:.2%}")
    print(f"  Avg Duration: {stats['performance']['avg_duration_seconds']:.2f}s")

    print("\n✅ Resource manager test completed!")


if __name__ == "__main__":
    main()
