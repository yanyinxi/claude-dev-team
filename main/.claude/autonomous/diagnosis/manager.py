#!/usr/bin/env python3
"""
诊断管理器
Diagnosis Manager

功能：
1. 统一管理健康监控和差距分析
2. 协调诊断流程
3. 生成综合诊断报告
4. 触发改进任务
"""

from datetime import datetime
from typing import Dict, Any, Optional

from .health_monitor import HealthMonitor
from .gap_analyzer import GapAnalyzer
from ..core.logging_utils import get_logger
from ..database.init_db import DatabaseManager


class DiagnosisManager:
    """诊断管理器"""

    def __init__(
        self,
        config: Dict[str, Any],
        db_manager: DatabaseManager
    ):
        """
        初始化诊断管理器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.db_manager = db_manager
        self.logger = get_logger("diagnosis_manager", log_file=".claude/autonomous/logs/manager.log")

        # 初始化组件
        self.health_monitor: Optional[HealthMonitor] = None
        self.gap_analyzer: Optional[GapAnalyzer] = None

        self._initialize_components()

    def _initialize_components(self):
        """初始化诊断组件"""
        diagnosis_config = self.config.get("diagnosis", {})

        # 初始化健康监控
        health_config = diagnosis_config.get("health_monitoring", {})
        if health_config.get("enabled", False):
            try:
                self.health_monitor = HealthMonitor(
                    config=health_config,
                    db_manager=self.db_manager
                )
                self.logger.info("Health monitor initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize health monitor: {e}")

        # 初始化差距分析
        gap_config = diagnosis_config.get("gap_analysis", {})
        if gap_config.get("enabled", False):
            try:
                self.gap_analyzer = GapAnalyzer(
                    config=gap_config,
                    db_manager=self.db_manager
                )
                self.logger.info("Gap analyzer initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize gap analyzer: {e}")

        self.logger.info("Diagnosis components initialized")

    def start(self):
        """启动诊断系统"""
        self.logger.info("Starting diagnosis system...")

        # 启动健康监控
        if self.health_monitor:
            try:
                self.health_monitor.start()
                self.logger.info("Health monitor started")
            except Exception as e:
                self.logger.error(f"Failed to start health monitor: {e}")

        self.logger.info("Diagnosis system started")

    def stop(self):
        """停止诊断系统"""
        self.logger.info("Stopping diagnosis system...")

        # 停止健康监控
        if self.health_monitor:
            try:
                self.health_monitor.stop()
                self.logger.info("Health monitor stopped")
            except Exception as e:
                self.logger.error(f"Failed to stop health monitor: {e}")

        self.logger.info("Diagnosis system stopped")

    def perform_full_diagnosis(self) -> Dict[str, Any]:
        """
        执行完整诊断

        Returns:
            Dict[str, Any]: 综合诊断报告
        """
        self.logger.info("Performing full diagnosis")

        diagnosis_report = {
            "timestamp": datetime.now().isoformat(),
            "health_report": None,
            "gap_analysis": None,
            "recommendations": [],
            "action_items": []
        }

        # 获取健康报告
        if self.health_monitor:
            try:
                health_report = self.health_monitor.get_health_report()
                diagnosis_report["health_report"] = health_report
                self.logger.info("Health report collected")
            except Exception as e:
                self.logger.error(f"Failed to get health report: {e}")

        # 执行差距分析
        if self.gap_analyzer:
            try:
                gap_analysis = self.gap_analyzer.analyze()
                diagnosis_report["gap_analysis"] = gap_analysis
                self.logger.info("Gap analysis completed")
            except Exception as e:
                self.logger.error(f"Failed to perform gap analysis: {e}")

        # 生成综合建议
        diagnosis_report["recommendations"] = self._generate_recommendations(diagnosis_report)

        # 生成行动项
        diagnosis_report["action_items"] = self._generate_action_items(diagnosis_report)

        self.logger.info(
            "Full diagnosis completed",
            context={
                "recommendations": len(diagnosis_report["recommendations"]),
                "action_items": len(diagnosis_report["action_items"])
            }
        )

        return diagnosis_report

    def _generate_recommendations(self, diagnosis_report: Dict[str, Any]) -> list:
        """
        生成综合建议

        Args:
            diagnosis_report: 诊断报告

        Returns:
            list: 建议列表
        """
        recommendations = []

        # 从健康报告提取建议
        health_report = diagnosis_report.get("health_report")
        if health_report:
            overall_status = health_report.get("overall_status")
            if overall_status in ["warning", "critical"]:
                recommendations.append({
                    "source": "health_monitor",
                    "priority": "high",
                    "message": f"系统健康状态为 {overall_status}，需要立即关注",
                    "details": health_report.get("metrics", {})
                })

        # 从差距分析提取建议
        gap_analysis = diagnosis_report.get("gap_analysis")
        if gap_analysis:
            gap_recommendations = gap_analysis.get("recommendations", [])
            for rec in gap_recommendations:
                recommendations.append({
                    "source": "gap_analyzer",
                    "priority": rec.get("priority", "medium"),
                    "category": rec.get("category"),
                    "action": rec.get("action"),
                    "steps": rec.get("steps", [])
                })

        return recommendations

    def _generate_action_items(self, diagnosis_report: Dict[str, Any]) -> list:
        """
        生成行动项（可转换为任务）

        Args:
            diagnosis_report: 诊断报告

        Returns:
            list: 行动项列表
        """
        action_items = []

        # 从建议生成行动项
        recommendations = diagnosis_report.get("recommendations", [])
        for rec in recommendations:
            priority_map = {
                "critical": 10,
                "high": 8,
                "medium": 5,
                "low": 3
            }

            action_items.append({
                "type": "improvement",
                "category": rec.get("category", "general"),
                "description": rec.get("action", rec.get("message")),
                "priority": priority_map.get(rec.get("priority", "medium"), 5),
                "steps": rec.get("steps", []),
                "source": rec.get("source"),
                "created_at": datetime.now().isoformat()
            })

        return action_items

    def get_health_report(self) -> Optional[Dict[str, Any]]:
        """
        获取健康报告

        Returns:
            Optional[Dict[str, Any]]: 健康报告
        """
        if self.health_monitor:
            return self.health_monitor.get_health_report()
        return None

    def get_gap_analysis(self) -> Optional[Dict[str, Any]]:
        """
        获取差距分析

        Returns:
            Optional[Dict[str, Any]]: 差距分析结果
        """
        if self.gap_analyzer:
            return self.gap_analyzer.get_last_analysis()
        return None

    def get_status(self) -> Dict[str, Any]:
        """
        获取诊断系统状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }

        if self.health_monitor:
            status["components"]["health_monitor"] = self.health_monitor.get_status()

        if self.gap_analyzer:
            status["components"]["gap_analyzer"] = self.gap_analyzer.get_status()

        return status


def main():
    """测试诊断管理器"""
    print("🧪 Testing Diagnosis Manager...")

    # 模拟配置
    config = {
        "diagnosis": {
            "health_monitoring": {
                "enabled": True,
                "check_interval_minutes": 1,
                "metrics": [
                    "system_uptime",
                    "error_rate",
                    "response_time",
                    "test_coverage",
                    "code_quality_score",
                    "intelligence_score"
                ]
            },
            "gap_analysis": {
                "enabled": True,
                "llm_model": "claude-sonnet-4-5",
                "analysis_depth": "comprehensive",
                "comparison_targets": [
                    "project_standards.md",
                    "best_practices"
                ]
            }
        }
    }

    # 创建依赖
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建管理器
    manager = DiagnosisManager(config, db_manager)

    # 启动诊断系统
    manager.start()

    # 获取状态
    status = manager.get_status()
    print(f"\n📊 Diagnosis System Status:")
    print(f"  Timestamp: {status['timestamp']}")
    print(f"  Components:")
    for component_name, component_status in status["components"].items():
        print(f"    - {component_name}:")
        print(f"        Enabled: {component_status.get('enabled', False)}")
        print(f"        Running: {component_status.get('running', False)}")

    # 等待健康监控收集数据
    import time
    print(f"\n⏳ Waiting for health monitoring...")
    time.sleep(65)

    # 执行完整诊断
    print(f"\n🔍 Performing full diagnosis...")
    diagnosis_report = manager.perform_full_diagnosis()

    # 打印诊断报告
    print(f"\n📋 Diagnosis Report:")
    print(f"  Timestamp: {diagnosis_report['timestamp']}")

    if diagnosis_report["health_report"]:
        health = diagnosis_report["health_report"]
        print(f"\n  Health Status: {health['overall_status']}")
        print(f"  Warning Count: {health['warning_count']}")

    if diagnosis_report["gap_analysis"]:
        gaps = diagnosis_report["gap_analysis"]
        print(f"\n  Gaps Found: {gaps['summary']['total_gaps']}")
        print(f"  By Severity: {gaps['summary']['by_severity']}")

    print(f"\n  Recommendations: {len(diagnosis_report['recommendations'])}")
    for i, rec in enumerate(diagnosis_report['recommendations'][:3], 1):
        print(f"    {i}. [{rec['priority']}] {rec.get('action', rec.get('message'))}")

    print(f"\n  Action Items: {len(diagnosis_report['action_items'])}")
    for i, item in enumerate(diagnosis_report['action_items'][:3], 1):
        print(f"    {i}. [{item['priority']}] {item['description']}")

    # 停止诊断系统
    manager.stop()

    print("\n✅ Diagnosis manager test completed!")


if __name__ == "__main__":
    main()
