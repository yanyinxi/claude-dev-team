# Unknown Strategy Rules

**更新时间**: 2026-04-19
**策略关键词**: unknown

## 说明

此文件用于记录无法归类到具体 Agent 策略的洞察。
auto_evolver.py 只在检测到有实质意义的事件时才写入（失败分析、并行模式、大规模修改等），
不再记录「任务成功完成」「快速响应」等无意义的默认状态。

## 新学到的洞察

## 真实执行数据

此规则文件的统计数据不再手工编造。真实执行指标由以下机制累积：

- 每次会话结束时，`session_evolver.py` 采集 git diff / agent 调用等真实数据到 `.claude/logs/sessions.jsonl`
- `strategy_updater.py` 基于真实指标做 EMA 更新到 `.claude/strategy_weights.json`
- 查看最近会话信号：`tail -n 5 .claude/logs/sessions.jsonl`
- 查看最新策略权重：`cat .claude/strategy_weights.json`
