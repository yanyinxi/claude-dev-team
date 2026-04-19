# .claude/lib/ - Agent 可调用库

此目录的模块不是自动执行的 hook，而是**给 agent 或 skill 按需调用的 Python 库代码**。

## 可用模块

| 模块 | 用途 | 谁会调用 |
|------|------|----------|
| `parallel_executor.py` | 并行执行多个 agent 任务 | orchestrator |
| `strategy_generator.py` | 生成策略变体（自博弈） | self-play-trainer |
| `quality_evaluator.py` | 对特定产出评分 | code-reviewer |
| `knowledge_graph.py` | 构建/查询知识图谱 | evolver, orchestrator |
| `knowledge_retriever.py` | 从 .claude/rules/ 检索经验 | 所有 agent |

## 使用方式

Agent/Skill 在自己的 prompt 或工作流里通过 Bash 工具显式调用：

```bash
python3 .claude/lib/knowledge_retriever.py --domain backend --query "API design"
```

## 与 hooks/ 的区别

- **`.claude/hooks/`** — Claude Code 在特定事件（PreToolUse、Stop 等）**自动**执行的脚本
- **`.claude/lib/`** — 不自动执行，只在 agent 明确调用时运行

## 为什么分开

早期这些库代码放在 `hooks/scripts/` 下，导致两个混淆：
1. 看起来像 hook 脚本，但 `settings.json` 从未引用它们
2. 未来维护者以为它们是自动系统的一部分，浪费时间研究

明确分离后，职责清晰：hooks 是"系统主动行为"，lib 是"agent 工具箱"。
