#!/usr/bin/env python3
"""
进化状态查看工具

用法：
  python3 .claude/lib/show_evolution.py           # 完整报告
  python3 .claude/lib/show_evolution.py --weights # 只看权重
  python3 .claude/lib/show_evolution.py --recent  # 只看最近会话
  python3 .claude/lib/show_evolution.py --agents  # 只看 agent 调用统计
"""
import json
import sys
from collections import Counter
from pathlib import Path

GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def bar(value: float, max_val: float = 10.0, width: int = 20) -> str:
    filled = int(value / max_val * width)
    color = GREEN if value >= 7 else YELLOW if value >= 5 else "\033[91m"
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET}"


def show_weights(weights_file: Path):
    if not weights_file.exists():
        print(f"{DIM}  权重文件不存在{RESET}")
        return

    with open(weights_file) as f:
        data = json.load(f)

    print(f"\n{BOLD}策略权重{RESET}  (EMA alpha=0.3，满分 10)")
    print("─" * 55)
    domains = [k for k in data if not k.startswith("_") and k != "metadata"]
    for domain in sorted(domains):
        w = data[domain]
        meta = data.get("metadata", {}).get(domain, {})
        count = meta.get("execution_count", 0)
        last_score = meta.get("last_session_score", "-")
        print(f"  {domain:12s} {bar(w)}  {w:.2f}  [{count} 次, 最近 {last_score}]")


def show_recent_sessions(sessions_file: Path, n: int = 5):
    if not sessions_file.exists():
        print(f"{DIM}  会话记录不存在（需要真实会话触发 Stop hook 后才会生成）{RESET}")
        return

    with open(sessions_file) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]

    sessions = []
    for ln in lines:
        try:
            r = json.loads(ln)
            if r.get("type") == "session_end":
                sessions.append(r)
        except json.JSONDecodeError:
            continue

    if not sessions:
        print(f"{DIM}  暂无会话记录{RESET}")
        return

    print(f"\n{BOLD}最近 {min(n, len(sessions))} 次会话{RESET}  (共 {len(sessions)} 次)")
    print("─" * 65)
    for s in sessions[-n:]:
        ts = s.get("timestamp", "")[:16]
        domain = s.get("primary_domain", "?")
        sig = s.get("signals", {})
        git = s.get("git_metrics", {})
        prod = sig.get("productivity", "?")
        files = git.get("files_changed", 0)
        added = git.get("lines_added", 0)
        removed = git.get("lines_removed", 0)
        agents = sig.get("agents_used_count", 0)
        has_tests = "✓测试" if sig.get("has_tests") else "✗测试"
        has_commit = "✓commit" if sig.get("commits_in_session") else "✗commit"
        prod_color = GREEN if prod == "focused" else YELLOW if prod == "broad" else "\033[91m"
        print(
            f"  {DIM}{ts}{RESET}  {BLUE}{domain:8s}{RESET}  "
            f"{prod_color}{prod:10s}{RESET}  "
            f"files={files} +{added}/-{removed}  "
            f"agents={agents}  {has_tests} {has_commit}"
        )


def show_agent_stats(invocations_file: Path):
    if not invocations_file.exists():
        print(f"{DIM}  agent 调用记录不存在{RESET}")
        return

    with open(invocations_file) as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]

    agents = []
    for ln in lines:
        try:
            r = json.loads(ln)
            if r.get("type") == "agent_invoked":
                agents.append(r.get("agent", "unknown"))
        except json.JSONDecodeError:
            continue

    if not agents:
        print(f"{DIM}  暂无 agent 调用记录{RESET}")
        return

    counter = Counter(agents)
    total = sum(counter.values())
    print(f"\n{BOLD}Agent 调用统计{RESET}  (共 {total} 次)")
    print("─" * 40)
    for agent, count in counter.most_common():
        pct = count / total * 100
        print(f"  {agent:25s}  {count:3d} 次  {bar(pct, 100, 15)}  {pct:.0f}%")


def main():
    project_root = Path(__file__).resolve().parents[1].parent
    # 如果从项目根目录运行
    if not (project_root / ".claude").exists():
        project_root = Path.cwd()

    logs_dir = project_root / ".claude" / "logs"
    weights_file = project_root / ".claude" / "strategy_weights.json"

    args = set(sys.argv[1:])
    show_all = not args

    print(f"{BOLD}═══ Claude Dev Team 进化状态 ═══{RESET}")

    if show_all or "--weights" in args:
        show_weights(weights_file)

    if show_all or "--recent" in args:
        show_recent_sessions(logs_dir / "sessions.jsonl")

    if show_all or "--agents" in args:
        show_agent_stats(logs_dir / "agent-invocations.jsonl")

    if show_all:
        print(f"\n{DIM}查看帮助：python3 .claude/lib/show_evolution.py --help{RESET}")

    print()


if __name__ == "__main__":
    main()
