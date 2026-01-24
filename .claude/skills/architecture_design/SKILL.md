---
name: architecture-design
description: 设计系统架构和技术方案。用于系统架构设计、技术栈选择、技术风险评估、技术决策制定。适用于新项目架构设计、技术选型、架构重构、技术方案评审等场景。
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Grep, Glob
context: fork
agent: tech-lead
---

# 架构设计技能

## 何时使用

- 设计系统架构
- 选择技术栈
- 评估技术风险
- 制定技术决策

## 项目标准

> 📖 参考 → `.claude/project_standards.md`

## 工作流程

1. **分析需求** - 理解 PRD，识别挑战
2. **架构设计** - 选择模式，定义组件
3. **技术选型** - 参考 project_standards.md
4. **API 设计** - RESTful 规范
5. **风险评估** - 识别并缓解风险

## 输出

- 技术设计 → `main/docs/tech_designs/[功能名].md`
- API 规范 → `main/docs/api/[功能名].yaml`

## 最佳实践

1. **遵循项目标准**：优先使用 project_standards.md 中定义的技术栈
2. **模块化设计**：保持组件独立，降低耦合
3. **可扩展性**：考虑未来扩展需求
4. **性能优先**：在设计阶段考虑性能瓶颈
5. **安全第一**：在架构层面考虑安全问题

## 参考资料

- 参考 @.claude/project_standards.md 获取项目技术标准
- 参考 @main/docs/tech_designs/ 查看历史技术设计

---

## 📈 进化记录（自动生成）

_此章节由 Evolver 自动更新，记录从实际任务执行中学到的经验和最佳实践。_
