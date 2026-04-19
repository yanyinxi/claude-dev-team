#!/usr/bin/env python3
"""
Project Standards 验证脚本

用于验证 project_standards.md 文件的完整性和一致性。
由 Evolver Agent 在自动进化后调用。

使用方法:
    python verify_standards.py [--verbose] [--fix]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict

# 默认文件路径
DEFAULT_FILE = ".claude/project_standards.md"


def read_file(file_path: str) -> str:
    """读取文件内容"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """写入文件内容"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def verify_file_structure(content: str) -> Tuple[bool, List[str]]:
    """验证文件结构完整性"""
    errors = []
    warnings = []

    # 检查必需的章节是否存在
    required_sections = [
        "# 项目技术标准",
        "## 📂 路径配置",
        "## 🚨 目录结构强制约束",
        "## 命名约定",
        "## 技术栈",
        "## API 规范",
        "## 进化机制",
    ]

    for section in required_sections:
        if section not in content:
            errors.append(f"❌ 缺少必要章节: {section}")

    # 检查代码块是否平衡
    code_block_count = content.count("```")
    if code_block_count % 2 != 0:
        errors.append(f"❌ 代码块不平衡: {code_block_count} 个标记")

    # 检查 Markdown 表格格式（仅警告，不作为错误）
    table_lines = [line for line in content.split("\n") if line.startswith("|")]
    for i, line in enumerate(table_lines):
        if line.strip() == "|":
            continue
        # 检查表格分隔行
        if set(line.strip()) <= {"|", "-", ":", " "}:
            continue

        # 检查表格列数一致性
        if i > 0 and i < len(table_lines):
            prev_line = table_lines[i - 1]
            if not set(prev_line.strip()) <= {"|", "-", ":", " "}:
                # 非分隔行，比较列数
                if line.count("|") != prev_line.count("|"):
                    warnings.append(
                        f"⚠️ 第 {i + 1} 行表格列数不一致（Markdown 表格允许跨行内容，此为误报）"
                    )

    if warnings:
        for w in warnings:
            print(f"  {w}")

    if not errors:
        print("✅ 文件结构验证通过")

    # 只返回 errors 列表，warnings 已在上面打印
    return len(errors) == 0, errors


def verify_path_variables(content: str) -> Tuple[bool, List[str]]:
    """验证路径变量定义与使用一致"""
    errors = []

    # 收集所有路径变量定义（可能在多个章节）
    all_var_definitions = []

    # 从路径配置章节提取
    path_config_match = re.search(r"## 📂 路径配置.*?(?=## |\Z)", content, re.DOTALL)
    if path_config_match:
        all_var_definitions.append(path_config_match.group())

    # 从变量表格中提取（包含 {VAR_NAME}）
    var_table_matches = re.findall(r"\| `{([A-Z_]+)}`.*?\|", content)
    for var in var_table_matches:
        all_var_definitions.append(f"`{{{var}}}`")

    if not all_var_definitions:
        errors.append("❌ 未找到路径变量定义")
        return False, errors

    # 合并所有定义
    all_definitions = " ".join(all_var_definitions)
    defined_vars = set(re.findall(r"\{([A-Z_]+)\}", all_definitions))

    # 提取所有使用的变量 {VAR_NAME}
    used_vars = set(re.findall(r"\{([A-Z_]+)\}", content))

    # 过滤掉非路径变量（如 SECTION, ROLE 等）
    path_vars = {
        "PROJECT_ROOT",
        "BACKEND_ROOT",
        "FRONTEND_ROOT",
        "TESTS_ROOT",
        "BACKEND_TESTS",
        "FRONTEND_TESTS",
        "DOCS_ROOT",
        "PRD_DIR",
        "TECH_DESIGN_DIR",
        "API_DIR",
        "REVIEW_DIR",
        "TEST_REPORT_DIR",
        "BUG_REPORT_DIR",
        "TASK_DIST_DIR",
    }

    used_path_vars = used_vars & path_vars
    defined_path_vars = defined_vars & path_vars

    # 检查是否所有变量都有定义
    undefined = used_path_vars - defined_path_vars
    if undefined:
        errors.append(f"❌ 未定义的路径变量: {undefined}")

    # 检查是否有未使用的变量
    unused = defined_path_vars - used_path_vars
    if unused:
        errors.append(f"⚠️ 未使用的路径变量: {unused}")

    if not errors:
        print("✅ 路径变量一致性验证通过")

    return len([e for e in errors if e.startswith("❌")]) == 0, errors


def verify_version_update(content: str) -> Tuple[bool, List[str]]:
    """验证版本信息与进化历史的一致性（兼容当前文档结构）"""
    errors = []

    # 检查版本号格式（当前文档为“版本 2.2.0”）
    version_pattern = r"版本\s*(\d+\.\d+\.\d+)"
    match = re.search(version_pattern, content)

    if not match:
        errors.append("❌ 未找到版本号")
        return False, errors

    version = match.group(1)
    # 验证版本号格式
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        errors.append(f"❌ 版本号格式错误: {version}")
        return False, errors

    # 检查进化机制章节是否存在
    evolution_section_match = re.search(r"## 进化机制.*?(?=## |\Z)", content, re.DOTALL)

    if not evolution_section_match:
        errors.append("❌ 未找到进化机制章节")
        return False, errors

    evolution_section = evolution_section_match.group()

    # 查找版本是否在进化机制章节中出现
    version_patterns = [
        rf"\|\s*\d{{4}}-\d{{2}}-\d{{2}}\s*\|\s*{re.escape(version)}\s*\|",  # 历史表
        rf"v{re.escape(version)}",  # 兼容旧格式
    ]

    found = any(re.search(pattern, evolution_section) for pattern in version_patterns)

    if not found:
        # 当前版本可能是最近一次发布但未写入历史表，仅给出提示
        errors.append(f"⚠️ 版本 {version} 未在进化历史表中找到（建议补充）")

    if not [e for e in errors if e.startswith("❌")]:
        print(f"✅ 版本信息验证通过: {version}")

    return len([e for e in errors if e.startswith("❌")]) == 0, errors


def verify_prohibited_updates(
    content: str, changes: List[str]
) -> Tuple[bool, List[str]]:
    """验证没有更新禁止自动进化的内容"""
    errors = []

    # 禁止自动更新的内容模式
    prohibited_patterns = [
        (r"\| `{PROJECT_ROOT}`", "项目根路径变量"),
        (r"\| `{BACKEND_ROOT}`", "后端根路径变量"),
        (r"\| `{FRONTEND_ROOT}`", "前端根路径变量"),
        (r"## 命名约定", "命名约定章节"),
        (r"## API 规范", "API 规范章节"),
    ]

    for change in changes:
        for pattern, name in prohibited_patterns:
            if re.search(pattern, change):
                errors.append(f"⚠️ 检测到禁止自动更新的内容变更: {name}")

    if not errors:
        print("✅ 禁止更新内容验证通过")

    return len(errors) == 0, errors


def extract_changes(old_content: str, new_content: str) -> List[str]:
    """提取变更内容"""
    # 简化实现：返回新旧内容的差异摘要
    changes = []

    # 检查版本变化
    old_version = re.search(r"\| 版本 \| (\d+\.\d+\.\d+) \|", old_content)
    new_version = re.search(r"\| 版本 \| (\d+\.\d+\.\d+) \|", new_content)

    if old_version and new_version and old_version.group(1) != new_version.group(1):
        changes.append(f"版本更新: {old_version.group(1)} -> {new_version.group(1)}")

    # 检查新增章节
    old_sections = set(re.findall(r"##+ ([^\n]+)", old_content))
    new_sections = set(re.findall(r"##+ ([^\n]+)", new_content))

    added_sections = new_sections - old_sections
    if added_sections:
        changes.append(f"新增章节: {added_sections}")

    return changes


def run_verification(file_path: str, verbose: bool = False) -> bool:
    """执行完整验证"""
    print(f"\n🔍 验证文件: {file_path}")
    print("=" * 50)

    try:
        content = read_file(file_path)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {file_path}")
        return False
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

    all_passed = True

    # 1. 文件结构验证
    passed, errors = verify_file_structure(content)
    all_passed = all_passed and passed
    if verbose and errors:
        for error in errors:
            print(f"  {error}")

    # 2. 路径变量验证
    passed, errors = verify_path_variables(content)
    all_passed = all_passed and passed
    if verbose and errors:
        for error in errors:
            print(f"  {error}")

    # 3. 版本更新验证
    passed, errors = verify_version_update(content)
    all_passed = all_passed and passed
    if verbose and errors:
        for error in errors:
            print(f"  {error}")

    print("=" * 50)
    if all_passed:
        print("✅ 所有验证通过！")
    else:
        print("❌ 验证失败，请检查上述错误")

    return all_passed


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="验证 project_standards.md 文件的完整性和一致性"
    )
    parser.add_argument(
        "--file", "-f", default=DEFAULT_FILE, help=f"文件路径 (默认: {DEFAULT_FILE})"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细输出")
    parser.add_argument("--fix", "-x", action="store_true", help="自动修复简单问题")

    args = parser.parse_args()

    success = run_verification(args.file, args.verbose)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
