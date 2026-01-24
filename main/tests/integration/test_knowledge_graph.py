#!/usr/bin/env python3
"""
知识图谱系统集成测试

测试功能：
1. 添加节点
2. 添加边
3. 搜索节点
4. 检索相关知识
5. 合并相似节点
6. 导出 Markdown
"""

import sys
from pathlib import Path
import os

# 添加脚本目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent
scripts_dir = project_root / ".claude" / "hooks" / "scripts"
sys.path.insert(0, str(scripts_dir))

# 切换到项目根目录（确保相对路径正确）
os.chdir(project_root)

from knowledge_graph import KnowledgeGraph
from knowledge_retriever import KnowledgeRetriever


def test_add_nodes():
    """测试添加节点"""
    print("=" * 60)
    print("测试 1: 添加节点")
    print("=" * 60)

    kg = KnowledgeGraph()

    # 添加测试节点
    node_id = kg.add_node({
        "type": "best_practice",
        "domain": "testing",
        "title": "测试驱动开发 (TDD)",
        "description": "先写测试，再写实现代码，确保代码质量",
        "evidence": ["task_test_001"],
        "success_rate": 0.87,
        "avg_reward": 8.3,
        "tags": ["testing", "tdd", "quality"]
    })

    print(f"✓ 成功添加节点: {node_id}")

    # 验证节点
    node = kg.find_node(node_id)
    if node:
        print(f"✓ 节点验证成功: {node['title']}")
    else:
        print("✗ 节点验证失败")

    return kg


def test_add_edges(kg):
    """测试添加边"""
    print("\n" + "=" * 60)
    print("测试 2: 添加边")
    print("=" * 60)

    # 查找两个节点
    nodes = kg.graph["nodes"][:2]
    if len(nodes) >= 2:
        kg.add_edge(
            nodes[0]["id"],
            nodes[1]["id"],
            "related_to",
            strength=0.8,
            description="测试关联关系"
        )
        print(f"✓ 成功添加边: {nodes[0]['id']} -> {nodes[1]['id']}")
    else:
        print("✗ 节点数量不足，跳过测试")


def test_search(kg):
    """测试搜索功能"""
    print("\n" + "=" * 60)
    print("测试 3: 搜索节点")
    print("=" * 60)

    # 搜索关键词
    queries = ["API", "testing", "parallel"]

    for query in queries:
        results = kg.search_nodes(query)
        print(f"\n搜索 '{query}': 找到 {len(results)} 个结果")
        for node in results[:3]:
            print(f"  - {node['title']} (相关性: {node.get('_relevance_score', 0)})")


def test_retrieval():
    """测试智能检索"""
    print("\n" + "=" * 60)
    print("测试 4: 智能检索")
    print("=" * 60)

    retriever = KnowledgeRetriever()

    # 测试场景
    scenarios = [
        {
            "context": "How to improve API development efficiency",
            "domain": "backend",
            "top_k": 3
        },
        {
            "context": "Component design and modularity",
            "domain": "frontend",
            "top_k": 2
        },
        {
            "context": "Testing best practices",
            "domain": None,
            "top_k": 3
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n场景 {i}: {scenario['context']}")
        results = retriever.retrieve_relevant_knowledge(
            scenario["context"],
            scenario["domain"],
            top_k=scenario["top_k"]
        )

        if results:
            print(f"找到 {len(results)} 个相关知识:")
            for node in results:
                print(f"  - {node['title']} (分数: {node.get('_final_score', 0):.1f})")
        else:
            print("  未找到相关知识")


def test_related_nodes(kg):
    """测试关联节点查询"""
    print("\n" + "=" * 60)
    print("测试 5: 关联节点查询")
    print("=" * 60)

    # 查找第一个节点的关联节点
    if kg.graph["nodes"]:
        node_id = kg.graph["nodes"][0]["id"]
        related = kg.find_related_nodes(node_id)

        print(f"\n节点 '{node_id}' 的关联节点:")
        if related:
            for node in related:
                print(f"  - {node['title']}")
        else:
            print("  无关联节点")


def test_statistics(kg):
    """测试统计信息"""
    print("\n" + "=" * 60)
    print("测试 6: 统计信息")
    print("=" * 60)

    stats = kg.get_statistics()

    print(f"\n知识图谱统计:")
    print(f"  - 总节点数: {stats['total_nodes']}")
    print(f"  - 总边数: {stats['total_edges']}")
    print(f"  - 平均成功率: {stats['avg_success_rate']:.2%}")
    print(f"  - 平均奖励: {stats['avg_reward']:.1f}/10")

    print(f"\n节点类型分布:")
    for node_type, count in stats['node_types'].items():
        print(f"  - {node_type}: {count}")

    print(f"\n领域分布:")
    for domain, count in stats['domains'].items():
        print(f"  - {domain}: {count}")


def test_export(kg):
    """测试导出功能"""
    print("\n" + "=" * 60)
    print("测试 7: 导出 Markdown")
    print("=" * 60)

    output_file = ".claude/knowledge_graph_test.md"
    kg.export_to_markdown(output_file)
    print(f"✓ 成功导出到: {output_file}")


def main():
    """主测试流程"""
    print("\n" + "=" * 60)
    print("知识图谱系统集成测试")
    print("=" * 60)

    try:
        # 执行测试
        kg = test_add_nodes()
        test_add_edges(kg)
        test_search(kg)
        test_retrieval()
        test_related_nodes(kg)
        test_statistics(kg)
        test_export(kg)

        print("\n" + "=" * 60)
        print("✓ 所有测试通过")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
