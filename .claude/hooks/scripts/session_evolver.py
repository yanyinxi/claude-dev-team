#!/usr/bin/env python3
"""
Session Evolver - Stop Hook

会话结束时采集真实执行数据，这是整个自进化系统的数据源。
原则：只采集可验证的真实信号，不编造数据。

数据来源：
- git diff --stat: 真实的文件变更统计
- git log: 真实的 commit 记录
- 本次会话内 SubagentStop 累积记录：被调用过的 agent 列表
- 文件类型分布：推断活动领域
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


def run_git(args: List[str], cwd: str) -> str:
    """运行 git 命令，失败时返回空字符串而不抛异常。"""
    try:
        result = subprocess.run(
            ["git"] + args, cwd=cwd,
            capture_output=True, text=True, timeout=5, check=False
        )
        return result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def collect_git_metrics(project_root: str) -> Dict[str, Any]:
    """
    采集真实的 git 指标。这是进化系统的真正数据来源。
    """
    diff_stat = run_git(["diff", "--stat", "HEAD"], project_root)
    status_short = run_git(["status", "--short"], project_root)
    last_commits = run_git(["log", "-5", "--oneline"], project_root)
    name_only = run_git(["diff", "--name-only", "HEAD"], project_root)

    # 解析文件列表
    files = [f for f in name_only.splitlines() if f.strip()]

    # 文件类型分布（真实信号，不编造）
    categorize = {
        "backend": sum(1 for f in files if f.startswith("main/backend/")),
        "frontend": sum(1 for f in files if f.startswith("main/frontend/")),
        "tests": sum(1 for f in files if f.startswith("main/tests/") or "/tests/" in f),
        "docs": sum(1 for f in files if f.startswith("main/docs/") or f.endswith(".md")),
        "config": sum(1 for f in files if f.startswith(".claude/") or f.endswith(".json")),
    }

    # 解析 diff --stat 的最后一行，形如 " 5 files changed, 30 insertions(+), 10 deletions(-)"
    lines_added = 0
    lines_removed = 0
    if diff_stat:
        last = diff_stat.splitlines()[-1] if diff_stat.splitlines() else ""
        for part in last.split(","):
            part = part.strip()
            if "insertion" in part:
                lines_added = int(part.split()[0]) if part.split()[0].isdigit() else 0
            elif "deletion" in part:
                lines_removed = int(part.split()[0]) if part.split()[0].isdigit() else 0

    return {
        "files_changed": len(files),
        "files_by_domain": categorize,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "file_list": files[:20],  # 只保留前 20 个文件名
        "recent_commits": last_commits.splitlines()[:5],
        "has_uncommitted": bool(status_short),
    }


def collect_agent_invocations(logs_dir: Path, session_id: str) -> List[str]:
    """
    从本次会话的 SubagentStop 日志中收集被调用的 agent 列表。
    """
    invocations_file = logs_dir / "agent-invocations.jsonl"
    if not invocations_file.exists():
        return []

    agents = []
    with open(invocations_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                if record.get("session_id") == session_id:
                    agents.append(record.get("agent", "unknown"))
            except json.JSONDecodeError:
                continue
    return agents


def infer_primary_domain(metrics: Dict[str, Any]) -> str:
    """根据真实的文件分布推断主要活动领域。"""
    domains = metrics.get("files_by_domain", {})
    if not domains or sum(domains.values()) == 0:
        return "idle"
    return max(domains.items(), key=lambda x: x[1])[0]


def compute_quality_signals(metrics: Dict[str, Any], agents: List[str]) -> Dict[str, Any]:
    """
    基于真实数据计算质量信号（不是编造的评分）。
    每个信号都是可验证的事实，而不是拍脑袋的数字。
    """
    files_changed = metrics.get("files_changed", 0)
    lines_changed = metrics.get("lines_added", 0) + metrics.get("lines_removed", 0)
    test_files = metrics.get("files_by_domain", {}).get("tests", 0)

    return {
        "productivity": "none" if files_changed == 0
                        else "focused" if files_changed <= 5
                        else "broad" if files_changed <= 15
                        else "sprawling",
        "has_tests": test_files > 0,
        "test_ratio": round(test_files / files_changed, 2) if files_changed else 0.0,
        "volume_lines": lines_changed,
        "agents_used_count": len(set(agents)),
        "agents_unique": sorted(set(agents)),
        "commits_in_session": any(c for c in metrics.get("recent_commits", [])),
    }


def main():
    """
    Stop Hook 入口：采集真实会话数据并写入 sessions.jsonl。
    """
    try:
        raw = sys.stdin.read().strip()
        hook_data = json.loads(raw) if raw else {}
    except (json.JSONDecodeError, OSError):
        hook_data = {}

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    logs_dir = Path(project_root) / ".claude" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    session_id = hook_data.get("session_id", f"session-{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # 采集真实指标
    git_metrics = collect_git_metrics(project_root)
    agents_used = collect_agent_invocations(logs_dir, session_id)
    signals = compute_quality_signals(git_metrics, agents_used)
    primary_domain = infer_primary_domain(git_metrics)

    record = {
        "type": "session_end",
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "stop_reason": hook_data.get("stop_reason", "end_turn"),
        "primary_domain": primary_domain,
        "git_metrics": git_metrics,
        "signals": signals,
    }

    # 写入会话日志（追加式）
    sessions_file = logs_dir / "sessions.jsonl"
    with open(sessions_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # 人类可读摘要输出到 stderr
    print(
        f"📊 会话记录: domain={primary_domain}, "
        f"files={git_metrics['files_changed']}, "
        f"lines=+{git_metrics['lines_added']}/-{git_metrics['lines_removed']}, "
        f"agents={len(agents_used)}",
        file=sys.stderr
    )


if __name__ == "__main__":
    main()
