#!/usr/bin/env python3
"""
监控系统 API 验证脚本
用途：验证所有监控 API 端点是否正常工作
"""

import asyncio
import httpx
from datetime import datetime


BASE_URL = "http://localhost:8000"


async def check_api_endpoint(client: httpx.AsyncClient, method: str, endpoint: str, description: str):
    """验证单个 API 端点"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'=' * 60}")
    print(f"📡 验证: {description}")
    print(f"   方法: {method}")
    print(f"   URL: {url}")
    print(f"{'=' * 60}")

    try:
        if method == "GET":
            response = await client.get(url, timeout=10.0)
        elif method == "POST":
            response = await client.post(url, json={}, timeout=10.0)
        else:
            print(f"❌ 不支持的方法: {method}")
            return False

        print(f"✅ 状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ 响应数据:")

            # 根据不同端点显示关键信息
            if "intelligence_score" in str(data):
                print(f"   • 智能水平: {data.get('data', {}).get('current_score', 'N/A')}")
            elif "total" in str(data):
                print(f"   • 总记录数: {data.get('data', {}).get('total', 'N/A')}")
            elif "issues" in str(data):
                issues = data.get('data', {}).get('issues', [])
                print(f"   • 发现问题: {len(issues)} 个")
            elif "agents" in str(data):
                agents = data.get('data', {}).get('agents', [])
                print(f"   • Agent 数量: {len(agents)} 个")
            elif "categories" in str(data):
                categories = data.get('data', {}).get('categories', [])
                print(f"   • 知识分类: {len(categories)} 个")

            # 显示部分响应数据
            import json
            print(f"\n   响应预览:")
            print(f"   {json.dumps(data, ensure_ascii=False, indent=2)[:500]}...")

            return True
        else:
            print(f"❌ 请求失败")
            print(f"   响应: {response.text[:200]}")
            return False

    except httpx.ConnectError:
        print(f"❌ 连接失败: 无法连接到 {BASE_URL}")
        print(f"   请确保后端服务已启动: python main/backend/main.py")
        return False
    except httpx.TimeoutException:
        print(f"❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


async def check_websocket():
    """验证 WebSocket 连接"""
    print(f"\n{'=' * 60}")
    print(f"🔌 验证: WebSocket 实时推送")
    print(f"   URL: ws://localhost:8000/ws/monitor/evolution")
    print(f"{'=' * 60}")

    try:
        import websockets

        async with websockets.connect("ws://localhost:8000/ws/monitor/evolution") as websocket:
            print("✅ WebSocket 连接成功")

            # 等待接收消息（最多 5 秒）
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"✅ 收到消息: {message[:100]}...")
                return True
            except asyncio.TimeoutError:
                print("⚠️  5 秒内未收到消息（这是正常的，因为没有新的进化事件）")
                return True

    except ImportError:
        print("⚠️  websockets 库未安装，跳过 WebSocket 验证")
        print("   安装命令: pip install websockets")
        return None
    except Exception as e:
        print(f"❌ WebSocket 连接失败: {e}")
        return False


async def main():
    """主函数"""
    print("=" * 60)
    print("🚀 监控系统 API 验证")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 验证端点列表
    endpoints = [
        ("GET", "/api/v1/monitor/intelligence-trend", "智能水平走势"),
        ("GET", "/api/v1/monitor/evolution-stream", "进化事件流"),
        ("GET", "/api/v1/monitor/diagnosis", "智能诊断结果"),
        ("GET", "/api/v1/monitor/agents", "Agent 性能数据"),
        ("GET", "/api/v1/monitor/knowledge-graph", "知识图谱"),
    ]

    results = []

    async with httpx.AsyncClient() as client:
        # 验证所有 REST API
        for method, endpoint, description in endpoints:
            success = await check_api_endpoint(client, method, endpoint, description)
            results.append((description, success))
            await asyncio.sleep(0.5)  # 避免请求过快

    # 验证 WebSocket
    ws_result = await check_websocket()
    if ws_result is not None:
        results.append(("WebSocket 实时推送", ws_result))

    # 打印验证总结
    print(f"\n{'=' * 60}")
    print("📊 验证总结")
    print(f"{'=' * 60}")

    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    for description, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {status}  {description}")

    print(f"\n总计: {success_count}/{total_count} 个验证通过")

    if success_count == total_count:
        print("\n🎉 所有验证通过！监控系统运行正常。")
    elif success_count == 0:
        print("\n❌ 所有验证失败！请检查：")
        print("   1. 后端服务是否已启动: python main/backend/main.py")
        print("   2. 数据库是否有数据: python main/backend/scripts/populate_monitor_data.py")
    else:
        print(f"\n⚠️  部分验证失败（{total_count - success_count} 个）")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    asyncio.run(main())
