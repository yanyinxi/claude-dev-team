#!/usr/bin/env python3
"""
基于 LLM 的任务触发器
LLM-Driven Task Trigger

功能：
1. 智能差距分析
2. 模式识别
3. 改进机会识别
4. 任务生成和入队
"""

import time
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import threading

from ..core.logging_utils import get_logger
from ..core.task_queue import TaskQueue
from ..database.init_db import DatabaseManager, TaskRepository


class LLMDrivenTrigger:
    """基于 LLM 的任务触发器"""

    def __init__(
        self,
        config: Dict[str, Any],
        task_queue: TaskQueue,
        db_manager: DatabaseManager
    ):
        """
        初始化 LLM 触发器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            task_queue: 任务队列实例
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.task_queue = task_queue
        self.task_repo = TaskRepository(db_manager)
        self.logger = get_logger("llm_driven_trigger", log_file=".claude/autonomous/logs/triggers.log")

        # 解析配置
        self.enabled = config.get("enabled", True)
        self.analysis_frequency = config.get("analysis_frequency", "daily")
        self.model = config.get("model", "claude-sonnet-4-5")
        self.triggers = config.get("triggers", [])

        # 运行状态
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # 分析间隔（根据频率配置）
        self.analysis_intervals = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "on-demand": None  # 手动触发
        }
        self.analysis_interval = self.analysis_intervals.get(self.analysis_frequency)

        # 上次分析时间
        self.last_analysis: Dict[str, datetime] = {}

    def start(self):
        """启动 LLM 触发器"""
        if not self.enabled:
            self.logger.info("LLM-driven trigger is disabled")
            return

        if self.running:
            self.logger.warning("LLM-driven trigger is already running")
            return

        if self.analysis_frequency == "on-demand":
            self.logger.info("LLM-driven trigger is in on-demand mode (manual trigger only)")
            return

        self.running = True
        self.thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.thread.start()

        self.logger.info(
            "LLM-driven trigger started",
            context={
                "triggers_count": len(self.triggers),
                "frequency": self.analysis_frequency
            }
        )

    def stop(self):
        """停止 LLM 触发器"""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

        self.logger.info("LLM-driven trigger stopped")

    def _analysis_loop(self):
        """分析循环：定期执行 LLM 分析"""
        while self.running:
            try:
                now = datetime.now()

                # 检查每个触发器
                for trigger_config in self.triggers:
                    name = trigger_config["name"]
                    last_analysis = self.last_analysis.get(name)

                    # 检查是否需要分析
                    if not last_analysis or (now - last_analysis) >= self.analysis_interval:
                        self._perform_analysis(trigger_config)
                        self.last_analysis[name] = now

                # 休眠 1 小时后再检查
                time.sleep(3600)

            except Exception as e:
                self.logger.exception(
                    "Error in LLM-driven trigger loop",
                    context={"error": str(e)}
                )
                time.sleep(3600)

    def _perform_analysis(self, trigger_config: Dict[str, Any]):
        """
        执行 LLM 分析

        Args:
            trigger_config: 触发器配置
        """
        name = trigger_config["name"]
        description = trigger_config["description"]
        priority = trigger_config["priority"]

        self.logger.info(
            f"Performing LLM analysis: {name}",
            context={"trigger_name": name}
        )

        try:
            # 根据触发器类型执行不同的分析
            if name == "gap_analysis":
                analysis_result = self._gap_analysis()
            elif name == "pattern_recognition":
                analysis_result = self._pattern_recognition()
            elif name == "improvement_opportunities":
                analysis_result = self._improvement_opportunities()
            else:
                self.logger.warning(f"Unknown LLM trigger type: {name}")
                return

            # 如果分析发现需要创建任务
            if analysis_result.get("create_task", False):
                self._create_task_from_analysis(trigger_config, analysis_result)

        except Exception as e:
            self.logger.exception(
                f"Failed to perform LLM analysis for {name}",
                context={"trigger_name": name, "error": str(e)}
            )

    def _gap_analysis(self) -> Dict[str, Any]:
        """
        差距分析：当前状态 vs 理想状态

        Returns:
            Dict[str, Any]: 分析结果
        """
        self.logger.info("Performing gap analysis")

        # TODO: 集成 Claude API 进行智能分析
        # 1. 读取 project_standards.md
        # 2. 分析当前代码库状态
        # 3. 识别差距和改进空间
        # 4. 生成任务建议

        # 模拟分析结果
        return {
            "create_task": True,
            "gaps_found": [
                "测试覆盖率低于 70%",
                "部分 API 缺少错误处理",
                "文档不完整"
            ],
            "recommendations": [
                "增加单元测试",
                "完善错误处理",
                "更新 API 文档"
            ]
        }

    def _pattern_recognition(self) -> Dict[str, Any]:
        """
        模式识别：发现重复问题

        Returns:
            Dict[str, Any]: 分析结果
        """
        self.logger.info("Performing pattern recognition")

        # TODO: 集成 Claude API 进行模式识别
        # 1. 分析执行历史
        # 2. 识别重复失败的任务
        # 3. 发现常见错误模式
        # 4. 生成预防性任务

        # 模拟分析结果
        return {
            "create_task": False,
            "patterns_found": [],
            "recommendations": []
        }

    def _improvement_opportunities(self) -> Dict[str, Any]:
        """
        改进机会识别

        Returns:
            Dict[str, Any]: 分析结果
        """
        self.logger.info("Identifying improvement opportunities")

        # TODO: 集成 Claude API 进行机会识别
        # 1. 分析代码质量指标
        # 2. 识别性能瓶颈
        # 3. 发现架构改进空间
        # 4. 生成优化任务

        # 模拟分析结果
        return {
            "create_task": True,
            "opportunities_found": [
                "数据库查询可以优化",
                "前端组件可以复用"
            ],
            "recommendations": [
                "添加数据库索引",
                "重构通用组件"
            ]
        }

    def _create_task_from_analysis(
        self,
        trigger_config: Dict[str, Any],
        analysis_result: Dict[str, Any]
    ):
        """
        从分析结果创建任务

        Args:
            trigger_config: 触发器配置
            analysis_result: 分析结果
        """
        name = trigger_config["name"]
        description = trigger_config["description"]
        priority = trigger_config["priority"]

        # 生成任务 ID
        now = datetime.now()
        task_id = f"llm-{name}-{now.strftime('%Y%m%d%H%M%S')}"

        try:
            # 创建任务元数据
            metadata = {
                "trigger_type": "llm_driven",
                "analysis_type": name,
                "analysis_result": analysis_result,
                "model": self.model,
                "triggered_at": now.isoformat()
            }

            # 构建详细描述
            detailed_description = f"{description}\n\n"
            if "gaps_found" in analysis_result:
                detailed_description += "发现的差距:\n"
                for gap in analysis_result["gaps_found"]:
                    detailed_description += f"- {gap}\n"
            if "recommendations" in analysis_result:
                detailed_description += "\n建议:\n"
                for rec in analysis_result["recommendations"]:
                    detailed_description += f"- {rec}\n"

            # 添加到数据库
            success = self.task_repo.create_task(
                task_id=task_id,
                task_type="llm_driven",
                description=detailed_description,
                priority=priority,
                scheduled_at=now,
                metadata=metadata
            )

            if success:
                # 添加到内存队列
                self.task_queue.add_task(
                    task_id=task_id,
                    task_type="llm_driven",
                    description=detailed_description,
                    priority=priority,
                    scheduled_at=now,
                    metadata=metadata
                )

                self.logger.info(
                    f"LLM analysis task created: {task_id}",
                    context={
                        "task_id": task_id,
                        "analysis_type": name,
                        "priority": priority
                    }
                )
            else:
                self.logger.error(
                    f"Failed to create task in database: {task_id}",
                    context={"task_id": task_id, "analysis_type": name}
                )

        except Exception as e:
            self.logger.exception(
                f"Failed to create task from LLM analysis {name}",
                context={"analysis_type": name, "error": str(e)}
            )

    def trigger_manual_analysis(self, analysis_type: str):
        """
        手动触发分析

        Args:
            analysis_type: 分析类型（gap_analysis, pattern_recognition, improvement_opportunities）
        """
        # 查找匹配的触发器配置
        for trigger_config in self.triggers:
            if trigger_config["name"] == analysis_type:
                self._perform_analysis(trigger_config)
                return

        self.logger.warning(f"Unknown analysis type: {analysis_type}")

    def get_status(self) -> Dict[str, Any]:
        """
        获取触发器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "enabled": self.enabled,
            "running": self.running,
            "frequency": self.analysis_frequency,
            "model": self.model,
            "triggers_count": len(self.triggers),
            "last_analysis": {
                name: timestamp.isoformat()
                for name, timestamp in self.last_analysis.items()
            }
        }


def main():
    """测试 LLM 触发器"""
    print("🧪 Testing LLM-Driven Trigger...")

    # 模拟配置
    config = {
        "enabled": True,
        "analysis_frequency": "on-demand",
        "model": "claude-sonnet-4-5",
        "triggers": [
            {
                "name": "gap_analysis",
                "description": "差距分析：当前状态 vs 理想状态",
                "priority": 7
            },
            {
                "name": "pattern_recognition",
                "description": "模式识别：发现重复问题",
                "priority": 6
            },
            {
                "name": "improvement_opportunities",
                "description": "改进机会识别",
                "priority": 5
            }
        ]
    }

    # 创建依赖
    task_queue = TaskQueue()
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建触发器
    trigger = LLMDrivenTrigger(config, task_queue, db_manager)

    # 获取状态
    status = trigger.get_status()
    print(f"\n📊 Trigger Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Frequency: {status['frequency']}")
    print(f"  Model: {status['model']}")
    print(f"  Triggers: {status['triggers_count']}")

    # 手动触发分析
    print(f"\n🎯 Triggering manual analysis...")
    trigger.trigger_manual_analysis("gap_analysis")
    trigger.trigger_manual_analysis("improvement_opportunities")

    # 等待分析完成
    time.sleep(2)

    # 检查队列
    print(f"\n📋 Task Queue Status:")
    stats = task_queue.get_statistics()
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Ready tasks: {stats['ready_tasks']}")

    print("\n✅ LLM-driven trigger test completed!")


if __name__ == "__main__":
    main()
