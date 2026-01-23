#!/usr/bin/env python3
"""
学习历史保存器 (Learning History Saver)

职责：
1. 在对话压缩前（PreCompact Hook）触发
2. 保存 AlphaZero 学习历史到持久化文件
3. 防止学习成果因对话压缩而丢失
4. 支持跨会话学习和历史追溯

使用 Claude Code 原生 PreCompact Hook 机制实现。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def load_experience_pool() -> List[Dict[str, Any]]:
    """
    加载经验池数据。

    Returns:
        经验列表
    """
    experience_file = Path(".claude/experience_pool.json")

    if not experience_file.exists():
        return []

    try:
        with open(experience_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def load_strategy_rules() -> Dict[str, Any]:
    """
    加载所有策略规则文件。

    Returns:
        策略规则字典
    """
    rules_dir = Path(".claude/rules")

    if not rules_dir.exists():
        return {}

    rules = {}
    for rule_file in rules_dir.glob("*.md"):
        try:
            content = rule_file.read_text(encoding='utf-8')
            rules[rule_file.stem] = {
                "file": str(rule_file),
                "content": content,
                "size": len(content)
            }
        except IOError:
            continue

    return rules


def save_learning_snapshot(session_id: str = None) -> Dict[str, Any]:
    """
    保存学习快照。

    Args:
        session_id: 会话 ID（可选）

    Returns:
        快照元数据
    """
    timestamp = datetime.now().isoformat()

    # 加载当前学习数据
    experiences = load_experience_pool()
    rules = load_strategy_rules()

    # 构建快照
    snapshot = {
        "timestamp": timestamp,
        "session_id": session_id or "unknown",
        "version": "1.0",
        "statistics": {
            "total_experiences": len(experiences),
            "total_rules": len(rules),
            "strategies": list(rules.keys())
        },
        "experiences": experiences,
        "rules": rules
    }

    # 保存到历史文件
    history_dir = Path(".claude/learning_history")
    history_dir.mkdir(exist_ok=True)

    # 使用时间戳作为文件名
    snapshot_file = history_dir / f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        # 同时更新最新快照链接
        latest_file = history_dir / "latest.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "snapshot_file": str(snapshot_file),
            "latest_file": str(latest_file),
            "statistics": snapshot["statistics"]
        }

    except IOError as e:
        return {
            "success": False,
            "error": str(e)
        }


def cleanup_old_snapshots(keep_count: int = 10):
    """
    清理旧的快照文件，只保留最近的 N 个。

    Args:
        keep_count: 保留的快照数量
    """
    history_dir = Path(".claude/learning_history")

    if not history_dir.exists():
        return

    # 获取所有快照文件（排除 latest.json）
    snapshots = sorted(
        [f for f in history_dir.glob("snapshot_*.json")],
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    # 删除多余的快照
    for old_snapshot in snapshots[keep_count:]:
        try:
            old_snapshot.unlink()
        except IOError:
            pass


def main():
    """
    主函数：处理 PreCompact Hook 输入。

    Claude Code Hook 传递 JSON 格式数据到 stdin。
    """
    try:
        # 读取 Hook 输入
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        input_data = {}

    # 提取会话 ID
    session_id = input_data.get("session_id", "unknown")

    # 保存学习快照
    result = save_learning_snapshot(session_id)

    # 清理旧快照
    cleanup_old_snapshots(keep_count=10)

    # 输出结果
    if result["success"]:
        output = {
            "action": "saved",
            "message": f"✅ 学习历史已保存到 {result['snapshot_file']}",
            "statistics": result["statistics"],
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(output, ensure_ascii=False))
        sys.exit(0)
    else:
        output = {
            "action": "error",
            "message": f"❌ 保存失败: {result['error']}",
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(output, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
