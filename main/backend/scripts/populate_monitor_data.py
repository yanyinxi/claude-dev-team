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
from models.db import Base, MonitorIntelligence, MonitorDiagnosis, MonitorAgentPerformance
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

        print("\n" + "=" * 60)
        print("✅ 测试数据生成完成！")
        print("=" * 60)
        print("\n📊 数据统计：")
        print("  • 智能水平记录: 28 条（最近 7 天）")
        print("  • 诊断记录: 3 条")
        print("  • Agent 性能记录: 11 条")
        print("\n🌐 现在可以访问监控页面查看数据：")
        print("  http://localhost:5173/monitor")
        print("\n💡 提示：如果前端仍显示 0.00，请点击「刷新数据」按钮")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
