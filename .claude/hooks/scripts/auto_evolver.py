#!/usr/bin/env python3
"""
Auto Evolver - SubagentStop Hook

职责单一：记录 agent 被调用的事实。
所有真实的执行评估在 Stop hook 里基于 git 数据完成，这里只做最简单的事实记录。

为什么这样设计：
- SubagentStop hook 的 stdin 只有 tool_input.subagent_type 可靠
- 没有 duration/files_modified/success 等可信字段
- 过去的实现虚构这些字段、给出 8.5 的假分，误导用户以为系统在学习
- 现在改为只记录"谁在什么时候被调用"，真实数据由 session_evolver 采集
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def main():
    try:
        raw = sys.stdin.read().strip()
        input_data = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, OSError):
        input_data = {}

    tool_input = input_data.get("tool_input", {})
    agent_name = tool_input.get("subagent_type", "unknown")
    session_id = input_data.get("session_id", "unknown")

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    logs_dir = Path(project_root) / ".claude" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "type": "agent_invoked",
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "agent": agent_name,
    }

    invocations_file = logs_dir / "agent-invocations.jsonl"
    with open(invocations_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"📝 Agent 调用已记录: {agent_name}", file=sys.stderr)


if __name__ == "__main__":
    main()
