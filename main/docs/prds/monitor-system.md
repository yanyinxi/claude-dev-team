# 产品需求文档：Claude Dev Team 监控中心

## 1. 概述

### 1.1 问题陈述
当前 Claude Dev Team 系统缺乏可视化监控界面，无法直观了解系统的智能水平、进化动态、Agent 性能和知识积累情况。开发者和用户需要一个实时监控中心来：
- 追踪系统智能水平的变化趋势
- 查看实时进化事件和对比详情
- 获得 AI 驱动的智能诊断和修复建议
- 监控各个 Agent 的性能和进度
- 可视化知识图谱的增长

### 1.2 解决方案描述
构建一个全面的监控中心，包含 5 个核心模块：
1. **智能水平走势图**：展示系统智能水平随时间的变化，包含学习路径里程碑
2. **实时进化动态**：事件流展示最新进化记录，支持展开查看对比详情
3. **智能诊断中心**：AI 自动分析系统问题并给出修复建议（置顶显示）
4. **Agent 性能监控**：展示各 Agent 的当前进度和历史性能数据
5. **知识图谱**：卡片式展示系统知识库，按类型分组

### 1.3 成功指标
- 监控页面加载时间 < 2 秒
- 实时数据推送延迟 < 500ms
- 智能诊断准确率 > 85%
- 用户满意度 > 4.5/5
- 页面响应流畅，无卡顿

---

## 2. 用户故事

### 2.1 开发者视角
**作为开发者**，我想查看系统智能水平的变化趋势，以便了解系统是否在持续进化和改进。

**作为开发者**，我想实时看到进化事件，以便及时发现系统学到的新知识和最佳实践。

**作为开发者**，我想获得 AI 诊断建议，以便快速定位和修复系统问题。

### 2.2 项目管理者视角
**作为项目管理者**，我想监控各 Agent 的性能，以便评估团队协作效率和识别瓶颈。

**作为项目管理者**，我想查看知识图谱，以便了解系统积累的知识资产。

---

## 3. 功能需求

### 3.1 智能水平走势图
#### 3.1.1 核心功能
- 展示智能水平随时间的变化曲线（折线图）
- 智能水平计算公式：
  ```
  智能水平 = (策略权重×0.3 + 知识丰富度×0.25 + 质量趋势×0.25 + 进化频率×0.2) × 10
  ```
- 标注学习路径里程碑（关键事件点）
- 支持时间范围筛选（最近 7 天、30 天、全部）
- 鼠标悬停显示详细数据

#### 3.1.2 数据来源
- 策略权重：从 `.claude/rules/*.md` 文件统计
- 知识丰富度：从 Agent 配置文件和 Skill 文件统计
- 质量趋势：从代码审查和测试报告统计
- 进化频率：从进化记录统计

### 3.2 实时进化动态
#### 3.2.1 核心功能
- 事件流展示最新进化记录（时间倒序）
- 每条记录显示：时间、Agent、策略类型、简要描述
- 支持展开/折叠查看详细对比
- 对比详情包括：变更前后内容、影响范围、奖励分数
- 实时推送新事件（WebSocket）

#### 3.2.2 数据来源
- 从 `.claude/rules/*.md` 文件解析进化记录
- 从 `project_standards.md` 解析进化历史

### 3.3 智能诊断中心（置顶）
#### 3.3.1 核心功能
- AI 自动分析系统问题（每小时执行一次）
- 诊断维度：
  - 性能瓶颈（慢查询、大文件、重复代码）
  - 安全风险（硬编码密钥、SQL 注入、XSS）
  - 代码质量（复杂度、测试覆盖率、文档完整性）
  - 架构问题（耦合度、依赖循环、违反规范）
- 按严重程度分级：Critical、Important、Suggestion
- 提供一键修复按钮（自动生成修复代码）
- 显示诊断时间和下次诊断倒计时

#### 3.3.2 数据来源
- 静态代码分析（Ruff、ESLint）
- 测试覆盖率报告
- 代码审查记录
- 性能监控数据

### 3.4 Agent 性能监控
#### 3.4.1 核心功能
- 展示所有 Agent 的当前进度（进度条）
- 显示历史性能数据（成功率、平均耗时、任务数）
- 支持按 Agent 类型筛选
- 点击 Agent 查看详细历史记录

#### 3.4.2 数据来源
- 从 `.claude/agents/*.md` 文件解析 Agent 信息
- 从任务执行日志统计性能数据

### 3.5 知识图谱
#### 3.5.1 核心功能
- 卡片式展示知识条目
- 按类型分组：策略规则、最佳实践、代码模板、错误处理
- 每张卡片显示：标题、描述、来源、更新时间
- 支持搜索和筛选
- 点击卡片查看完整内容

#### 3.5.2 数据来源
- 从 `.claude/rules/*.md` 文件解析策略规则
- 从 `project_standards.md` 解析最佳实践
- 从 `.claude/skills/*/SKILL.md` 文件解析技能知识

---

## 4. 非功能需求

### 4.1 性能
- 页面首次加载时间 < 2 秒
- 实时数据推送延迟 < 500ms
- 支持 1000+ 条进化记录的流畅滚动
- 图表渲染时间 < 300ms

### 4.2 安全
- 所有 API 接口需要认证（JWT Token）
- 敏感数据（密钥、密码）不在前端展示
- WebSocket 连接需要认证

### 4.3 用户体验
- 响应式设计，支持桌面和平板
- 深色模式支持
- 流畅的动画效果
- 清晰的错误提示

### 4.4 可维护性
- 代码遵循项目规范（命名、注释、目录结构）
- 组件化设计，易于扩展
- 完整的单元测试和集成测试

---

## 5. 验收标准

### 5.1 智能水平走势图
- [ ] 正确计算智能水平（公式验证）
- [ ] 折线图正确展示数据
- [ ] 里程碑标注清晰可见
- [ ] 时间范围筛选功能正常
- [ ] 鼠标悬停显示详细数据

### 5.2 实时进化动态
- [ ] 事件流按时间倒序展示
- [ ] 展开/折叠功能正常
- [ ] 对比详情正确显示
- [ ] WebSocket 实时推送正常
- [ ] 支持 1000+ 条记录流畅滚动

### 5.3 智能诊断中心
- [ ] AI 诊断自动执行（每小时）
- [ ] 问题按严重程度分级
- [ ] 一键修复功能正常
- [ ] 诊断结果准确率 > 85%
- [ ] 显示诊断时间和倒计时

### 5.4 Agent 性能监控
- [ ] 正确展示所有 Agent 进度
- [ ] 历史性能数据准确
- [ ] 筛选功能正常
- [ ] 详细历史记录可查看

### 5.5 知识图谱
- [ ] 卡片式展示清晰
- [ ] 按类型分组正确
- [ ] 搜索和筛选功能正常
- [ ] 点击查看完整内容

---

## 6. 技术考虑

### 6.1 API 端点需求
```
GET  /api/v1/monitor/intelligence-trend    # 智能水平走势数据
GET  /api/v1/monitor/evolution-stream      # 进化事件流
GET  /api/v1/monitor/diagnosis             # 智能诊断结果
POST /api/v1/monitor/diagnosis/fix         # 一键修复
GET  /api/v1/monitor/agents                # Agent 性能数据
GET  /api/v1/monitor/knowledge-graph       # 知识图谱数据
WS   /ws/monitor/evolution                 # WebSocket 实时推送
```

### 6.2 数据库变更
- 新增 `monitor_intelligence` 表（智能水平历史记录）
- 新增 `monitor_diagnosis` 表（诊断记录）
- 新增 `monitor_agent_performance` 表（Agent 性能记录）

### 6.3 第三方集成
- Chart.js 或 ECharts（图表库）
- Socket.IO 或原生 WebSocket（实时推送）
- Anthropic Claude API（智能诊断）

### 6.4 文件命名规范
#### 后端（monitor_ 开头）
- `main/backend/api/routes/monitor_router.py`
- `main/backend/services/monitor_service.py`
- `main/backend/services/monitor_intelligence.py`
- `main/backend/services/monitor_diagnosis.py`
- `main/backend/models/monitor_schema.py`

#### 前端（Monitor 开头）
- `main/frontend/pages/Monitor.vue`
- `main/frontend/components/MonitorIntelligenceChart.vue`
- `main/frontend/components/MonitorEvolutionStream.vue`
- `main/frontend/components/MonitorDiagnosis.vue`
- `main/frontend/components/MonitorAgentProgress.vue`
- `main/frontend/components/MonitorKnowledgeGraph.vue`
- `main/frontend/services/monitor.ts`
- `main/frontend/stores/monitorStore.ts`

---

## 7. 里程碑和优先级

### 7.1 P0（必须实现）
- 智能水平走势图
- 实时进化动态
- 智能诊断中心
- Agent 性能监控
- 知识图谱

### 7.2 P1（重要但可延后）
- WebSocket 实时推送
- 一键修复功能
- 深色模式

### 7.3 P2（可选）
- 导出报告功能
- 自定义仪表盘
- 移动端适配

---

## 8. 风险和依赖

### 8.1 风险
- AI 诊断准确率可能不达标（需要多次迭代优化）
- 实时推送可能存在性能瓶颈（需要压力测试）
- 数据量大时图表渲染可能卡顿（需要分页或虚拟滚动）

### 8.2 依赖
- 依赖 Anthropic Claude API（智能诊断）
- 依赖现有的 Agent 配置文件和规则文件
- 依赖后端 FastAPI 框架和前端 Vue 3 框架

---

## 9. 附录

### 9.1 参考资料
- `.claude/project_standards.md`（项目技术标准）
- `.claude/agents/*.md`（Agent 配置）
- `.claude/rules/*.md`（策略规则）

### 9.2 术语表
- **智能水平**：系统综合能力的量化指标
- **进化事件**：系统学习到新知识或最佳实践的记录
- **Agent**：执行特定任务的 AI 代理
- **知识图谱**：系统积累的知识条目集合
