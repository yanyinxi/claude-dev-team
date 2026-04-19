#!/usr/bin/env python3
"""
路径验证器 (Path Validator)

职责：
1. 在文件操作前（PreToolUse Hook）验证路径合法性
2. 强制执行项目目录结构约束
3. 防止在错误位置创建文件

强制约束：
- ❌ 禁止在根目录创建 tests/, scripts/, src/, backend/, frontend/
- ❌ 禁止在非 main/tests/ 目录创建测试文件
- ✅ 所有测试必须放在 main/tests/ 目录下
- ✅ 所有代码必须放在 main/ 子目录下
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, Any, Optional


# 禁止的根目录路径模式
FORBIDDEN_ROOT_PATHS = [
    r"^tests/",           # 根目录 tests/
    r"^scripts/",         # 根目录 scripts/
    r"^src/",             # 根目录 src/
    r"^backend/",         # 根目录 backend/
    r"^frontend/",        # 根目录 frontend/
]

# 禁止的嵌套路径模式（防止错误的目录结构）
FORBIDDEN_NESTED_PATHS = [
    r"^main/backend/main/",   # 禁止 main/backend/main/
    r"^main/frontend/main/",  # 禁止 main/frontend/main/
    r"^main/backend/docs/",   # 禁止 main/backend/docs/（应该用 main/docs/）
    r"^main/frontend/docs/",  # 禁止 main/frontend/docs/（应该用 main/docs/）
]

# 允许的路径模式
ALLOWED_PATHS = [
    r"^main/backend/",
    r"^main/frontend/",
    r"^main/tests/",      # 唯一允许的测试目录
    r"^main/docs/",
    r"^main/examples/",
    r"^\.claude/",        # .claude/ and all subdirectories
    r"^\.github/",
    r"^README\.md$",
    r"^CLAUDE\.md$",
    r"^\.gitignore$",
    r"^package\.json$",
    r"^pyproject\.toml$",
]

# 测试文件模式
TEST_FILE_PATTERNS = [
    r"test_.*\.py$",      # test_xxx.py
    r".*_test\.py$",      # xxx_test.py
    r"test.*\.ts$",       # test.ts, testUtils.ts
    r".*\.test\.ts$",     # xxx.test.ts
    r".*\.spec\.ts$",     # xxx.spec.ts
    r".*\.test\.js$",     # xxx.test.js
    r".*\.spec\.js$",     # xxx.spec.js
]


def is_test_file(file_path: str) -> bool:
    """
    判断是否为测试文件。

    Args:
        file_path: 文件路径

    Returns:
        是否为测试文件
    """
    return any(re.search(pattern, file_path) for pattern in TEST_FILE_PATTERNS)


def _violation(reason: str) -> Dict[str, Any]:
    return {"reason": reason}


def validate_path(file_path: str) -> Optional[Dict[str, Any]]:
    """
    验证文件路径是否合法。返回 None 表示合法，返回 dict 表示违规原因。
    """
    # 防止路径穿越攻击（../）
    if ".." in Path(file_path).parts:
        return _violation(f"❌ 检测到路径穿越：{file_path}\n\n请使用相对于项目根目录的规范路径。")

    # 防止符号链接绕过
    project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    abs_path = project_root / file_path
    if abs_path.exists() and abs_path.is_symlink():
        resolved = abs_path.resolve()
        try:
            resolved.relative_to(project_root)
        except ValueError:
            return _violation(f"❌ 符号链接指向项目外部：{file_path} → {resolved}\n\n禁止操作项目目录外的文件。")

    # 检查禁止的根目录路径
    for pattern in FORBIDDEN_ROOT_PATHS:
        if re.match(pattern, file_path):
            return _violation(
                f"❌ 禁止在根目录创建 {file_path}！\n\n"
                f"📋 正确做法：\n"
                f"  - 后端代码 → main/backend/\n"
                f"  - 前端代码 → main/frontend/\n"
                f"  - 测试文件 → main/tests/\n"
                f"  - 文档文件 → main/docs/\n"
                f"  - 脚本文件 → main/backend/scripts/\n\n"
                f"请参考 CLAUDE.md 中的目录结构约束。"
            )

    # 检查禁止的嵌套路径
    for pattern in FORBIDDEN_NESTED_PATHS:
        if re.match(pattern, file_path):
            return _violation(
                f"❌ 禁止创建 {file_path}！\n\n"
                f"🚫 错误的目录结构：\n"
                f"  - main/backend/main/     ❌\n"
                f"  - main/backend/docs/     ❌\n"
                f"  - main/frontend/main/    ❌\n"
                f"  - main/frontend/docs/    ❌\n\n"
                f"✅ 文档统一放 main/docs/，请参考 CLAUDE.md。"
            )

    # 检查测试文件位置
    if is_test_file(file_path) and not file_path.startswith("main/tests/"):
        return _violation(
            f"❌ 测试文件必须放在 main/tests/ 目录下！\n\n"
            f"当前路径：{file_path}\n"
            f"正确路径：main/tests/{Path(file_path).name}\n\n"
            f"  main/tests/backend/     # 后端测试\n"
            f"  main/tests/frontend/    # 前端测试\n"
            f"  main/tests/integration/ # 集成测试"
        )

    # 检查是否在允许的路径
    allowed = any(re.match(pattern, file_path) for pattern in ALLOWED_PATHS)
    if not allowed:
        return _violation(
            f"⚠️ 警告：{file_path} 不在标准目录结构中。\n\n"
            f"📋 标准目录结构：\n"
            f"  main/backend/    # 后端代码\n"
            f"  main/frontend/   # 前端代码\n"
            f"  main/tests/      # 测试文件\n"
            f"  main/docs/       # 文档\n"
            f"  main/examples/   # 示例代码\n"
            f"  .claude/         # Claude 配置\n\n"
            f"如果确实需要在此位置创建文件，请先咨询用户。"
        )

    return None


def main():
    """
    主函数：处理 PreToolUse Hook 输入。

    Claude Code Hook 传递 JSON 格式数据到 stdin。
    """
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        sys.exit(0)

    # 提取工具信息
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只验证文件写入操作
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    # 获取文件路径
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # 转换为相对路径（如果是绝对路径）
    project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    file_path_obj = Path(file_path)
    if file_path_obj.is_absolute():
        try:
            file_path = str(file_path_obj.relative_to(project_root))
        except ValueError:
            # 如果路径不在项目根目录下，保持原样
            pass

    # 验证路径
    error = validate_path(file_path)

    if error:
        # 路径非法，阻止操作（官方 PreToolUse schema）
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": error["reason"]
            }
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(2)

    # 路径合法，允许操作
    sys.exit(0)


if __name__ == "__main__":
    main()
