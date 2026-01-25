#!/usr/bin/env python3
"""
健康监控模块
Health Monitor Module

功能：
1. 系统健康指标监控
2. 异常检测
3. 性能分析
4. 健康报告生成
"""

import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import threading

from ..core.logging_utils import get_logger
from ..database.init_db import DatabaseManager, MetricsRepository


class HealthMonitor:
    """健康监控器"""

    def __init__(
        self,
        config: Dict[str, Any],
        db_manager: DatabaseManager
    ):
        """
        初始化健康监控器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.metrics_repo = MetricsRepository(db_manager)
        self.logger = get_logger("health_monitor", log_file=".claude/autonomous/logs/diagnosis.log")

        # 解析配置
        self.enabled = config.get("enabled", True)
        self.check_interval = config.get("check_interval_minutes", 60) * 60  # 转换为秒
        self.metrics = config.get("metrics", [])

        # 运行状态
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # 健康状态
        self.health_status: Dict[str, Any] = {}

    def start(self):
        """启动健康监控"""
        if not self.enabled:
            self.logger.info("Health monitoring is disabled")
            return

        if self.running:
            self.logger.warning("Health monitoring is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

        self.logger.info(
            "Health monitoring started",
            context={
                "check_interval": self.check_interval,
                "metrics_count": len(self.metrics)
            }
        )

    def stop(self):
        """停止健康监控"""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)

        self.logger.info("Health monitoring stopped")

    def _monitor_loop(self):
        """监控循环：定期收集健康指标"""
        while self.running:
            try:
                # 收集所有指标
                self._collect_metrics()

                # 休眠后再检查
                time.sleep(self.check_interval)

            except Exception as e:
                self.logger.exception(
                    "Error in health monitoring loop",
                    context={"error": str(e)}
                )
                time.sleep(self.check_interval)

    def _collect_metrics(self):
        """收集所有健康指标"""
        self.logger.debug("Collecting health metrics")

        for metric_name in self.metrics:
            try:
                if metric_name == "system_uptime":
                    self._collect_system_uptime()
                elif metric_name == "error_rate":
                    self._collect_error_rate()
                elif metric_name == "response_time":
                    self._collect_response_time()
                elif metric_name == "test_coverage":
                    self._collect_test_coverage()
                elif metric_name == "code_quality_score":
                    self._collect_code_quality_score()
                elif metric_name == "intelligence_score":
                    self._collect_intelligence_score()
                else:
                    self.logger.warning(f"Unknown metric: {metric_name}")

            except Exception as e:
                self.logger.error(
                    f"Failed to collect metric {metric_name}",
                    context={"metric_name": metric_name, "error": str(e)}
                )

    def _collect_system_uptime(self):
        """收集系统运行时间"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time

            self.metrics_repo.record_metric(
                metric_name="system_uptime",
                metric_value=uptime_seconds,
                metadata={"unit": "seconds"}
            )

            self.health_status["system_uptime"] = {
                "value": uptime_seconds,
                "unit": "seconds",
                "status": "healthy"
            }

            self.logger.debug(
                "System uptime collected",
                context={"uptime_seconds": uptime_seconds}
            )

        except Exception as e:
            self.logger.error(f"Failed to collect system uptime: {e}")

    def _collect_error_rate(self):
        """收集错误率"""
        try:
            # TODO: 从执行历史中计算错误率
            # 1. 查询最近 24 小时的任务执行记录
            # 2. 计算失败任务比例
            # 3. 记录到指标数据库

            # 模拟错误率
            error_rate = 0.02  # 2%

            self.metrics_repo.record_metric(
                metric_name="error_rate",
                metric_value=error_rate,
                metadata={"unit": "percentage"}
            )

            self.health_status["error_rate"] = {
                "value": error_rate,
                "unit": "percentage",
                "status": "healthy" if error_rate < 0.05 else "warning"
            }

            self.logger.debug(
                "Error rate collected",
                context={"error_rate": error_rate}
            )

        except Exception as e:
            self.logger.error(f"Failed to collect error rate: {e}")

    def _collect_response_time(self):
        """收集响应时间"""
        try:
            # TODO: 从执行历史中计算平均响应时间
            # 1. 查询最近 1 小时的任务执行记录
            # 2. 计算平均执行时长
            # 3. 记录到指标数据库

            # 模拟响应时间
            response_time_ms = 350

            self.metrics_repo.record_metric(
                metric_name="response_time_ms",
                metric_value=response_time_ms,
                metadata={"unit": "milliseconds"}
            )

            self.health_status["response_time"] = {
                "value": response_time_ms,
                "unit": "milliseconds",
                "status": "healthy" if response_time_ms < 500 else "warning"
            }

            self.logger.debug(
                "Response time collected",
                context={"response_time_ms": response_time_ms}
            )

        except Exception as e:
            self.logger.error(f"Failed to collect response time: {e}")

    def _collect_test_coverage(self):
        """收集测试覆盖率"""
        try:
            # TODO: 从测试报告中读取覆盖率
            # 1. 运行 pytest --cov
            # 2. 解析覆盖率报告
            # 3. 记录到指标数据库

            # 模拟测试覆盖率
            test_coverage = 0.75  # 75%

            self.metrics_repo.record_metric(
                metric_name="test_coverage",
                metric_value=test_coverage,
                metadata={"unit": "percentage"}
            )

            self.health_status["test_coverage"] = {
                "value": test_coverage,
                "unit": "percentage",
                "status": "healthy" if test_coverage >= 0.7 else "warning"
            }

            self.logger.debug(
                "Test coverage collected",
                context={"test_coverage": test_coverage}
            )

        except Exception as e:
            self.logger.error(f"Failed to collect test coverage: {e}")

    def _collect_code_quality_score(self):
        """收集代码质量分数"""
        try:
            # TODO: 从代码质量工具中读取分数
            # 1. 运行 ruff check
            # 2. 计算质量分数
            # 3. 记录到指标数据库

            # 模拟代码质量分数
            code_quality_score = 8.5  # 0-10 分

            self.metrics_repo.record_metric(
                metric_name="code_quality_score",
                metric_value=code_quality_score,
                metadata={"unit": "score", "max": 10}
            )

            self.health_status["code_quality_score"] = {
                "value": code_quality_score,
                "unit": "score",
                "status": "healthy" if code_quality_score >= 7.0 else "warning"
            }

            self.logger.debug(
                "Code quality score collected",
                context={"code_quality_score": code_quality_score}
            )

        except Exception as e:
            self.logger.error(f"Failed to collect code quality score: {e}")

    def _collect_intelligence_score(self):
        """收集智能化分数"""
        try:
            # TODO: 计算系统智能化程度
            # 1. 分析自动化任务比例
            # 2. 评估 LLM 驱动任务效果
            # 3. 计算智能化分数

            # 模拟智能化分数
            intelligence_score = 7.0  # 0-10 分

            self.metrics_repo.record_metric(
                metric_name="intelligence_score",
                metric_value=intelligence_score,
                metadata={"unit": "score", "max": 10}
            )

            self.health_status["intelligence_score"] = {
                "value": intelligence_score,
                "unit": "score",
                "status": "healthy" if intelligence_score >= 6.0 else "warning"
            }

            self.logger.debug(
                "Intelligence score collected",
                context={"intelligence_score": intelligence_score}
            )

        except Exception as e:
            self.logger.error(f"Failed to collect intelligence score: {e}")

    def get_health_report(self) -> Dict[str, Any]:
        """
        获取健康报告

        Returns:
            Dict[str, Any]: 健康报告
        """
        # 计算整体健康状态
        overall_status = "healthy"
        warning_count = sum(
            1 for metric in self.health_status.values()
            if metric.get("status") == "warning"
        )

        if warning_count > 0:
            overall_status = "warning"
        if warning_count >= len(self.health_status) / 2:
            overall_status = "critical"

        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "warning_count": warning_count,
            "metrics": self.health_status
        }

    def get_status(self) -> Dict[str, Any]:
        """
        获取监控器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "enabled": self.enabled,
            "running": self.running,
            "check_interval": self.check_interval,
            "metrics_count": len(self.metrics),
            "health_report": self.get_health_report()
        }


def main():
    """测试健康监控器"""
    print("🧪 Testing Health Monitor...")

    # 模拟配置
    config = {
        "enabled": True,
        "check_interval_minutes": 1,  # 1 分钟（测试用）
        "metrics": [
            "system_uptime",
            "error_rate",
            "response_time",
            "test_coverage",
            "code_quality_score",
            "intelligence_score"
        ]
    }

    # 创建依赖
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建监控器
    monitor = HealthMonitor(config, db_manager)

    # 启动监控
    monitor.start()

    # 获取状态
    status = monitor.get_status()
    print(f"\n📊 Monitor Status:")
    print(f"  Enabled: {status['enabled']}")
    print(f"  Running: {status['running']}")
    print(f"  Check Interval: {status['check_interval']} seconds")

    # 等待收集指标
    print(f"\n⏳ Waiting for metrics collection...")
    time.sleep(65)  # 等待超过 1 分钟

    # 获取健康报告
    report = monitor.get_health_report()
    print(f"\n📋 Health Report:")
    print(f"  Timestamp: {report['timestamp']}")
    print(f"  Overall Status: {report['overall_status']}")
    print(f"  Warning Count: {report['warning_count']}")
    print(f"\n  Metrics:")
    for metric_name, metric_data in report["metrics"].items():
        print(f"    - {metric_name}: {metric_data['value']} {metric_data['unit']} ({metric_data['status']})")

    # 停止监控
    monitor.stop()

    print("\n✅ Health monitor test completed!")


if __name__ == "__main__":
    main()
