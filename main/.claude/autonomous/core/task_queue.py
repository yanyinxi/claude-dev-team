#!/usr/bin/env python3
"""
任务队列模块
Task Queue Module

功能：
1. 内存中的优先级任务队列
2. 支持任务的添加、获取、更新
3. 按优先级和计划时间排序
4. 与数据库层集成
"""

import heapq
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field
import threading


@dataclass(order=True)
class QueuedTask:
    """队列中的任务"""

    # 排序字段（优先级越高越先执行，计划时间越早越先执行）
    priority: int = field(compare=True)
    scheduled_at: datetime = field(compare=True)

    # 任务数据（不参与排序）
    task_id: str = field(compare=False)
    task_type: str = field(compare=False)
    description: str = field(compare=False)
    metadata: Dict[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self):
        # 反转优先级，使得高优先级排在前面
        self.priority = -self.priority


class TaskQueue:
    """任务队列管理器"""

    def __init__(self):
        """初始化任务队列"""
        self._queue: List[QueuedTask] = []
        self._lock = threading.Lock()
        self._task_map: Dict[str, QueuedTask] = {}

    def add_task(
        self,
        task_id: str,
        task_type: str,
        description: str,
        priority: int,
        scheduled_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        添加任务到队列

        Args:
            task_id: 任务 ID
            task_type: 任务类型
            description: 任务描述
            priority: 优先级（1-10，10 最高）
            scheduled_at: 计划执行时间
            metadata: 额外元数据

        Returns:
            bool: 添加是否成功
        """
        with self._lock:
            # 检查任务是否已存在
            if task_id in self._task_map:
                print(f"⚠️ Task {task_id} already exists in queue")
                return False

            # 创建任务对象
            task = QueuedTask(
                priority=priority,
                scheduled_at=scheduled_at or datetime.now(),
                task_id=task_id,
                task_type=task_type,
                description=description,
                metadata=metadata or {}
            )

            # 添加到堆和映射
            heapq.heappush(self._queue, task)
            self._task_map[task_id] = task

            print(f"✅ Task {task_id} added to queue (priority: {priority})")
            return True

    def get_next_task(self) -> Optional[QueuedTask]:
        """
        获取下一个待执行的任务（不移除）

        Returns:
            Optional[QueuedTask]: 下一个任务，如果队列为空则返回 None
        """
        with self._lock:
            if not self._queue:
                return None

            # 获取堆顶任务（优先级最高且计划时间最早）
            return self._queue[0]

    def pop_next_task(self) -> Optional[QueuedTask]:
        """
        获取并移除下一个待执行的任务

        Returns:
            Optional[QueuedTask]: 下一个任务，如果队列为空则返回 None
        """
        with self._lock:
            if not self._queue:
                return None

            # 弹出堆顶任务
            task = heapq.heappop(self._queue)

            # 从映射中移除
            if task.task_id in self._task_map:
                del self._task_map[task.task_id]

            print(f"📤 Task {task.task_id} popped from queue")
            return task

    def remove_task(self, task_id: str) -> bool:
        """
        从队列中移除指定任务

        Args:
            task_id: 任务 ID

        Returns:
            bool: 移除是否成功
        """
        with self._lock:
            if task_id not in self._task_map:
                print(f"⚠️ Task {task_id} not found in queue")
                return False

            # 从映射中移除
            task = self._task_map.pop(task_id)

            # 从堆中移除（需要重建堆）
            self._queue = [t for t in self._queue if t.task_id != task_id]
            heapq.heapify(self._queue)

            print(f"🗑️ Task {task_id} removed from queue")
            return True

    def get_task(self, task_id: str) -> Optional[QueuedTask]:
        """
        获取指定任务（不移除）

        Args:
            task_id: 任务 ID

        Returns:
            Optional[QueuedTask]: 任务对象，如果不存在则返回 None
        """
        with self._lock:
            return self._task_map.get(task_id)

    def get_all_tasks(self) -> List[QueuedTask]:
        """
        获取所有任务（按优先级排序）

        Returns:
            List[QueuedTask]: 任务列表
        """
        with self._lock:
            return sorted(self._queue)

    def get_ready_tasks(self) -> List[QueuedTask]:
        """
        获取所有已到计划时间的任务

        Returns:
            List[QueuedTask]: 就绪任务列表
        """
        with self._lock:
            now = datetime.now()
            return [task for task in sorted(self._queue) if task.scheduled_at <= now]

    def size(self) -> int:
        """
        获取队列大小

        Returns:
            int: 队列中的任务数量
        """
        with self._lock:
            return len(self._queue)

    def is_empty(self) -> bool:
        """
        检查队列是否为空

        Returns:
            bool: 队列是否为空
        """
        with self._lock:
            return len(self._queue) == 0

    def clear(self):
        """清空队列"""
        with self._lock:
            self._queue.clear()
            self._task_map.clear()
            print("🧹 Task queue cleared")

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取队列统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        with self._lock:
            now = datetime.now()
            ready_count = sum(1 for task in self._queue if task.scheduled_at <= now)

            # 按任务类型统计
            type_counts = {}
            for task in self._queue:
                type_counts[task.task_type] = type_counts.get(task.task_type, 0) + 1

            # 按优先级统计
            priority_counts = {}
            for task in self._queue:
                # 恢复原始优先级（因为存储时反转了）
                original_priority = -task.priority
                priority_counts[original_priority] = priority_counts.get(original_priority, 0) + 1

            return {
                "total_tasks": len(self._queue),
                "ready_tasks": ready_count,
                "pending_tasks": len(self._queue) - ready_count,
                "tasks_by_type": type_counts,
                "tasks_by_priority": priority_counts,
                "next_task": self._queue[0].task_id if self._queue else None
            }


def main():
    """测试任务队列"""
    print("🧪 Testing Task Queue...")

    # 创建任务队列
    queue = TaskQueue()

    # 添加测试任务
    queue.add_task(
        task_id="task-1",
        task_type="time_based",
        description="Daily health check",
        priority=5,
        scheduled_at=datetime.now()
    )

    queue.add_task(
        task_id="task-2",
        task_type="metric_based",
        description="High error rate detected",
        priority=9,
        scheduled_at=datetime.now()
    )

    queue.add_task(
        task_id="task-3",
        task_type="llm_driven",
        description="Gap analysis",
        priority=7,
        scheduled_at=datetime.now()
    )

    # 打印统计信息
    stats = queue.get_statistics()
    print(f"\n📊 Queue Statistics:")
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Ready tasks: {stats['ready_tasks']}")
    print(f"  Next task: {stats['next_task']}")
    print(f"  Tasks by type: {stats['tasks_by_type']}")
    print(f"  Tasks by priority: {stats['tasks_by_priority']}")

    # 获取就绪任务
    print(f"\n📋 Ready Tasks:")
    for task in queue.get_ready_tasks():
        print(f"  - {task.task_id}: {task.description} (priority: {-task.priority})")

    # 弹出任务
    print(f"\n🎯 Popping Tasks:")
    while not queue.is_empty():
        task = queue.pop_next_task()
        if task:
            print(f"  - {task.task_id}: {task.description} (priority: {-task.priority})")

    print("\n✅ Task Queue test completed!")


if __name__ == "__main__":
    main()
