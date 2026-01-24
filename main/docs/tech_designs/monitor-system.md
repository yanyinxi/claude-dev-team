# 技术设计文档：Claude Dev Team 监控中心

## 1. 概述

### 1.1 设计目标
构建一个实时监控中心，提供系统智能水平追踪、进化动态展示、AI 智能诊断、Agent 性能监控和知识图谱可视化功能。

### 1.2 技术选型理由
- **前端**：Vue 3 + TypeScript + ECharts（符合项目标准，组件化设计）
- **后端**：FastAPI + SQLAlchemy（异步高性能，符合项目标准）
- **实时通信**：原生 WebSocket（轻量级，无需额外依赖）
- **图表库**：ECharts（功能强大，性能优秀，中文文档完善）
- **AI 诊断**：Anthropic Claude API（项目已集成）

### 1.3 核心指标
- 页面加载时间 < 2 秒
- WebSocket 推送延迟 < 500ms
- 图表渲染时间 < 300ms
- 支持 1000+ 条记录流畅滚动

---

## 2. 系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      前端层 (Vue 3)                          │
├─────────────────────────────────────────────────────────────┤
│  Monitor.vue (主页面)                                        │
│  ├─ MonitorIntelligenceChart.vue (智能水平走势图)            │
│  ├─ MonitorDiagnosis.vue (智能诊断中心 - 置顶)              │
│  ├─ MonitorEvolutionStream.vue (实时进化动态)               │
│  ├─ MonitorAgentProgress.vue (Agent 性能监控)               │
│  └─ MonitorKnowledgeGraph.vue (知识图谱)                    │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    后端层 (FastAPI)                          │
├─────────────────────────────────────────────────────────────┤
│  API 路由层 (monitor_router.py)                              │
│  ├─ GET  /api/v1/monitor/intelligence-trend                 │
│  ├─ GET  /api/v1/monitor/evolution-stream                   │
│  ├─ GET  /api/v1/monitor/diagnosis                          │
│  ├─ POST /api/v1/monitor/diagnosis/fix                      │
│  ├─ GET  /api/v1/monitor/agents                             │
│  ├─ GET  /api/v1/monitor/knowledge-graph                    │
│  └─ WS   /ws/monitor/evolution                              │
├─────────────────────────────────────────────────────────────┤
│  业务逻辑层 (Services)                                       │
│  ├─ monitor_intelligence.py (智能水平计算)                  │
│  ├─ monitor_diagnosis.py (AI 诊断服务)                      │
│  └─ monitor_service.py (通用监控服务)                       │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    数据层 (SQLite)                           │
├─────────────────────────────────────────────────────────────┤
│  - monitor_intelligence (智能水平历史)                       │
│  - monitor_diagnosis (诊断记录)                             │
│  - monitor_agent_performance (Agent 性能)                   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  文件系统 (配置文件)                         │
├─────────────────────────────────────────────────────────────┤
│  - .claude/agents/*.md (Agent 配置)                         │
│  - .claude/rules/*.md (策略规则)                            │
│  - .claude/skills/*/SKILL.md (技能知识)                     │
│  - .claude/project_standards.md (最佳实践)                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 前端框架 | Vue 3 | 3.x | UI 框架 |
| 类型系统 | TypeScript | 5.x | 类型安全 |
| 状态管理 | Pinia | 2.x | 全局状态 |
| 图表库 | ECharts | 5.x | 数据可视化 |
| HTTP 客户端 | Axios | 1.x | API 请求 |
| 后端框架 | FastAPI | 0.100+ | Web 框架 |
| ORM | SQLAlchemy | 2.x | 数据库操作 |
| 数据验证 | Pydantic | 2.x | 数据模型 |
| 数据库 | SQLite | 3.x | 数据存储 |
| AI 服务 | Anthropic Claude | API | 智能诊断 |


---

## 3. API 设计

### 3.1 REST API 接口

#### 3.1.1 获取智能水平走势数据

```http
GET /api/v1/monitor/intelligence-trend?days=7
```

**请求参数**:
- `days` (可选): 时间范围，默认 7 天，可选 7/30/all

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "trend": [
      {
        "timestamp": "2026-01-20T10:00:00Z",
        "intelligence_score": 7.5,
        "strategy_weight": 0.8,
        "knowledge_richness": 0.7,
        "quality_trend": 0.75,
        "evolution_frequency": 0.6
      }
    ],
    "milestones": [
      {
        "timestamp": "2026-01-18T15:30:00Z",
        "event": "新增 AlphaZero 自博弈学习系统",
        "intelligence_score": 8.2
      }
    ]
  }
}
```


#### 3.1.2 获取进化事件流

```http
GET /api/v1/monitor/evolution-stream?limit=50&offset=0
```

**请求参数**:
- `limit` (可选): 每页数量，默认 50
- `offset` (可选): 偏移量，默认 0

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 1234,
    "events": [
      {
        "id": "evt_001",
        "timestamp": "2026-01-24T08:30:00Z",
        "agent": "backend-developer",
        "strategy": "backend",
        "description": "先定义接口契约，再并行开发前后端",
        "reward": 8.2,
        "diff": {
          "before": "直接开始编码",
          "after": "先定义 API 契约，确保前后端接口一致",
          "impact": "减少 30% 的接口对接时间"
        }
      }
    ]
  }
}
```


#### 3.1.3 获取智能诊断结果

```http
GET /api/v1/monitor/diagnosis
```

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "last_diagnosis_time": "2026-01-24T08:00:00Z",
    "next_diagnosis_time": "2026-01-24T09:00:00Z",
    "issues": [
      {
        "id": "issue_001",
        "severity": "Critical",
        "category": "performance",
        "title": "数据库查询性能瓶颈",
        "description": "question_service.py 中存在 N+1 查询问题",
        "location": "main/backend/services/question_service.py:45",
        "suggestion": "使用 joinedload 预加载关联数据",
        "auto_fixable": true,
        "fix_code": "query.options(joinedload(Question.answers))"
      },
      {
        "id": "issue_002",
        "severity": "Important",
        "category": "security",
        "title": "硬编码密钥风险",
        "description": "config.py 中存在硬编码的 SECRET_KEY",
        "location": "main/backend/core/config.py:12",
        "suggestion": "使用环境变量存储敏感信息",
        "auto_fixable": false
      }
    ]
  }
}
```


#### 3.1.4 一键修复问题

```http
POST /api/v1/monitor/diagnosis/fix
Content-Type: application/json

{
  "issue_id": "issue_001"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "修复成功",
  "data": {
    "issue_id": "issue_001",
    "fixed": true,
    "changes": [
      {
        "file": "main/backend/services/question_service.py",
        "line": 45,
        "before": "query = session.query(Question)",
        "after": "query = session.query(Question).options(joinedload(Question.answers))"
      }
    ]
  }
}
```

#### 3.1.5 获取 Agent 性能数据

```http
GET /api/v1/monitor/agents?type=all
```

**请求参数**:
- `type` (可选): Agent 类型筛选，默认 all

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "agents": [
      {
        "name": "backend-developer",
        "type": "developer",
        "current_progress": 75,
        "status": "working",
        "performance": {
          "total_tasks": 120,
          "success_rate": 0.92,
          "avg_duration_seconds": 180,
          "last_active": "2026-01-24T08:30:00Z"
        }
      }
    ]
  }
}
```


#### 3.1.6 获取知识图谱数据

```http
GET /api/v1/monitor/knowledge-graph?category=all&search=
```

**请求参数**:
- `category` (可选): 知识类型筛选，可选 strategy/best-practice/template/error-handling/all
- `search` (可选): 搜索关键词

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "categories": {
      "strategy": {
        "count": 45,
        "items": [
          {
            "id": "kb_001",
            "title": "前后端并行开发策略",
            "description": "先定义接口契约，再并行开发前后端",
            "source": ".claude/rules/collaboration.md",
            "updated_at": "2026-01-22T10:00:00Z",
            "tags": ["collaboration", "efficiency"]
          }
        ]
      },
      "best-practice": {
        "count": 32,
        "items": []
      }
    }
  }
}
```

### 3.2 WebSocket 接口

#### 3.2.1 实时进化事件推送

```
WS /ws/monitor/evolution?token=<jwt_token>
```

**连接认证**:
- 通过 URL 参数传递 JWT Token

**服务端推送消息格式**:
```json
{
  "type": "evolution_event",
  "data": {
    "id": "evt_002",
    "timestamp": "2026-01-24T08:35:00Z",
    "agent": "frontend-developer",
    "strategy": "frontend",
    "description": "组件拆分策略优化",
    "reward": 7.8
  }
}
```

**客户端心跳**:
```json
{
  "type": "ping"
}
```

**服务端心跳响应**:
```json
{
  "type": "pong"
}
```


---

## 4. 数据库设计

### 4.1 表结构

#### 4.1.1 monitor_intelligence (智能水平历史记录)

```sql
CREATE TABLE monitor_intelligence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    intelligence_score REAL NOT NULL,           -- 智能水平总分 (0-10)
    strategy_weight REAL NOT NULL,              -- 策略权重 (0-1)
    knowledge_richness REAL NOT NULL,           -- 知识丰富度 (0-1)
    quality_trend REAL NOT NULL,                -- 质量趋势 (0-1)
    evolution_frequency REAL NOT NULL,          -- 进化频率 (0-1)
    milestone_event TEXT,                       -- 里程碑事件（可选）
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp)
);
```

**智能水平计算公式**:
```python
intelligence_score = (
    strategy_weight * 0.3 +
    knowledge_richness * 0.25 +
    quality_trend * 0.25 +
    evolution_frequency * 0.2
) * 10
```

**数据来源**:
- `strategy_weight`: 统计 `.claude/rules/*.md` 文件中的策略规则数量和质量
- `knowledge_richness`: 统计 Agent 配置、Skill 文件、最佳实践数量
- `quality_trend`: 统计代码审查通过率、测试覆盖率
- `evolution_frequency`: 统计最近 7 天的进化记录数量


#### 4.1.2 monitor_diagnosis (诊断记录)

```sql
CREATE TABLE monitor_diagnosis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diagnosis_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    issue_id VARCHAR(50) NOT NULL UNIQUE,       -- 问题唯一标识
    severity VARCHAR(20) NOT NULL,              -- Critical/Important/Suggestion
    category VARCHAR(50) NOT NULL,              -- performance/security/quality/architecture
    title VARCHAR(200) NOT NULL,                -- 问题标题
    description TEXT NOT NULL,                  -- 问题描述
    location VARCHAR(500),                      -- 文件位置
    suggestion TEXT,                            -- 修复建议
    auto_fixable BOOLEAN DEFAULT FALSE,         -- 是否可自动修复
    fix_code TEXT,                              -- 修复代码
    status VARCHAR(20) DEFAULT 'open',          -- open/fixed/ignored
    fixed_at DATETIME,                          -- 修复时间
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_severity (severity),
    INDEX idx_status (status),
    INDEX idx_diagnosis_time (diagnosis_time)
);
```

**诊断维度**:
1. **性能瓶颈** (performance): 慢查询、大文件、重复代码
2. **安全风险** (security): 硬编码密钥、SQL 注入、XSS
3. **代码质量** (quality): 复杂度、测试覆盖率、文档完整性
4. **架构问题** (architecture): 耦合度、依赖循环、违反规范


#### 4.1.3 monitor_agent_performance (Agent 性能记录)

```sql
CREATE TABLE monitor_agent_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name VARCHAR(100) NOT NULL,           -- Agent 名称
    agent_type VARCHAR(50) NOT NULL,            -- developer/reviewer/tester/orchestrator
    task_id VARCHAR(100),                       -- 任务 ID
    status VARCHAR(20) NOT NULL,                -- working/completed/failed
    progress INTEGER DEFAULT 0,                 -- 进度 (0-100)
    duration_seconds INTEGER,                   -- 任务耗时（秒）
    success BOOLEAN,                            -- 是否成功
    error_message TEXT,                         -- 错误信息
    started_at DATETIME NOT NULL,               -- 开始时间
    completed_at DATETIME,                      -- 完成时间
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_agent_name (agent_name),
    INDEX idx_status (status),
    INDEX idx_started_at (started_at)
);
```

**性能指标计算**:
- `total_tasks`: 总任务数
- `success_rate`: 成功率 = 成功任务数 / 总任务数
- `avg_duration_seconds`: 平均耗时 = 总耗时 / 完成任务数

---

## 5. 前端组件设计

### 5.1 组件结构

```
main/frontend/pages/
└── Monitor.vue                              # 监控主页面

main/frontend/components/
├── MonitorIntelligenceChart.vue             # 智能水平走势图
├── MonitorDiagnosis.vue                     # 智能诊断中心（置顶）
├── MonitorEvolutionStream.vue               # 实时进化动态
├── MonitorAgentProgress.vue                 # Agent 性能监控
└── MonitorKnowledgeGraph.vue                # 知识图谱

main/frontend/services/
└── monitor.ts                               # 监控 API 服务

main/frontend/stores/
└── monitorStore.ts                          # 监控状态管理
```


### 5.2 核心组件设计

#### 5.2.1 Monitor.vue (主页面)

**职责**:
- 布局管理（5 个子组件）
- WebSocket 连接管理
- 全局状态初始化

**布局结构**:
```
┌─────────────────────────────────────────────────────────┐
│  Header (标题 + 刷新按钮)                                │
├─────────────────────────────────────────────────────────┤
│  MonitorDiagnosis (智能诊断中心 - 置顶)                 │
├─────────────────────────────────────────────────────────┤
│  MonitorIntelligenceChart (智能水平走势图)              │
├──────────────────────┬──────────────────────────────────┤
│  MonitorEvolution    │  MonitorAgentProgress            │
│  Stream              │  (Agent 性能监控)                │
│  (实时进化动态)      │                                  │
├──────────────────────┴──────────────────────────────────┤
│  MonitorKnowledgeGraph (知识图谱)                       │
└─────────────────────────────────────────────────────────┘
```

**关键逻辑**:
```typescript
// WebSocket 连接管理
const ws = ref<WebSocket | null>(null)

const connectWebSocket = () => {
  const token = userStore.token
  ws.value = new WebSocket(`ws://localhost:8000/ws/monitor/evolution?token=${token}`)
  
  ws.value.onmessage = (event) => {
    const message = JSON.parse(event.data)
    if (message.type === 'evolution_event') {
      monitorStore.addEvolutionEvent(message.data)
    }
  }
  
  // 心跳保活
  setInterval(() => {
    ws.value?.send(JSON.stringify({ type: 'ping' }))
  }, 30000)
}
```


#### 5.2.2 MonitorIntelligenceChart.vue (智能水平走势图)

**职责**:
- 展示智能水平随时间的变化曲线
- 标注学习路径里程碑
- 支持时间范围筛选

**技术实现**:
- 使用 ECharts 折线图
- 数据点悬停显示详细信息
- 里程碑使用 markPoint 标注

**ECharts 配置示例**:
```typescript
const chartOption = {
  title: { text: '系统智能水平走势' },
  tooltip: {
    trigger: 'axis',
    formatter: (params: any) => {
      const data = params[0].data
      return `
        时间: ${data.timestamp}<br/>
        智能水平: ${data.intelligence_score.toFixed(2)}<br/>
        策略权重: ${data.strategy_weight.toFixed(2)}<br/>
        知识丰富度: ${data.knowledge_richness.toFixed(2)}<br/>
        质量趋势: ${data.quality_trend.toFixed(2)}<br/>
        进化频率: ${data.evolution_frequency.toFixed(2)}
      `
    }
  },
  xAxis: { type: 'time' },
  yAxis: { type: 'value', min: 0, max: 10 },
  series: [{
    type: 'line',
    data: trendData.value,
    smooth: true,
    markPoint: {
      data: milestones.value.map(m => ({
        coord: [m.timestamp, m.intelligence_score],
        value: m.event
      }))
    }
  }]
}
```


#### 5.2.3 MonitorDiagnosis.vue (智能诊断中心)

**职责**:
- 展示 AI 诊断结果（置顶显示）
- 按严重程度分级展示
- 提供一键修复功能

**UI 设计**:
```
┌─────────────────────────────────────────────────────────┐
│  🤖 智能诊断中心                                         │
│  上次诊断: 2026-01-24 08:00  |  下次诊断: 09:00 (58分钟后) │
├─────────────────────────────────────────────────────────┤
│  🔴 Critical (2)                                        │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 数据库查询性能瓶颈                                 │ │
│  │ 位置: main/backend/services/question_service.py:45│ │
│  │ 建议: 使用 joinedload 预加载关联数据              │ │
│  │ [一键修复] [查看详情] [忽略]                      │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  🟡 Important (3)                                       │
│  🟢 Suggestion (5)                                      │
└─────────────────────────────────────────────────────────┘
```

**关键逻辑**:
```typescript
// 一键修复
const handleFix = async (issueId: string) => {
  try {
    const result = await monitorService.fixIssue(issueId)
    ElMessage.success('修复成功')
    // 刷新诊断结果
    await loadDiagnosis()
  } catch (error) {
    ElMessage.error('修复失败: ' + error.message)
  }
}

// 倒计时显示
const nextDiagnosisCountdown = computed(() => {
  const now = Date.now()
  const next = new Date(diagnosisData.value.next_diagnosis_time).getTime()
  const diff = next - now
  const minutes = Math.floor(diff / 60000)
  return `${minutes}分钟后`
})
```


#### 5.2.4 MonitorEvolutionStream.vue (实时进化动态)

**职责**:
- 事件流展示最新进化记录
- 支持展开/折叠查看详细对比
- 实时接收 WebSocket 推送

**UI 设计**:
```
┌─────────────────────────────────────────────────────────┐
│  📊 实时进化动态                                         │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐ │
│  │ 🕐 2026-01-24 08:35  |  backend-developer         │ │
│  │ 策略: backend  |  奖励: 8.2/10                    │ │
│  │ 先定义接口契约，再并行开发前后端                   │ │
│  │ [展开详情 ▼]                                      │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 🕐 2026-01-24 08:30  |  frontend-developer        │ │
│  │ 策略: frontend  |  奖励: 7.8/10                   │ │
│  │ 组件拆分策略优化                                   │ │
│  │ [展开详情 ▼]                                      │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  [加载更多]                                            │
└─────────────────────────────────────────────────────────┘
```

**关键逻辑**:
```typescript
// 虚拟滚动（支持 1000+ 条记录）
import { useVirtualList } from '@vueuse/core'

const { list, containerProps, wrapperProps } = useVirtualList(
  events,
  { itemHeight: 120 }
)

// 实时接收新事件
watch(() => monitorStore.latestEvent, (newEvent) => {
  if (newEvent) {
    events.value.unshift(newEvent)
    // 显示新事件提示
    ElNotification({
      title: '新进化事件',
      message: newEvent.description,
      type: 'success'
    })
  }
})
```


#### 5.2.5 MonitorAgentProgress.vue (Agent 性能监控)

**职责**:
- 展示所有 Agent 的当前进度
- 显示历史性能数据
- 支持按类型筛选

**UI 设计**:
```
┌─────────────────────────────────────────────────────────┐
│  🤖 Agent 性能监控                                       │
│  筛选: [全部] [开发者] [审查者] [测试者]                │
├─────────────────────────────────────────────────────────┤
│  backend-developer                                      │
│  ████████████████░░░░ 75%  |  状态: 工作中              │
│  总任务: 120  |  成功率: 92%  |  平均耗时: 3分钟        │
│  [查看详情]                                             │
├─────────────────────────────────────────────────────────┤
│  frontend-developer                                     │
│  ██████████████████░░ 90%  |  状态: 工作中              │
│  总任务: 95  |  成功率: 88%  |  平均耗时: 2.5分钟      │
│  [查看详情]                                             │
└─────────────────────────────────────────────────────────┘
```

**关键逻辑**:
```typescript
// 进度条颜色
const getProgressColor = (progress: number) => {
  if (progress >= 80) return '#67C23A'  // 绿色
  if (progress >= 50) return '#E6A23C'  // 黄色
  return '#F56C6C'  // 红色
}

// 状态徽章
const getStatusBadge = (status: string) => {
  const badges = {
    working: { text: '工作中', type: 'success' },
    completed: { text: '已完成', type: 'info' },
    failed: { text: '失败', type: 'danger' }
  }
  return badges[status] || badges.working
}
```


#### 5.2.6 MonitorKnowledgeGraph.vue (知识图谱)

**职责**:
- 卡片式展示知识条目
- 按类型分组
- 支持搜索和筛选

**UI 设计**:
```
┌─────────────────────────────────────────────────────────┐
│  📚 知识图谱                                             │
│  搜索: [_______]  |  类型: [全部▼]                      │
├─────────────────────────────────────────────────────────┤
│  策略规则 (45)                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│  │ 前后端   │ │ 并行开发 │ │ API 优先 │               │
│  │ 并行开发 │ │ 策略     │ │ 设计     │               │
│  │ 策略     │ │          │ │          │               │
│  │ 更新:    │ │ 更新:    │ │ 更新:    │               │
│  │ 01-22    │ │ 01-20    │ │ 01-18    │               │
│  └──────────┘ └──────────┘ └──────────┘               │
│                                                         │
│  最佳实践 (32)                                          │
│  ┌──────────┐ ┌──────────┐                            │
│  │ 三层防护 │ │ 数据库   │                            │
│  │ 体系     │ │ 策略     │                            │
│  └──────────┘ └──────────┘                            │
└─────────────────────────────────────────────────────────┘
```

**关键逻辑**:
```typescript
// 搜索和筛选
const filteredKnowledge = computed(() => {
  let result = knowledgeData.value
  
  // 类型筛选
  if (selectedCategory.value !== 'all') {
    result = result.filter(item => item.category === selectedCategory.value)
  }
  
  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(item =>
      item.title.toLowerCase().includes(keyword) ||
      item.description.toLowerCase().includes(keyword)
    )
  }
  
  return result
})

// 点击卡片查看详情
const handleCardClick = (item: KnowledgeItem) => {
  ElDialog.open({
    title: item.title,
    content: item.fullContent,
    width: '60%'
  })
}
```


---

## 6. 后端服务设计

### 6.1 文件结构

```
main/backend/
├── api/routes/
│   └── monitor_router.py                    # 监控路由
├── services/
│   ├── monitor_service.py                   # 通用监控服务
│   ├── monitor_intelligence.py              # 智能水平计算服务
│   └── monitor_diagnosis.py                 # AI 诊断服务
├── models/
│   └── monitor_schema.py                    # Pydantic 模型
└── migrations/
    └── add_monitor_tables.py                # 数据库迁移脚本
```

### 6.2 核心服务实现

#### 6.2.1 monitor_intelligence.py (智能水平计算)

**职责**:
- 计算系统智能水平
- 统计策略权重、知识丰富度、质量趋势、进化频率
- 识别学习路径里程碑

**核心算法**:
```python
class IntelligenceCalculator:
    """智能水平计算器"""
    
    def calculate_intelligence_score(self) -> IntelligenceScore:
        """
        计算智能水平总分
        
        公式: (策略权重×0.3 + 知识丰富度×0.25 + 质量趋势×0.25 + 进化频率×0.2) × 10
        """
        strategy_weight = self._calculate_strategy_weight()
        knowledge_richness = self._calculate_knowledge_richness()
        quality_trend = self._calculate_quality_trend()
        evolution_frequency = self._calculate_evolution_frequency()
        
        intelligence_score = (
            strategy_weight * 0.3 +
            knowledge_richness * 0.25 +
            quality_trend * 0.25 +
            evolution_frequency * 0.2
        ) * 10
        
        return IntelligenceScore(
            intelligence_score=intelligence_score,
            strategy_weight=strategy_weight,
            knowledge_richness=knowledge_richness,
            quality_trend=quality_trend,
            evolution_frequency=evolution_frequency
        )
    
    def _calculate_strategy_weight(self) -> float:
        """
        计算策略权重 (0-1)
        
        数据来源: .claude/rules/*.md 文件
        计算方法: (策略规则数量 / 100) × (平均奖励分数 / 10)
        """
        rules_dir = Path(".claude/rules")
        total_rules = 0
        total_reward = 0.0
        
        for rule_file in rules_dir.glob("*.md"):
            content = rule_file.read_text()
            # 解析规则数量
            rules = re.findall(r"###.*洞察", content)
            total_rules += len(rules)
            # 解析平均奖励
            rewards = re.findall(r"平均奖励.*?(\d+\.?\d*)/10", content)
            if rewards:
                total_reward += sum(float(r) for r in rewards) / len(rewards)
        
        if total_rules == 0:
            return 0.0
        
        rule_score = min(total_rules / 100, 1.0)
        reward_score = total_reward / (10 * len(list(rules_dir.glob("*.md"))))
        
        return (rule_score + reward_score) / 2
```

    
    def _calculate_knowledge_richness(self) -> float:
        """
        计算知识丰富度 (0-1)
        
        数据来源:
        - .claude/agents/*.md (Agent 配置)
        - .claude/skills/*/SKILL.md (技能知识)
        - .claude/project_standards.md (最佳实践)
        
        计算方法: (Agent数量×10 + Skill数量×20 + 最佳实践数量×5) / 500
        """
        agents_count = len(list(Path(".claude/agents").glob("*.md")))
        skills_count = len(list(Path(".claude/skills").glob("*/SKILL.md")))
        
        # 统计最佳实践数量
        standards_file = Path(".claude/project_standards.md")
        best_practices = 0
        if standards_file.exists():
            content = standards_file.read_text()
            best_practices = len(re.findall(r"###.*最佳实践", content))
        
        knowledge_score = (
            agents_count * 10 +
            skills_count * 20 +
            best_practices * 5
        ) / 500
        
        return min(knowledge_score, 1.0)
    
    def _calculate_quality_trend(self) -> float:
        """
        计算质量趋势 (0-1)
        
        数据来源:
        - main/docs/reviews/*.md (代码审查记录)
        - 测试覆盖率报告
        
        计算方法: (代码审查通过率×0.6 + 测试覆盖率×0.4)
        """
        # 统计代码审查通过率
        reviews_dir = Path("main/docs/reviews")
        if not reviews_dir.exists():
            return 0.5  # 默认值
        
        total_reviews = 0
        passed_reviews = 0
        
        for review_file in reviews_dir.glob("*.md"):
            content = review_file.read_text()
            total_reviews += 1
            if "通过" in content or "LGTM" in content:
                passed_reviews += 1
        
        review_pass_rate = passed_reviews / total_reviews if total_reviews > 0 else 0.5
        
        # 测试覆盖率（假设从测试报告读取）
        test_coverage = 0.75  # 默认值，实际应从测试报告解析
        
        return review_pass_rate * 0.6 + test_coverage * 0.4
    
    def _calculate_evolution_frequency(self) -> float:
        """
        计算进化频率 (0-1)
        
        数据来源: .claude/rules/*.md 文件的更新时间
        计算方法: 最近 7 天的进化记录数量 / 50
        """
        rules_dir = Path(".claude/rules")
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_updates = 0
        
        for rule_file in rules_dir.glob("*.md"):
            mtime = datetime.fromtimestamp(rule_file.stat().st_mtime)
            if mtime > seven_days_ago:
                recent_updates += 1
        
        return min(recent_updates / 50, 1.0)
```


#### 6.2.2 monitor_diagnosis.py (AI 诊断服务)

**职责**:
- 使用 Claude API 分析代码问题
- 生成修复建议
- 执行自动修复

**核心实现**:
```python
class DiagnosisService:
    """AI 诊断服务"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def run_diagnosis(self) -> List[DiagnosisIssue]:
        """
        执行智能诊断
        
        诊断维度:
        1. 性能瓶颈 (performance)
        2. 安全风险 (security)
        3. 代码质量 (quality)
        4. 架构问题 (architecture)
        """
        issues = []
        
        # 1. 性能瓶颈检测
        issues.extend(await self._detect_performance_issues())
        
        # 2. 安全风险检测
        issues.extend(await self._detect_security_issues())
        
        # 3. 代码质量检测
        issues.extend(await self._detect_quality_issues())
        
        # 4. 架构问题检测
        issues.extend(await self._detect_architecture_issues())
        
        # 保存到数据库
        for issue in issues:
            await self._save_issue(issue)
        
        return issues
    
    async def _detect_performance_issues(self) -> List[DiagnosisIssue]:
        """检测性能瓶颈"""
        issues = []
        
        # 扫描后端代码
        backend_dir = Path("main/backend")
        for py_file in backend_dir.rglob("*.py"):
            content = py_file.read_text()
            
            # 使用 Claude API 分析
            prompt = f"""
            分析以下 Python 代码的性能问题:
            
            文件: {py_file}
            
            ```python
            {content}
            ```
            
            请识别:
            1. N+1 查询问题
            2. 大文件读取
            3. 重复计算
            4. 未使用索引的查询
            
            返回 JSON 格式:
            {{
                "issues": [
                    {{
                        "line": 45,
                        "severity": "Critical",
                        "title": "问题标题",
                        "description": "问题描述",
                        "suggestion": "修复建议",
                        "fix_code": "修复代码"
                    }}
                ]
            }}
            """
            
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # 解析响应
            result = json.loads(response.content[0].text)
            for issue_data in result.get("issues", []):
                issues.append(DiagnosisIssue(
                    issue_id=f"perf_{uuid.uuid4().hex[:8]}",
                    severity=issue_data["severity"],
                    category="performance",
                    title=issue_data["title"],
                    description=issue_data["description"],
                    location=f"{py_file}:{issue_data['line']}",
                    suggestion=issue_data["suggestion"],
                    auto_fixable=bool(issue_data.get("fix_code")),
                    fix_code=issue_data.get("fix_code")
                ))
        
        return issues
```

    
    async def _detect_security_issues(self) -> List[DiagnosisIssue]:
        """检测安全风险"""
        issues = []
        
        # 检测硬编码密钥
        for py_file in Path("main/backend").rglob("*.py"):
            content = py_file.read_text()
            
            # 正则匹配常见密钥模式
            patterns = [
                (r'SECRET_KEY\s*=\s*["\']([^"\']+)["\']', "硬编码 SECRET_KEY"),
                (r'API_KEY\s*=\s*["\']([^"\']+)["\']', "硬编码 API_KEY"),
                (r'PASSWORD\s*=\s*["\']([^"\']+)["\']', "硬编码密码"),
            ]
            
            for pattern, title in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(DiagnosisIssue(
                        issue_id=f"sec_{uuid.uuid4().hex[:8]}",
                        severity="Critical",
                        category="security",
                        title=title,
                        description=f"在 {py_file}:{line_num} 发现硬编码敏感信息",
                        location=f"{py_file}:{line_num}",
                        suggestion="使用环境变量存储敏感信息",
                        auto_fixable=False
                    ))
        
        return issues
    
    async def auto_fix_issue(self, issue_id: str) -> FixResult:
        """
        自动修复问题
        
        Args:
            issue_id: 问题 ID
        
        Returns:
            修复结果
        """
        # 从数据库获取问题详情
        issue = await self._get_issue(issue_id)
        
        if not issue.auto_fixable:
            raise ValueError("该问题不支持自动修复")
        
        # 读取文件
        file_path = Path(issue.location.split(":")[0])
        content = file_path.read_text()
        
        # 应用修复代码
        # 这里简化处理，实际应该更智能地定位和替换
        lines = content.split('\n')
        line_num = int(issue.location.split(":")[1]) - 1
        
        # 替换问题行
        lines[line_num] = issue.fix_code
        
        # 写回文件
        file_path.write_text('\n'.join(lines))
        
        # 更新数据库状态
        await self._update_issue_status(issue_id, "fixed")
        
        return FixResult(
            issue_id=issue_id,
            fixed=True,
            changes=[{
                "file": str(file_path),
                "line": line_num + 1,
                "before": content.split('\n')[line_num],
                "after": issue.fix_code
            }]
        )
```


#### 6.2.3 monitor_service.py (通用监控服务)

**职责**:
- 解析进化事件流
- 统计 Agent 性能
- 解析知识图谱

**核心实现**:
```python
class MonitorService:
    """通用监控服务"""
    
    async def get_evolution_stream(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> EvolutionStreamResponse:
        """
        获取进化事件流
        
        数据来源: .claude/rules/*.md 文件
        """
        events = []
        rules_dir = Path(".claude/rules")
        
        for rule_file in rules_dir.glob("*.md"):
            content = rule_file.read_text()
            
            # 解析策略关键词
            strategy_match = re.search(r"策略关键词.*?:\s*(.+)", content)
            strategy = strategy_match.group(1) if strategy_match else "unknown"
            
            # 解析洞察记录
            insights = re.findall(
                r"### (.*?)\n\n- \*\*Agent\*\*: (.+?)\n- \*\*描述\*\*: (.+?)(?:\n\n|$)",
                content,
                re.DOTALL
            )
            
            for insight_type, agent, description in insights:
                # 解析奖励分数（如果有）
                reward_match = re.search(r"平均奖励.*?(\d+\.?\d*)/10", content)
                reward = float(reward_match.group(1)) if reward_match else 0.0
                
                events.append(EvolutionEvent(
                    id=f"evt_{uuid.uuid4().hex[:8]}",
                    timestamp=datetime.fromtimestamp(rule_file.stat().st_mtime),
                    agent=agent.strip(),
                    strategy=strategy.strip(),
                    description=description.strip(),
                    reward=reward
                ))
        
        # 按时间倒序排序
        events.sort(key=lambda e: e.timestamp, reverse=True)
        
        # 分页
        total = len(events)
        events = events[offset:offset + limit]
        
        return EvolutionStreamResponse(
            total=total,
            events=events
        )
    
    async def get_agent_performance(
        self,
        agent_type: str = "all"
    ) -> List[AgentPerformance]:
        """
        获取 Agent 性能数据
        
        数据来源:
        - .claude/agents/*.md (Agent 配置)
        - monitor_agent_performance 表 (性能记录)
        """
        agents = []
        agents_dir = Path(".claude/agents")
        
        for agent_file in agents_dir.glob("*.md"):
            agent_name = agent_file.stem
            
            # 从数据库查询性能数据
            performance_data = await self._query_agent_performance(agent_name)
            
            agents.append(AgentPerformance(
                name=agent_name,
                type=self._get_agent_type(agent_name),
                current_progress=performance_data.get("progress", 0),
                status=performance_data.get("status", "idle"),
                performance=PerformanceMetrics(
                    total_tasks=performance_data.get("total_tasks", 0),
                    success_rate=performance_data.get("success_rate", 0.0),
                    avg_duration_seconds=performance_data.get("avg_duration", 0),
                    last_active=performance_data.get("last_active")
                )
            ))
        
        # 类型筛选
        if agent_type != "all":
            agents = [a for a in agents if a.type == agent_type]
        
        return agents
```

    
    async def get_knowledge_graph(
        self,
        category: str = "all",
        search: str = ""
    ) -> KnowledgeGraphResponse:
        """
        获取知识图谱数据
        
        数据来源:
        - .claude/rules/*.md (策略规则)
        - .claude/project_standards.md (最佳实践)
        - .claude/skills/*/SKILL.md (技能知识)
        """
        categories = {
            "strategy": [],
            "best-practice": [],
            "template": [],
            "error-handling": []
        }
        
        # 解析策略规则
        rules_dir = Path(".claude/rules")
        for rule_file in rules_dir.glob("*.md"):
            content = rule_file.read_text()
            
            # 提取洞察
            insights = re.findall(
                r"### (.*?)\n\n- \*\*Agent\*\*: (.+?)\n- \*\*描述\*\*: (.+?)(?:\n\n|$)",
                content,
                re.DOTALL
            )
            
            for insight_type, agent, description in insights:
                categories["strategy"].append(KnowledgeItem(
                    id=f"kb_{uuid.uuid4().hex[:8]}",
                    title=f"{agent} - {insight_type}",
                    description=description.strip(),
                    source=str(rule_file),
                    updated_at=datetime.fromtimestamp(rule_file.stat().st_mtime),
                    tags=[agent.strip(), "strategy"]
                ))
        
        # 解析最佳实践
        standards_file = Path(".claude/project_standards.md")
        if standards_file.exists():
            content = standards_file.read_text()
            
            # 提取最佳实践章节
            practices = re.findall(
                r"### (.+?)\n\n(.+?)(?=\n###|\Z)",
                content,
                re.DOTALL
            )
            
            for title, description in practices:
                if "最佳实践" in title or "Best Practice" in title:
                    categories["best-practice"].append(KnowledgeItem(
                        id=f"kb_{uuid.uuid4().hex[:8]}",
                        title=title.strip(),
                        description=description.strip()[:200] + "...",
                        source=str(standards_file),
                        updated_at=datetime.fromtimestamp(standards_file.stat().st_mtime),
                        tags=["best-practice"]
                    ))
        
        # 类型筛选
        if category != "all":
            filtered_categories = {category: categories.get(category, [])}
        else:
            filtered_categories = categories
        
        # 搜索筛选
        if search:
            for cat, items in filtered_categories.items():
                filtered_categories[cat] = [
                    item for item in items
                    if search.lower() in item.title.lower() or
                       search.lower() in item.description.lower()
                ]
        
        return KnowledgeGraphResponse(categories=filtered_categories)
```


### 6.3 WebSocket 实现

```python
# main/backend/api/routes/monitor_router.py

from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """断开连接"""
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        """广播消息到所有连接"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                # 连接已断开，移除
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/ws/monitor/evolution")
async def websocket_evolution_stream(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    WebSocket 实时进化事件推送
    
    认证: 通过 URL 参数传递 JWT Token
    """
    # 验证 Token
    try:
        user = await verify_token(token)
    except:
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    # 接受连接
    await manager.connect(websocket)
    
    try:
        while True:
            # 接收客户端消息（心跳）
            data = await websocket.receive_json()
            
            if data.get("type") == "ping":
                # 响应心跳
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# 后台任务：监听文件变化并推送事件
async def watch_evolution_events():
    """
    监听 .claude/rules/*.md 文件变化
    当有新进化事件时，通过 WebSocket 推送
    """
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    
    class RulesFileHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.src_path.endswith(".md"):
                # 解析新事件
                new_event = parse_evolution_event(event.src_path)
                
                # 广播到所有连接
                asyncio.create_task(manager.broadcast({
                    "type": "evolution_event",
                    "data": new_event.dict()
                }))
    
    observer = Observer()
    observer.schedule(RulesFileHandler(), ".claude/rules", recursive=False)
    observer.start()
```


---

## 7. 数据模型 (Pydantic)

### 7.1 请求/响应模型

```python
# main/backend/models/monitor_schema.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict

# ==================== 智能水平相关 ====================

class IntelligenceScore(BaseModel):
    """智能水平分数"""
    intelligence_score: float = Field(..., ge=0, le=10, description="智能水平总分")
    strategy_weight: float = Field(..., ge=0, le=1, description="策略权重")
    knowledge_richness: float = Field(..., ge=0, le=1, description="知识丰富度")
    quality_trend: float = Field(..., ge=0, le=1, description="质量趋势")
    evolution_frequency: float = Field(..., ge=0, le=1, description="进化频率")

class Milestone(BaseModel):
    """学习路径里程碑"""
    timestamp: datetime
    event: str
    intelligence_score: float

class IntelligenceTrendResponse(BaseModel):
    """智能水平走势响应"""
    trend: List[IntelligenceScore]
    milestones: List[Milestone]

# ==================== 进化事件相关 ====================

class EvolutionDiff(BaseModel):
    """进化对比详情"""
    before: str
    after: str
    impact: str

class EvolutionEvent(BaseModel):
    """进化事件"""
    id: str
    timestamp: datetime
    agent: str
    strategy: str
    description: str
    reward: float
    diff: Optional[EvolutionDiff] = None

class EvolutionStreamResponse(BaseModel):
    """进化事件流响应"""
    total: int
    events: List[EvolutionEvent]

# ==================== 诊断相关 ====================

class DiagnosisIssue(BaseModel):
    """诊断问题"""
    id: str
    severity: str = Field(..., description="Critical/Important/Suggestion")
    category: str = Field(..., description="performance/security/quality/architecture")
    title: str
    description: str
    location: Optional[str] = None
    suggestion: Optional[str] = None
    auto_fixable: bool = False
    fix_code: Optional[str] = None

class DiagnosisResponse(BaseModel):
    """诊断响应"""
    last_diagnosis_time: datetime
    next_diagnosis_time: datetime
    issues: List[DiagnosisIssue]

class FixRequest(BaseModel):
    """修复请求"""
    issue_id: str

class FixChange(BaseModel):
    """修复变更"""
    file: str
    line: int
    before: str
    after: str

class FixResult(BaseModel):
    """修复结果"""
    issue_id: str
    fixed: bool
    changes: List[FixChange]

# ==================== Agent 性能相关 ====================

class PerformanceMetrics(BaseModel):
    """性能指标"""
    total_tasks: int
    success_rate: float
    avg_duration_seconds: int
    last_active: Optional[datetime] = None

class AgentPerformance(BaseModel):
    """Agent 性能"""
    name: str
    type: str
    current_progress: int = Field(..., ge=0, le=100)
    status: str = Field(..., description="working/completed/failed/idle")
    performance: PerformanceMetrics

class AgentPerformanceResponse(BaseModel):
    """Agent 性能响应"""
    agents: List[AgentPerformance]

# ==================== 知识图谱相关 ====================

class KnowledgeItem(BaseModel):
    """知识条目"""
    id: str
    title: str
    description: str
    source: str
    updated_at: datetime
    tags: List[str]

class KnowledgeCategory(BaseModel):
    """知识分类"""
    count: int
    items: List[KnowledgeItem]

class KnowledgeGraphResponse(BaseModel):
    """知识图谱响应"""
    categories: Dict[str, KnowledgeCategory]
```


---

## 8. 性能优化策略

### 8.1 前端优化

| 优化项 | 策略 | 预期效果 |
|--------|------|---------|
| **虚拟滚动** | 使用 `@vueuse/core` 的 `useVirtualList` | 支持 1000+ 条记录流畅滚动 |
| **图表懒加载** | ECharts 按需加载，使用 `v-lazy` | 减少首屏加载时间 50% |
| **数据缓存** | Pinia 缓存 API 响应，5 分钟过期 | 减少重复请求 80% |
| **WebSocket 心跳** | 30 秒心跳保活，断线自动重连 | 保持连接稳定性 |
| **组件懒加载** | 使用 `defineAsyncComponent` | 减少初始 bundle 大小 30% |

### 8.2 后端优化

| 优化项 | 策略 | 预期效果 |
|--------|------|---------|
| **数据库索引** | 在 `timestamp`、`agent_name`、`status` 字段建索引 | 查询速度提升 10 倍 |
| **异步处理** | 使用 `asyncio` 并发处理文件解析 | 响应时间减少 60% |
| **缓存策略** | 智能水平数据缓存 5 分钟 | 减少计算开销 90% |
| **分页查询** | 默认 50 条/页，最大 100 条/页 | 避免大数据量传输 |
| **定时任务** | AI 诊断每小时执行一次，避免频繁调用 | 节省 API 成本 95% |

### 8.3 WebSocket 优化

| 优化项 | 策略 | 预期效果 |
|--------|------|---------|
| **连接池管理** | 最大 100 个并发连接 | 避免资源耗尽 |
| **消息压缩** | 使用 gzip 压缩大消息 | 减少带宽 70% |
| **心跳机制** | 30 秒心跳，3 次失败断开 | 及时清理僵尸连接 |
| **断线重连** | 指数退避重连策略 | 提升连接稳定性 |

---

## 9. 安全设计

### 9.1 认证授权

| 安全项 | 实现方式 |
|--------|---------|
| **API 认证** | 所有接口需要 JWT Token |
| **WebSocket 认证** | URL 参数传递 Token，连接时验证 |
| **权限控制** | 管理员才能执行一键修复 |
| **Token 刷新** | Token 过期自动刷新 |

### 9.2 数据安全

| 安全项 | 实现方式 |
|--------|---------|
| **敏感信息过滤** | 诊断结果不展示密钥、密码 |
| **SQL 注入防护** | 使用 SQLAlchemy 参数化查询 |
| **XSS 防护** | 前端使用 `v-html` 时过滤 HTML |
| **CSRF 防护** | POST 请求需要 CSRF Token |

### 9.3 代码安全

| 安全项 | 实现方式 |
|--------|---------|
| **自动修复限制** | 只修复白名单文件，禁止修改核心配置 |
| **修复审计** | 所有修复操作记录到数据库 |
| **回滚机制** | 修复前备份原文件，支持一键回滚 |

---

## 10. 测试策略

### 10.1 单元测试

| 测试对象 | 测试工具 | 覆盖率目标 |
|---------|---------|-----------|
| **智能水平计算** | Pytest | 90% |
| **AI 诊断服务** | Pytest + Mock | 85% |
| **前端组件** | Vitest | 80% |
| **API 接口** | Pytest + httpx | 90% |

### 10.2 集成测试

| 测试场景 | 测试方法 |
|---------|---------|
| **API 端到端** | 使用 Pytest 测试完整请求流程 |
| **WebSocket 连接** | 测试连接、推送、断线重连 |
| **数据库操作** | 测试 CRUD 和事务 |

### 10.3 性能测试

| 测试指标 | 测试工具 | 目标值 |
|---------|---------|--------|
| **页面加载时间** | Lighthouse | < 2 秒 |
| **API 响应时间** | Locust | < 500ms |
| **WebSocket 延迟** | 自定义脚本 | < 500ms |
| **并发连接数** | Locust | 支持 100 并发 |


---

## 11. 部署方案

### 11.1 开发环境

```bash
# 后端启动
cd main/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 前端启动
cd main/frontend
npm run dev
```

### 11.2 生产环境

```bash
# 后端部署（使用 Gunicorn + Uvicorn）
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# 前端构建
npm run build

# Nginx 配置
server {
    listen 80;
    server_name monitor.example.com;
    
    # 前端静态文件
    location / {
        root /var/www/monitor/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # WebSocket 代理
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 11.3 环境变量

```bash
# .env
DATABASE_URL=sqlite:///main/backend/db/ket_exam.db
SECRET_KEY=your-secret-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key
CORS_ORIGINS=http://localhost:5173,https://monitor.example.com
```

---

## 12. 开发计划

### 12.1 里程碑

| 阶段 | 任务 | 预计时间 | 负责人 |
|------|------|---------|--------|
| **阶段 1** | 数据库设计 + 后端 API | 2 天 | backend-developer |
| **阶段 2** | 前端组件开发 | 2 天 | frontend-developer |
| **阶段 3** | WebSocket 实时推送 | 1 天 | backend-developer |
| **阶段 4** | AI 诊断服务 | 1 天 | backend-developer |
| **阶段 5** | 集成测试 + 优化 | 1 天 | test |
| **阶段 6** | 代码审查 + 部署 | 1 天 | code-reviewer |

**总计**: 8 天

### 12.2 任务分配

#### 后端任务 (backend-developer)

| 任务 | 复杂度 | 估算时间 |
|------|--------|----------|
| 创建数据库表和迁移脚本 | 3 | 2 小时 |
| 实现智能水平计算服务 | 6 | 6 小时 |
| 实现 AI 诊断服务 | 7 | 8 小时 |
| 实现通用监控服务 | 5 | 4 小时 |
| 实现 REST API 路由 | 4 | 4 小时 |
| 实现 WebSocket 推送 | 6 | 6 小时 |
| 编写单元测试 | 5 | 4 小时 |

**小计**: 34 小时（约 4-5 天）

#### 前端任务 (frontend-developer)

| 任务 | 复杂度 | 估算时间 |
|------|--------|----------|
| 创建 Monitor.vue 主页面 | 4 | 3 小时 |
| 实现 MonitorIntelligenceChart.vue | 6 | 5 小时 |
| 实现 MonitorDiagnosis.vue | 5 | 4 小时 |
| 实现 MonitorEvolutionStream.vue | 6 | 5 小时 |
| 实现 MonitorAgentProgress.vue | 4 | 3 小时 |
| 实现 MonitorKnowledgeGraph.vue | 5 | 4 小时 |
| 实现 monitorStore.ts 状态管理 | 4 | 3 小时 |
| 实现 monitor.ts API 服务 | 3 | 2 小时 |
| WebSocket 连接管理 | 5 | 4 小时 |
| 编写单元测试 | 4 | 3 小时 |

**小计**: 36 小时（约 4-5 天）

---

## 13. 风险和缓解

### 13.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| **AI 诊断准确率不达标** | 高 | 中 | 多次迭代优化 Prompt，增加测试用例 |
| **WebSocket 性能瓶颈** | 中 | 低 | 限制并发连接数，使用消息队列 |
| **图表渲染卡顿** | 中 | 中 | 使用虚拟滚动，分页加载数据 |
| **文件解析性能问题** | 中 | 低 | 使用异步并发处理，缓存解析结果 |

### 13.2 业务风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| **需求变更** | 中 | 中 | 模块化设计，易于扩展 |
| **数据量增长** | 中 | 高 | 数据库分页，定期清理历史数据 |
| **API 成本超预算** | 低 | 低 | 限制诊断频率，使用缓存 |

---

## 14. 附录

### 14.1 参考文档

- PRD 文档: `main/docs/prds/monitor-system.md`
- 项目技术标准: `.claude/project_standards.md`
- Agent 配置: `.claude/agents/*.md`
- 策略规则: `.claude/rules/*.md`

### 14.2 相关技术文档

- [ECharts 官方文档](https://echarts.apache.org/zh/index.html)
- [FastAPI WebSocket 文档](https://fastapi.tiangolo.com/advanced/websockets/)
- [Anthropic Claude API 文档](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Pinia 官方文档](https://pinia.vuejs.org/)

### 14.3 文件清单

#### 后端文件

```
main/backend/
├── api/routes/monitor_router.py
├── services/
│   ├── monitor_service.py
│   ├── monitor_intelligence.py
│   └── monitor_diagnosis.py
├── models/monitor_schema.py
└── migrations/add_monitor_tables.py
```

#### 前端文件

```
main/frontend/
├── pages/Monitor.vue
├── components/
│   ├── MonitorIntelligenceChart.vue
│   ├── MonitorDiagnosis.vue
│   ├── MonitorEvolutionStream.vue
│   ├── MonitorAgentProgress.vue
│   └── MonitorKnowledgeGraph.vue
├── services/monitor.ts
└── stores/monitorStore.ts
```

#### 数据库文件

```
main/backend/db/
└── ket_exam.db (新增 3 个表)
```

---

## 15. 总结

本技术设计文档详细描述了 Claude Dev Team 监控中心的完整实现方案，包括：

1. **系统架构**: 前后端分离，使用 Vue 3 + FastAPI + SQLite
2. **API 设计**: 6 个 REST 接口 + 1 个 WebSocket 接口
3. **数据库设计**: 3 个新表（智能水平、诊断记录、Agent 性能）
4. **前端组件**: 5 个核心组件（走势图、诊断、事件流、性能、知识图谱）
5. **后端服务**: 智能水平计算、AI 诊断、通用监控服务
6. **性能优化**: 虚拟滚动、缓存、异步处理、WebSocket 优化
7. **安全设计**: JWT 认证、敏感信息过滤、自动修复限制
8. **测试策略**: 单元测试、集成测试、性能测试
9. **部署方案**: 开发环境 + 生产环境配置

**关键技术点**:
- 智能水平计算公式：`(策略权重×0.3 + 知识丰富度×0.25 + 质量趋势×0.25 + 进化频率×0.2) × 10`
- WebSocket 实时推送延迟 < 500ms
- ECharts 图表可视化
- 文件命名规范：后端 `monitor_` 前缀，前端 `Monitor` 前缀

**预计开发时间**: 8 天（后端 4-5 天，前端 4-5 天，并行开发）

**成功指标**:
- 页面加载时间 < 2 秒
- 实时数据推送延迟 < 500ms
- 智能诊断准确率 > 85%
- 用户满意度 > 4.5/5
