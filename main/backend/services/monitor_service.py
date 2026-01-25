"""
监控系统 - 通用监控服务

功能：
1. 解析进化事件流（从数据库读取）
2. 统计 Agent 性能
3. 解析知识图谱
4. 提供数据查询接口

数据来源：
- monitor_evolution_events 表（进化事件）
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
    EvolutionDiff,
    EvolutionStreamResponse,
    AgentPerformance,
    PerformanceMetrics,
    KnowledgeItem,
    KnowledgeCategory,
    KnowledgeGraphResponse
)
from models.db import MonitorEvolutionEvent
from core.database import get_db
from sqlalchemy import select, desc


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

        数据来源: monitor_evolution_events 表

        Args:
            limit: 每页数量
            offset: 偏移量

        Returns:
            EvolutionStreamResponse: 进化事件流响应
        """
        events = []

        # 从数据库读取进化事件
        async for db in get_db():
            # 查询总数
            count_query = select(MonitorEvolutionEvent)
            result = await db.execute(count_query)
            all_events = result.scalars().all()
            total = len(all_events)

            # 查询分页数据（按时间倒序）
            query = (
                select(MonitorEvolutionEvent)
                .order_by(desc(MonitorEvolutionEvent.timestamp))
                .limit(limit)
                .offset(offset)
            )
            result = await db.execute(query)
            db_events = result.scalars().all()

            # 转换为 Pydantic 模型
            for db_event in db_events:
                # 构建 diff 对象（如果有）
                diff = None
                if db_event.diff_before and db_event.diff_after:
                    diff = EvolutionDiff(
                        before=db_event.diff_before,
                        after=db_event.diff_after,
                        impact=db_event.diff_impact or ""
                    )

                events.append(EvolutionEvent(
                    id=db_event.event_id,
                    timestamp=db_event.timestamp,
                    agent=db_event.agent,
                    strategy=db_event.strategy,
                    description=db_event.description,
                    reward=db_event.reward / 10.0,  # 转换回 0-10 范围
                    diff=diff
                ))

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
