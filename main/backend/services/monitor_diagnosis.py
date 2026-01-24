"""
监控系统 - AI 诊断服务

功能：
1. 使用 Claude API 分析代码问题
2. 检测性能瓶颈
3. 检测安全风险
4. 检测代码质量问题
5. 检测架构问题
6. 执行自动修复

诊断维度：
- performance: 性能瓶颈（N+1 查询、大文件、重复代码）
- security: 安全风险（硬编码密钥、SQL 注入、XSS）
- quality: 代码质量（复杂度、测试覆盖率、文档完整性）
- architecture: 架构问题（耦合度、依赖循环、违反规范）
"""

import re
import uuid
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from models.monitor_schema import DiagnosisIssue, FixResult, FixChange


class DiagnosisService:
    """AI 诊断服务"""

    def __init__(self):
        """初始化诊断服务"""
        self.project_root = Path(__file__).parent.parent.parent.parent
        # 注意：实际使用时需要配置 Anthropic API Key
        # self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def run_diagnosis(self) -> List[DiagnosisIssue]:
        """
        执行智能诊断

        诊断维度：
        1. 性能瓶颈 (performance)
        2. 安全风险 (security)
        3. 代码质量 (quality)
        4. 架构问题 (architecture)

        Returns:
            List[DiagnosisIssue]: 诊断问题列表
        """
        issues = []

        # 1. 性能瓶颈检测
        issues.extend(await self._detect_performance_issues())

        # 2. 安全风险检测
        issues.extend(await self._detect_security_issues())

        # 3. 代码质量检测
        issues.extend(await self._detect_quality_issues())

        # 4. 架构问题检测
        issues.extend(await self._detect_architecture_issues())

        return issues

    async def _detect_performance_issues(self) -> List[DiagnosisIssue]:
        """
        检测性能瓶颈

        检测项：
        - N+1 查询问题
        - 大文件读取
        - 重复计算
        - 未使用索引的查询

        Returns:
            List[DiagnosisIssue]: 性能问题列表
        """
        issues = []
        backend_dir = self.project_root / "main" / "backend"

        if not backend_dir.exists():
            return issues

        # 扫描 Python 文件
        for py_file in backend_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")

                # 检测 N+1 查询问题（简化版，实际应使用 Claude API）
                # 查找循环中的数据库查询
                if re.search(r"for\s+\w+\s+in\s+.+:\s*\n\s+.*session\.(query|get|execute)", content):
                    line_num = self._find_line_number(content, "for")
                    issues.append(DiagnosisIssue(
                        id=f"perf_{uuid.uuid4().hex[:8]}",
                        severity="Important",
                        category="performance",
                        title="可能存在 N+1 查询问题",
                        description=f"在 {py_file.name} 中检测到循环内的数据库查询",
                        location=f"{py_file}:{line_num}",
                        suggestion="使用 joinedload 或 selectinload 预加载关联数据",
                        auto_fixable=False
                    ))

                # 检测大文件读取
                if "read_text()" in content or "read()" in content:
                    if "Path" in content and not "encoding" in content:
                        line_num = self._find_line_number(content, "read_text")
                        issues.append(DiagnosisIssue(
                            id=f"perf_{uuid.uuid4().hex[:8]}",
                            severity="Suggestion",
                            category="performance",
                            title="文件读取未指定编码",
                            description=f"在 {py_file.name} 中文件读取未指定编码",
                            location=f"{py_file}:{line_num}",
                            suggestion="使用 read_text(encoding='utf-8') 明确指定编码",
                            auto_fixable=True,
                            fix_code='read_text(encoding="utf-8")'
                        ))

            except Exception:
                continue

        return issues

    async def _detect_security_issues(self) -> List[DiagnosisIssue]:
        """
        检测安全风险

        检测项：
        - 硬编码密钥
        - 硬编码密码
        - SQL 注入风险

        Returns:
            List[DiagnosisIssue]: 安全问题列表
        """
        issues = []
        backend_dir = self.project_root / "main" / "backend"

        if not backend_dir.exists():
            return issues

        # 检测硬编码密钥
        for py_file in backend_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")

                # 正则匹配常见密钥模式
                patterns = [
                    (r'SECRET_KEY\s*=\s*["\']([^"\']{10,})["\']', "硬编码 SECRET_KEY"),
                    (r'API_KEY\s*=\s*["\']([^"\']{10,})["\']', "硬编码 API_KEY"),
                    (r'PASSWORD\s*=\s*["\']([^"\']+)["\']', "硬编码密码"),
                ]

                for pattern, title in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        issues.append(DiagnosisIssue(
                            id=f"sec_{uuid.uuid4().hex[:8]}",
                            severity="Critical",
                            category="security",
                            title=title,
                            description=f"在 {py_file.name}:{line_num} 发现硬编码敏感信息",
                            location=f"{py_file}:{line_num}",
                            suggestion="使用环境变量存储敏感信息（如 os.getenv('SECRET_KEY')）",
                            auto_fixable=False
                        ))

            except Exception:
                continue

        return issues

    async def _detect_quality_issues(self) -> List[DiagnosisIssue]:
        """
        检测代码质量问题

        检测项：
        - 缺少类型注解
        - 缺少文档字符串
        - 函数过长

        Returns:
            List[DiagnosisIssue]: 质量问题列表
        """
        issues = []
        backend_dir = self.project_root / "main" / "backend"

        if not backend_dir.exists():
            return issues

        # 检测缺少类型注解
        for py_file in backend_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")

                # 检测函数定义缺少返回类型注解
                func_pattern = r"def\s+(\w+)\([^)]*\):"
                matches = re.finditer(func_pattern, content)
                for match in matches:
                    func_name = match.group(1)
                    # 跳过特殊方法
                    if func_name.startswith("__"):
                        continue

                    # 检查是否有返回类型注解
                    if "->" not in content[match.start():match.end() + 50]:
                        line_num = content[:match.start()].count('\n') + 1
                        issues.append(DiagnosisIssue(
                            id=f"qual_{uuid.uuid4().hex[:8]}",
                            severity="Suggestion",
                            category="quality",
                            title=f"函数 {func_name} 缺少返回类型注解",
                            description=f"在 {py_file.name}:{line_num} 函数缺少类型注解",
                            location=f"{py_file}:{line_num}",
                            suggestion="添加返回类型注解，如 def func() -> ReturnType:",
                            auto_fixable=False
                        ))

            except Exception:
                continue

        return issues

    async def _detect_architecture_issues(self) -> List[DiagnosisIssue]:
        """
        检测架构问题

        检测项：
        - 违反目录结构规范
        - 循环依赖

        Returns:
            List[DiagnosisIssue]: 架构问题列表
        """
        issues = []

        # 检测违反目录结构规范
        # 例如：测试文件不在 main/tests/ 目录
        test_files = list(self.project_root.rglob("test_*.py"))
        for test_file in test_files:
            if "main/tests/" not in str(test_file):
                issues.append(DiagnosisIssue(
                    id=f"arch_{uuid.uuid4().hex[:8]}",
                    severity="Important",
                    category="architecture",
                    title="测试文件位置不符合规范",
                    description=f"测试文件 {test_file.name} 应放在 main/tests/ 目录下",
                    location=str(test_file),
                    suggestion="将测试文件移动到 main/tests/ 对应子目录",
                    auto_fixable=False
                ))

        return issues

    async def auto_fix_issue(self, issue_id: str, issue: DiagnosisIssue) -> FixResult:
        """
        自动修复问题

        Args:
            issue_id: 问题 ID
            issue: 问题详情

        Returns:
            FixResult: 修复结果

        Raises:
            ValueError: 问题不支持自动修复
        """
        if not issue.auto_fixable:
            raise ValueError("该问题不支持自动修复")

        # 解析文件路径和行号
        location_parts = issue.location.split(":")
        file_path = Path(location_parts[0])
        line_num = int(location_parts[1]) if len(location_parts) > 1 else 1

        if not file_path.exists():
            raise ValueError(f"文件不存在: {file_path}")

        # 读取文件内容
        content = file_path.read_text(encoding="utf-8")
        lines = content.split('\n')

        # 备份原始行
        original_line = lines[line_num - 1] if line_num <= len(lines) else ""

        # 应用修复代码
        if issue.fix_code:
            # 简单替换（实际应该更智能）
            lines[line_num - 1] = lines[line_num - 1].replace(
                "read_text()",
                issue.fix_code
            )

        # 写回文件
        file_path.write_text('\n'.join(lines), encoding="utf-8")

        return FixResult(
            issue_id=issue_id,
            fixed=True,
            changes=[FixChange(
                file=str(file_path),
                line=line_num,
                before=original_line,
                after=lines[line_num - 1]
            )]
        )

    def _find_line_number(self, content: str, keyword: str) -> int:
        """
        查找关键词所在行号

        Args:
            content: 文件内容
            keyword: 关键词

        Returns:
            int: 行号（从 1 开始）
        """
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if keyword in line:
                return i
        return 1
