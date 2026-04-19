# Claude Dev Team Skills

本目录包含所有可复用的技能（Skills），每个技能都符合 Agent Skills 开放标准。

## 技能列表

| 技能名称 | 描述 | 关联 Agent | 用户可调用 |
|---------|------|-----------|-----------|
| requirement-analysis | 需求分析和 PRD 生成 | product-manager | ✅ |
| architecture-design | 系统架构设计 | tech-lead | ✅ |
| api-design | RESTful API 设计 | tech-lead | ✅ |
| testing | 测试用例设计和执行 | test | ✅ |
| code-quality | 代码质量审查 | code-reviewer | ✅ |
| task-distribution | 任务分配和工作量估算 | orchestrator | ✅ |

## 技能标准格式

每个技能都包含以下元数据：

```yaml
---
name: skill-name                    # 技能名称
description: 详细描述               # Claude 用于决策何时使用
disable-model-invocation: false    # 是否禁用自动调用
user-invocable: true               # 用户是否可以手动调用
allowed-tools: Read, Write, ...    # 允许使用的工具
context: fork                      # 执行上下文（fork = 子代理）
agent: agent-name                  # 关联的专门代理
---
```

## 目录结构

每个技能目录包含：

```
skill_name/
├── SKILL.md           # 技能定义（必需）
├── examples/          # 示例文件
└── templates/         # 模板文件
```

## 使用方式

### 1. 自动调用

Claude 会根据任务需求自动选择合适的技能：

```
用户: "请分析这个需求并生成 PRD"
→ Claude 自动调用 requirement-analysis 技能
```

### 2. 手动调用

用户可以通过菜单或命令手动调用技能：

```bash
/skill requirement-analysis
```

### 3. 在 Agent 中调用

Agent 可以通过 Skill 工具调用其他技能：

```python
# 在 product-manager agent 中
skill("requirement-analysis", prompt="分析用户登录需求")
```

## 技能开发指南

### 创建新技能

1. 创建技能目录：
```bash
mkdir -p .claude/skills/new_skill/{examples,templates}
```

2. 创建 SKILL.md 文件，包含标准元数据

3. 添加示例和模板文件

4. 在 README.md 中注册新技能

### 技能最佳实践

1. **清晰的描述**：description 字段应该详细说明技能的用途和适用场景
2. **工具限制**：使用 allowed-tools 限制技能可以使用的工具
3. **上下文隔离**：使用 context: fork 在子代理中运行，避免污染主上下文
4. **关联 Agent**：指定专门的 agent，确保技能由合适的角色执行
5. **提供模板**：在 templates/ 目录提供可复用的模板文件
6. **添加示例**：在 examples/ 目录提供实际使用示例

## 技能进化

每个技能的 SKILL.md 文件末尾都有「进化记录」章节，由维护者按需更新：

```markdown
## 📈 进化记录（手动维护）

_此章节由维护者按需更新，记录从实际任务执行中学到的经验和最佳实践。_
```

## 参考资料

- Agent Skills 开放标准：https://docs.anthropic.com/claude/docs/agent-skills
- Claude Code 文档：https://docs.anthropic.com/claude-code
- 项目技术标准：@.claude/project_standards.md
