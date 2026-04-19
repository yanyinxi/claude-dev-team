#!/usr/bin/env python3
"""
Session Evolver - Stop Hook Script
会话结束时记录进化日志。
Stop hook 的 stdin 数据结构极简（可能为空），
改为从 git 和环境变量获取真实可靠的会话信息。
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_git(args: list, cwd: str) -> str:
    try:
        result = subprocess.run(
            ["git"] + args, cwd=cwd,
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def main():
    # Stop hook 传入的 stdin 可能为空或仅含极简数据，优先读取但不依赖
    try:
        raw = sys.stdin.read().strip()
        hook_data = json.loads(raw) if raw else {}
    except Exception:
        hook_data = {}

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    logs_dir = Path(project_root) / ".claude" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # 从 git 获取真实数据
    modified_files = run_git(["status", "--short"], project_root)
    last_commit = run_git(["log", "-1", "--oneline"], project_root)
    changed_count = len([l for l in modified_files.splitlines() if l.strip()])

    # 根据修改文件推断本次主要活动领域
    activity = "general"
    if modified_files:
        lines = modified_files.lower()
        if "backend" in lines or ".py" in lines:
            activity = "backend"
        elif "frontend" in lines or ".vue" in lines or ".ts" in lines:
            activity = "frontend"
        elif "test" in lines:
            activity = "testing"
        elif ".claude" in lines:
            activity = "system-config"

    record = {
        "timestamp": datetime.now().isoformat(),
        "session_id": hook_data.get("session_id", f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
        "stop_reason": hook_data.get("stop_reason", "end_turn"),
        "activity_domain": activity,
        "git_summary": {
            "modified_files_count": changed_count,
            "last_commit": last_commit,
            "modified_files": modified_files[:500] if modified_files else ""
        },
        "evolution_notes": f"本次会话主要活动：{activity}，涉及 {changed_count} 个文件变更"
    }

    log_file = logs_dir / "evolution-log.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ 会话进化日志已记录 [{activity}] → {log_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
