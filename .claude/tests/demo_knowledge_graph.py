#!/usr/bin/env python3
"""
知识图谱系统演示脚本

展示如何在实际场景中使用知识图谱系统
"""

import sys
from pathlib import Path

# 添加脚本目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_graph import KnowledgeGraph
from knowledge_retriever import KnowledgeRetriever


def demo_scenario_1():
    """场景 1: 新任务开始前 - 检索相关经验"""
    print("\n" + "=" * 60)
    print("场景 1: 新任务开始前 - 检索相关经验")
    print("=" * 60)

    print("\n任务描述: 实现用户认证 API，支持 JWT Token")

    retriever = KnowledgeRetriever()

    # 检索相关经验
    results = retriever.retrieve_relevant_knowledge(
        context="API authentication JWT token backend",
        domain="backend",
        top_k=3
    )

    if results:
        print("\n📚 找到以下相关经验：\n")
        for i, node in enumerate(results, 1):
            print(f"{i}. {node['title']}")
            print(f"   描述: {node['description']}")
            print(f"   成功率: {node.get('success_rate', 0):.0%}")
            print(f"   平均奖励: {node.get('avg_reward', 0):.1f}/10")
            print(f"   相关性分数: {node.get('_final_score', 0):.1f}")
            print()
    else:
        print("\n未找到相关经验")


def demo_scenario_2():
    """场景 2: 任务完成后 - 添加新经验"""
    print("\n" + "=" * 60)
    print("场景 2: 任务完成后 - 添加新经验")
    print("=" * 60)

    print("\n任务结果: 成功实现 JWT 认证，奖励 9.0/10")

    kg = KnowledgeGraph()

    # 添加新的最佳实践
    node_id = kg.add_node({
        "type": "best_practice",
        "domain": "backend",
        "title": "JWT Token 无状态认证",
        "description": "使用 JWT 实现无状态认证，提高系统可扩展性和性能",
        "evidence": ["task_auth_jwt_001"],
        "success_rate": 1.0,
        "avg_reward": 9.0,
        "tags": ["auth", "jwt", "security", "stateless"]
    })

    print(f"\n✓ 成功添加新经验: {node_id}")

    # 添加关联关系
    api_first_node = kg.search_nodes("API-first", domain="backend")
    if api_first_node:
        kg.add_edge(
            from_id=node_id,
            to_id=api_first_node[0]["id"],
            relation="enhances",
            strength=0.85,
            description="JWT 认证增强 API 安全性"
        )
        print(f"✓ 添加关联关系: {node_id} -> {api_first_node[0]['id']}")


def demo_scenario_3():
    """场景 3: 代码审查 - 查找改进建议"""
    print("\n" + "=" * 60)
    print("场景 3: 代码审查 - 查找改进建议")
    print("=" * 60)

    print("\n审查内容: 检查 API 错误处理是否规范")

    kg = KnowledgeGraph()

    # 搜索改进建议
    results = kg.search_nodes("error", node_type="improvement")

    if results:
        print("\n⚠️ 找到以下改进建议：\n")
        for node in results:
            print(f"- {node['title']}")
            print(f"  {node['description']}")
            print(f"  成功率: {node.get('success_rate', 0):.0%}")
            print()
    else:
        print("\n未找到相关改进建议")


def demo_scenario_4():
    """场景 4: 知识图谱维护 - 合并相似节点"""
    print("\n" + "=" * 60)
    print("场景 4: 知识图谱维护 - 合并相似节点")
    print("=" * 60)

    kg = KnowledgeGraph()

    print(f"\n合并前节点数: {len(kg.graph['nodes'])}")

    # 执行合并
    merged = kg.merge_similar_nodes(threshold=0.85)

    if merged:
        print(f"\n✓ 合并了 {len(merged)} 对相似节点:")
        for old1, old2, new in merged:
            print(f"  - {old1} + {old2} -> {new}")
    else:
        print("\n未发现需要合并的相似节点")

    print(f"\n合并后节点数: {len(kg.graph['nodes'])}")


def demo_scenario_5():
    """场景 5: 统计分析 - 查看知识图谱概况"""
    print("\n" + "=" * 60)
    print("场景 5: 统计分析 - 查看知识图谱概况")
    print("=" * 60)

    kg = KnowledgeGraph()
    stats = kg.get_statistics()

    print("\n📊 知识图谱统计:")
    print(f"  - 总节点数: {stats['total_nodes']}")
    print(f"  - 总边数: {stats['total_edges']}")
    print(f"  - 平均成功率: {stats['avg_success_rate']:.2%}")
    print(f"  - 平均奖励: {stats['avg_reward']:.1f}/10")

    print("\n📈 节点类型分布:")
    for node_type, count in sorted(stats['node_types'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {node_type}: {count}")

    print("\n🌍 领域分布:")
    for domain, count in sorted(stats['domains'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {domain}: {count}")


def demo_scenario_6():
    """场景 6: 导出文档 - 生成知识库"""
    print("\n" + "=" * 60)
    print("场景 6: 导出文档 - 生成知识库")
    print("=" * 60)

    kg = KnowledgeGraph()

    output_file = ".claude/knowledge_graph_demo.md"
    kg.export_to_markdown(output_file)

    print(f"\n✓ 成功导出知识图谱到: {output_file}")
    print("  可以使用 Markdown 阅读器查看完整的知识库")


def main():
    """运行所有演示场景"""
    print("\n" + "=" * 60)
    print("知识图谱系统演示")
    print("=" * 60)

    try:
        demo_scenario_1()  # 检索相关经验
        demo_scenario_2()  # 添加新经验
        demo_scenario_3()  # 查找改进建议
        demo_scenario_4()  # 合并相似节点
        demo_scenario_5()  # 统计分析
        demo_scenario_6()  # 导出文档

        print("\n" + "=" * 60)
        print("✓ 演示完成")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
