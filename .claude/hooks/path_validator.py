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

# 允许的路径模式
ALLOWED_PATHS = [
    r"^main/backend/",
    r"^main/frontend/",
    r"^main/tests/",      # 唯一允许的测试目录
    r"^main/docs/",
    r"^examples/",
    r"^\.claude/",
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


def validate_path(file_path: str, tool_name: str) -> Optional[Dict[str, Any]]:
    """
    验证文件路径是否合法。

    Args:
        file_path: 文件路径
        tool_name: 工具名称（Write, Edit）

    Returns:
        如果路径非法，返回错误信息；否则返回 None
    """
    # 检查是否在禁止的根目录路径
    for pattern in FORBIDDEN_ROOT_PATHS:
        if re.match(pattern, file_path):
            return {
                "decision": "block",
                "reason": f"❌ 禁止在根目录创建 {file_path}！\n\n"
                         f"📋 正确做法：\n"
                         f"  - 后端代码 → main/backend/\n"
                         f"  - 前端代码 → main/frontend/\n"
                         f"  - 测试文件 → main/tests/\n"
                         f"  - 文档文件 → main/docs/\n"
                         f"  - 脚本文件 → main/backend/scripts/\n\n"
                         f"请参考 CLAUDE.md 中的目录结构约束。"
            }

    # 检查测试文件是否在正确位置
    if is_test_file(file_path):
        if not file_path.startswith("main/tests/"):
            return {
                "decision": "block",
                "reason": f"❌ 测试文件必须放在 main/tests/ 目录下！\n\n"
                         f"当前路径：{file_path}\n"
                         f"正确路径：main/tests/{Path(file_path).name}\n\n"
                         f"📋 测试目录结构：\n"
                         f"  main/tests/\n"
                         f"  ├── backend/     # 后端测试\n"
                         f"  ├── frontend/    # 前端测试\n"
                         f"  └── integration/ # 集成测试\n\n"
                         f"这是强制约束，所有测试必须遵守！"
            }

    # 检查是否在允许的路径
    allowed = any(re.match(pattern, file_path) for pattern in ALLOWED_PATHS)
    if not allowed:
        return {
            "decision": "block",
            "reason": f"⚠️ 警告：{file_path} 不在标准目录结构中。\n\n"
                     f"📋 标准目录结构：\n"
                     f"  main/backend/    # 后端代码\n"
                     f"  main/frontend/   # 前端代码\n"
                     f"  main/tests/      # 测试文件\n"
                     f"  main/docs/       # 文档\n"
                     f"  examples/        # 示例代码\n"
                     f"  .claude/         # Claude 配置\n\n"
                     f"如果确实需要在此位置创建文件，请先咨询用户。"
        }

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

    # 验证路径
    error = validate_path(file_path, tool_name)

    if error:
        # 路径非法，阻止操作
        output = {
            "hookEventName": "PreToolUse",
            "decision": error["decision"],
            "reason": error["reason"]
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(2)  # 退出码 2 表示阻止操作

    # 路径合法，允许操作
    sys.exit(0)


if __name__ == "__main__":
    main()
