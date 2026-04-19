# .claude 目录治理规范

> 目标：让 `.claude/` 目录更易读、可维护、可长期演进。  
> 原则：代码与配置是事实源，运行时产物不进仓库，历史文档按需保留。

## 分层模型

### 1. 核心资产（必须保留）
- `agents/`：Agent 提示词与职责边界
- `hooks/`：自动化钩子（只保留 `settings.json` 引用的脚本）
- `lib/`：可复用库模块
- `rules/`：策略规则
- `settings.json` / `project_standards.md` / `capabilities.json`

### 2. 运行时产物（不应入库）
- `.claude/logs/*.jsonl`
- `.claude/strategy_variants.json`
- `.claude/execution_results/`
- `__pycache__/`, `.DS_Store`

### 3. 历史归档（可选保留）
- `.claude/docs/history/` 下文档用于追溯背景，不作为当前实现依据
- 当目录复杂度过高时，可按时间批次归档到外部知识库

## 本次已清理项（2026-04-19）

- 删除遗留缓存：`__pycache__/`、`.DS_Store`
- 删除遗留日志：`.claude/logs/evolution-log.jsonl`
- 删除旧路径历史产物：`.claude/hooks/execution_results/`
- 统一策略变体输出路径：`.claude/strategy_variants.json`（替代 `hooks/strategy_variants.json`）

## 删除判定标准

一个文件满足任意一条即可进入“可删候选”：
- 不在 `settings.json` hooks 中被引用，且无代码调用
- 仅由历史版本写入，当前实现已替代
- 纯运行时缓存/中间结果，可由脚本重新生成
- 文档声明与代码不一致且无保留价值

## 每周治理例行命令

```bash
# 一键清理运行时噪音
bash .claude/tests/cleanup-claude-artifacts.sh

# 1) 能力声明与文档一致性
python3 .claude/tests/verify_capabilities.py

# 2) Hook 引用完整性
python3 .claude/tests/verify_hook_references.py

# 3) 配置总校验
bash .claude/tests/validate-config.sh

# 4) 清理运行时缓存
find .claude -type d -name '__pycache__' -prune -exec rm -rf {} +
find .claude -name '.DS_Store' -delete
```

## 目录维护建议

1. 新增文件前先决定类别：核心资产 / 运行产物 / 历史归档。
2. 运行产物必须配套 `.gitignore` 规则。
3. 文档里出现命令路径，必须能直接执行或明确标记“未实现”。
4. 历史文档一律放 `docs/history/`，且首段注明“非当前事实源”。
