#!/usr/bin/env python3
"""
监控系统测试数据生成脚本
用途：向数据库插入示例监控数据，用于测试监控页面
"""

import sys
import os
from datetime import datetime, timedelta
import asyncio

# 添加后端目录到 Python 路径
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from core.database import get_db, engine
from models.db import Base, MonitorIntelligence, MonitorDiagnosis, MonitorAgentPerformance, MonitorEvolutionEvent
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tables():
    """创建监控相关表"""
    print("📊 创建监控表...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ 表创建完成")


async def populate_intelligence_data():
    """生成智能水平历史数据（最近 7 天）"""
    print("\n📈 生成智能水平数据...")

    async for db in get_db():
        # 生成最近 7 天的数据，每天 4 个数据点
        base_date = datetime.now() - timedelta(days=7)

        for day in range(7):
            for hour in [0, 6, 12, 18]:
                timestamp = base_date + timedelta(days=day, hours=hour)

                # 模拟智能水平逐步提升（从 3.0 到 6.5）
                base_score = 3.0 + (day * 0.5)
                intelligence_score = base_score + (hour / 24.0)

                record = MonitorIntelligence(
                    timestamp=timestamp,
                    intelligence_score=round(intelligence_score, 2),
                    strategy_weight=round(0.3 + (day * 0.02), 2),
                    knowledge_richness=round(0.4 + (day * 0.03), 2),
                    quality_trend=round(0.7 + (day * 0.04), 2),
                    evolution_frequency=round(0.1 + (day * 0.01), 2),
                    milestone_event=f"Day {day + 1} Progress" if hour == 12 else None
                )
                db.add(record)

        await db.commit()
        print(f"✅ 已生成 {7 * 4} 条智能水平记录")
        break


async def populate_diagnosis_data():
    """生成诊断数据"""
    print("\n🔍 生成诊断数据...")

    async for db in get_db():
        # 先删除已存在的诊断记录（避免唯一约束冲突）
        from sqlalchemy import delete
        await db.execute(delete(MonitorDiagnosis))
        await db.commit()

        # 示例诊断记录 1：性能问题
        diagnosis1 = MonitorDiagnosis(
            issue_id="DIAG-001",
            diagnosis_time=datetime.now() - timedelta(hours=2),
            category="performance",
            severity="important",
            title="数据库查询性能优化",
            description="检测到 3 个慢查询，平均响应时间超过 500ms",
            suggestion="建议添加索引：users(email), questions(module, difficulty)",
            auto_fixable=True,
            fix_code="ALTER TABLE users ADD INDEX idx_email (email);"
        )
        db.add(diagnosis1)

        # 示例诊断记录 2：代码质量
        diagnosis2 = MonitorDiagnosis(
            issue_id="DIAG-002",
            diagnosis_time=datetime.now() - timedelta(hours=1),
            category="quality",
            severity="suggestion",
            title="代码复杂度过高",
            description="monitor_service.py 中的 get_evolution_stream 函数复杂度为 15，建议拆分",
            suggestion="将函数拆分为多个小函数，每个函数职责单一",
            auto_fixable=False
        )
        db.add(diagnosis2)

        # 示例诊断记录 3：架构建议
        diagnosis3 = MonitorDiagnosis(
            issue_id="DIAG-003",
            diagnosis_time=datetime.now() - timedelta(minutes=30),
            category="architecture",
            severity="suggestion",
            title="缓存策略优化",
            description="智能水平计算频繁调用，建议添加缓存",
            suggestion="使用 Redis 缓存智能水平计算结果，TTL 设置为 5 分钟",
            auto_fixable=False
        )
        db.add(diagnosis3)

        await db.commit()
        print("✅ 已生成 3 条诊断记录")
        break


async def populate_agent_performance_data():
    """生成 Agent 性能数据"""
    print("\n🤖 生成 Agent 性能数据...")

    async for db in get_db():
        # Agent 列表：(agent_name, agent_type, avg_duration_seconds)
        agents = [
            ("orchestrator", "orchestrator", 45),
            ("product-manager", "manager", 32),
            ("tech-lead", "architect", 38),
            ("frontend-developer", "developer", 52),
            ("backend-developer", "developer", 48),
            ("test", "tester", 28),
            ("code-reviewer", "reviewer", 15),
            ("evolver", "evolver", 12),
            ("progress-viewer", "viewer", 5),
            ("strategy-selector", "selector", 22),
            ("self-play-trainer", "trainer", 65),
        ]

        task_counter = 1
        for agent_name, agent_type, duration_seconds in agents:
            # 为每个 Agent 创建一个已完成的任务记录
            started_at = datetime.now() - timedelta(seconds=duration_seconds)
            completed_at = datetime.now()

            record = MonitorAgentPerformance(
                agent_name=agent_name,
                agent_type=agent_type,
                task_id=f"TASK-{task_counter:03d}",
                status="completed",
                progress=100,
                duration_seconds=duration_seconds,
                success=True,
                error_message=None,
                started_at=started_at,
                completed_at=completed_at
            )
            db.add(record)
            task_counter += 1

        await db.commit()
        print(f"✅ 已生成 {len(agents)} 个 Agent 的性能记录")
        break


async def populate_evolution_events():
    """生成进化事件测试数据（最近 30 天）"""
    print("\n🧬 生成进化事件数据...")

    async for db in get_db():
        # 先删除已存在的进化事件（避免唯一约束冲突）
        from sqlalchemy import delete
        await db.execute(delete(MonitorEvolutionEvent))
        await db.commit()

        # 定义测试数据模板
        event_templates = [
            {
                "agent": "backend-developer",
                "strategy": "api-design",
                "description": "优化 API 端点设计，统一使用 RESTful 风格",
                "reward": 8.5,
                "diff_before": "使用混合的 API 风格，部分端点不符合 REST 规范",
                "diff_after": "所有 API 端点统一使用 RESTful 风格，资源命名用复数",
                "diff_impact": "API 一致性提升 40%，前端对接效率提高 30%"
            },
            {
                "agent": "frontend-developer",
                "strategy": "component-design",
                "description": "组件拆分优化，提高代码复用率",
                "reward": 9.0,
                "diff_before": "大型组件包含过多逻辑，难以维护",
                "diff_after": "拆分为多个小组件，每个组件职责单一",
                "diff_impact": "代码复用率提升 50%，维护成本降低 35%"
            },
            {
                "agent": "test",
                "strategy": "testing",
                "description": "添加集成测试，覆盖关键业务流程",
                "reward": 8.8,
                "diff_before": "只有单元测试，缺少集成测试",
                "diff_after": "添加集成测试，覆盖用户登录、答题、进度统计等关键流程",
                "diff_impact": "测试覆盖率提升至 85%，Bug 发现率提高 60%"
            },
            {
                "agent": "code-reviewer",
                "strategy": "code-quality",
                "description": "引入代码质量检查工具，自动化审查",
                "reward": 7.5,
                "diff_before": "手动代码审查，效率低且容易遗漏",
                "diff_after": "使用 Ruff 自动检查代码质量，配置 pre-commit hook",
                "diff_impact": "代码审查效率提升 70%，代码质量问题减少 45%"
            },
            {
                "agent": "orchestrator",
                "strategy": "collaboration",
                "description": "优化前后端并行开发流程",
                "reward": 9.2,
                "diff_before": "前后端串行开发，效率低",
                "diff_after": "先定义 API 契约，前后端并行开发",
                "diff_impact": "开发效率提升 50%，交付周期缩短 40%"
            },
            {
                "agent": "backend-developer",
                "strategy": "database",
                "description": "数据库查询优化，添加索引",
                "reward": 8.0,
                "diff_before": "慢查询导致 API 响应时间超过 500ms",
                "diff_after": "添加索引，优化查询语句",
                "diff_impact": "API 响应时间降低至 50ms，性能提升 10 倍"
            },
            {
                "agent": "frontend-developer",
                "strategy": "state-management",
                "description": "优化状态管理，减少不必要的渲染",
                "reward": 7.8,
                "diff_before": "全局状态变化导致大量组件重新渲染",
                "diff_after": "使用 Pinia 模块化状态管理，精确控制渲染范围",
                "diff_impact": "页面渲染性能提升 60%，用户体验显著改善"
            },
            {
                "agent": "evolver",
                "strategy": "system-evolution",
                "description": "自动提炼最佳实践到规则库",
                "reward": 9.5,
                "diff_before": "最佳实践散落在各处，难以复用",
                "diff_after": "自动从执行结果中提炼最佳实践，更新到规则库",
                "diff_impact": "知识复用率提升 80%，系统智能水平持续提升"
            },
            {
                "agent": "strategy-selector",
                "strategy": "strategy-selection",
                "description": "引入 AlphaZero 策略选择机制",
                "reward": 9.8,
                "diff_before": "手动选择策略，效率低且容易出错",
                "diff_after": "使用 AlphaZero 自博弈学习，自动选择最优策略",
                "diff_impact": "策略选择准确率提升至 95%，任务成功率提高 40%"
            },
            {
                "agent": "backend-developer",
                "strategy": "error-handling",
                "description": "统一错误处理机制",
                "reward": 8.3,
                "diff_before": "错误响应格式不统一，前端难以处理",
                "diff_after": "使用 AppException 及其子类，统一错误响应格式",
                "diff_impact": "错误处理一致性提升 100%，前端开发效率提高 25%"
            }
        ]

        # 生成最近 30 天的进化事件
        base_date = datetime.now() - timedelta(days=30)
        event_counter = 1

        for day in range(30):
            # 每天生成 1-3 个事件
            events_per_day = (day % 3) + 1

            for i in range(events_per_day):
                # 循环使用模板
                template = event_templates[(event_counter - 1) % len(event_templates)]

                # 计算事件时间（随机分布在当天）
                hour = (i * 8) % 24
                timestamp = base_date + timedelta(days=day, hours=hour)

                # 创建事件记录
                event = MonitorEvolutionEvent(
                    event_id=f"EVT-{event_counter:04d}",
                    timestamp=timestamp,
                    agent=template["agent"],
                    strategy=template["strategy"],
                    description=template["description"],
                    reward=int(template["reward"] * 10),  # 转换为整数 (0-100)
                    diff_before=template.get("diff_before"),
                    diff_after=template.get("diff_after"),
                    diff_impact=template.get("diff_impact")
                )
                db.add(event)
                event_counter += 1

        await db.commit()
        print(f"✅ 已生成 {event_counter - 1} 条进化事件记录（最近 30 天）")
        break


async def main():
    """主函数"""
    print("=" * 60)
    print("🚀 监控系统测试数据生成器")
    print("=" * 60)

    try:
        # 1. 创建表
        await create_tables()

        # 2. 生成智能水平数据
        await populate_intelligence_data()

        # 3. 生成诊断数据
        await populate_diagnosis_data()

        # 4. 生成 Agent 性能数据
        await populate_agent_performance_data()

        # 5. 生成进化事件数据
        await populate_evolution_events()

        print("\n" + "=" * 60)
        print("✅ 测试数据生成完成！")
        print("=" * 60)
        print("\n📊 数据统计：")
        print("  • 智能水平记录: 28 条（最近 7 天）")
        print("  • 诊断记录: 3 条")
        print("  • Agent 性能记录: 11 条")
        print("  • 进化事件记录: ~60 条（最近 30 天）")
        print("\n🌐 现在可以访问监控页面查看数据：")
        print("  http://localhost:5173/monitor")
        print("\n💡 提示：如果前端仍显示 0.00，请点击「刷新数据」按钮")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
