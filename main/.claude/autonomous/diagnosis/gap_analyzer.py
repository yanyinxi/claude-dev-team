#!/usr/bin/env python3
"""
差距分析模块
Gap Analyzer Module

功能：
1. 当前状态 vs 理想状态分析
2. 识别改进空间
3. 生成改进建议
4. 与 LLM 集成
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core.logging_utils import get_logger
from ..database.init_db import DatabaseManager, TaskRepository, MetricsRepository


class GapAnalyzer:
    """差距分析器"""

    def __init__(
        self,
        config: Dict[str, Any],
        db_manager: DatabaseManager
    ):
        """
        初始化差距分析器

        Args:
            config: 配置字典（来自 autonomous_config.yaml）
            db_manager: 数据库管理器实例
        """
        self.config = config
        self.task_repo = TaskRepository(db_manager)
        self.metrics_repo = MetricsRepository(db_manager)
        self.logger = get_logger("gap_analyzer", log_file=".claude/autonomous/logs/diagnosis.log")

        # 解析配置
        self.enabled = config.get("enabled", True)
        self.llm_model = config.get("llm_model", "claude-sonnet-4-5")
        self.analysis_depth = config.get("analysis_depth", "comprehensive")
        self.comparison_targets = config.get("comparison_targets", [])

        # 分析结果缓存
        self.last_analysis: Optional[Dict[str, Any]] = None
        self.last_analysis_time: Optional[datetime] = None

    def analyze(self) -> Dict[str, Any]:
        """
        执行差距分析

        Returns:
            Dict[str, Any]: 分析结果
        """
        self.logger.info("Starting gap analysis")

        try:
            # 收集当前状态
            current_state = self._collect_current_state()

            # 加载理想状态
            ideal_state = self._load_ideal_state()

            # 执行差距分析
            gaps = self._identify_gaps(current_state, ideal_state)

            # 生成改进建议
            recommendations = self._generate_recommendations(gaps)

            # 计算优先级
            prioritized_gaps = self._prioritize_gaps(gaps)

            # 构建分析结果
            analysis_result = {
                "timestamp": datetime.now().isoformat(),
                "analysis_depth": self.analysis_depth,
                "current_state": current_state,
                "ideal_state": ideal_state,
                "gaps": prioritized_gaps,
                "recommendations": recommendations,
                "summary": self._generate_summary(prioritized_gaps)
            }

            # 缓存结果
            self.last_analysis = analysis_result
            self.last_analysis_time = datetime.now()

            self.logger.info(
                "Gap analysis completed",
                context={
                    "gaps_found": len(prioritized_gaps),
                    "recommendations": len(recommendations)
                }
            )

            return analysis_result

        except Exception as e:
            self.logger.exception(
                "Failed to perform gap analysis",
                context={"error": str(e)}
            )
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "gaps": [],
                "recommendations": []
            }

    def _collect_current_state(self) -> Dict[str, Any]:
        """
        收集当前系统状态

        Returns:
            Dict[str, Any]: 当前状态
        """
        self.logger.debug("Collecting current state")

        current_state = {
            "code_quality": self._analyze_code_quality(),
            "test_coverage": self._analyze_test_coverage(),
            "documentation": self._analyze_documentation(),
            "architecture": self._analyze_architecture(),
            "performance": self._analyze_performance(),
            "security": self._analyze_security()
        }

        return current_state

    def _analyze_code_quality(self) -> Dict[str, Any]:
        """分析代码质量"""
        # TODO: 集成 ruff, pylint 等工具
        # 1. 运行代码质量检查
        # 2. 统计问题数量和类型
        # 3. 计算质量分数

        # 模拟代码质量分析
        return {
            "score": 8.5,
            "issues": {
                "critical": 0,
                "high": 2,
                "medium": 5,
                "low": 10
            },
            "metrics": {
                "complexity": 6.2,
                "maintainability": 8.0,
                "duplication": 3.5
            }
        }

    def _analyze_test_coverage(self) -> Dict[str, Any]:
        """分析测试覆盖率"""
        # TODO: 集成 pytest-cov
        # 1. 运行测试覆盖率分析
        # 2. 统计覆盖率数据
        # 3. 识别未覆盖的关键代码

        # 模拟测试覆盖率分析
        return {
            "overall": 0.75,
            "by_module": {
                "backend": 0.80,
                "frontend": 0.70,
                "utils": 0.85
            },
            "uncovered_critical": [
                "main/backend/services/payment_service.py",
                "main/backend/api/routes/admin_router.py"
            ]
        }

    def _analyze_documentation(self) -> Dict[str, Any]:
        """分析文档完整性"""
        # TODO: 扫描文档文件
        # 1. 检查 README、API 文档、架构文档
        # 2. 识别缺失的文档
        # 3. 评估文档质量

        # 模拟文档分析
        return {
            "completeness": 0.65,
            "missing": [
                "API 端点文档不完整",
                "缺少部署指南",
                "缺少故障排查文档"
            ],
            "outdated": [
                "README.md 版本信息过时",
                "架构图需要更新"
            ]
        }

    def _analyze_architecture(self) -> Dict[str, Any]:
        """分析架构设计"""
        # TODO: 分析代码结构
        # 1. 检查目录结构
        # 2. 分析模块依赖
        # 3. 识别架构问题

        # 模拟架构分析
        return {
            "score": 8.0,
            "issues": [
                "部分模块耦合度过高",
                "缺少统一的错误处理机制"
            ],
            "strengths": [
                "清晰的分层架构",
                "良好的模块化设计"
            ]
        }

    def _analyze_performance(self) -> Dict[str, Any]:
        """分析性能指标"""
        # TODO: 从指标数据库读取性能数据
        recent_metrics = self.metrics_repo.get_recent_metrics("response_time_ms", days=7)

        if recent_metrics:
            avg_response_time = sum(m["metric_value"] for m in recent_metrics) / len(recent_metrics)
        else:
            avg_response_time = 0

        return {
            "response_time_ms": avg_response_time,
            "bottlenecks": [
                "数据库查询未优化",
                "缺少缓存机制"
            ],
            "optimization_opportunities": [
                "添加 Redis 缓存",
                "优化 N+1 查询"
            ]
        }

    def _analyze_security(self) -> Dict[str, Any]:
        """分析安全性"""
        # TODO: 集成安全扫描工具
        # 1. 扫描常见漏洞
        # 2. 检查依赖安全性
        # 3. 识别安全风险

        # 模拟安全分析
        return {
            "score": 7.5,
            "vulnerabilities": {
                "critical": 0,
                "high": 1,
                "medium": 3,
                "low": 5
            },
            "issues": [
                "部分 API 缺少认证",
                "敏感数据未加密存储"
            ]
        }

    def _load_ideal_state(self) -> Dict[str, Any]:
        """
        加载理想状态（从 project_standards.md 等）

        Returns:
            Dict[str, Any]: 理想状态
        """
        self.logger.debug("Loading ideal state")

        ideal_state = {
            "code_quality": {
                "score": 9.0,
                "max_issues": {
                    "critical": 0,
                    "high": 0,
                    "medium": 3,
                    "low": 10
                }
            },
            "test_coverage": {
                "overall": 0.80,
                "critical_modules": 0.90
            },
            "documentation": {
                "completeness": 0.90,
                "required": [
                    "README.md",
                    "API 文档",
                    "架构文档",
                    "部署指南",
                    "故障排查文档"
                ]
            },
            "architecture": {
                "score": 9.0,
                "principles": [
                    "低耦合高内聚",
                    "单一职责原则",
                    "依赖倒置原则"
                ]
            },
            "performance": {
                "response_time_ms": 300,
                "cache_hit_rate": 0.80
            },
            "security": {
                "score": 9.0,
                "max_vulnerabilities": {
                    "critical": 0,
                    "high": 0,
                    "medium": 2,
                    "low": 5
                }
            }
        }

        return ideal_state

    def _identify_gaps(
        self,
        current_state: Dict[str, Any],
        ideal_state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        识别差距

        Args:
            current_state: 当前状态
            ideal_state: 理想状态

        Returns:
            List[Dict[str, Any]]: 差距列表
        """
        self.logger.debug("Identifying gaps")

        gaps = []

        # 代码质量差距
        if current_state["code_quality"]["score"] < ideal_state["code_quality"]["score"]:
            gaps.append({
                "category": "code_quality",
                "severity": "medium",
                "current": current_state["code_quality"]["score"],
                "target": ideal_state["code_quality"]["score"],
                "gap": ideal_state["code_quality"]["score"] - current_state["code_quality"]["score"],
                "description": f"代码质量分数低于目标 ({current_state['code_quality']['score']} < {ideal_state['code_quality']['score']})"
            })

        # 测试覆盖率差距
        if current_state["test_coverage"]["overall"] < ideal_state["test_coverage"]["overall"]:
            gaps.append({
                "category": "test_coverage",
                "severity": "high",
                "current": current_state["test_coverage"]["overall"],
                "target": ideal_state["test_coverage"]["overall"],
                "gap": ideal_state["test_coverage"]["overall"] - current_state["test_coverage"]["overall"],
                "description": f"测试覆盖率低于目标 ({current_state['test_coverage']['overall']*100:.1f}% < {ideal_state['test_coverage']['overall']*100:.1f}%)"
            })

        # 文档完整性差距
        if current_state["documentation"]["completeness"] < ideal_state["documentation"]["completeness"]:
            gaps.append({
                "category": "documentation",
                "severity": "medium",
                "current": current_state["documentation"]["completeness"],
                "target": ideal_state["documentation"]["completeness"],
                "gap": ideal_state["documentation"]["completeness"] - current_state["documentation"]["completeness"],
                "description": f"文档完整性低于目标 ({current_state['documentation']['completeness']*100:.1f}% < {ideal_state['documentation']['completeness']*100:.1f}%)",
                "missing": current_state["documentation"]["missing"]
            })

        # 性能差距
        if current_state["performance"]["response_time_ms"] > ideal_state["performance"]["response_time_ms"]:
            gaps.append({
                "category": "performance",
                "severity": "high",
                "current": current_state["performance"]["response_time_ms"],
                "target": ideal_state["performance"]["response_time_ms"],
                "gap": current_state["performance"]["response_time_ms"] - ideal_state["performance"]["response_time_ms"],
                "description": f"响应时间高于目标 ({current_state['performance']['response_time_ms']:.0f}ms > {ideal_state['performance']['response_time_ms']:.0f}ms)",
                "bottlenecks": current_state["performance"]["bottlenecks"]
            })

        # 安全性差距
        if current_state["security"]["score"] < ideal_state["security"]["score"]:
            gaps.append({
                "category": "security",
                "severity": "critical",
                "current": current_state["security"]["score"],
                "target": ideal_state["security"]["score"],
                "gap": ideal_state["security"]["score"] - current_state["security"]["score"],
                "description": f"安全分数低于目标 ({current_state['security']['score']} < {ideal_state['security']['score']})",
                "issues": current_state["security"]["issues"]
            })

        return gaps

    def _generate_recommendations(self, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        生成改进建议

        Args:
            gaps: 差距列表

        Returns:
            List[Dict[str, Any]]: 改进建议列表
        """
        self.logger.debug("Generating recommendations")

        recommendations = []

        for gap in gaps:
            category = gap["category"]

            if category == "code_quality":
                recommendations.append({
                    "category": category,
                    "priority": "medium",
                    "action": "运行代码质量检查并修复问题",
                    "steps": [
                        "运行 ruff check 识别问题",
                        "修复 high 和 medium 级别问题",
                        "重构复杂度过高的函数"
                    ]
                })

            elif category == "test_coverage":
                recommendations.append({
                    "category": category,
                    "priority": "high",
                    "action": "增加测试覆盖率",
                    "steps": [
                        "识别未覆盖的关键代码",
                        "编写单元测试",
                        "编写集成测试",
                        "目标：覆盖率达到 80%"
                    ]
                })

            elif category == "documentation":
                recommendations.append({
                    "category": category,
                    "priority": "medium",
                    "action": "完善文档",
                    "steps": [
                        "补充缺失的文档",
                        "更新过时的文档",
                        "添加代码示例"
                    ],
                    "missing": gap.get("missing", [])
                })

            elif category == "performance":
                recommendations.append({
                    "category": category,
                    "priority": "high",
                    "action": "优化性能",
                    "steps": [
                        "添加 Redis 缓存",
                        "优化数据库查询",
                        "添加数据库索引",
                        "实现查询结果缓存"
                    ],
                    "bottlenecks": gap.get("bottlenecks", [])
                })

            elif category == "security":
                recommendations.append({
                    "category": category,
                    "priority": "critical",
                    "action": "修复安全问题",
                    "steps": [
                        "添加 API 认证",
                        "加密敏感数据",
                        "更新依赖版本",
                        "运行安全扫描"
                    ],
                    "issues": gap.get("issues", [])
                })

        return recommendations

    def _prioritize_gaps(self, gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        按优先级排序差距

        Args:
            gaps: 差距列表

        Returns:
            List[Dict[str, Any]]: 排序后的差距列表
        """
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

        return sorted(
            gaps,
            key=lambda g: (severity_order.get(g["severity"], 4), -g["gap"])
        )

    def _generate_summary(self, gaps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成分析摘要

        Args:
            gaps: 差距列表

        Returns:
            Dict[str, Any]: 摘要
        """
        severity_counts = {}
        for gap in gaps:
            severity = gap["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "total_gaps": len(gaps),
            "by_severity": severity_counts,
            "top_priorities": [
                gap["description"]
                for gap in gaps[:3]
            ]
        }

    def get_last_analysis(self) -> Optional[Dict[str, Any]]:
        """
        获取上次分析结果

        Returns:
            Optional[Dict[str, Any]]: 上次分析结果
        """
        return self.last_analysis

    def get_status(self) -> Dict[str, Any]:
        """
        获取分析器状态

        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "enabled": self.enabled,
            "llm_model": self.llm_model,
            "analysis_depth": self.analysis_depth,
            "last_analysis_time": self.last_analysis_time.isoformat() if self.last_analysis_time else None,
            "last_analysis_summary": self.last_analysis.get("summary") if self.last_analysis else None
        }


def main():
    """测试差距分析器"""
    print("🧪 Testing Gap Analyzer...")

    # 模拟配置
    config = {
        "enabled": True,
        "llm_model": "claude-sonnet-4-5",
        "analysis_depth": "comprehensive",
        "comparison_targets": [
            "project_standards.md",
            "best_practices",
            "industry_benchmarks"
        ]
    }

    # 创建依赖
    db_manager = DatabaseManager()
    db_manager.initialize()

    # 创建分析器
    analyzer = GapAnalyzer(config, db_manager)

    # 执行分析
    print(f"\n🔍 Performing gap analysis...")
    result = analyzer.analyze()

    # 打印结果
    print(f"\n📊 Analysis Results:")
    print(f"  Timestamp: {result['timestamp']}")
    print(f"  Total Gaps: {result['summary']['total_gaps']}")
    print(f"  By Severity: {result['summary']['by_severity']}")

    print(f"\n🎯 Top Priorities:")
    for i, priority in enumerate(result['summary']['top_priorities'], 1):
        print(f"  {i}. {priority}")

    print(f"\n💡 Recommendations:")
    for rec in result['recommendations'][:3]:
        print(f"  - [{rec['priority']}] {rec['action']}")
        for step in rec['steps']:
            print(f"      • {step}")

    print("\n✅ Gap analyzer test completed!")


if __name__ == "__main__":
    main()
