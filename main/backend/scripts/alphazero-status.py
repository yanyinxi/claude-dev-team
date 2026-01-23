#!/usr/bin/env python3
"""
AlphaZero 自博弈学习系统 - 状态监控面板

功能：
1. 查看系统状态
2. 监控经验池增长
3. 查看策略规则更新
4. 追踪学习效果

运行方式：
    python3 scripts/alphazero-status.py
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import re


class AlphaZeroStatusViewer:
    """AlphaZero 系统状态查看器"""

    def __init__(self):
        # .claude 目录在项目根目录 (claude-dev-team/.claude)
        # 脚本位置: claude-dev-team/main/backend/scripts/alphazero-status.py
        script_dir = Path(__file__).parent
        self.project_dir = script_dir.parent.parent.parent  # 项目根目录
        self.claude_dir = self.project_dir / ".claude"
        self.rules_dir = self.claude_dir / "rules"
        self.experience_file = self.claude_dir / "experience_pool.json"
        self.settings_file = self.claude_dir / "settings.json"

    def print_header(self):
        """打印标题"""
        print("\n" + "=" * 70)
        print("🤖 AlphaZero 自博弈学习系统 - 状态监控面板")
        print("=" * 70)
        print(f"项目目录: {self.project_dir}")
        print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def check_files(self):
        """检查系统文件"""
        print("\n📁 系统文件状态")
        print("-" * 50)

        files = {
            "Agent": [
                ".claude/agents/strategy-selector.md",
                ".claude/agents/self-play-trainer.md",
                ".claude/agents/evolver.md",
            ],
            "Hooks": [
                ".claude/hooks/reward_evaluator.py",
                ".claude/hooks/strategy_learner.py",
            ],
            "Rules": [
                ".claude/rules/frontend.md",
                ".claude/rules/backend.md",
                ".claude/rules/collaboration.md",
            ],
            "Config": [
                ".claude/settings.json",
                ".claude/experience_pool.json",
            ],
        }

        total = 0
        present = 0

        for category, file_list in files.items():
            print(f"\n【{category}】")
            for f in file_list:
                path = self.project_dir / f
                exists = path.exists()
                total += 1
                if exists:
                    present += 1
                    mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime(
                        "%m-%d %H:%M"
                    )
                    size = path.stat().st_size
                    print(f"  ✅ {f.split('/')[-1]:30} {mtime:8} {size:>6} bytes")
                else:
                    print(f"  ❌ {f.split('/')[-1]:30} 不存在")

        print(f"\n📊 文件完整性: {present}/{total}")

        return present == total

    def show_hooks_status(self):
        """查看 Hooks 配置"""
        print("\n🪝 Hooks 配置状态")
        print("-" * 50)

        try:
            with open(self.settings_file, "r") as f:
                data = json.load(f)

            hooks = data.get("hooks", {})

            # 定义需要检查的 Hook 配置
            hook_checks = [
                ("PostToolUse (Task)", "reward_evaluator.py", "奖励评估"),
                ("PostToolUse (Write|Edit)", "quality-gate.sh", "质量门禁"),
                ("SubagentStop", "strategy_learner.py", "策略学习"),
                ("PreToolUse (Bash)", "safety-check.sh", "安全检查"),
                ("UserPromptSubmit", "context-enhancer.sh", "上下文增强"),
                ("Stop", "提示", "进化提醒"),
            ]

            for hook_name, script, desc in hook_checks:
                configured = False

                if "Task" in hook_name:
                    for h in hooks.get("PostToolUse", []):
                        if "Task" in h.get("matcher", ""):
                            for hook in h.get("hooks", []):
                                if script in hook.get("command", ""):
                                    configured = True
                                    break
                            if configured:
                                break
                else:
                    hook_type = hook_name.split()[0]
                    for h in hooks.get(hook_type, []):
                        for hook in h.get("hooks", []):
                            if script in hook.get("command", "") or (
                                script == "提示" and "echo" in hook.get("command", "")
                            ):
                                configured = True
                                break

                status = "✅" if configured else "❌"
                print(f"  {status} {hook_name:25} → {desc}")

        except Exception as e:
            print(f"  ❌ 读取配置失败: {e}")

    def show_experience_pool(self):
        """查看经验池统计"""
        print("\n📈 经验池统计")
        print("-" * 50)

        if not self.experience_file.exists():
            print("  ℹ️ 经验池为空，尚未积累数据")
            return

        try:
            with open(self.experience_file, "r") as f:
                experiences = json.load(f)

            if not experiences:
                print("  ℹ️ 经验池为空，尚未积累数据")
                return

            # 统计
            total = len(experiences)

            # 按 Agent 统计
            by_agent = {}
            by_keyword = {}
            total_reward = 0

            for e in experiences:
                # Agent 统计
                agent = e.get("agent", "unknown")
                by_agent[agent] = by_agent.get(agent, 0) + 1

                # 关键词统计
                keyword = e.get("strategy_keyword", "general")
                by_keyword[keyword] = by_keyword.get(keyword, 0) + 1

                # 奖励统计
                total_reward += e.get("reward", 0)

            avg_reward = total_reward / total if total > 0 else 0

            print(f"\n  总经验数: {total} 条")
            print(f"  平均奖励: {avg_reward:.1f}/10 分")

            # 按 Agent
            print("\n  按 Agent 分布:")
            for agent, count in sorted(by_agent.items(), key=lambda x: -x[1]):
                bar_len = count * 10 // total if total > 0 else 0
                bar = "█" * bar_len
                print(f"    {agent:25} {count:3} 条 {bar}")

            # 按关键词
            print("\n  按策略类型分布:")
            for keyword, count in sorted(by_keyword.items(), key=lambda x: -x[1]):
                bar_len = count * 10 // total if total > 0 else 0
                bar = "█" * bar_len
                print(f"    {keyword:25} {count:3} 条 {bar}")

            # 最近 24 小时
            recent_cutoff = datetime.now() - timedelta(hours=24)
            recent = [
                e
                for e in experiences
                if datetime.fromisoformat(e.get("timestamp", "2000-01-01"))
                > recent_cutoff
            ]
            print(f"\n  最近 24 小时: {len(recent)} 条")

        except Exception as e:
            print(f"  ❌ 读取经验池失败: {e}")

    def show_rules_summary(self):
        """查看策略规则摘要"""
        print("\n📋 策略规则摘要")
        print("-" * 50)

        if not self.rules_dir.exists():
            print("  ℹ️ 规则目录不存在")
            return

        rule_files = list(self.rules_dir.glob("*.md"))

        for rf in rule_files:
            content = rf.read_text()
            lines = len(content.split("\n"))

            # 检查更新时间
            update_match = re.search(
                r"更新时间:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", content
            )
            update_time = update_match.group(1) if update_match else "未知"

            # 检查洞察数量
            insights = content.count("### ")

            print(f"\n  【{rf.stem}】")
            print(f"    更新时间: {update_time}")
            print(f"    文件大小: {len(content)} bytes")
            print(f"    洞察数量: {insights} 条")

    def show_usage_guide(self):
        """显示使用指南"""
        print("\n" + "=" * 70)
        print("📖 使用指南")
        print("=" * 70)

        print("""
【如何触发系统学习】

1. 执行任何任务
   方式 A: "实现一个按钮组件"
   方式 B: "使用 strategy-selector 优化用户管理功能的分配策略"
   方式 C: "使用 self-play-trainer 优化登录功能的策略"

2. 系统自动执行
   - reward_evaluator 计算奖励分数
   - strategy_learner 更新策略规则
   - evolver 提炼到全局知识库

3. 查看学习成果
   运行: python3 scripts/alphazero-status.py

【如何观察效果】

1. 经验池增长
   - 每次任务后增加记录
   - 包含 Agent、奖励分数、策略类型

2. 策略规则更新
   - 记录有效的策略模式
   - 避免重复错误

3. 系统越来越聪明
   - 相同场景任务效率提升
   - 策略选择更精准
        """)

    def show_log_guide(self):
        """显示日志查看指南"""
        print("\n📜 日志查看")
        print("-" * 50)
        print("""
  查看经验池:
    cat .claude/experience_pool.json | python3 -m json.tool

  查看前端策略:
    cat .claude/rules/frontend.md

  查看后端策略:
    cat .claude/rules/backend.md

  查看协作策略:
    cat .claude/rules/collaboration.md

  实时监控 (macOS):
    watch -n 5 'python3 scripts/alphazero-status.py'

  实时监控 (Linux):
    while true; do clear; python3 scripts/alphazero-status.py; sleep 5; done
        """)

    def run(self):
        """运行完整状态检查"""
        self.print_header()

        files_ok = self.check_files()
        self.show_hooks_status()
        self.show_experience_pool()
        self.show_rules_summary()
        self.show_usage_guide()
        self.show_log_guide()

        print("\n" + "=" * 70)
        print("✅ 状态检查完成")
        print("=" * 70)

        return files_ok


if __name__ == "__main__":
    viewer = AlphaZeroStatusViewer()
    success = viewer.run()
    exit(0 if success else 1)
