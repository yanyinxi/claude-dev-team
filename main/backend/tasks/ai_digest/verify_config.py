#!/usr/bin/env python3
"""
配置验证脚本

用于验证 AI 日报任务配置是否正确
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from main.backend.tasks.ai_digest.config import config


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("AI 日报任务配置验证")
    print("=" * 80 + "\n")

    # 验证配置
    print("1. 验证配置...")
    if config.validate():
        print("   ✅ 配置验证通过\n")
    else:
        print("   ❌ 配置验证失败\n")
        return 1

    # 打印配置
    print("2. 当前配置:")
    config.print_config()

    # 检查目录
    print("\n3. 检查目录...")
    docs_dir = config.get_docs_dir()
    log_dir = config.get_log_dir()

    if docs_dir.exists():
        print(f"   ✅ 文档目录存在: {docs_dir}")
    else:
        print(f"   ⚠️  文档目录不存在: {docs_dir}")
        docs_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ 已创建文档目录")

    if log_dir.exists():
        print(f"   ✅ 日志目录存在: {log_dir}")
    else:
        print(f"   ⚠️  日志目录不存在: {log_dir}")
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ 已创建日志目录")

    # 检查 Claude CLI
    print("\n4. 检查 Claude CLI...")
    import subprocess
    try:
        result = subprocess.run(
            [config.CLAUDE_CLI_COMMAND, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            print(f"   ✅ Claude CLI 可用: {result.stdout.strip()}")
        else:
            print(f"   ❌ Claude CLI 不可用: {result.stderr}")
            return 1
    except FileNotFoundError:
        print(f"   ❌ Claude CLI 未找到: {config.CLAUDE_CLI_COMMAND}")
        print(f"   提示: 请确保 Claude CLI 已安装并在 PATH 中")
        return 1
    except Exception as e:
        print(f"   ❌ 检查失败: {e}")
        return 1

    print("\n" + "=" * 80)
    print("✅ 所有检查通过，配置正确！")
    print("=" * 80 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
