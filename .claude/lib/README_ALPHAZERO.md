# AlphaZero 风格策略对比系统（当前实现）

> 本文档描述 `.claude/lib/strategy_generator.py` 与 `.claude/lib/parallel_executor.py` 的真实状态。

## 当前实现边界
- 已实现：策略变体生成（4 类变体）
- 已实现：基于关键词的复杂度评估与策略推荐
- 已实现：并发执行框架（`asyncio.gather`）
- 当前为模拟：`parallel_executor.py` 通过 `_simulate_execution(...)` 生成结果
- 未实现：直接调用 Claude Code `background_task` 做真实多 agent 执行
- 未实现：训练后自动写入 `.claude/rules/*.md`

## 组件说明

### 1) `strategy_generator.py`
```bash
python3 .claude/lib/strategy_generator.py
python3 .claude/lib/strategy_generator.py "实现用户认证系统"
```

输出内容：
- 策略变体列表（parallel_high / granular / sequential / hybrid）
- 复杂度分数（1-10）
- 推荐策略
- 变体文件：`.claude/strategy_variants.json`

### 2) `parallel_executor.py`
```bash
python3 .claude/lib/parallel_executor.py
```

输出内容：
- 4 个策略变体的模拟执行结果
- 对比分析与最佳变体
- 执行结果文件：`.claude/execution_results/execution_*.json`
- 权重更新：`.claude/strategy_weights.json`

## 与 Hook 的关系
- `parallel_executor.py` 不是 Hook 自动触发脚本，需手动调用。
- Stop Hook (`session_evolver.py` + `strategy_updater.py`) 负责真实会话信号采集与 EMA 更新。

## 推荐使用方式
1. 先用 `strategy_generator.py` 生成候选策略。
2. 需要快速预评估时，用 `parallel_executor.py` 做模拟对比。
3. 真正执行阶段，交由 orchestrator + 专业 agent 任务流。
4. 会话结束后从 `.claude/logs/sessions.jsonl` 与 `.claude/strategy_weights.json` 查看反馈。

## 常见问题

### Q: 为什么叫“并行执行器”却是模拟？
A: 当前版本用于策略评估沙箱，后续若要接入真实 subagent 并行执行，需要单独实现与测试。

### Q: 是否会自动把最佳实践写入 rules？
A: 当前不会。规则文件更新需要人工/显式脚本流程。

### Q: 如何判断哪些能力是已实现的？
A: 查看 `.claude/capabilities.json` 与 `python3 .claude/tests/verify_capabilities.py` 校验结果。

---

**更新时间**: 2026-04-19
