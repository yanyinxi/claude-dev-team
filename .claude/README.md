# .claude 目录结构说明

> Claude Dev Team 配置目录。代码为唯一事实源，文档必须追随代码。

## 目录结构（核心）

```text
.claude/
├── agents/                    # 专业 agent 提示词
├── docs/                      # 文档与快速参考
├── hooks/
│   ├── path_validator.py      # PreToolUse(Write|Edit)
│   └── scripts/
│       ├── setup_env.sh
│       ├── safety-check.sh
│       ├── quality-gate.sh
│       ├── context-enhancer.sh
│       ├── auto_evolver.py    # SubagentStop: 记录 agent 调用事实
│       ├── session_evolver.py # Stop: 采集真实会话指标
│       └── strategy_updater.py# Stop: EMA 更新策略权重
├── lib/                       # 按需调用的工具库（非 Hook 自动执行）
│   ├── strategy_generator.py
│   ├── parallel_executor.py   # 当前为策略对比沙箱（模拟执行）
│   ├── knowledge_graph.py
│   ├── knowledge_retriever.py
│   ├── quality_evaluator.py
│   └── show_evolution.py
├── rules/                     # 策略规则文档
├── tests/                     # .claude 基础设施测试脚本
├── logs/
│   ├── sessions.jsonl
│   └── agent-invocations.jsonl
├── execution_results/         # 手动运行 parallel_executor 后生成
├── settings.json
├── settings.local.json
├── project_standards.md
├── knowledge_graph.json
├── strategy_variants.json
├── strategy_weights.json
└── capabilities.json          # 能力状态清单（implemented/planned/deprecated）
```

## 核心事实

### 1) Hooks 的真实职责
- `auto_evolver.py`: 只记录 Subagent 调用事实
- `session_evolver.py`: 采集真实 git 与协作信号
- `strategy_updater.py`: 基于真实信号更新策略权重

### 2) AlphaZero 相关模块的当前状态
- `strategy_generator.py`: 已实现，推荐策略会读取 `strategy_weights.json` 的领域 EMA 权重做一档偏置
- `parallel_executor.py`: 已实现“策略对比沙箱”，但执行结果来自模拟逻辑
- 自动写入 `rules/*.md`: 当前未实现

### 3) 知识图谱相关模块的当前状态
- `knowledge_graph.py`: 已实现库 API
- `knowledge_retriever.py`: 已实现 stdin JSON 检索
- `knowledge_graph.py add-node/search/stats` 命令行子命令：当前未实现
- `knowledge_retriever.py --stats`：当前未实现

## 常用命令

```bash
# 清理运行时噪音文件
bash .claude/tests/cleanup-claude-artifacts.sh

# Hook 引用校验
python3 .claude/tests/verify_hook_references.py

# 能力声明与代码一致性校验
python3 .claude/tests/verify_capabilities.py

# 配置校验
bash .claude/tests/validate-config.sh

# project_standards 校验
python3 .claude/tests/verify_standards.py --verbose
```

## 维护原则
- 代码是单一事实源。
- 文档中出现“可运行命令”必须可验证。
- `planned/deprecated` 能力不得写成已实现。
- 任何偏差优先修正文档，再评估是否真的需要补实现。

## 防漂移机制
- 能力清单：`.claude/capabilities.json`
- 自动校验：`.claude/tests/verify_capabilities.py`
- CI 门禁：`.github/workflows/ci.yml`
- PR 清单：`.github/pull_request_template.md`

## 目录治理
- 治理规范：`.claude/docs/directory-governance.md`
- 运行产物（logs / strategy_variants / execution_results）默认不入库
- 历史文档统一放在 `.claude/docs/history/`

---

**版本**: 3.2.0 | **更新时间**: 2026-04-19
