# Claude Dev Team - 快速参考手册

> 只保留当前代码中已实现、可直接验证的能力。

## 自动反馈与策略更新

### 核心命令
```bash
# 测试自动反馈链路（采集 + 权重更新）
bash .claude/tests/test_auto_feedback.sh

# 查看最近会话信号
tail -n 5 .claude/logs/sessions.jsonl

# 查看策略权重
cat .claude/strategy_weights.json
```

### 质量信号来源
- `session_evolver.py`: 从 git diff / agent 调用记录采集真实信号
- `strategy_updater.py`: 基于真实信号做 EMA 更新
- `auto_evolver.py`: 只记录 Subagent 调用事实

---

## AlphaZero 风格策略工具（当前实现）

### 核心命令
```bash
# 生成策略变体
python3 .claude/lib/strategy_generator.py

# 任务复杂度分析 + 推荐策略
python3 .claude/lib/strategy_generator.py "任务描述"

# 运行策略对比沙箱（当前为模拟执行）
python3 .claude/lib/parallel_executor.py

# 运行完整测试
bash .claude/tests/test-alphazero.sh
```

### 说明
- `parallel_executor.py` 当前用于**策略对比沙箱**，执行逻辑是 `_simulate_execution(...)`。
- 不会自动触发真实 subagent 执行。
- 不会自动写入 `.claude/rules/*.md`。
- `strategy_generator.py` 的推荐策略会叠加 `strategy_weights.json` 中的领域 EMA 权重（复杂度为基线，权重做一档偏置）。

---

## 知识图谱（当前实现）

### Python API 使用
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

results = kg.search_nodes("API", domain="backend")
stats = kg.get_statistics()
```

### 检索脚本使用（stdin JSON）
```bash
echo '{"context":"API development","domain":"backend","top_k":3}' | \
  python3 .claude/lib/knowledge_retriever.py
```

### 当前边界
- `knowledge_graph.py` 支持库级 API，但**未提供 argparse 子命令 CLI**（如 `add-node/search/stats`）。
- `knowledge_retriever.py` 当前不支持 `--stats` 参数。

---

## Hooks 系统

### 事件类型
- `SessionStart` - 会话开始时
- `PreToolUse` - 工具调用前
- `PostToolUse` - 工具成功后
- `Stop` - 主 agent 完成时
- `SubagentStop` - 子代理完成时
- `UserPromptSubmit` - 用户提交提示时

### 配置检查
```bash
python3 .claude/tests/verify_hook_references.py
bash .claude/tests/validate-config.sh
```

---

## Agent 系统

### 核心代理
- `strategy-selector` - 根据任务复杂度推荐策略
- `self-play-trainer` - 对比多策略并输出分析
- `orchestrator` - 协调整体执行流程

### 推荐实践
- 简单任务：直接用 `strategy-selector`
- 复杂任务：先 `strategy-selector`，再按需 `self-play-trainer`
- 高风险改动：先补测试再执行 Stop Hook 路径验证

---

## 文档与能力防漂移

### 必跑校验
```bash
python3 .claude/tests/verify_capabilities.py
python3 .claude/tests/verify_hook_references.py
python3 .claude/tests/verify_standards.py --verbose
```

### 单一事实源
- 代码是最终事实源
- 能力状态清单：`.claude/capabilities.json`
- 文档不得将 `planned/deprecated` 能力描述为“可直接运行”

---

## 目录治理与清理

### 规则文档
- `.claude/docs/directory-governance.md`

### 常用清理命令
```bash
# 一键清理运行时噪音
bash .claude/tests/cleanup-claude-artifacts.sh

# 清理缓存
find .claude -type d -name '__pycache__' -prune -exec rm -rf {} +
find .claude -name '.DS_Store' -delete

# 查看运行时日志
ls -lh .claude/logs/
```

---

## 常用路径
- `.claude/settings.json` - Hooks 与权限配置
- `.claude/strategy_weights.json` - 策略权重（Stop Hook 更新）
- `.claude/logs/sessions.jsonl` - 会话真实信号
- `.claude/logs/agent-invocations.jsonl` - Subagent 调用事实
- `.claude/knowledge_graph.json` - 知识图谱数据
- `.claude/strategy_variants.json` - 策略变体输出

---

**版本**: 3.2.0 | **更新时间**: 2026-04-19
