#!/usr/bin/env python3
"""
知识图谱核心模块 - 管理项目经验的节点和关联关系

功能：
1. 知识节点的 CRUD 操作
2. 关联关系管理
3. 相似节点自动合并
4. 智能搜索和检索
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import re


class KnowledgeGraph:
    """知识图谱管理类"""

    def __init__(self, graph_file: str = ".claude/knowledge_graph.json"):
        """
        初始化知识图谱

        Args:
            graph_file: 知识图谱数据文件路径
        """
        self.graph_file = Path(graph_file)
        self.graph = self._load_graph()

    def _load_graph(self) -> Dict:
        """
        加载知识图谱数据

        Returns:
            dict: 包含 nodes 和 edges 的图谱数据
        """
        if self.graph_file.exists():
            try:
                with open(self.graph_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Failed to load {self.graph_file}, creating new graph")
                return {"nodes": [], "edges": []}
        return {"nodes": [], "edges": []}

    def _save_graph(self):
        """保存知识图谱到文件"""
        self.graph_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.graph_file, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, indent=2, ensure_ascii=False)

    def add_node(self, node: Dict) -> str:
        """
        添加知识节点

        Args:
            node: 节点数据，必须包含 type 字段

        Returns:
            str: 节点 ID
        """
        # 生成节点 ID
        node_id = node.get("id") or f"{node['type']}_{len(self.graph['nodes']) + 1:03d}"
        node["id"] = node_id
        node["created_at"] = node.get("created_at") or datetime.now().isoformat()
        node["updated_at"] = datetime.now().isoformat()

        # 检查是否已存在
        existing = self.find_node(node_id)
        if existing:
            self.update_node(node_id, node)
        else:
            self.graph["nodes"].append(node)
            self._save_graph()

        return node_id

    def add_edge(self, from_id: str, to_id: str, relation: str, strength: float = 1.0, description: str = ""):
        """
        添加关联关系

        Args:
            from_id: 源节点 ID
            to_id: 目标节点 ID
            relation: 关系类型（如 depends_on, similar_to, conflicts_with）
            strength: 关系强度（0-1）
            description: 关系描述
        """
        # 检查节点是否存在
        if not self.find_node(from_id) or not self.find_node(to_id):
            print(f"Warning: Node {from_id} or {to_id} not found")
            return

        # 检查是否已存在相同关系
        for edge in self.graph["edges"]:
            if edge["from"] == from_id and edge["to"] == to_id and edge["relation"] == relation:
                # 更新现有关系
                edge["strength"] = strength
                edge["description"] = description
                self._save_graph()
                return

        # 添加新关系
        edge = {
            "from": from_id,
            "to": to_id,
            "relation": relation,
            "strength": strength,
            "description": description
        }
        self.graph["edges"].append(edge)
        self._save_graph()

    def find_node(self, node_id: str) -> Optional[Dict]:
        """
        查找节点

        Args:
            node_id: 节点 ID

        Returns:
            dict: 节点数据，如果不存在返回 None
        """
        for node in self.graph["nodes"]:
            if node["id"] == node_id:
                return node
        return None

    def update_node(self, node_id: str, updates: Dict) -> bool:
        """
        更新节点

        Args:
            node_id: 节点 ID
            updates: 更新的字段

        Returns:
            bool: 是否更新成功
        """
        for node in self.graph["nodes"]:
            if node["id"] == node_id:
                node.update(updates)
                node["updated_at"] = datetime.now().isoformat()
                self._save_graph()
                return True
        return False

    def find_related_nodes(self, node_id: str, relation: Optional[str] = None) -> List[Dict]:
        """
        查找相关节点

        Args:
            node_id: 节点 ID
            relation: 关系类型（可选，不指定则返回所有关系）

        Returns:
            list: 相关节点列表
        """
        related_ids = []
        for edge in self.graph["edges"]:
            if edge["from"] == node_id:
                if relation is None or edge["relation"] == relation:
                    related_ids.append(edge["to"])

        return [self.find_node(nid) for nid in related_ids if self.find_node(nid)]

    def search_nodes(self, query: str, domain: Optional[str] = None, node_type: Optional[str] = None) -> List[Dict]:
        """
        搜索节点

        Args:
            query: 搜索关键词
            domain: 领域过滤（如 backend, frontend）
            node_type: 节点类型过滤（如 best_practice, improvement）

        Returns:
            list: 匹配的节点列表，按相关性排序
        """
        results = []
        query_lower = query.lower()

        for node in self.graph["nodes"]:
            # 域过滤
            if domain and node.get("domain") != domain:
                continue

            # 类型过滤
            if node_type and node.get("type") != node_type:
                continue

            # 文本匹配
            score = 0
            if query_lower in node.get("title", "").lower():
                score += 10
            if query_lower in node.get("description", "").lower():
                score += 5

            # 标签匹配
            tags = node.get("tags", [])
            if any(query_lower in tag.lower() for tag in tags):
                score += 8

            if score > 0:
                node_copy = node.copy()
                node_copy["_relevance_score"] = score
                results.append(node_copy)

        # 按相关性和成功率排序
        results.sort(key=lambda x: (x.get("_relevance_score", 0), x.get("success_rate", 0)), reverse=True)
        return results

    def merge_similar_nodes(self, threshold: float = 0.8) -> List[Tuple[str, str, str]]:
        """
        合并相似节点

        Args:
            threshold: 相似度阈值（0-1）

        Returns:
            list: 合并记录列表 [(old_id1, old_id2, new_id), ...]
        """
        merged_records = []
        nodes_to_remove = set()

        for i, node1 in enumerate(self.graph["nodes"]):
            if node1["id"] in nodes_to_remove:
                continue

            for node2 in self.graph["nodes"][i + 1:]:
                if node2["id"] in nodes_to_remove:
                    continue

                # 计算相似度
                similarity = self._calculate_similarity(node1, node2)

                if similarity > threshold:
                    # 合并节点
                    merged_node = self._merge_nodes(node1, node2)
                    new_id = self.add_node(merged_node)

                    # 更新边的引用
                    self._update_edge_references(node1["id"], new_id)
                    self._update_edge_references(node2["id"], new_id)

                    # 标记待删除
                    nodes_to_remove.add(node1["id"])
                    nodes_to_remove.add(node2["id"])

                    merged_records.append((node1["id"], node2["id"], new_id))
                    break

        # 删除旧节点
        for node_id in nodes_to_remove:
            self._remove_node(node_id)

        return merged_records

    def _calculate_similarity(self, node1: Dict, node2: Dict) -> float:
        """
        计算两个节点的相似度

        Args:
            node1: 节点1
            node2: 节点2

        Returns:
            float: 相似度（0-1）
        """
        # 标题相似度
        title_sim = self._text_similarity(node1.get("title", ""), node2.get("title", ""))

        # 描述相似度
        desc_sim = self._text_similarity(node1.get("description", ""), node2.get("description", ""))

        # 领域相同性
        domain_match = 1.0 if node1.get("domain") == node2.get("domain") else 0.0

        # 类型相同性
        type_match = 1.0 if node1.get("type") == node2.get("type") else 0.0

        # 加权平均
        similarity = (title_sim * 0.4 + desc_sim * 0.3 + domain_match * 0.2 + type_match * 0.1)

        return similarity

    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        计算文本相似度（基于词汇重叠）

        Args:
            text1: 文本1
            text2: 文本2

        Returns:
            float: 相似度（0-1）
        """
        if not text1 or not text2:
            return 0.0

        # 分词（简单实现：按空格和标点分割）
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))

        if not words1 or not words2:
            return 0.0

        # Jaccard 相似度
        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _merge_nodes(self, node1: Dict, node2: Dict) -> Dict:
        """
        合并两个节点

        Args:
            node1: 节点1
            node2: 节点2

        Returns:
            dict: 合并后的节点
        """
        merged = node1.copy()

        # 合并证据
        evidence1 = node1.get("evidence", [])
        evidence2 = node2.get("evidence", [])
        merged["evidence"] = list(set(evidence1 + evidence2))

        # 合并标签
        tags1 = node1.get("tags", [])
        tags2 = node2.get("tags", [])
        merged["tags"] = list(set(tags1 + tags2))

        # 计算平均成功率
        sr1 = node1.get("success_rate", 0)
        sr2 = node2.get("success_rate", 0)
        merged["success_rate"] = (sr1 + sr2) / 2

        # 计算平均奖励
        ar1 = node1.get("avg_reward", 0)
        ar2 = node2.get("avg_reward", 0)
        merged["avg_reward"] = (ar1 + ar2) / 2

        # 合并描述（取较长的）
        desc1 = node1.get("description", "")
        desc2 = node2.get("description", "")
        merged["description"] = desc1 if len(desc1) > len(desc2) else desc2

        # 生成新 ID
        merged["id"] = f"{merged['type']}_merged_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return merged

    def _update_edge_references(self, old_id: str, new_id: str):
        """
        更新边的节点引用

        Args:
            old_id: 旧节点 ID
            new_id: 新节点 ID
        """
        for edge in self.graph["edges"]:
            if edge["from"] == old_id:
                edge["from"] = new_id
            if edge["to"] == old_id:
                edge["to"] = new_id

    def _remove_node(self, node_id: str):
        """
        删除节点及其相关边

        Args:
            node_id: 节点 ID
        """
        # 删除节点
        self.graph["nodes"] = [n for n in self.graph["nodes"] if n["id"] != node_id]

        # 删除相关边
        self.graph["edges"] = [
            e for e in self.graph["edges"]
            if e["from"] != node_id and e["to"] != node_id
        ]

        self._save_graph()

    def get_statistics(self) -> Dict:
        """
        获取知识图谱统计信息

        Returns:
            dict: 统计信息
        """
        stats = {
            "total_nodes": len(self.graph["nodes"]),
            "total_edges": len(self.graph["edges"]),
            "node_types": {},
            "domains": {},
            "avg_success_rate": 0.0,
            "avg_reward": 0.0
        }

        # 统计节点类型
        for node in self.graph["nodes"]:
            node_type = node.get("type", "unknown")
            stats["node_types"][node_type] = stats["node_types"].get(node_type, 0) + 1

            domain = node.get("domain", "unknown")
            stats["domains"][domain] = stats["domains"].get(domain, 0) + 1

        # 计算平均值
        if self.graph["nodes"]:
            total_sr = sum(n.get("success_rate", 0) for n in self.graph["nodes"])
            total_ar = sum(n.get("avg_reward", 0) for n in self.graph["nodes"])
            stats["avg_success_rate"] = total_sr / len(self.graph["nodes"])
            stats["avg_reward"] = total_ar / len(self.graph["nodes"])

        return stats

    def export_to_markdown(self, output_file: str):
        """
        导出知识图谱为 Markdown 文档

        Args:
            output_file: 输出文件路径
        """
        lines = ["# 知识图谱\n\n"]

        # 统计信息
        stats = self.get_statistics()
        lines.append("## 统计信息\n\n")
        lines.append(f"- 总节点数: {stats['total_nodes']}\n")
        lines.append(f"- 总边数: {stats['total_edges']}\n")
        lines.append(f"- 平均成功率: {stats['avg_success_rate']:.2%}\n")
        lines.append(f"- 平均奖励: {stats['avg_reward']:.1f}/10\n\n")

        # 按类型分组节点
        nodes_by_type = {}
        for node in self.graph["nodes"]:
            node_type = node.get("type", "unknown")
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)

        # 输出节点
        for node_type, nodes in sorted(nodes_by_type.items()):
            lines.append(f"## {node_type.replace('_', ' ').title()}\n\n")

            for node in sorted(nodes, key=lambda x: x.get("success_rate", 0), reverse=True):
                lines.append(f"### {node.get('title', 'Untitled')}\n\n")
                lines.append(f"- **ID**: {node['id']}\n")
                lines.append(f"- **领域**: {node.get('domain', 'N/A')}\n")
                lines.append(f"- **描述**: {node.get('description', 'N/A')}\n")
                lines.append(f"- **成功率**: {node.get('success_rate', 0):.2%}\n")
                lines.append(f"- **平均奖励**: {node.get('avg_reward', 0):.1f}/10\n")

                evidence = node.get("evidence", [])
                if evidence:
                    lines.append(f"- **证据**: {', '.join(evidence)}\n")

                tags = node.get("tags", [])
                if tags:
                    lines.append(f"- **标签**: {', '.join(tags)}\n")

                lines.append("\n")

        # 写入文件
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)


# 使用示例
if __name__ == "__main__":
    kg = KnowledgeGraph()

    # 添加示例节点
    node_id = kg.add_node({
        "type": "best_practice",
        "domain": "backend",
        "title": "API-first 并行开发",
        "description": "先定义接口契约，再并行开发前后端",
        "evidence": ["task_123"],
        "success_rate": 0.92,
        "avg_reward": 8.5,
        "tags": ["api", "parallel", "efficiency"]
    })

    print(f"Added node: {node_id}")

    # 搜索节点
    results = kg.search_nodes("API", domain="backend")
    print(f"\nSearch results: {len(results)} nodes found")
    for node in results:
        print(f"- {node['title']} (relevance: {node.get('_relevance_score', 0)})")

    # 统计信息
    stats = kg.get_statistics()
    print(f"\nStatistics:")
    print(f"- Total nodes: {stats['total_nodes']}")
    print(f"- Total edges: {stats['total_edges']}")
    print(f"- Avg success rate: {stats['avg_success_rate']:.2%}")

    # 导出为 Markdown
    kg.export_to_markdown(".claude/knowledge_graph.md")
    print("\nExported to .claude/knowledge_graph.md")

