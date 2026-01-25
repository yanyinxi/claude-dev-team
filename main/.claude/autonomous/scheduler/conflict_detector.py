#!/usr/bin/env python3
"""
冲突检测器
Conflict Detector

功能：
1. 检测重复任务
2. 检测冲突任务
3. 检测依赖关系
4. 提供冲突解决建议
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

from ..core.logging_utils import get_logger


class ConflictDetector:
    """冲突检测器"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化冲突检测器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
        """
        self.config = config
        self.logger = get_logger("conflict_detector", log_file=".claude/autonomous/logs/scheduler.log")

        # 冲突检测配置
        self.duplicate_window_hours = config.get("duplicate_window_hours", 24)
        self.conflict_rules = config.get("conflict_rules", [])

    def detect_conflicts(
        self,
        new_task: Dict[str, Any],
        existing_tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        检测任务冲突

        Args:
            new_task: 新任务
            existing_tasks: 现有任务列表

        Returns:
            Dict[str, Any]: 冲突检测结果
        """
        self.logger.debug(
            f"Detecting conflicts for task {new_task.get('task_id')}",
            context={"existing_tasks_count": len(existing_tasks)}
        )

        conflicts = {
            "has_conflicts": False,
            "duplicate_tasks": [],
            "conflicting_tasks": [],
            "blocking_tasks": [],
            "recommendations": []
        }

        # 检测重复任务
        duplicates = self._detect_duplicates(new_task, existing_tasks)
        if duplicates:
            conflicts["has_conflicts"] = True
            conflicts["duplicate_tasks"] = duplicates
            conflicts["recommendations"].append({
                "type": "skip",
                "reason": f"Found {len(duplicates)} duplicate task(s)",
                "details": duplicates
            })

        # 检测冲突任务
        conflicting = self._detect_conflicting_tasks(new_task, existing_tasks)
        if conflicting:
            conflicts["has_conflicts"] = True
            conflicts["conflicting_tasks"] = conflicting
            conflicts["recommendations"].append({
                "type": "delay",
                "reason": f"Found {len(conflicting)} conflicting task(s)",
                "details": conflicting
            })

        # 检测阻塞任务
        blocking = self._detect_blocking_tasks(new_task, existing_tasks)
        if blocking:
            conflicts["has_conflicts"] = True
            conflicts["blocking_tasks"] = blocking
            conflicts["recommendations"].append({
                "type": "wait",
                "reason": f"Found {len(blocking)} blocking task(s)",
                "details": blocking
            })

        self.logger.debug(
            f"Conflict detection completed for task {new_task.get('task_id')}",
            context={
                "has_conflicts": conflicts["has_conflicts"],
                "duplicates": len(conflicts["duplicate_tasks"]),
                "conflicting": len(conflicts["conflicting_tasks"]),
                "blocking": len(conflicts["blocking_tasks"])
            }
        )

        return conflicts

    def _detect_duplicates(
        self,
        new_task: Dict[str, Any],
        existing_tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        检测重复任务

        Args:
            new_task: 新任务
            existing_tasks: 现有任务列表

        Returns:
            List[Dict[str, Any]]: 重复任务列表
        """
        duplicates = []
        new_task_signature = self._get_task_signature(new_task)

        # 时间窗口
        cutoff_time = datetime.now() - timedelta(hours=self.duplicate_window_hours)

        for task in existing_tasks:
            # 跳过已完成或失败的任务
            if task.get("status") in ["completed", "failed"]:
                continue

            # 检查时间窗口
            created_at = task.get("created_at")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            if created_at and created_at < cutoff_time:
                continue

            # 比较任务签名
            task_signature = self._get_task_signature(task)
            if new_task_signature == task_signature:
                duplicates.append({
                    "task_id": task.get("task_id"),
                    "created_at": task.get("created_at"),
                    "status": task.get("status"),
                    "similarity": 1.0
                })

        return duplicates

    def _detect_conflicting_tasks(
        self,
        new_task: Dict[str, Any],
        existing_tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        检测冲突任务

        Args:
            new_task: 新任务
            existing_tasks: 现有任务列表

        Returns:
            List[Dict[str, Any]]: 冲突任务列表
        """
        conflicting = []
        new_agent = new_task.get("agent_type")
        new_metadata = new_task.get("metadata", {})

        for task in existing_tasks:
            # 跳过已完成或失败的任务
            if task.get("status") in ["completed", "failed"]:
                continue

            task_agent = task.get("agent_type")
            task_metadata = task.get("metadata", {})

            # 检查冲突规则
            for rule in self.conflict_rules:
                if self._matches_conflict_rule(
                    rule,
                    new_agent,
                    new_metadata,
                    task_agent,
                    task_metadata
                ):
                    conflicting.append({
                        "task_id": task.get("task_id"),
                        "agent_type": task_agent,
                        "status": task.get("status"),
                        "conflict_reason": rule.get("reason", "Unknown conflict")
                    })
                    break

        return conflicting

    def _detect_blocking_tasks(
        self,
        new_task: Dict[str, Any],
        existing_tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        检测阻塞任务

        Args:
            new_task: 新任务
            existing_tasks: 现有任务列表

        Returns:
            List[Dict[str, Any]]: 阻塞任务列表
        """
        blocking = []
        new_metadata = new_task.get("metadata", {})
        dependencies = new_metadata.get("depends_on", [])

        if not dependencies:
            return blocking

        for task in existing_tasks:
            task_id = task.get("task_id")
            if task_id in dependencies:
                # 检查任务状态
                status = task.get("status")
                if status not in ["completed"]:
                    blocking.append({
                        "task_id": task_id,
                        "agent_type": task.get("agent_type"),
                        "status": status,
                        "blocking_reason": "Dependency not completed"
                    })

        return blocking

    def _get_task_signature(self, task: Dict[str, Any]) -> str:
        """
        获取任务签名（用于重复检测）

        Args:
            task: 任务信息

        Returns:
            str: 任务签名
        """
        # 使用 agent_type + trigger_name + 关键元数据生成签名
        agent_type = task.get("agent_type", "")
        trigger_name = task.get("trigger_name", "")
        metadata = task.get("metadata", {})

        # 提取关键元数据
        key_metadata = {
            "target_file": metadata.get("target_file"),
            "target_module": metadata.get("target_module"),
            "analysis_type": metadata.get("analysis_type")
        }

        # 过滤 None 值
        key_metadata = {k: v for k, v in key_metadata.items() if v is not None}

        # 生成签名
        signature = f"{agent_type}:{trigger_name}:{str(sorted(key_metadata.items()))}"
        return signature

    def _matches_conflict_rule(
        self,
        rule: Dict[str, Any],
        agent1: str,
        metadata1: Dict[str, Any],
        agent2: str,
        metadata2: Dict[str, Any]
    ) -> bool:
        """
        检查是否匹配冲突规则

        Args:
            rule: 冲突规则
            agent1: 代理1类型
            metadata1: 代理1元数据
            agent2: 代理2类型
            metadata2: 代理2元数据

        Returns:
            bool: 是否匹配
        """
        # 检查代理类型
        agents = rule.get("agents", [])
        if agents and agent1 not in agents:
            return False
        if agents and agent2 not in agents:
            return False

        # 检查目标文件冲突
        if rule.get("check_target_file", False):
            file1 = metadata1.get("target_file")
            file2 = metadata2.get("target_file")
            if file1 and file2 and file1 == file2:
                return True

        # 检查目标模块冲突
        if rule.get("check_target_module", False):
            module1 = metadata1.get("target_module")
            module2 = metadata2.get("target_module")
            if module1 and module2 and module1 == module2:
                return True

        return False

    def resolve_conflicts(
        self,
        conflicts: Dict[str, Any],
        new_task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        解决冲突

        Args:
            conflicts: 冲突检测结果
            new_task: 新任务

        Returns:
            Dict[str, Any]: 解决方案
        """
        if not conflicts["has_conflicts"]:
            return {
                "action": "proceed",
                "reason": "No conflicts detected"
            }

        # 优先级：重复 > 冲突 > 阻塞
        if conflicts["duplicate_tasks"]:
            return {
                "action": "skip",
                "reason": "Duplicate task detected",
                "details": conflicts["duplicate_tasks"]
            }

        if conflicts["blocking_tasks"]:
            return {
                "action": "wait",
                "reason": "Blocking tasks detected",
                "details": conflicts["blocking_tasks"],
                "wait_for": [t["task_id"] for t in conflicts["blocking_tasks"]]
            }

        if conflicts["conflicting_tasks"]:
            # 根据优先级决定
            new_priority = new_task.get("priority_score", 0)
            max_conflict_priority = max(
                (t.get("priority_score", 0) for t in conflicts["conflicting_tasks"]),
                default=0
            )

            if new_priority > max_conflict_priority:
                return {
                    "action": "proceed",
                    "reason": "New task has higher priority",
                    "note": "Consider pausing conflicting tasks"
                }
            else:
                return {
                    "action": "delay",
                    "reason": "Conflicting tasks have higher priority",
                    "details": conflicts["conflicting_tasks"]
                }

        return {
            "action": "proceed",
            "reason": "Conflicts can be resolved"
        }

    def get_status(self) -> Dict[str, Any]:
        """
        获取检测器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "duplicate_window_hours": self.duplicate_window_hours,
            "conflict_rules_count": len(self.conflict_rules)
        }


def main():
    """测试冲突检测器"""
    print("🧪 Testing Conflict Detector...")

    # 模拟配置
    config = {
        "duplicate_window_hours": 24,
        "conflict_rules": [
            {
                "agents": ["frontend-developer", "backend-developer"],
                "check_target_file": True,
                "reason": "Multiple agents modifying the same file"
            },
            {
                "agents": ["code-reviewer"],
                "check_target_module": True,
                "reason": "Code review in progress for this module"
            }
        ]
    }

    # 创建检测器
    detector = ConflictDetector(config)

    # 模拟新任务
    new_task = {
        "task_id": "task-new",
        "agent_type": "frontend-developer",
        "trigger_name": "code_change",
        "priority_score": 7.5,
        "metadata": {
            "target_file": "main/frontend/components/UserCard.vue"
        }
    }

    # 模拟现有任务
    existing_tasks = [
        {
            "task_id": "task-1",
            "agent_type": "frontend-developer",
            "trigger_name": "code_change",
            "status": "running",
            "created_at": datetime.now().isoformat(),
            "priority_score": 8.0,
            "metadata": {
                "target_file": "main/frontend/components/UserCard.vue"
            }
        },
        {
            "task_id": "task-2",
            "agent_type": "backend-developer",
            "trigger_name": "api_change",
            "status": "pending",
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "priority_score": 6.0,
            "metadata": {
                "target_module": "user_service"
            }
        },
        {
            "task_id": "task-3",
            "agent_type": "test",
            "trigger_name": "test_coverage_low",
            "status": "completed",
            "created_at": (datetime.now() - timedelta(hours=5)).isoformat(),
            "priority_score": 5.0,
            "metadata": {}
        }
    ]

    # 检测冲突
    print(f"\n🔍 Detecting conflicts...")
    conflicts = detector.detect_conflicts(new_task, existing_tasks)

    # 打印结果
    print(f"\n📊 Conflict Detection Results:")
    print(f"  Has Conflicts: {conflicts['has_conflicts']}")
    print(f"  Duplicate Tasks: {len(conflicts['duplicate_tasks'])}")
    print(f"  Conflicting Tasks: {len(conflicts['conflicting_tasks'])}")
    print(f"  Blocking Tasks: {len(conflicts['blocking_tasks'])}")

    if conflicts["duplicate_tasks"]:
        print(f"\n  🔄 Duplicate Tasks:")
        for dup in conflicts["duplicate_tasks"]:
            print(f"    - {dup['task_id']} (similarity: {dup['similarity']})")

    if conflicts["conflicting_tasks"]:
        print(f"\n  ⚠️ Conflicting Tasks:")
        for conf in conflicts["conflicting_tasks"]:
            print(f"    - {conf['task_id']}: {conf['conflict_reason']}")

    # 解决冲突
    print(f"\n💡 Resolving conflicts...")
    resolution = detector.resolve_conflicts(conflicts, new_task)
    print(f"  Action: {resolution['action']}")
    print(f"  Reason: {resolution['reason']}")

    # 获取状态
    status = detector.get_status()
    print(f"\n📊 Detector Status:")
    print(f"  Duplicate Window: {status['duplicate_window_hours']} hours")
    print(f"  Conflict Rules: {status['conflict_rules_count']}")

    print("\n✅ Conflict detector test completed!")


if __name__ == "__main__":
    main()
