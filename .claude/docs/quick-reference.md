# Claude Dev Team - 快速参考手册

> 所有核心功能的快速查询指南

## 自动反馈系统

### 核心命令
```bash
# 测试自动反馈系统
bash .claude/hooks/scripts/test_auto_feedback.sh

# 查看策略权重
cat .claude/strategy_weights.json
```

### 质量评分维度
- **效率** (25%): 任务完成速度
- **代码质量** (30%): 代码规范和可维护性
- **测试覆盖率** (25%): 测试完整性
- **文档完整性** (20%): 文档质量

### 权重更新机制
```
新权重 = 0.3 × 本次得分 + 0.7 × 历史权重
```

---

## AlphaZero 自博弈学习系统

### 核心命令
```bash
# 生成策略变体
python3 .claude/hooks/scripts/strategy_generator.py

# 分析任务并推荐策略
python3 .claude/hooks/scripts/strategy_generator.py "任务描述"

# 运行自博弈训练
python3 .claude/hooks/scripts/parallel_executor.py

# 运行完整测试
bash .claude/hooks/scripts/test-alphazero.sh
```

### 4 种策略变体

| 变体 | 并行度 | 适用场景 | Agent 数量 |
|------|--------|---------|-----------|
| **parallel_high** | 高 | 独立任务多 | 5 |
| **granular** | 中 | 需要精细控制 | 3 |
| **sequential** | 低 | 强依赖任务 | 1 |
| **hybrid** | 自适应 | 复杂任务 | 3 |

### 复杂度映射

| 复杂度 | 推荐策略 |
|--------|---------|
| 1-3 (简单) | sequential |
| 4-6 (中等) | granular |
| 7-8 (复杂) | hybrid |
| 9-10 (超复杂) | parallel_high |

### Agent 调用
```python
# 策略选择
Task(agent="strategy-selector", prompt="分析任务: ...")

# 自博弈训练
Task(agent="self-play-trainer", prompt="对比策略: ...")
```

---

## 知识图谱系统

### 核心命令
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

### 节点类型
- `best_practice` - 最佳实践
- `anti_pattern` - 反模式
- `lesson_learned` - 经验教训
- `innovation` - 创新想法
- `tool` - 工具/技术
- `pattern` - 设计模式

### 关系类型
- `depends_on` - 依赖关系
- `conflicts_with` - 冲突关系
- `enhances` - 增强关系
- `alternative_to` - 替代关系
- `evolved_from` - 进化关系

---

## Hooks 系统

### 事件类型
- `SessionStart` - 会话开始时
- `PreToolUse` - 工具调用前
- `PostToolUse` - 工具成功后
- `Stop` - 主 agent 完成时
- `SubagentStop` - 子代理完成时
- `UserPromptSubmit` - 用户提交提示时

### 配置示例
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/path_validator.py"
      }]
    }]
  }
}
```

---

## Agent 系统

### 11 个专业代理

| 代理 | 触发词 | 模型 |
|------|--------|------|
| **strategy-selector** | 策略选择、智能分配 | opus |
| **self-play-trainer** | 自博弈、多策略对比 | opus |
| **orchestrator** | 协调、管理流程 | opus |
| **product-manager** | 需求分析、PRD | sonnet |
| **tech-lead** | 架构设计、技术选型 | sonnet |
| **frontend-developer** | 前端、UI、组件 | sonnet |
| **backend-developer** | 后端、API、数据库 | sonnet |
| **test** | 测试、测试计划 | sonnet |
| **code-reviewer** | 代码审查、PR 审查 | sonnet |
| **evolver** | 进化、学习、改进 | sonnet |
| **progress-viewer** | 进度、状态 | haiku |

### Agent 调用
```python
# 前台任务
result = Task(agent="backend-developer", prompt="实现用户认证 API")

# 后台任务（并行执行）
t1 = background_task(agent="frontend-developer", prompt="实现登录页面")
t2 = background_task(agent="backend-developer", prompt="实现登录 API")
r1 = background_output(task_id=t1)
r2 = background_output(task_id=t2)
```

---

## Skills 系统

### 6 个可复用技能

| Skill | 用途 | Agent |
|-------|------|-------|
| **requirement-analysis** | 需求分析和 PRD 生成 | product-manager |
| **architecture-design** | 系统架构设计 | tech-lead |
| **api-design** | RESTful API 设计 | tech-lead |
| **testing** | 测试规划和执行 | test |
| **code-quality** | 代码质量审查 | code-reviewer |
| **task-distribution** | 任务拆分和分配 | tech-lead |

### Skill 调用
```python
# 通过 Skill 工具调用
Skill(skill="requirement-analysis", args="用户认证系统")

# 通过斜杠命令调用
/requirement-analysis 用户认证系统
```

---

## Rules 系统

### 5 个策略规则文件

| 文件 | 适用路径 | 关键词 |
|------|---------|--------|
| **backend.md** | `main/backend/**/*.py` | backend, api, database |
| **frontend.md** | `main/frontend/**/*.{vue,ts,js}` | frontend, vue, components |
| **collaboration.md** | 全局 | collaboration, orchestration |
| **system-design.md** | 全局 | system-design, architecture |
| **general.md** | 全局 | general |

---

## 常用命令

### 测试命令
```bash
# 测试所有 Hooks
bash .claude/hooks/scripts/test-all-hooks.sh

# 测试 AlphaZero 系统
bash .claude/hooks/scripts/test-alphazero.sh

# 测试自动反馈系统
bash .claude/hooks/scripts/test_auto_feedback.sh

# 验证项目标准
python3 .claude/hooks/scripts/verify_standards.py --verbose
```

### 配置文件
- `.claude/settings.json` - 主配置文件（权限、Hooks）
- `.claude/settings.local.json` - 本地配置（不提交到 Git）
- `.claude/strategy_weights.json` - 策略权重（自动更新）
- `.claude/knowledge_graph.json` - 知识图谱数据

---

## 文件结构

```
.claude/
├── agents/              # 11 个专业代理配置
├── skills/              # 6 个可复用技能
├── rules/               # 5 个策略规则文件
├── hooks/               # Hooks 系统
│   ├── scripts/         # 可执行脚本
│   ├── execution_results/  # 执行结果历史
│   ├── strategy_variants.json  # 策略变体配置
│   └── strategy_weights.json   # 策略权重
├── docs/                # 文档目录
├── tests/               # 测试脚本
├── settings.json        # 主配置文件
├── strategy_weights.json  # 策略权重（根目录）
├── knowledge_graph.json   # 知识图谱数据
└── project_standards.md   # 项目技术标准
```

---

**版本**: 3.0.0 | **更新时间**: 2026-01-24
