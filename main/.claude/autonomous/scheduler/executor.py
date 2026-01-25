#!/usr/bin/env python3
"""
任务执行器
Task Executor

功能：
1. 管理任务队列（优先级队列）
2. 协调优先级计算、冲突检测、资源管理
3. 执行任务并跟踪结果
4. 提供执行状态和统计
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import heapq
import threading

from .priority_calculator import PriorityCalculator
from .conflict_detector import ConflictDetector
from .resource_manager import ResourceManager
from ..core.logging_utils import get_logger


class TaskExecutor:
    """任务执行器"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化任务执行器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
        """
        self.config = config
        self.logger = get_logger("task_executor", log_file=".claude/autonomous/logs/scheduler.log")

        # 初始化组件
        self.priority_calculator = PriorityCalculator(config)
        self.conflict_detector = ConflictDetector(config)
        self.resource_manager = ResourceManager(config)

        # 任务队列（优先级队列）
        self.task_queue: List[tuple[float, int, Dict[str, Any]]] = []  # (priority, counter, task)
        self.task_counter = 0  # 用于打破优先级相同的情况
        self.queue_lock = threading.Lock()

        # 执行状态
        self.running = False
        self.executor_thread: Optional[threading.Thread] = None

        # 任务存储
        self.pending_tasks: Dict[str, Dict[str, Any]] = {}  # task_id -> task
        self.completed_tasks: List[Dict[str, Any]] = []
        self.failed_tasks: List[Dict[str, Any]] = []

    def start(self):
        """启动执行器"""
        if self.running:
            self.logger.warning("Executor already running")
            return

        self.running = True
        self.executor_thread = threading.Thread(target=self._execution_loop, daemon=True)
        self.executor_thread.start()
        self.logger.info("Task executor started")

    def stop(self):
        """停止执行器"""
        if not self.running:
            return

        self.running = False
        if self.executor_thread:
            self.executor_thread.join(timeout=5)
        self.logger.info("Task executor stopped")

    def submit_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        提交任务到队列

        Args:
            task: 任务信息

        Returns:
            Dict[str, Any]: 提交结果
        """
        task_id = task.get("task_id")
        self.logger.info(f"Submitting task {task_id}")

        # 计算优先级
        context = self._build_context()
        priority_score = self.priority_calculator.calculate_priority(task, context)
        task["priority_score"] = priority_score

        # 检测冲突
        existing_tasks = list(self.pending_tasks.values())
        conflicts = self.conflict_detector.detect_conflicts(task, existing_tasks)

        if conflicts["has_conflicts"]:
            # 解决冲突
            resolution = self.conflict_detector.resolve_conflicts(conflicts, task)

            if resolution["action"] == "skip":
                self.logger.warning(
                    f"Task {task_id} skipped due to conflicts",
                    context={"reason": resolution["reason"]}
                )
                return {
                    "status": "skipped",
                    "reason": resolution["reason"],
                    "conflicts": conflicts
                }

            elif resolution["action"] == "wait":
                self.logger.info(
                    f"Task {task_id} waiting for dependencies",
                    context={"wait_for": resolution.get("wait_for", [])}
                )
                task["blocked_by"] = resolution.get("wait_for", [])

            elif resolution["action"] == "delay":
                self.logger.info(
                    f"Task {task_id} delayed due to conflicts",
                    context={"reason": resolution["reason"]}
                )
                # 降低优先级
                priority_score *= 0.8
                task["priority_score"] = priority_score

        # 添加到队列
        with self.queue_lock:
            # 使用负优先级（heapq 是最小堆，我们需要最大堆）
            heapq.heappush(
                self.task_queue,
                (-priority_score, self.task_counter, task)
            )
            self.task_counter += 1
            self.pending_tasks[task_id] = task

        self.logger.info(
            f"Task {task_id} submitted successfully",
            context={
                "priority_score": priority_score,
                "queue_size": len(self.task_queue)
            }
        )

        return {
            "status": "queued",
            "task_id": task_id,
            "priority_score": priority_score,
            "queue_position": len(self.task_queue)
        }

    def _execution_loop(self):
        """执行循环（在后台线程中运行）"""
        self.logger.info("Execution loop started")

        while self.running:
            try:
                # 检查是否有可执行的任务
                task = self._get_next_executable_task()

                if task:
                    # 执行任务
                    self._execute_task(task)
                else:
                    # 没有可执行任务，等待一段时间
                    import time
                    time.sleep(5)

            except Exception as e:
                self.logger.exception(
                    "Error in execution loop",
                    context={"error": str(e)}
                )
                import time
                time.sleep(10)

        self.logger.info("Execution loop stopped")

    def _get_next_executable_task(self) -> Optional[Dict[str, Any]]:
        """
        获取下一个可执行的任务

        Returns:
            Optional[Dict[str, Any]]: 任务信息，如果没有可执行任务则返回 None
        """
        with self.queue_lock:
            if not self.task_queue:
                return None

            # 检查队列中的任务
            temp_queue = []
            executable_task = None

            while self.task_queue:
                priority, counter, task = heapq.heappop(self.task_queue)
                task_id = task.get("task_id")

                # 检查是否被阻塞
                blocked_by = task.get("blocked_by", [])
                if blocked_by:
                    # 检查阻塞任务是否已完成
                    still_blocked = any(
                        dep_id in self.pending_tasks
                        for dep_id in blocked_by
                    )

                    if still_blocked:
                        # 仍然被阻塞，放回队列
                        temp_queue.append((priority, counter, task))
                        continue
                    else:
                        # 阻塞已解除
                        task["blocked_by"] = []

                # 检查资源可用性
                can_execute, reason = self.resource_manager.can_execute_task(task)

                if can_execute:
                    # 找到可执行任务
                    executable_task = task
                    break
                else:
                    # 资源不可用，放回队列
                    temp_queue.append((priority, counter, task))

            # 将未执行的任务放回队列
            for item in temp_queue:
                heapq.heappush(self.task_queue, item)

            return executable_task

    def _execute_task(self, task: Dict[str, Any]):
        """
        执行任务

        Args:
            task: 任务信息
        """
        task_id = task.get("task_id")
        agent_type = task.get("agent_type")

        self.logger.info(
            f"Executing task {task_id}",
            context={
                "agent_type": agent_type,
                "priority": task.get("priority_score")
            }
        )

        # 获取资源
        if not self.resource_manager.acquire_resources(task):
            self.logger.error(f"Failed to acquire resources for task {task_id}")
            return

        try:
            # 执行任务（这里需要集成实际的任务执行逻辑）
            result = self._run_task(task)

            # 记录成功
            task["status"] = "completed"
            task["result"] = result
            task["completed_at"] = datetime.now().isoformat()

            self.completed_tasks.append(task)

            # 从待处理列表中移除
            if task_id in self.pending_tasks:
                del self.pending_tasks[task_id]

            self.logger.info(
                f"Task {task_id} completed successfully",
                context={"result": result}
            )

        except Exception as e:
            # 记录失败
            task["status"] = "failed"
            task["error"] = str(e)
            task["failed_at"] = datetime.now().isoformat()

            self.failed_tasks.append(task)

            # 从待处理列表中移除
            if task_id in self.pending_tasks:
                del self.pending_tasks[task_id]

            self.logger.exception(
                f"Task {task_id} failed",
                context={"error": str(e)}
            )

        finally:
            # 释放资源
            self.resource_manager.release_resources(
                task_id,
                {
                    "status": task.get("status"),
                    "success": task.get("status") == "completed"
                }
            )

    def _run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行任务（实际执行逻辑）

        Args:
            task: 任务信息

        Returns:
            Dict[str, Any]: 执行结果
        """
        # TODO: 集成实际的任务执行逻辑
        # 这里需要根据 agent_type 调用相应的 Agent
        # 例如：调用 Task 工具执行子代理

        agent_type = task.get("agent_type")
        task_description = task.get("description")

        self.logger.info(
            f"Running task with agent {agent_type}",
            context={"description": task_description}
        )

        # 模拟任务执行
        import time
        time.sleep(2)  # 模拟执行时间

        return {
            "status": "success",
            "message": f"Task executed by {agent_type}",
            "timestamp": datetime.now().isoformat()
        }

    def _build_context(self) -> Dict[str, Any]:
        """
        构建上下文信息（用于优先级计算）

        Returns:
            Dict[str, Any]: 上下文信息
        """
        return {
            "running_tasks": len(self.resource_manager.running_tasks),
            "max_concurrent_tasks": self.resource_manager.max_concurrent_tasks,
            "blocked_tasks": [
                task for task in self.pending_tasks.values()
                if task.get("blocked_by")
            ]
        }

    def get_status(self) -> Dict[str, Any]:
        """
        获取执行器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        with self.queue_lock:
            queue_size = len(self.task_queue)

        resource_stats = self.resource_manager.get_resource_stats()

        return {
            "timestamp": datetime.now().isoformat(),
            "running": self.running,
            "queue": {
                "size": queue_size,
                "pending_tasks": len(self.pending_tasks)
            },
            "completed": {
                "total": len(self.completed_tasks),
                "recent": self.completed_tasks[-10:] if self.completed_tasks else []
            },
            "failed": {
                "total": len(self.failed_tasks),
                "recent": self.failed_tasks[-10:] if self.failed_tasks else []
            },
            "resources": resource_stats
        }

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        获取任务状态

        Args:
            task_id: 任务 ID

        Returns:
            Optional[Dict[str, Any]]: 任务状态
        """
        # 检查待处理任务
        if task_id in self.pending_tasks:
            task = self.pending_tasks[task_id]
            return {
                "task_id": task_id,
                "status": "pending",
                "priority_score": task.get("priority_score"),
                "blocked_by": task.get("blocked_by", [])
            }

        # 检查已完成任务
        for task in self.completed_tasks:
            if task.get("task_id") == task_id:
                return {
                    "task_id": task_id,
                    "status": "completed",
                    "completed_at": task.get("completed_at"),
                    "result": task.get("result")
                }

        # 检查失败任务
        for task in self.failed_tasks:
            if task.get("task_id") == task_id:
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "failed_at": task.get("failed_at"),
                    "error": task.get("error")
                }

        return None


def main():
    """测试任务执行器"""
    print("🧪 Testing Task Executor...")

    # 模拟配置
    config = {
        "max_concurrent_tasks": 3,
        "max_tasks_per_hour": 5,
        "max_tasks_per_day": 20,
        "duplicate_window_hours": 24,
        "conflict_rules": [],
        "priority_formula": "base_priority * urgency_multiplier * resource_availability"
    }

    # 创建执行器
    executor = TaskExecutor(config)

    # 启动执行器
    executor.start()

    # 提交测试任务
    print(f"\n📝 Submitting test tasks...")
    tasks = [
        {
            "task_id": f"task-{i}",
            "agent_type": "frontend-developer" if i % 2 == 0 else "backend-developer",
            "description": f"Test task {i}",
            "priority": 5 + i,
            "created_at": datetime.now().isoformat(),
            "metadata": {}
        }
        for i in range(5)
    ]

    for task in tasks:
        result = executor.submit_task(task)
        print(f"  Task {task['task_id']}: {result['status']} (priority: {result.get('priority_score', 0):.2f})")

    # 等待任务执行
    print(f"\n⏳ Waiting for tasks to execute...")
    import time
    time.sleep(15)

    # 获取状态
    print(f"\n📊 Executor Status:")
    status = executor.get_status()
    print(f"  Running: {status['running']}")
    print(f"  Queue Size: {status['queue']['size']}")
    print(f"  Pending Tasks: {status['queue']['pending_tasks']}")
    print(f"  Completed: {status['completed']['total']}")
    print(f"  Failed: {status['failed']['total']}")
    print(f"  Running Tasks: {status['resources']['concurrent']['current']}")

    # 停止执行器
    executor.stop()

    print("\n✅ Task executor test completed!")


if __name__ == "__main__":
    main()
