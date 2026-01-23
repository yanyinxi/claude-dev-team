"""
AlphaZero 监控系统 - API 路由

提供 Claude Dev Team 系统运行状态监控接口。
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# 项目根目录
# monitor_router.py 位于: main/backend/api/routes/monitor_router.py
# 需要往上 4 级到项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
CLAUDE_DIR = PROJECT_ROOT / ".claude"
EXPERIENCE_FILE = CLAUDE_DIR / "experience_pool.json"


class SystemStats(BaseModel):
    """系统状态数据"""

    # 文件状态
    agents_count: int = 0
    hooks_count: int = 0
    rules_count: int = 0
    experience_count: int = 0

    # 经验池统计
    avg_reward: float = 0.0
    recent_24h_count: int = 0

    # 按 Agent 分布
    by_agent: dict = {}

    # 按策略类型分布
    by_keyword: dict = {}

    # 系统健康状态
    healthy: bool = True


class AgentInfo(BaseModel):
    """Agent 信息"""

    name: str = "unknown"
    description: str = ""
    tools: list = []
    file_size: int = 0
    updated: str = "未知"


class RuleInfo(BaseModel):
    """规则文件信息"""

    name: str = "unknown"
    updated: str = "未知"
    insights_count: int = 0
    file_size: int = 0


@router.get("/stats")
async def get_system_stats() -> SystemStats:
    """
    获取系统运行状态统计

    返回：
    - 文件完整性检查
    - 经验池统计
    - 按 Agent 和策略类型分布
    """
    stats = SystemStats()

    # 1. 检查文件
    agents_dir = CLAUDE_DIR / "agents"
    hooks_dir = CLAUDE_DIR / "hooks"
    rules_dir = CLAUDE_DIR / "rules"

    # 统计文件
    if agents_dir.exists():
        stats.agents_count = len(list(agents_dir.glob("*.md")))

    if hooks_dir.exists():
        stats.hooks_count = len(list(hooks_dir.glob("*.py")))

    if rules_dir.exists():
        stats.rules_count = len(list(rules_dir.glob("*.md")))

    # 2. 读取经验池
    if EXPERIENCE_FILE.exists() and EXPERIENCE_FILE.stat().st_size > 0:
        try:
            with open(EXPERIENCE_FILE, "r", encoding="utf-8") as f:
                experiences = json.load(f)

            stats.experience_count = len(experiences)

            if experiences:
                # 计算平均奖励
                total_reward = sum(e.get("reward", 0) for e in experiences)
                stats.avg_reward = round(total_reward / len(experiences), 2)

                # 按 Agent 统计
                by_agent = {}
                by_keyword = {}

                cutoff = datetime.now() - timedelta(hours=24)
                recent_count = 0

                for e in experiences:
                    # Agent 统计
                    agent = e.get("agent", "unknown")
                    by_agent[agent] = by_agent.get(agent, 0) + 1

                    # 关键词统计
                    keyword = e.get("strategy_keyword", "general")
                    by_keyword[keyword] = by_keyword.get(keyword, 0) + 1

                    # 最近 24 小时
                    try:
                        timestamp = datetime.fromisoformat(
                            e.get("timestamp", "2000-01-01")
                        )
                        if timestamp > cutoff:
                            recent_count += 1
                    except:
                        pass

                stats.by_agent = by_agent
                stats.by_keyword = by_keyword
                stats.recent_24h_count = recent_count

        except (json.JSONDecodeError, IOError) as e:
            stats.healthy = False
            raise HTTPException(status_code=500, detail=f"读取经验池失败: {str(e)}")
    else:
        # 空经验池是正常状态
        pass

    return stats


@router.get("/agents")
async def get_agents_info() -> list[AgentInfo]:
    """
    获取所有 Agent 信息
    """
    agents = []
    agents_dir = CLAUDE_DIR / "agents"

    if not agents_dir.exists():
        return []

    agent_files = [
        "strategy-selector.md",
        "self-play-trainer.md",
        "evolver.md",
        "backend-developer.md",
        "frontend-developer.md",
        "orchestrator.md",
        "product-manager.md",
        "tech-lead.md",
        "code-reviewer.md",
        "test.md",
        "progress-viewer.md",
    ]

    for agent_file in agent_files:
        file_path = agents_dir / agent_file
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            # 提取名称
            name = None
            for line in content.split("\n"):
                if line.startswith("name:"):
                    name = line.replace("name:", "").strip()
                    break

            # 提取描述（第一行）
            description = ""
            if "---" in content:
                parts = content.split("---")
                if len(parts) >= 2:
                    desc_part = parts[1].strip()
                    for line in desc_part.split("\n")[:3]:
                        if line.strip() and not line.startswith("---"):
                            description += line.strip()[:100] + " "

            # 获取文件信息
            stat = file_path.stat()

            agents.append(
                AgentInfo(
                    name=name or agent_file.replace(".md", ""),
                    description=description.strip()[:150],
                    tools=[],  # 可以扩展提取
                    file_size=stat.st_size,
                    updated=datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                )
            )

    return agents


@router.get("/rules")
async def get_rules_info() -> list[RuleInfo]:
    """
    获取所有策略规则信息
    """
    rules = []
    rules_dir = CLAUDE_DIR / "rules"

    if not rules_dir.exists():
        return []

    import re

    for rule_file in rules_dir.glob("*.md"):
        content = rule_file.read_text(encoding="utf-8")

        # 提取更新时间
        update_match = re.search(
            r"更新时间:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", content
        )
        updated = update_match.group(1) if update_match else "未知"

        # 统计洞察数量
        insights_count = content.count("### ")

        # 文件大小
        file_size = len(content)

        rules.append(
            RuleInfo(
                name=rule_file.stem,
                updated=updated,
                insights_count=insights_count,
                file_size=file_size,
            )
        )

    return rules


@router.get("/experience")
async def get_experience_pool(limit: int = 50) -> dict:
    """
    获取经验池数据

    参数：
    - limit: 返回记录数量限制（默认50）
    """
    if not EXPERIENCE_FILE.exists():
        return {"total": 0, "records": [], "message": "经验池为空"}

    try:
        with open(EXPERIENCE_FILE, "r", encoding="utf-8") as f:
            experiences = json.load(f)

        # 返回最近记录
        recent = experiences[-limit:] if limit > 0 else experiences

        return {
            "total": len(experiences),
            "records": recent,
            "avg_reward": round(
                sum(e.get("reward", 0) for e in experiences) / len(experiences), 2
            )
            if experiences
            else 0,
        }

    except (json.JSONDecodeError, IOError):
        raise HTTPException(status_code=500, detail="读取经验池失败")


@router.get("/hooks")
async def get_hooks_status() -> dict:
    """
    获取 Hooks 配置状态
    """
    settings_file = PROJECT_ROOT / ".claude" / "settings.json"

    if not settings_file.exists():
        return {"error": "settings.json 不存在"}

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)

        hooks = settings.get("hooks", {})

        # 返回 Hook 配置
        result = {}
        for hook_name, hook_configs in hooks.items():
            result[hook_name] = []
            for config in hook_configs:
                result[hook_name].append(
                    {
                        "matcher": config.get("matcher", ""),
                        "hooks": [
                            {
                                "type": h.get("type"),
                                "command": h.get("command", "")[:80] + "..."
                                if len(h.get("command", "")) > 80
                                else h.get("command", ""),
                            }
                            for h in config.get("hooks", [])
                        ],
                    }
                )

        return result

    except (json.JSONDecodeError, IOError):
        raise HTTPException(status_code=500, detail="读取配置失败")


@router.get("/health")
async def health_check() -> dict:
    """
    系统健康检查
    """
    checks = {
        "agents": (CLAUDE_DIR / "agents").exists(),
        "hooks": (CLAUDE_DIR / "hooks").exists(),
        "rules": (CLAUDE_DIR / "rules").exists(),
        "settings": (PROJECT_ROOT / ".claude" / "settings.json").exists(),
    }

    all_healthy = all(checks.values())

    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": checks,
        "timestamp": datetime.now().isoformat(),
    }
