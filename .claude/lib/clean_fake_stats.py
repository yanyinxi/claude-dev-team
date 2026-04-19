#!/usr/bin/env python3
"""
清理 .claude/rules/*.md 中的虚假统计数据。

原则：
- 保留最佳实践、反模式、示例（这些是真实的知识）
- 删除编造的数字（平均奖励 X/10、成功率 X%、基于 X 次执行）
- 替换为明确标记：真实数据将从 sessions.jsonl 累积
"""

import re
import sys
from pathlib import Path

# 需要删除的虚假统计行（整行匹配）
FAKE_LINE_PATTERNS = [
    r"^- \*\*成功率\*\*:\s*\d+%?\s*$",
    r"^- \*\*平均奖励\*\*:.*$",
    r"^- \*\*证据\*\*:\s*基于\s*\d+\s*次任务执行.*$",
    r"^\*\*平均奖励\*\*:.*$",
    r"^\*\*成功率\*\*:.*$",
]

# 需要删除的虚假统计块（多行）
FAKE_BLOCK_PATTERNS = [
    # "### 📊 聚合洞察 (基于 N 次执行)" 整个块
    r"### 📊 聚合洞察 \(基于 \d+ 次执行\)\s*\n(?:.*\n){0,8}?(?=\n## |\n### |\Z)",
    # "## 聚合经验（基于 N 次执行）" 直到下一个 ## 的整个块
    r"## 聚合经验.*?\n(?:(?!\n## ).*\n)*",
    # "### 📊 统计数据" 块
    r"### 📊 统计数据\s*\n(?:.*\n){0,10}?(?=\n### |\n## |\Z)",
]


def clean_file(path: Path) -> bool:
    """清理单个文件，返回是否有修改。"""
    original = path.read_text(encoding="utf-8")
    content = original

    # 先移除多行块
    for pattern in FAKE_BLOCK_PATTERNS:
        content = re.sub(pattern, "", content, flags=re.MULTILINE)

    # 再按行清理单行
    lines = content.splitlines()
    kept = [ln for ln in lines
            if not any(re.match(p, ln.rstrip()) for p in FAKE_LINE_PATTERNS)]
    content = "\n".join(kept)

    # 规范化：最多两个连续空行
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 确保末尾有单个换行
    content = content.rstrip() + "\n"

    # 在文档末尾加真实数据说明
    if "## 真实执行数据" not in content:
        content += (
            "\n## 真实执行数据\n\n"
            "此规则文件的统计数据不再手工编造。真实执行指标由以下机制累积：\n\n"
            "- 每次会话结束时，`session_evolver.py` 采集 git diff / agent 调用等真实数据到 "
            "`.claude/logs/sessions.jsonl`\n"
            "- `strategy_updater.py` 基于真实指标做 EMA 更新到 `.claude/strategy_weights.json`\n"
            "- 查看最近会话信号：`tail -n 5 .claude/logs/sessions.jsonl`\n"
            "- 查看最新策略权重：`cat .claude/strategy_weights.json`\n"
        )

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    rules_dir = Path(".claude/rules")
    if not rules_dir.exists():
        print(f"❌ 目录不存在: {rules_dir}", file=sys.stderr)
        sys.exit(1)

    changed = []
    for md in sorted(rules_dir.glob("*.md")):
        if clean_file(md):
            changed.append(md.name)

    if changed:
        print(f"✅ 已清理 {len(changed)} 个文件: {', '.join(changed)}")
    else:
        print("ℹ️  无需清理")


if __name__ == "__main__":
    main()
