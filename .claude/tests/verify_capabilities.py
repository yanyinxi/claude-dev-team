#!/usr/bin/env python3
"""
验证能力清单与文档声明是否与代码一致。

校验内容：
1) implemented 能力必须能在代码中找到证据（文件存在 + 关键片段存在）
2) planned/deprecated 能力的 forbidden_doc_patterns 不能在文档中作为“可运行能力”出现
3) 文档中的 .claude 命令路径必须真实存在（支持 python3/bash/cat/ls/tail/head）
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = PROJECT_ROOT / ".claude" / "capabilities.json"
DOC_ROOT = PROJECT_ROOT / ".claude"
EXCLUDE_DOC_PREFIXES = [
    ".claude/docs/history/",
]
ALLOWED_STATUSES = {"implemented", "planned", "deprecated"}

# 识别文档里常见命令中的 .claude 路径
COMMAND_PATH_RE = re.compile(
    r"(?:python3|bash|cat|ls|tail|head)\s+(\.claude/[\w./\-]+)",
    re.IGNORECASE,
)


def iter_markdown_files() -> List[Path]:
    files = []
    for path in DOC_ROOT.rglob("*.md"):
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        if any(rel.startswith(prefix) for prefix in EXCLUDE_DOC_PREFIXES):
            continue
        files.append(path)
    return sorted(files)


def load_manifest() -> Dict:
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def check_implemented_evidence(cap: Dict) -> List[str]:
    errors: List[str] = []
    evidence = cap.get("evidence") or {}
    path = evidence.get("path")
    contains = evidence.get("contains", [])

    if not path:
        return [f"{cap['id']}: implemented 能力缺少 evidence.path"]

    abs_path = PROJECT_ROOT / path
    if not abs_path.is_file():
        return [f"{cap['id']}: 证据文件不存在: {path}"]

    text = abs_path.read_text(encoding="utf-8")
    for token in contains:
        if token not in text:
            errors.append(f"{cap['id']}: 证据文件缺少关键片段: {token}")

    return errors


def is_context_explicitly_unimplemented(line: str) -> bool:
    markers = ["未实现", "计划", "planned", "not implemented", "当前不支持", "历史", "deprecated"]
    lower = line.lower()
    return any(m.lower() in lower for m in markers)


def check_forbidden_patterns(cap: Dict, docs: List[Path]) -> List[str]:
    errors: List[str] = []
    patterns = cap.get("forbidden_doc_patterns", [])
    if not patterns:
        return errors

    for doc in docs:
        rel = doc.relative_to(PROJECT_ROOT).as_posix()
        for lineno, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern in patterns:
                if pattern in line and not is_context_explicitly_unimplemented(line):
                    errors.append(
                        f"{cap['id']}: 文档出现禁止声明 {rel}:{lineno} -> {pattern}"
                    )
    return errors


def check_command_paths(docs: List[Path]) -> List[str]:
    errors: List[str] = []

    for doc in docs:
        rel = doc.relative_to(PROJECT_ROOT).as_posix()
        lines = doc.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            for match in COMMAND_PATH_RE.finditer(line):
                ref = match.group(1)

                # 通配符和目录说明跳过
                if "*" in ref or ref.endswith("/"):
                    continue

                target = PROJECT_ROOT / ref
                if not target.exists():
                    errors.append(f"命令路径不存在: {rel}:{lineno} -> {ref}")

    return errors


def validate_manifest_schema(manifest: Dict) -> Tuple[List[str], List[Dict]]:
    errors: List[str] = []
    caps = manifest.get("capabilities")

    if not isinstance(caps, list):
        return ["capabilities.json 缺少 capabilities 数组"], []

    seen = set()
    for item in caps:
        cid = item.get("id")
        status = item.get("status")

        if not cid:
            errors.append("发现缺少 id 的 capability")
            continue
        if cid in seen:
            errors.append(f"重复 capability id: {cid}")
        seen.add(cid)

        if status not in ALLOWED_STATUSES:
            errors.append(f"{cid}: 非法 status={status}")

    return errors, caps


def main() -> int:
    if not MANIFEST.is_file():
        print(f"❌ 未找到能力清单: {MANIFEST}", file=sys.stderr)
        return 1

    manifest = load_manifest()
    schema_errors, caps = validate_manifest_schema(manifest)

    docs = iter_markdown_files()
    errors: List[str] = []
    errors.extend(schema_errors)

    for cap in caps:
        status = cap.get("status")
        if status == "implemented":
            errors.extend(check_implemented_evidence(cap))
        else:
            errors.extend(check_forbidden_patterns(cap, docs))

    errors.extend(check_command_paths(docs))

    print(f"Checked capabilities: {len(caps)}")
    print(f"Checked docs: {len(docs)} markdown files")

    if errors:
        print("\n❌ 验证失败:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\n✅ capabilities 与文档声明一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
