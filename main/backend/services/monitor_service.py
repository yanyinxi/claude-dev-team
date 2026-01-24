"""
监控系统 - 通用监控服务

功能：
1. 解析进化事件流
2. 统计 Agent 性能
3. 解析知识图谱
4. 提供数据查询接口

数据来源：
- .claude/rules/*.md (策略规则)
- .claude/agents/*.md (Agent 配置)
- .claude/skills/*/SKILL.md (技能知识)
- .claude/project_standards.md (最佳实践)
"""

import re
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from models.monitor_schema import (
    EvolutionEvent,
    EvolutionStreamResponse,
    AgentPerformance,
    PerformanceMetrics,
    KnowledgeItem,
    KnowledgeCategory,
    KnowledgeGraphResponse
)


class MonitorService:
    """通用监控服务"""

    def __init__(self):
        """初始化监控服务"""
        self.project_root = Path(__file__).parent.parent.parent.parent

    async def get_evolution_stream(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> EvolutionStreamResponse:
        """
        获取进化事件流

        数据来源: .claude/rules/*.md 文件

        Args:
            limit: 每页数量
            offset: 偏移量

        Returns:
            EvolutionStreamResponse: 进化事件流响应
        """
        events = []
        rules_dir = self.project_root / ".claude" / "rules"

        if not rules_dir.exists():
            return EvolutionStreamResponse(total=0, events=[])

        # 解析所有规则文件
        for rule_file in rules_dir.glob("*.md"):
            try:
                content = rule_file.read_text(encoding="utf-8")

                # 解析策略关键词
                strategy_match = re.search(r"策略关键词.*?:\s*(.+)", content)
                strategy = strategy_match.group(1).strip() if strategy_match else "unknown"

                # 解析洞察记录
                # 匹配格式: ### ✅ 最佳实践\n\n- **Agent**: backend-developer\n- **描述**: xxx
                insight_pattern = r"### (.+?)\n\n- \*\*Agent\*\*:\s*(.+?)\n- \*\*描述\*\*:\s*(.+?)(?=\n\n|\Z)"
                insights = re.findall(insight_pattern, content, re.DOTALL)

                for insight_type, agent, description in insights:
                    # 解析平均奖励（如果有）
                    reward_match = re.search(r"平均奖励.*?(\d+\.?\d*)/10", content)
                    reward = float(reward_match.group(1)) if reward_match else 0.0

                    # 获取文件修改时间作为事件时间
                    mtime = datetime.fromtimestamp(rule_file.stat().st_mtime)

                    events.append(EvolutionEvent(
                        id=f"evt_{uuid.uuid4().hex[:8]}",
                        timestamp=mtime,
                        agent=agent.strip(),
                        strategy=strategy,
                        description=description.strip(),
                        reward=reward
                    ))

            except Exception:
                continue

        # 按时间倒序排序
        events.sort(key=lambda e: e.timestamp, reverse=True)

        # 分页
        total = len(events)
        events = events[offset:offset + limit]

        return EvolutionStreamResponse(
            total=total,
            events=events
        )

    async def get_agent_performance(
        self,
        agent_type: str = "all"
    ) -> List[AgentPerformance]:
        """
        获取 Agent 性能数据

        数据来源:
        - .claude/agents/*.md (Agent 配置)
        - 模拟性能数据（实际应从数据库查询）

        Args:
            agent_type: Agent 类型筛选

        Returns:
            List[AgentPerformance]: Agent 性能列表
        """
        agents = []
        agents_dir = self.project_root / ".claude" / "agents"

        if not agents_dir.exists():
            return agents

        # 遍历所有 Agent 配置文件
        for agent_file in agents_dir.glob("*.md"):
            agent_name = agent_file.stem

            # 解析 Agent 类型
            agent_type_value = self._get_agent_type(agent_name)

            # 类型筛选
            if agent_type != "all" and agent_type_value != agent_type:
                continue

            # 模拟性能数据（实际应从数据库查询）
            # 这里使用文件修改时间和文件大小模拟数据
            mtime = datetime.fromtimestamp(agent_file.stat().st_mtime)
            file_size = agent_file.stat().st_size

            # 根据文件大小模拟任务数量
            total_tasks = min(file_size // 100, 200)
            success_rate = 0.85 + (hash(agent_name) % 15) / 100  # 0.85-1.0

            agents.append(AgentPerformance(
                name=agent_name,
                type=agent_type_value,
                current_progress=min((hash(agent_name) % 100), 100),
                status=self._get_agent_status(agent_name),
                performance=PerformanceMetrics(
                    total_tasks=total_tasks,
                    success_rate=round(success_rate, 2),
                    avg_duration_seconds=120 + (hash(agent_name) % 180),
                    last_active=mtime
                )
            ))

        return agents

    async def get_knowledge_graph(
        self,
        category: str = "all",
        search: str = ""
    ) -> KnowledgeGraphResponse:
        """
        获取知识图谱数据

        数据来源:
        - .claude/rules/*.md (策略规则)
        - .claude/project_standards.md (最佳实践)
        - .claude/skills/*/SKILL.md (技能知识)

        Args:
            category: 知识类型筛选
            search: 搜索关键词

        Returns:
            KnowledgeGraphResponse: 知识图谱响应
        """
        categories: Dict[str, List[KnowledgeItem]] = {
            "strategy": [],
            "best-practice": [],
            "template": [],
            "error-handling": []
        }

        # 1. 解析策略规则
        rules_dir = self.project_root / ".claude" / "rules"
        if rules_dir.exists():
            for rule_file in rules_dir.glob("*.md"):
                try:
                    content = rule_file.read_text(encoding="utf-8")

                    # 提取洞察
                    insight_pattern = r"### (.+?)\n\n- \*\*Agent\*\*:\s*(.+?)\n- \*\*描述\*\*:\s*(.+?)(?=\n\n|\Z)"
                    insights = re.findall(insight_pattern, content, re.DOTALL)

                    for insight_type, agent, description in insights:
                        categories["strategy"].append(KnowledgeItem(
                            id=f"kb_{uuid.uuid4().hex[:8]}",
                            title=f"{agent.strip()} - {insight_type.strip()}",
                            description=description.strip()[:200],
                            source=str(rule_file),
                            updated_at=datetime.fromtimestamp(rule_file.stat().st_mtime),
                            tags=[agent.strip(), "strategy"]
                        ))

                except Exception:
                    continue

        # 2. 解析最佳实践
        standards_file = self.project_root / ".claude" / "project_standards.md"
        if standards_file.exists():
            try:
                content = standards_file.read_text(encoding="utf-8")

                # 提取最佳实践章节
                practice_pattern = r"### (.+?)\n\n(.+?)(?=\n###|\Z)"
                practices = re.findall(practice_pattern, content, re.DOTALL)

                for title, description in practices:
                    if "最佳实践" in title or "Best Practice" in title:
                        categories["best-practice"].append(KnowledgeItem(
                            id=f"kb_{uuid.uuid4().hex[:8]}",
                            title=title.strip(),
                            description=description.strip()[:200],
                            source=str(standards_file),
                            updated_at=datetime.fromtimestamp(standards_file.stat().st_mtime),
                            tags=["best-practice"]
                        ))

            except Exception:
                pass

        # 3. 解析技能知识
        skills_dir = self.project_root / ".claude" / "skills"
        if skills_dir.exists():
            for skill_file in skills_dir.glob("*/SKILL.md"):
                try:
                    content = skill_file.read_text(encoding="utf-8")

                    # 提取技能标题和描述
                    title_match = re.search(r"# (.+)", content)
                    title = title_match.group(1).strip() if title_match else skill_file.parent.name

                    # 提取第一段作为描述
                    desc_match = re.search(r"##.+?\n\n(.+?)(?=\n##|\Z)", content, re.DOTALL)
                    description = desc_match.group(1).strip()[:200] if desc_match else ""

                    categories["template"].append(KnowledgeItem(
                        id=f"kb_{uuid.uuid4().hex[:8]}",
                        title=title,
                        description=description,
                        source=str(skill_file),
                        updated_at=datetime.fromtimestamp(skill_file.stat().st_mtime),
                        tags=["skill", "template"]
                    ))

                except Exception:
                    continue

        # 类型筛选
        if category != "all":
            filtered_categories = {category: categories.get(category, [])}
        else:
            filtered_categories = categories

        # 搜索筛选
        if search:
            for cat, items in filtered_categories.items():
                filtered_categories[cat] = [
                    item for item in items
                    if search.lower() in item.title.lower() or
                       search.lower() in item.description.lower()
                ]

        # 构建响应
        response_categories = {}
        for cat, items in filtered_categories.items():
            response_categories[cat] = KnowledgeCategory(
                count=len(items),
                items=items
            )

        return KnowledgeGraphResponse(categories=response_categories)

    def _get_agent_type(self, agent_name: str) -> str:
        """
        获取 Agent 类型

        Args:
            agent_name: Agent 名称

        Returns:
            str: Agent 类型
        """
        type_mapping = {
            "backend-developer": "developer",
            "frontend-developer": "developer",
            "code-reviewer": "reviewer",
            "test": "tester",
            "orchestrator": "orchestrator",
            "product-manager": "manager",
            "tech-lead": "lead",
            "evolver": "system",
            "progress-viewer": "system",
            "strategy-selector": "system",
            "self-play-trainer": "system"
        }
        return type_mapping.get(agent_name, "other")

    def _get_agent_status(self, agent_name: str) -> str:
        """
        获取 Agent 状态（模拟）

        Args:
            agent_name: Agent 名称

        Returns:
            str: Agent 状态
        """
        # 根据名称哈希模拟状态
        status_hash = hash(agent_name) % 4
        statuses = ["idle", "working", "completed", "idle"]
        return statuses[status_hash]
