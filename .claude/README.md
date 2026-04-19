# .claude 目录结构说明

> Claude Dev Team v3.0 配置目录 - 完全 LLM 驱动的智能协作系统

## 📁 目录结构

```
.claude/
├── agents/                    # 11 个专业代理配置
│   ├── backend-developer.md
│   ├── code-reviewer.md
│   ├── evolver.md
│   ├── frontend-developer.md
│   ├── orchestrator.md
│   ├── product-manager.md
│   ├── progress-viewer.md
│   ├── self-play-trainer.md
│   ├── strategy-selector.md
│   ├── tech-lead.md
│   └── test.md
│
├── skills/                    # 6 个可复用技能
│   ├── ai_daily_digest/
│   ├── api_design/
│   ├── architecture_design/
│   ├── code_quality/
│   ├── llm-driven-collaboration/
│   ├── requirement_analysis/
│   ├── task_distribution/
│   ├── testing/
│   ├── README.md
│   └── REFACTORING_SUMMARY.md
│
├── rules/                     # 5 个策略规则文件
│   ├── backend.md             # 后端开发规则 (main/backend/**/*.py)
│   ├── collaboration.md       # 协作策略规则 (全局)
│   ├── frontend.md            # 前端开发规则 (main/frontend/**/*.{vue,ts,js})
│   ├── general.md             # 通用开发规则 (全局)
│   └── system-design.md       # 系统设计规则 (全局)
│
├── hooks/                     # Hooks 系统
│   ├── scripts/               # 可执行脚本
│   │   ├── auto_evolver.py              # 自动进化脚本 (8.0KB)
│   │   ├── context-enhancer.sh          # 上下文增强脚本
│   │   ├── knowledge_graph.py           # 知识图谱核心模块 (16KB)
│   │   ├── knowledge_retriever.py       # 知识检索模块 (7.4KB)
│   │   ├── parallel_executor.py         # 并行执行器 (13KB)
│   │   ├── quality-gate.sh              # 质量检查脚本
│   │   ├── quality_evaluator.py         # 质量评估模块 (6.3KB)
│   │   ├── README_ALPHAZERO.md          # AlphaZero 系统文档 (10KB)
│   │   ├── safety-check.sh              # 安全检查脚本
│   │   ├── setup_env.sh                 # 环境设置脚本
│   │   ├── strategy_generator.py        # 策略生成器 (9.4KB)
│   │   ├── strategy_updater.py          # 策略更新器 (5.8KB)
│   │   └── session_evolver.py           # 会话进化记录脚本
│   │
│   ├── execution_results/     # 执行结果历史
│   │   └── execution_*.json
│   │
│   ├── path_validator.py      # 路径验证器
│   ├── strategy_variants.json # 策略变体配置
│   └── strategy_weights.json  # 策略权重（hooks 目录）
│
├── docs/                      # 文档目录（整理后）
│   ├── claude-code-reference.md         # Claude Code 通用规范
│   ├── hooks-design.md                  # Hooks 设计文档
│   ├── hooks-unification-completed.md   # Hooks 统一完成报告
│   ├── hooks-verification-unification.md # Hooks 验证统一
│   ├── implementation-summary.md        # 实现总结
│   ├── knowledge-graph.md               # 知识图谱完整文档（合并）
│   ├── quick-reference.md               # 快速参考手册（合并）
│   ├── stop-hook-fix.md                 # Stop Hook 修复
│   └── verify-standards-analysis.md     # 标准验证分析
│
├── tests/                     # 测试脚本
│   ├── llm-driven-tests.md
│   └── validate-config.sh
│
├── settings.json              # 主配置文件（带中文注释）
├── settings.local.json        # 本地配置（不提交到 Git）
├── strategy_weights.json      # 策略权重（根目录，带中文注释）
├── knowledge_graph.json       # 知识图谱数据
└── project_standards.md       # 项目技术标准
```

## 📊 文件统计

| 类别 | 数量 | 说明 |
|------|------|------|
| **Agents** | 11 | 专业代理配置文件 |
| **Skills** | 8 | 可复用技能（含 README） |
| **Rules** | 5 | 策略规则文件 |
| **Hooks Scripts** | 24 | 可执行脚本和测试 |
| **Docs** | 9 | 整理后的文档 |
| **Config** | 4 | 配置文件（settings, weights, knowledge_graph, project_standards） |

## 🎯 核心配置文件

### 1. settings.json
- **用途**: 主配置文件
- **内容**: 权限、Hooks、模型、LLM 驱动配置
- **特点**: 已添加完整中文注释

### 2. strategy_weights.json
- **用途**: 策略权重配置
- **更新**: 自动更新（EMA, alpha=0.3）
- **特点**: 已添加完整中文注释

### 3. knowledge_graph.json
- **用途**: 知识图谱数据存储
- **内容**: 节点、边、统计信息
- **更新**: 自动更新

### 4. project_standards.md
- **用途**: 项目技术标准（单一事实来源）
- **内容**: 路径配置、命名约定、API 规范、最佳实践
- **特点**: 支持自动进化

## 📚 文档整理说明

### 合并的文档

| 原文件 | 合并到 | 说明 |
|--------|--------|------|
| `QUICK_REFERENCE.md` | `docs/quick-reference.md` | 快速参考手册 |
| `KNOWLEDGE_GRAPH_QUICKREF.md` | `docs/quick-reference.md` | 知识图谱快速参考 |
| `hooks/scripts/QUICK_REFERENCE.md` | `docs/quick-reference.md` | AlphaZero 快速参考 |
| `knowledge_graph.md` | `docs/knowledge-graph.md` | 知识图谱文档 |
| `knowledge_graph_demo.md` | `docs/knowledge-graph.md` | 知识图谱演示 |
| `knowledge_graph_test.md` | `docs/knowledge-graph.md` | 知识图谱测试 |
| `hooks/scripts/README_KNOWLEDGE_GRAPH.md` | `docs/knowledge-graph.md` | 知识图谱 README |
| `AUTO_FEEDBACK_SYSTEM.md` | 已删除 | 内容已整合到 quick-reference.md |
| `README.md` | 已删除 | 内容已整合到其他文档 |
| `hooks/scripts/IMPLEMENTATION_SUMMARY.md` | 保留原位置 | AlphaZero 实现总结 |
| `hooks/scripts/README.md` | 已删除 | 内容已整合 |

### 优化效果

- **文件数量减少**: 从 70+ 个文件减少到 60+ 个文件
- **文档集中**: 所有文档统一放在 `docs/` 目录
- **中文注释**: 配置文件添加完整中文注释
- **Token 优化**: 合并重复内容，减少 token 使用

## 🔧 使用指南

### 快速查询
```bash
# 查看快速参考
cat .claude/docs/quick-reference.md

# 查看知识图谱
cat .claude/docs/knowledge-graph.md

# 查看配置文件
cat .claude/settings.json
```

### 测试命令
```bash
# 测试所有 Hooks
bash .claude/tests/test-all-hooks.sh

# 测试 AlphaZero 系统
bash .claude/tests/test-alphazero.sh

# 验证项目标准
python3 .claude/tests/verify_standards.py --verbose
```

### 配置修改
- **权限配置**: 修改 `.claude/settings.json` 的 `permissions` 部分
- **Hooks 配置**: 修改 `.claude/settings.json` 的 `hooks` 部分
- **策略权重**: 自动更新，无需手动修改

## 📝 维护说明

### 自动更新的文件
- `strategy_weights.json` - 策略权重（每次任务执行后）
- `knowledge_graph.json` - 知识图谱（新增经验时）
- `rules/*.md` - 策略规则（Evolver 自动更新）

### 需要手动维护的文件
- `settings.json` - 权限和 Hooks 配置
- `project_standards.md` - 项目技术标准（路径配置需人工审核）
- `agents/*.md` - 代理配置（重大变更需人工审核）

## 🎉 整理完成

- ✅ 文档已整理归类
- ✅ 配置文件已添加中文注释
- ✅ 重复文件已合并
- ✅ Token 使用已优化
- ✅ 目录结构清晰规范

---

**版本**: 3.0.0 | **整理时间**: 2026-01-24 | **状态**: ✅ 完成
