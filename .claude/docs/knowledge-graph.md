# 知识图谱系统文档

> 以代码为准：本文档描述 `.claude/lib/knowledge_graph.py` 与 `.claude/lib/knowledge_retriever.py` 的当前真实能力。

## 当前能力边界
- 已实现：知识节点增删改查（库 API）、关系管理、搜索、统计、Markdown 导出
- 已实现：`knowledge_retriever.py` 的 stdin JSON 检索模式
- 未实现：`knowledge_graph.py add-node/search/stats` 这类 argparse 子命令 CLI
- 未实现：`knowledge_retriever.py --stats` 参数

---

## 快速开始

### 1) Python API
```python
from knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()

node_id = kg.add_node({
    "type": "best_practice",
    "domain": "backend",
    "title": "API-first 并行开发",
    "description": "先定义接口契约，再并行开发前后端",
    "success_rate": 0.92,
    "avg_reward": 8.5,
    "tags": ["api", "parallel"]
})

kg.add_edge(node_id, "best_practice_002", "enhances", strength=0.8)

results = kg.search_nodes("API", domain="backend")
stats = kg.get_statistics()

kg.export_to_markdown(".claude/knowledge_graph.md")
```

### 2) 检索脚本（stdin JSON）
```bash
echo '{"context":"How to improve API development","domain":"backend","top_k":5}' | \
  python3 .claude/lib/knowledge_retriever.py
```

输入 JSON 字段：
- `context`（必填）
- `domain`（可选）
- `type`（可选）
- `top_k`（可选，默认 5）

---

## 核心 API

### KnowledgeGraph
- `add_node(node: Dict) -> str`
- `add_edge(from_id, to_id, relation, strength=1.0, description="")`
- `find_node(node_id) -> Optional[Dict]`
- `update_node(node_id, updates) -> bool`
- `find_related_nodes(node_id, relation=None) -> List[Dict]`
- `search_nodes(query, domain=None, node_type=None) -> List[Dict]`
- `merge_similar_nodes(threshold=0.8) -> List[Tuple[str, str, str]]`
- `get_statistics() -> Dict`
- `export_to_markdown(output_file)`

### KnowledgeRetriever
- `retrieve_relevant_knowledge(context, domain=None, node_type=None, top_k=5)`
- `retrieve_by_domain(domain, top_k=10)`
- `retrieve_by_type(node_type, top_k=10)`
- `retrieve_related(node_id, relation=None)`
- `format_results(results, include_score=True)`

---

## 数据文件
- `.claude/knowledge_graph.json`：节点与边数据
- `.claude/knowledge_graph.md`：导出后的知识文档（按需生成）

---

## 测试与验证
```bash
# 运行 knowledge_graph.py 自带示例 main（非 argparse CLI）
python3 .claude/lib/knowledge_graph.py

# 验证检索脚本
echo '{"context":"API development","domain":"backend","top_k":3}' | \
  python3 .claude/lib/knowledge_retriever.py

# 运行集成演示
python3 .claude/tests/demo_knowledge_graph.py
```

---

## 设计原则
- 代码优先，文档追随
- 未实现能力不能写成“可直接运行命令”
- 新增能力前先评估是否直接服务当前目标

---

**更新时间**: 2026-04-19
