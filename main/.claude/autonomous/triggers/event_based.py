#!/usr/bin/env python3
"""
基于事件的任务触发器
Event-Based Task Trigger

功能：
1. Git Hook 集成
2. 文件系统监控
3. 外部事件接收
4. 任务生成和入队
"""

import os
import subprocess
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
from pathlib import Path
import threading
import queue

from ..core.logging_utils import get_logger
from ..core.task_queue import TaskQueue
from ..database.init_db import DatabaseManager, TaskRepository


class EventBasedTrigger:
    """基于事件的任务触发器"""

    def __init__(
        self,
        config: Dict[str, Any],
        task_queue: TaskQueue,
        db_manager: DatabaseManager
    ):
        """
        初始化事件触发器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            task_queue: 任务队列实例
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.task_queue = task_queue
        self.task_repo = TaskRepository(db_manager)
        self.logger = get_logger("event_based_trigger", log_file=".claude/autonomous/logs/triggers.log")

        # 解析配置
        self.enabled = config.get("enabled", True)
        self.triggers = config.get("triggers", [])

        # 事件队列
        self.event_queue: queue.Queue = queue.Queue()
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # 事件处理器映射
        self.event_handlers: Dict[str, Callable] = {
            "post-commit": self._handle_post_commit,
            "pre-push": self._handle_pre_push,
            "deployment": self._handle_deployment,
        }

    def start(self):
        """启动事件触发器"""
        if not self.enabled:
            self.logger.info("Event-based trigger is disabled")
            return

        if self.running:
            self.logger.warning("Event-based trigger is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._process_events, daemon=True)
        self.thread.start()

        self.logger.info(
            "Event-based trigger started",
            context={"triggers_count": len(self.triggers)}
        )

    def stop(self):
        """停止事件触发器"""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

        self.logger.info("Event-based trigger stopped")

    def trigger_event(self, event_type: str, event_data: Optional[Dict[str, Any]] = None):
        """
        触发事件

        Args:
            event_type: 事件类型（post-commit, pre-push, deployment 等）
            event_data: 事件数据
        """
        self.event_queue.put({
            "type": event_type,
            "data": event_data or {},
            "timestamp": datetime.now()
        })

        self.logger.debug(
            f"Event queued: {event_type}",
            context={"event_type": event_type, "data": event_data}
        )

    def _process_events(self):
        """处理事件队列"""
        while self.running:
            try:
                # 从队列获取事件（超时 1 秒）
                event = self.event_queue.get(timeout=1)

                event_type = event["type"]
                event_data = event["data"]
                timestamp = event["timestamp"]

                # 查找匹配的触发器配置
                for trigger_config in self.triggers:
                    if trigger_config["event"] == event_type:
                        self._create_task_from_event(trigger_config, event_data, timestamp)

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.exception(
                    "Error processing event",
                    context={"error": str(e)}
                )

    def _create_task_from_event(
        self,
        trigger_config: Dict[str, Any],
        event_data: Dict[str, Any],
        timestamp: datetime
    ):
        """
        从事件创建任务

        Args:
            trigger_config: 触发器配置
            event_data: 事件数据
            timestamp: 事件时间戳
        """
        name = trigger_config["name"]
        event_type = trigger_config["event"]
        description = trigger_config["description"]
        priority = trigger_config["priority"]

        # 生成任务 ID
        task_id = f"event-{name}-{timestamp.strftime('%Y%m%d%H%M%S')}"

        try:
            # 创建任务元数据
            metadata = {
                "trigger_type": "event_based",
                "event_type": event_type,
                "event_name": name,
                "event_data": event_data,
                "triggered_at": timestamp.isoformat()
            }

            # 添加到数据库
            success = self.task_repo.create_task(
                task_id=task_id,
                task_type="event_based",
                description=description,
                priority=priority,
                scheduled_at=timestamp,
                metadata=metadata
            )

            if success:
                # 添加到内存队列
                self.task_queue.add_task(
                    task_id=task_id,
                    task_type="event_based",
                    description=description,
                    priority=priority,
                    scheduled_at=timestamp,
                    metadata=metadata
                )

                self.logger.info(
                    f"Task created from event: {task_id}",
                    context={
                        "task_id": task_id,
                        "event_type": event_type,
                        "priority": priority
                    }
                )
            else:
                self.logger.error(
                    f"Failed to create task in database: {task_id}",
                    context={"task_id": task_id, "event_type": event_type}
                )

        except Exception as e:
            self.logger.exception(
                f"Failed to create task from event {event_type}",
                context={"event_type": event_type, "error": str(e)}
            )

    def _handle_post_commit(self, event_data: Dict[str, Any]):
        """
        处理 post-commit 事件

        Args:
            event_data: 事件数据（commit hash, message, author 等）
        """
        self.logger.info(
            "Handling post-commit event",
            context=event_data
        )
        # 具体处理逻辑（代码分析、测试触发等）

    def _handle_pre_push(self, event_data: Dict[str, Any]):
        """
        处理 pre-push 事件

        Args:
            event_data: 事件数据（branch, remote 等）
        """
        self.logger.info(
            "Handling pre-push event",
            context=event_data
        )
        # 具体处理逻辑（代码验证、测试运行等）

    def _handle_deployment(self, event_data: Dict[str, Any]):
        """
        处理 deployment 事件

        Args:
            event_data: 事件数据（environment, version 等）
        """
        self.logger.info(
            "Handling deployment event",
            context=event_data
        )
        # 具体处理逻辑（健康检查、监控等）

    def install_git_hooks(self, repo_path: str = "."):
        """
        安装 Git Hooks

        Args:
            repo_path: Git 仓库路径
        """
        hooks_dir = Path(repo_path) / ".git" / "hooks"
        if not hooks_dir.exists():
            self.logger.error(f"Git hooks directory not found: {hooks_dir}")
            return

        # 安装 post-commit hook
        post_commit_hook = hooks_dir / "post-commit"
        post_commit_script = """#!/bin/bash
# Autonomous Evolution System - Post-Commit Hook

# 获取提交信息
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MESSAGE=$(git log -1 --pretty=%B)
COMMIT_AUTHOR=$(git log -1 --pretty=%an)

# 触发事件（调用 Python 脚本）
python3 .claude/autonomous/triggers/trigger_event.py post-commit \\
    --commit-hash "$COMMIT_HASH" \\
    --commit-message "$COMMIT_MESSAGE" \\
    --commit-author "$COMMIT_AUTHOR"
"""

        try:
            with open(post_commit_hook, 'w') as f:
                f.write(post_commit_script)
            os.chmod(post_commit_hook, 0o755)
            self.logger.info(f"Installed post-commit hook: {post_commit_hook}")
        except Exception as e:
            self.logger.error(f"Failed to install post-commit hook: {e}")

        # 安装 pre-push hook
        pre_push_hook = hooks_dir / "pre-push"
        pre_push_script = """#!/bin/bash
# Autonomous Evolution System - Pre-Push Hook

# 获取分支信息
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE=$1

# 触发事件
python3 .claude/autonomous/triggers/trigger_event.py pre-push \\
    --branch "$BRANCH" \\
    --remote "$REMOTE"
"""

        try:
            with open(pre_push_hook, 'w') as f:
                f.write(pre_push_script)
            os.chmod(pre_push_hook, 0o755)
            self.logger.info(f"Installed pre-push hook: {pre_push_hook}")
        except Exception as e:
            self.logger.error(f"Failed to install pre-push hook: {e}")

    def get_status(self) -> Dict[str, Any]:
        """
        获取触发器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "enabled": self.enabled,
            "running": self.running,
            "triggers_count": len(self.triggers),
            "event_queue_size": self.event_queue.qsize()
        }


def main():
    """测试事件触发器"""
    print("🧪 Testing Event-Based Trigger...")

    # 模拟配置
    config = {
        "enabled": True,
        "triggers": [
            {
                "name": "post_commit_analysis",
                "event": "post-commit",
                "description": "提交后代码分析",
                "priority": 6
            },
            {
                "name": "pre_push_validation",
                "event": "pre-push",
                "description": "推送前验证",
                "priority": 8
            }
        ]
    }

    # 创建依赖
    task_queue = TaskQueue()
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建触发器
    trigger = EventBasedTrigger(config, task_queue, db_manager)

    # 启动触发器
    trigger.start()

    # 获取状态
    status = trigger.get_status()
    print(f"\n📊 Trigger Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Running: {status['running']}")
    print(f"  Triggers: {status['triggers_count']}")

    # 模拟事件
    print(f"\n🎯 Triggering test events...")
    trigger.trigger_event("post-commit", {
        "commit_hash": "abc123",
        "commit_message": "Test commit",
        "commit_author": "Test User"
    })

    trigger.trigger_event("pre-push", {
        "branch": "main",
        "remote": "origin"
    })

    # 等待事件处理
    import time
    time.sleep(2)

    # 检查队列
    print(f"\n📋 Task Queue Status:")
    stats = task_queue.get_statistics()
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Ready tasks: {stats['ready_tasks']}")

    # 停止触发器
    trigger.stop()

    print("\n✅ Event-based trigger test completed!")


if __name__ == "__main__":
    main()
