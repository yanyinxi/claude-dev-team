#!/usr/bin/env python3
"""
Quality Evaluator - 质量评估模块
提供多维度质量评分算法
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class QualityScore:
    """质量评分结果"""
    overall: float  # 总分 (0-10)
    efficiency: float  # 效率 (0-10)
    code_quality: float  # 代码质量 (0-10)
    test_coverage: float  # 测试覆盖率 (0-10)
    documentation: float  # 文档完整性 (0-10)
    details: Dict[str, Any]  # 详细信息


class QualityEvaluator:
    """质量评估器"""

    def __init__(self):
        self.weights = {
            "efficiency": 0.25,
            "code_quality": 0.30,
            "test_coverage": 0.25,
            "documentation": 0.20
        }

    def evaluate(self, execution_data: Dict[str, Any]) -> QualityScore:
        """
        评估任务质量

        Args:
            execution_data: 执行数据，包含：
                - duration: 执行时间（秒）
                - files_modified: 修改的文件列表
                - test_files: 测试文件列表
                - doc_files: 文档文件列表
                - success: 是否成功
                - errors: 错误列表

        Returns:
            QualityScore: 质量评分结果
        """
        # 评估各个维度
        efficiency = self._evaluate_efficiency(execution_data)
        code_quality = self._evaluate_code_quality(execution_data)
        test_coverage = self._evaluate_test_coverage(execution_data)
        documentation = self._evaluate_documentation(execution_data)

        # 计算总分
        overall = (
            efficiency * self.weights["efficiency"] +
            code_quality * self.weights["code_quality"] +
            test_coverage * self.weights["test_coverage"] +
            documentation * self.weights["documentation"]
        )

        return QualityScore(
            overall=round(overall, 2),
            efficiency=round(efficiency, 2),
            code_quality=round(code_quality, 2),
            test_coverage=round(test_coverage, 2),
            documentation=round(documentation, 2),
            details={
                "duration": execution_data.get("duration", 0),
                "files_modified": len(execution_data.get("files_modified", [])),
                "test_files": len(execution_data.get("test_files", [])),
                "doc_files": len(execution_data.get("doc_files", []))
            }
        )

    def _evaluate_efficiency(self, data: Dict[str, Any]) -> float:
        """
        评估效率（0-10分）

        考虑因素：
        - 执行时间
        - 并行执行
        - 文件修改数
        """
        score = 7.0  # 基础分

        # 执行时间评分
        duration = data.get("duration", 0)
        if duration < 60:
            score += 2.0  # 非常快
        elif duration < 180:
            score += 1.0  # 快
        elif duration > 300:
            score -= 1.0  # 慢

        # 并行执行加分
        if data.get("parallel_execution", False):
            score += 1.0

        # 文件修改数评分
        files_modified = len(data.get("files_modified", []))
        if files_modified > 0:
            score += 0.5

        return min(10.0, max(0.0, score))

    def _evaluate_code_quality(self, data: Dict[str, Any]) -> float:
        """
        评估代码质量（0-10分）

        考虑因素：
        - 是否成功
        - 错误数量
        - 代码文件数量
        """
        score = 7.0  # 基础分

        # 成功率评分
        if data.get("success", True):
            score += 2.0
        else:
            score -= 2.0

        # 错误数量评分
        errors = len(data.get("errors", []))
        if errors == 0:
            score += 1.0
        elif errors > 3:
            score -= 1.0

        # 代码文件数量评分
        files_modified = len(data.get("files_modified", []))
        if files_modified > 0:
            score += 0.5

        return min(10.0, max(0.0, score))

    def _evaluate_test_coverage(self, data: Dict[str, Any]) -> float:
        """
        评估测试覆盖率（0-10分）

        考虑因素：
        - 测试文件数量
        - 测试与代码文件比例
        """
        score = 5.0  # 基础分

        test_files = len(data.get("test_files", []))
        code_files = len(data.get("files_modified", []))

        # 测试文件数量评分
        if test_files > 0:
            score += 2.0
        if test_files > 2:
            score += 1.0

        # 测试覆盖率评分
        if code_files > 0:
            coverage_ratio = test_files / code_files
            if coverage_ratio >= 0.5:
                score += 2.0
            elif coverage_ratio >= 0.3:
                score += 1.0

        return min(10.0, max(0.0, score))

    def _evaluate_documentation(self, data: Dict[str, Any]) -> float:
        """
        评估文档完整性（0-10分）

        考虑因素：
        - 文档文件数量
        - 文档与代码文件比例
        """
        score = 6.0  # 基础分

        doc_files = len(data.get("doc_files", []))
        code_files = len(data.get("files_modified", []))

        # 文档文件数量评分
        if doc_files > 0:
            score += 2.0
        if doc_files > 1:
            score += 1.0

        # 文档覆盖率评分
        if code_files > 0:
            doc_ratio = doc_files / code_files
            if doc_ratio >= 0.3:
                score += 1.0

        return min(10.0, max(0.0, score))


def main():
    """测试质量评估器"""
    evaluator = QualityEvaluator()

    # 测试数据
    test_data = {
        "duration": 45,
        "files_modified": ["main/backend/api/routes/user_router.py", "main/backend/services/user_service.py"],
        "test_files": ["main/tests/backend/test_user.py"],
        "doc_files": ["main/docs/api/user-api.md"],
        "success": True,
        "errors": [],
        "parallel_execution": True
    }

    # 评估
    score = evaluator.evaluate(test_data)

    # 输出结果
    print(f"Overall Score: {score.overall}/10")
    print(f"Efficiency: {score.efficiency}/10")
    print(f"Code Quality: {score.code_quality}/10")
    print(f"Test Coverage: {score.test_coverage}/10")
    print(f"Documentation: {score.documentation}/10")
    print(f"\nDetails: {score.details}")


if __name__ == "__main__":
    main()
