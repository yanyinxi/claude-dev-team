#!/usr/bin/env python3
"""
进化系统端到端测试

测试目标：证明进化系统能从真实数据中正确学习。

场景：
1. 高质量会话（focused + tests）→ 应该被高分奖励
2. 低质量会话（sprawling + no tests）→ 应该被低分惩罚
3. 多次累积 → EMA 应该平滑收敛
4. agent 调用记录 → 真实写入和聚合
5. 权重持久化 → 跨会话保留

每个场景都不依赖 hook 数据，直接调用模块函数验证算法正确性。
"""
import json
import sys
import tempfile
from pathlib import Path

# 让测试能导入 hook 脚本
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks" / "scripts"))

from strategy_updater import score_session, update_weights, read_latest_session  # noqa: E402


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def assert_eq(actual, expected, msg: str) -> bool:
    if actual == expected:
        print(f"  {GREEN}✓{RESET} {msg}: {actual}")
        return True
    print(f"  {RED}✗{RESET} {msg}: 期望 {expected}, 实际 {actual}")
    return False


def assert_close(actual: float, expected: float, tol: float, msg: str) -> bool:
    if abs(actual - expected) <= tol:
        print(f"  {GREEN}✓{RESET} {msg}: {actual:.2f} (期望 {expected:.2f}±{tol})")
        return True
    print(f"  {RED}✗{RESET} {msg}: 期望 {expected:.2f}±{tol}, 实际 {actual:.2f}")
    return False


def assert_gt(actual: float, threshold: float, msg: str) -> bool:
    if actual > threshold:
        print(f"  {GREEN}✓{RESET} {msg}: {actual:.2f} > {threshold}")
        return True
    print(f"  {RED}✗{RESET} {msg}: 期望 > {threshold}, 实际 {actual:.2f}")
    return False


def assert_lt(actual: float, threshold: float, msg: str) -> bool:
    if actual < threshold:
        print(f"  {GREEN}✓{RESET} {msg}: {actual:.2f} < {threshold}")
        return True
    print(f"  {RED}✗{RESET} {msg}: 期望 < {threshold}, 实际 {actual:.2f}")
    return False


def make_session(domain: str, productivity: str, has_tests: bool, test_ratio: float,
                 lines: int, agents_count: int, has_commit: bool) -> dict:
    """构造模拟的会话记录。"""
    return {
        "type": "session_end",
        "primary_domain": domain,
        "git_metrics": {
            "files_changed": 5 if productivity == "focused" else 25,
            "lines_added": lines // 2,
            "lines_removed": lines // 2,
        },
        "signals": {
            "productivity": productivity,
            "has_tests": has_tests,
            "test_ratio": test_ratio,
            "volume_lines": lines,
            "agents_used_count": agents_count,
            "agents_unique": [f"agent-{i}" for i in range(agents_count)],
            "commits_in_session": has_commit,
        },
    }


def test_scoring_logic() -> int:
    print(f"\n{BOLD}测试 1: 评分函数合理性{RESET}")
    failures = 0

    ideal = make_session("backend", "focused", True, 0.4, 200, 4, True)
    score_ideal = score_session(ideal)
    if not assert_gt(score_ideal, 7.5, "理想会话应得高分"):
        failures += 1

    bad = make_session("backend", "sprawling", False, 0.0, 1500, 1, False)
    score_bad = score_session(bad)
    if not assert_lt(score_bad, 5.0, "糟糕会话应得低分"):
        failures += 1

    idle = make_session("idle", "none", False, 0.0, 0, 0, False)
    score_idle = score_session(idle)
    if not assert_lt(score_idle, 4.5, "无产出会话应被惩罚"):
        failures += 1

    mediocre = make_session("backend", "focused", False, 0.0, 100, 1, True)
    score_mediocre = score_session(mediocre)
    if not assert_close(score_mediocre, 7.8, 1.0, "聚焦无测试应中等偏上"):
        failures += 1

    if score_ideal > score_mediocre > score_bad:
        print(f"  {GREEN}✓{RESET} 评分单调性: {score_ideal:.2f} > {score_mediocre:.2f} > {score_bad:.2f}")
    else:
        print(f"  {RED}✗{RESET} 评分单调性失败")
        failures += 1

    return failures


def test_ema_update() -> int:
    print(f"\n{BOLD}测试 2: EMA 权重更新{RESET}")
    failures = 0

    with tempfile.TemporaryDirectory() as tmp:
        weights_file = Path(tmp) / "weights.json"

        session1 = make_session("backend", "focused", True, 0.5, 100, 3, True)
        score1 = score_session(session1)
        update_weights(weights_file, "backend", score1, session1)

        with open(weights_file) as f:
            data = json.load(f)
        expected1 = round(5.0 * 0.7 + score1 * 0.3, 2)
        if not assert_eq(data["backend"], expected1, "首次 EMA 更新"):
            failures += 1
        if not assert_eq(data["metadata"]["backend"]["execution_count"], 1, "执行次数"):
            failures += 1

        for _ in range(10):
            update_weights(weights_file, "backend", 9.0, session1)

        with open(weights_file) as f:
            data = json.load(f)
        if not assert_gt(data["backend"], 8.0, "连续高分后权重收敛到高位"):
            failures += 1
        if not assert_eq(data["metadata"]["backend"]["execution_count"], 11, "累计执行次数"):
            failures += 1

        prev_weight = data["backend"]
        update_weights(weights_file, "backend", 2.0, session1)
        with open(weights_file) as f:
            data = json.load(f)
        if not assert_lt(data["backend"], prev_weight, "低分使权重下降"):
            failures += 1
        expected_after_drop = round(prev_weight * 0.7 + 2.0 * 0.3, 2)
        if not assert_close(data["backend"], expected_after_drop, 0.05, "EMA 平滑性"):
            failures += 1

    return failures


def test_session_log_io() -> int:
    print(f"\n{BOLD}测试 3: 会话日志读写{RESET}")
    failures = 0

    with tempfile.TemporaryDirectory() as tmp:
        sessions_file = Path(tmp) / "sessions.jsonl"

        result = read_latest_session(sessions_file)
        if not assert_eq(result, None, "不存在文件返回 None"):
            failures += 1

        records = [
            make_session("backend", "focused", True, 0.3, 100, 2, True),
            make_session("frontend", "broad", False, 0.0, 200, 1, False),
            make_session("tests", "focused", True, 1.0, 50, 1, True),
        ]
        with open(sessions_file, "w") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")

        latest = read_latest_session(sessions_file)
        if latest and latest.get("primary_domain") == "tests":
            print(f"  {GREEN}✓{RESET} 正确读取最后一条记录: {latest['primary_domain']}")
        else:
            print(f"  {RED}✗{RESET} 读取最后一条失败: {latest}")
            failures += 1

        with open(sessions_file, "a") as f:
            f.write("invalid json line\n")
        latest = read_latest_session(sessions_file)
        if latest and latest.get("primary_domain") == "tests":
            print(f"  {GREEN}✓{RESET} 跳过损坏行，找到最后有效记录")
        else:
            print(f"  {RED}✗{RESET} 未能跳过损坏行")
            failures += 1

    return failures


def test_hook_subprocess() -> int:
    print(f"\n{BOLD}测试 4: Hook 脚本子进程调用{RESET}")
    failures = 0

    import subprocess
    import os

    project_root = Path(__file__).resolve().parents[2]

    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "CLAUDE_PROJECT_DIR": tmp}
        Path(tmp, ".claude", "logs").mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ["python3", str(project_root / ".claude/hooks/scripts/auto_evolver.py")],
            input='{"session_id":"test-1","tool_input":{"subagent_type":"backend-developer"}}',
            capture_output=True, text=True, env=env, timeout=10, check=False
        )
        if result.returncode == 0:
            print(f"  {GREEN}✓{RESET} auto_evolver 退出 0")
        else:
            print(f"  {RED}✗{RESET} auto_evolver 失败: {result.stderr}")
            failures += 1

        invocations = Path(tmp, ".claude/logs/agent-invocations.jsonl")
        if invocations.exists() and "backend-developer" in invocations.read_text():
            print(f"  {GREEN}✓{RESET} agent 调用已写入日志")
        else:
            print(f"  {RED}✗{RESET} agent 调用未写入")
            failures += 1

        result = subprocess.run(
            ["python3", str(project_root / ".claude/hooks/scripts/session_evolver.py")],
            input='{"session_id":"test-1"}',
            capture_output=True, text=True, env=env, timeout=10, check=False
        )
        if result.returncode == 0:
            print(f"  {GREEN}✓{RESET} session_evolver 在无 git 环境下不崩溃")
        else:
            print(f"  {RED}✗{RESET} session_evolver 崩溃: {result.stderr}")
            failures += 1

        sessions_file = Path(tmp, ".claude/logs/sessions.jsonl")
        sessions_file.write_text(
            json.dumps(make_session("backend", "focused", True, 0.5, 100, 3, True)) + "\n"
        )

        result = subprocess.run(
            ["python3", str(project_root / ".claude/hooks/scripts/strategy_updater.py")],
            input="",
            capture_output=True, text=True, env=env, timeout=10, check=False
        )
        if result.returncode == 0:
            print(f"  {GREEN}✓{RESET} strategy_updater 退出 0")
        else:
            print(f"  {RED}✗{RESET} strategy_updater 失败: {result.stderr}")
            failures += 1

        weights = Path(tmp, ".claude/strategy_weights.json")
        if weights.exists():
            data = json.loads(weights.read_text())
            if "backend" in data and data["backend"] != 5.0:
                print(f"  {GREEN}✓{RESET} 策略权重已被更新: backend = {data['backend']}")
            else:
                print(f"  {RED}✗{RESET} 权重未被更新: {data}")
                failures += 1
        else:
            print(f"  {RED}✗{RESET} 权重文件未生成")
            failures += 1

    return failures


def test_cumulative_learning() -> int:
    print(f"\n{BOLD}测试 5: 累积学习行为（核心）{RESET}")
    failures = 0

    with tempfile.TemporaryDirectory() as tmp:
        weights_file = Path(tmp) / "weights.json"

        for _ in range(10):
            bad = make_session("backend", "sprawling", False, 0.0, 1500, 1, False)
            update_weights(weights_file, "backend", score_session(bad), bad)

        with open(weights_file) as f:
            mid_data = json.load(f)
        weight_after_bad = mid_data["backend"]
        print(f"  10 次糟糕会话后权重: {weight_after_bad:.2f}")

        for _ in range(10):
            good = make_session("backend", "focused", True, 0.4, 200, 4, True)
            update_weights(weights_file, "backend", score_session(good), good)

        with open(weights_file) as f:
            final_data = json.load(f)
        weight_after_good = final_data["backend"]
        print(f"  再 10 次优质会话后权重: {weight_after_good:.2f}")

        if not assert_lt(weight_after_bad, 5.0, "10次糟糕后权重应低于 5.0"):
            failures += 1
        if not assert_gt(weight_after_good, weight_after_bad, "优质后权重必须高于糟糕后"):
            failures += 1
        if not assert_eq(final_data["metadata"]["backend"]["execution_count"], 20, "总执行次数 = 20"):
            failures += 1

        last_signals = final_data["metadata"]["backend"]["last_signals"]
        if last_signals.get("productivity") == "focused" and last_signals.get("has_tests"):
            print(f"  {GREEN}✓{RESET} 最新会话信号正确保留（可审计）")
        else:
            print(f"  {RED}✗{RESET} 信号丢失: {last_signals}")
            failures += 1

    return failures


def main():
    print(f"{BOLD}进化系统端到端测试{RESET}")
    print("=" * 60)

    results = [
        ("评分逻辑", test_scoring_logic()),
        ("EMA 更新", test_ema_update()),
        ("会话日志 IO", test_session_log_io()),
        ("Hook 子进程", test_hook_subprocess()),
        ("累积学习", test_cumulative_learning()),
    ]

    print(f"\n{BOLD}测试结果汇总{RESET}")
    print("=" * 60)
    total_failures = 0
    for name, failures in results:
        status = f"{GREEN}通过{RESET}" if failures == 0 else f"{RED}失败 ({failures}){RESET}"
        print(f"  {name:20s} {status}")
        total_failures += failures

    print("=" * 60)
    if total_failures == 0:
        print(f"{GREEN}{BOLD}✅ 全部通过！进化系统可用。{RESET}")
        return 0
    print(f"{RED}{BOLD}❌ 失败 {total_failures} 项{RESET}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
