#!/usr/bin/env python3
"""
验证 .claude/settings.json 中所有 hooks 引用的脚本都真实存在。

CI 会跑这个脚本；它的职责是：settings.json 里每个 command 字段指向的脚本路径都能解析到磁盘上的真实文件。
"""

import json
import re
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]
    settings = project_root / ".claude" / "settings.json"

    with open(settings, "r", encoding="utf-8") as f:
        config = json.load(f)

    missing = []
    checked = []

    for event, items in config.get("hooks", {}).items():
        for item in items:
            for hook in item.get("hooks", []):
                cmd = hook.get("command", "")
                # 提取 $CLAUDE_PROJECT_DIR 后的路径
                match = re.search(r"\$CLAUDE_PROJECT_DIR[\"']?/([^\s\"']+)", cmd)
                if not match:
                    continue
                rel_path = match.group(1).strip('"')
                abs_path = project_root / rel_path
                checked.append(f"{event}: {rel_path}")
                if not abs_path.is_file():
                    missing.append(f"{event}: {rel_path}")

    print(f"Checked {len(checked)} hook scripts:")
    for c in checked:
        print(f"  ✓ {c}")

    if missing:
        print("\n❌ Missing scripts:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    print("\n✅ All hook scripts exist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
