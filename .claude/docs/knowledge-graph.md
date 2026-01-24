# 知识图谱系统完整文档

> 基于图结构的项目经验管理和智能检索系统

## 📊 当前统计

- **总节点数**: 6
- **总边数**: 4
- **平均成功率**: 90.33%
- **平均奖励**: 8.5/10

---

## 🚀 快速开始

### 安装

无需安装，直接使用 Python 3.10+ 即可。

### 基本使用

```python
from knowledge_graph import KnowledgeGraph

# 创建知识图谱
kg = KnowledgeGraph()

# 添加节点
node_id = kg.add_node({
    "type": "best_practice",
    "domain": "backend",
    "title": "API-first 并行开发",
    "description": "先定义接口契约，再并行开发前后端",
    "success_rate": 0.92,
    "avg_reward": 8.5,
    "tags": ["api", "parallel"]
})

# 搜索节点
results = kg.search_nodes("API")

# 导出文档
kg.export_to_markdown(".claude/knowledge_graph.md")
```

### 智能检索

```python
from knowledge_retriever import KnowledgeRetriever

retriever = KnowledgeRetriever()

# 基于上下文检索
results = retriever.retrieve_relevant_knowledge(
    context="How to improve API development",
    domain="backend",
    top_k=5
)

# 格式化输出
print(retriever.format_results(results))
```

### 命令行使用

```bash
# 添加节点
python3 .claude/hooks/scripts/knowledge_graph.py add-node \
  --type best_practice \
  --content "API-First 并行开发" \
  --tags "backend,collaboration"

# 搜索节点
python3 .claude/hooks/scripts/knowledge_graph.py search \
  --query "并行开发" \
  --type best_practice

# 添加关系
python3 .claude/hooks/scripts/knowledge_graph.py add-edge \
  --from node_001 \
  --to node_002 \
  --type "depends_on"

# 查看统计
python3 .claude/hooks/scripts/knowledge_graph.py stats
```

---

## 📚 核心概念

### 节点类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `best_practice` | 最佳实践 | API-first 并行开发 |
| `improvement` | 改进建议 | 统一错误处理格式 |
| `collaboration` | 协作模式 | 前后端并行开发 |
| `system_design` | 系统设计 | 三层防护体系 |
| `pitfall` | 常见陷阱 | 过度使用 Pinia |
| `anti_pattern` | 反模式 | 业务逻辑写在路由层 |
| `lesson_learned` | 经验教训 | 数据库连接池配置不当 |
| `innovation` | 创新想法 | 智能任务分解 |
| `tool` | 工具/技术 | FastAPI, Vue 3 |
| `pattern` | 设计模式 | CRUD 模板 |

### 关系类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `depends_on` | 依赖关系 | A 依赖 B |
| `enables` | 使能关系 | A 使能 B |
| `enhances` | 增强关系 | A 增强 B |
| `conflicts_with` | 冲突关系 | A 与 B 冲突 |
| `similar_to` | 相似关系 | A 类似 B |
| `alternative_to` | 替代关系 | A 可替代 B |
| `evolved_from` | 进化关系 | A 从 B 进化而来 |

---

## 🎯 功能特性

- ✅ 知识节点的 CRUD 操作
- ✅ 关联关系管理（依赖、增强、冲突等）
- ✅ 智能搜索和检索
- ✅ 相似节点自动合并
- ✅ 多维度相关性计算
- ✅ Markdown 导出
- ✅ 统计分析

---

## 📁 文件结构

```
.claude/
├── knowledge_graph.json           # 数据存储
└── hooks/scripts/
    ├── knowledge_graph.py         # 核心模块 (16KB)
    └── knowledge_retriever.py     # 检索模块 (7.4KB)

main/
├── docs/
│   ├── knowledge_graph_guide.md        # 使用指南
│   └── knowledge_graph_implementation.md  # 实现总结
└── tests/integration/
    └── test_knowledge_graph.py    # 集成测试 (5.6KB)
```

---

## 🧪 测试

```bash
# 运行集成测试
python3 main/tests/integration/test_knowledge_graph.py

# 测试核心模块
python3 .claude/hooks/scripts/knowledge_graph.py

# 测试检索功能
echo '{"context": "API development", "domain": "backend", "top_k": 3}' | \
  python3 .claude/hooks/scripts/knowledge_retriever.py
```

---

## 📖 当前知识库

### Best Practice (最佳实践)

#### 1. API-first 并行开发
- **ID**: best_practice_001
- **领域**: backend
- **描述**: 先定义接口契约，再并行开发前后端，提升开发效率
- **成功率**: 92.00%
- **平均奖励**: 8.5/10
- **证据**: task_alarm_clock, task_speed_quiz
- **标签**: api, parallel, efficiency, collaboration

#### 2. 组件拆分策略
- **ID**: best_practice_002
- **领域**: frontend
- **描述**: 将复杂组件拆分为多个小组件，提高可维护性和复用性
- **成功率**: 88.00%
- **平均奖励**: 8.2/10
- **证据**: task_alarm_management
- **标签**: component, modularity, reusability

### Collaboration (协作模式)

#### 1. 前后端并行开发模式
- **ID**: collaboration_001
- **领域**: general
- **描述**: 前后端开发者同时工作，通过接口契约协调，效率提升 30%
- **成功率**: 90.00%
- **平均奖励**: 8.8/10
- **证据**: task_alarm_clock, task_speed_quiz
- **标签**: collaboration, parallel, efficiency

### Improvement (改进建议)

#### 1. 统一错误处理格式
- **ID**: improvement_001
- **领域**: backend
- **描述**: 所有 API 应使用标准 ErrorResponse 格式，提高一致性
- **成功率**: 85.00%
- **平均奖励**: 7.8/10
- **证据**: code_review_001
- **标签**: error-handling, consistency, api

### System Design (系统设计)

#### 1. 三层防护体系
- **ID**: system_design_001
- **领域**: general
- **描述**: 文档化（被动教育）+ 自动执行（主动防护）+ 快速参考（辅助查询）
- **成功率**: 95.00%
- **平均奖励**: 9.5/10
- **证据**: path_validator_hook
- **标签**: architecture, documentation, automation

---

## 🔧 高级功能

### 相似节点合并

```python
# 自动合并相似度 > 0.8 的节点
merged = kg.merge_similar_nodes(threshold=0.8)
```

### 关联查询

```python
# 查找依赖节点
depends = kg.find_related_nodes("node_id", relation="depends_on")
```

### 统计分析

```python
stats = kg.get_statistics()
print(f"Total nodes: {stats['total_nodes']}")
print(f"Avg success rate: {stats['avg_success_rate']:.2%}")
```

---

## 🔗 与 Hooks 集成

### PreToolUse Hook

在任务开始前检索相关经验，注入到提示中。

### PostToolUse Hook

在任务完成后，将成功经验添加到知识图谱。

---

## 📚 相关文档

- [使用指南](../../main/docs/knowledge_graph_guide.md) - 详细的使用说明
- [实现总结](../../main/docs/knowledge_graph_implementation.md) - 实现细节
- [快速参考](quick-reference.md#知识图谱系统) - 快速查询

---

**版本**: 1.0.0 | **状态**: ✅ 完成 | **更新时间**: 2026-01-24
