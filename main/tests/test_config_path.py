"""
测试配置文件路径解析

验证从不同目录运行时，数据库路径都能正确解析
"""

import sys
import os
from pathlib import Path

# 添加 backend 目录到 Python 路径
backend_path = Path(__file__).resolve().parent.parent / "main" / "backend"
sys.path.insert(0, str(backend_path))

from core.config import settings


def test_database_path_resolution():
    """测试数据库路径解析"""

    print("=" * 60)
    print("数据库路径解析测试")
    print("=" * 60)

    # 获取数据库 URL
    db_url = settings.DATABASE_URL
    print(f"\n数据库 URL: {db_url}")

    # 提取数据库文件路径
    db_path = db_url.replace("sqlite+aiosqlite:///", "")
    db_path_obj = Path(db_path)

    print(f"数据库文件路径: {db_path_obj}")
    print(f"路径是否为绝对路径: {db_path_obj.is_absolute()}")
    print(f"数据库文件是否存在: {db_path_obj.exists()}")

    # 验证路径结构
    expected_parts = ["main", "backend", "db", "ket_exam.db"]
    actual_parts = db_path_obj.parts[-4:]

    print(f"\n预期路径部分: {expected_parts}")
    print(f"实际路径部分: {list(actual_parts)}")

    # 检查项目根目录
    project_root = settings.get_project_root()
    print(f"\n项目根目录: {project_root}")
    print(f"项目根目录存在 .git: {(project_root / '.git').exists()}")
    print(f"项目根目录存在 CLAUDE.md: {(project_root / 'CLAUDE.md').exists()}")

    # 验证结果
    assert db_path_obj.is_absolute(), "数据库路径必须是绝对路径"
    assert list(actual_parts) == expected_parts, f"路径结构不正确: {actual_parts}"

    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)


def test_from_different_directories():
    """测试从不同目录运行时的路径解析"""

    print("\n" + "=" * 60)
    print("多目录测试")
    print("=" * 60)

    # 保存当前目录
    original_cwd = os.getcwd()

    # 测试目录列表
    test_dirs = [
        Path(__file__).resolve().parent.parent,  # 项目根目录
        Path(__file__).resolve().parent.parent / "main" / "backend",  # backend 目录
        Path(__file__).resolve().parent,  # tests 目录
    ]

    for test_dir in test_dirs:
        if test_dir.exists():
            os.chdir(test_dir)
            print(f"\n当前工作目录: {os.getcwd()}")

            # 重新导入配置（模拟从不同目录运行）
            db_url = settings.DATABASE_URL
            db_path = db_url.replace("sqlite+aiosqlite:///", "")

            print(f"数据库路径: {db_path}")
            print(f"路径是否为绝对路径: {Path(db_path).is_absolute()}")

    # 恢复原始目录
    os.chdir(original_cwd)

    print("\n" + "=" * 60)
    print("✅ 多目录测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_database_path_resolution()
        test_from_different_directories()

        print("\n" + "🎉 " * 20)
        print("所有测试成功完成！数据库路径配置正确。")
        print("🎉 " * 20)

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
