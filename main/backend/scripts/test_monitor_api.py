#!/usr/bin/env python3
"""
监控系统 API 测试脚本
用途：测试监控系统的各个 API 端点是否正常工作
"""

import asyncio
import httpx
from datetime import datetime

# API 基础 URL
BASE_URL = "http://localhost:8000/api/v1/monitor"


async def test_intelligence_trend():
    """测试智能水平走势 API"""
    print("\n📊 测试智能水平走势 API...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/intelligence-trend?days=7")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功！获取到 {len(data['trend'])} 条智能水平记录")
            print(f"   当前智能水平: {data['trend'][-1]['intelligence_score']:.2f}")
        else:
            print(f"❌ 失败！状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")


async def test_evolution_stream():
    """测试进化事件流 API"""
    print("\n🧬 测试进化事件流 API...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/evolution-stream?limit=10&offset=0")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功！获取到 {data['total']} 条进化事件（显示前 10 条）")
            if data['events']:
                print(f"   最新事件: {data['events'][0]['description'][:50]}...")
                print(f"   Agent: {data['events'][0]['agent']}")
                print(f"   奖励: {data['events'][0]['reward']:.1f}/10")
            else:
                print("   ⚠️ 警告：没有进化事件数据，请运行 populate_monitor_data.py 生成测试数据")
        else:
            print(f"❌ 失败！状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")


async def test_diagnosis():
    """测试智能诊断 API"""
    print("\n🔍 测试智能诊断 API...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/diagnosis")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功！发现 {len(data['issues'])} 个问题")
            for issue in data['issues']:
                print(f"   - [{issue['severity']}] {issue['title']}")
        else:
            print(f"❌ 失败！状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")


async def test_agents():
    """测试 Agent 性能 API"""
    print("\n🤖 测试 Agent 性能 API...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/agents?agent_type=all")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功！获取到 {len(data['agents'])} 个 Agent 的性能数据")
            for agent in data['agents'][:3]:
                print(f"   - {agent['name']}: {agent['status']} (成功率: {agent['performance']['success_rate']:.0%})")
        else:
            print(f"❌ 失败！状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")


async def test_knowledge_graph():
    """测试知识图谱 API"""
    print("\n📚 测试知识图谱 API...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/knowledge-graph?category=all")
        if response.status_code == 200:
            data = response.json()
            total_items = sum(cat['count'] for cat in data['categories'].values())
            print(f"✅ 成功！获取到 {total_items} 条知识条目")
            for cat_name, cat_data in data['categories'].items():
                print(f"   - {cat_name}: {cat_data['count']} 条")
        else:
            print(f"❌ 失败！状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")


async def main():
    """主函数"""
    print("=" * 60)
    print("🚀 监控系统 API 测试")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API 地址: {BASE_URL}")

    try:
        # 测试各个 API 端点
        await test_intelligence_trend()
        await test_evolution_stream()
        await test_diagnosis()
        await test_agents()
        await test_knowledge_graph()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        print("\n💡 提示：")
        print("  1. 如果进化事件流没有数据，请运行: python scripts/populate_monitor_data.py")
        print("  2. 访问监控页面: http://localhost:5173/monitor")
        print("  3. 查看 API 文档: http://localhost:8000/docs")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
