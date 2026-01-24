# 技术设计文档：Claude Dev Team 进化可视化系统

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      前端 (Vue 3)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Evolution.vue│  │ ECharts 组件 │  │ WebSocket    │      │
│  │              │  │              │  │ 客户端       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    后端 (FastAPI)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Evolution    │  │ Intelligence │  │ WebSocket    │      │
│  │ Router       │  │ Service      │  │ Manager      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQLAlchemy
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据库 (SQLite)                           │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ evolution_   │  │ intelligence_│                        │
│  │ events       │  │ metrics      │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 前端 | Vue 3 | 3.x | UI 框架 |
| 前端 | TypeScript | 5.x | 类型安全 |
| 前端 | ECharts | 5.x | 数据可视化 |
| 前端 | WebSocket API | - | 实时通信 |
| 后端 | FastAPI | 0.100+ | Web 框架 |
| 后端 | SQLAlchemy | 2.x | ORM |
| 后端 | WebSocket | - | 实时推送 |
| 数据库 | SQLite | 3.x | 数据存储 |

## 2. 数据库设计

### 2.1 evolution_events 表

```sql
CREATE TABLE evolution_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- 'best_practice', 'improvement', 'collaboration', 'error_fix'
    agent VARCHAR(50) NOT NULL,
    strategy VARCHAR(50),
    content TEXT NOT NULL,
    reward FLOAT,
    metadata JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON evolution_events(timestamp);
CREATE INDEX idx_event_type ON evolution_events(event_type);
CREATE INDEX idx_agent ON evolution_events(agent);
```

### 2.2 intelligence_metrics 表

```sql
CREATE TABLE intelligence_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    strategy_weight FLOAT NOT NULL,      -- 策略权重 (0-1)
    knowledge_richness FLOAT NOT NULL,   -- 知识丰富度 (0-1)
    quality_trend FLOAT NOT NULL,        -- 质量趋势 (0-1)
    evolution_frequency FLOAT NOT NULL,  -- 进化频率 (0-1)
    intelligence_level FLOAT NOT NULL,   -- 智能水平 (0-100)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON intelligence_metrics(timestamp);
```

## 3. 后端 API 设计

### 3.1 REST API

#### 3.1.1 获取智能水平历史

```
GET /api/v1/evolution/intelligence-level?range=24h|7d|30d
```

**响应**:
```json
{
  "data": [
    {
      "timestamp": "2026-01-24T10:00:00",
      "intelligence_level": 85.5,
      "strategy_weight": 0.9,
      "knowledge_richness": 0.85,
      "quality_trend": 0.88,
      "evolution_frequency": 0.75
    }
  ],
  "current_level": 85.5,
  "trend": "up"
}
```

#### 3.1.2 获取进化事件列表

```
GET /api/v1/evolution/events?type=all|best_practice|improvement&limit=50
```

**响应**:
```json
{
  "events": [
    {
      "id": 1,
      "timestamp": "2026-01-24T10:00:00",
      "event_type": "best_practice",
      "agent": "backend-developer",
      "strategy": "api-first",
      "content": "先定义接口契约，再并行开发前后端",
      "reward": 8.5,
      "metadata": {
        "success_rate": 0.9,
        "avg_reward": 8.5
      }
    }
  ],
  "total": 100
}
```

#### 3.1.3 获取统计数据

```
GET /api/v1/evolution/statistics
```

**响应**:
```json
{
  "total_events": 150,
  "events_by_type": {
    "best_practice": 60,
    "improvement": 50,
    "collaboration": 30,
    "error_fix": 10
  },
  "events_by_agent": {
    "backend-developer": 40,
    "frontend-developer": 35,
    "orchestrator": 30
  },
  "avg_reward": 8.2,
  "intelligence_growth": 15.5
}
```

#### 3.1.4 获取里程碑

```
GET /api/v1/evolution/milestones
```

**响应**:
```json
{
  "milestones": [
    {
      "id": 1,
      "name": "首次进化",
      "description": "系统完成第一次自主学习",
      "achieved_at": "2026-01-20T10:00:00",
      "icon": "🎯"
    },
    {
      "id": 2,
      "name": "智能水平突破 80",
      "description": "系统智能水平首次突破 80 分",
      "achieved_at": "2026-01-22T15:30:00",
      "icon": "🚀"
    }
  ]
}
```

### 3.2 WebSocket API

#### 3.2.1 连接

```
WS /ws/evolution?token=<jwt_token>
```

#### 3.2.2 消息格式

**服务端推送**:
```json
{
  "type": "evolution_event",
  "data": {
    "id": 1,
    "timestamp": "2026-01-24T10:00:00",
    "event_type": "best_practice",
    "agent": "backend-developer",
    "content": "先定义接口契约，再并行开发前后端",
    "reward": 8.5
  }
}
```

```json
{
  "type": "intelligence_update",
  "data": {
    "intelligence_level": 85.5,
    "change": +2.3
  }
}
```

**客户端心跳**:
```json
{
  "type": "ping"
}
```

**服务端响应**:
```json
{
  "type": "pong"
}
```

## 4. 前端设计

### 4.1 页面结构

```
Evolution.vue
├── IntelligenceTrendChart.vue      # 智能水平走势图
├── EvolutionEventStream.vue        # 进化动态流
├── BrainVisualization.vue          # "大脑"可视化
└── EvolutionStatistics.vue         # 进化统计
```

### 4.2 组件设计

#### 4.2.1 IntelligenceTrendChart.vue

**功能**:
- 显示智能水平历史曲线
- 标注进化事件
- 支持时间范围切换

**Props**:
```typescript
interface Props {
  range: '24h' | '7d' | '30d'
}
```

**ECharts 配置**:
```typescript
{
  xAxis: { type: 'time' },
  yAxis: { type: 'value', min: 0, max: 100 },
  series: [
    {
      type: 'line',
      data: [[timestamp, intelligence_level], ...],
      markPoint: {
        data: [{ coord: [timestamp, level], name: 'event' }]
      }
    }
  ]
}
```

#### 4.2.2 EvolutionEventStream.vue

**功能**:
- 显示进化事件列表
- 实时接收新事件
- 支持事件筛选

**数据结构**:
```typescript
interface EvolutionEvent {
  id: number
  timestamp: string
  event_type: string
  agent: string
  content: string
  reward: number
}
```

#### 4.2.3 BrainVisualization.vue

**功能**:
- 显示系统状态动画
- 显示实时活动日志
- 显示学习进度

**状态**:
```typescript
type SystemState = 'idle' | 'thinking' | 'learning' | 'evolving'
```

**动画效果**:
- CSS 动画（脉冲、旋转）
- Vue Transition（淡入淡出）

#### 4.2.4 EvolutionStatistics.vue

**功能**:
- 显示统计数据
- 显示里程碑徽章
- 显示进化热力图

**图表类型**:
- 柱状图（按类型统计）
- 饼图（按 Agent 统计）
- 热力图（按时间和类型）

### 4.3 WebSocket 客户端

```typescript
class EvolutionWebSocket {
  private ws: WebSocket | null = null
  private reconnectTimer: number | null = null
  private heartbeatTimer: number | null = null

  connect(token: string) {
    this.ws = new WebSocket(`ws://localhost:8000/ws/evolution?token=${token}`)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.startHeartbeat()
    }

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data)
      this.handleMessage(message)
    }

    this.ws.onclose = () => {
      console.log('WebSocket closed')
      this.reconnect()
    }
  }

  private startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      this.send({ type: 'ping' })
    }, 30000)
  }

  private reconnect() {
    this.reconnectTimer = setTimeout(() => {
      this.connect(token)
    }, 5000)
  }

  send(message: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }

  close() {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer)
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer)
    this.ws?.close()
  }
}
```

## 5. 智能水平计算

### 5.1 计算公式

```
智能水平 = (策略权重 × 0.3 + 知识丰富度 × 0.3 + 质量趋势 × 0.2 + 进化频率 × 0.2) × 100
```

### 5.2 指标计算

#### 5.2.1 策略权重 (Strategy Weight)

```python
def calculate_strategy_weight() -> float:
    """计算策略权重 (0-1)"""
    # 从 .claude/rules/*.md 读取策略规则
    # 计算平均奖励值
    total_reward = 0
    count = 0

    for rule_file in rules_dir.glob("*.md"):
        content = rule_file.read_text()
        # 解析 "平均奖励: X/10"
        if match := re.search(r"平均奖励.*?(\d+\.?\d*)/10", content):
            total_reward += float(match.group(1))
            count += 1

    return (total_reward / count / 10) if count > 0 else 0.5
```

#### 5.2.2 知识丰富度 (Knowledge Richness)

```python
def calculate_knowledge_richness() -> float:
    """计算知识丰富度 (0-1)"""
    # 统计规则文件中的洞察数量
    total_insights = 0

    for rule_file in rules_dir.glob("*.md"):
        content = rule_file.read_text()
        # 统计 "### ✅" 和 "### ⚠️" 的数量
        total_insights += content.count("### ✅")
        total_insights += content.count("### ⚠️")

    # 归一化到 0-1（假设 50 个洞察为满分）
    return min(total_insights / 50, 1.0)
```

#### 5.2.3 质量趋势 (Quality Trend)

```python
def calculate_quality_trend() -> float:
    """计算质量趋势 (0-1)"""
    # 从最近 10 次进化事件计算平均奖励
    recent_events = db.query(EvolutionEvent)\
        .order_by(EvolutionEvent.timestamp.desc())\
        .limit(10)\
        .all()

    if not recent_events:
        return 0.5

    avg_reward = sum(e.reward for e in recent_events) / len(recent_events)
    return avg_reward / 10
```

#### 5.2.4 进化频率 (Evolution Frequency)

```python
def calculate_evolution_frequency() -> float:
    """计算进化频率 (0-1)"""
    # 计算最近 7 天的进化次数
    seven_days_ago = datetime.now() - timedelta(days=7)
    count = db.query(EvolutionEvent)\
        .filter(EvolutionEvent.timestamp >= seven_days_ago)\
        .count()

    # 归一化到 0-1（假设 20 次为满分）
    return min(count / 20, 1.0)
```

## 6. 性能优化

### 6.1 后端优化

1. **数据库索引**: 在 timestamp、event_type、agent 字段上创建索引
2. **查询优化**: 使用分页查询，限制返回数量
3. **缓存策略**: 使用 Redis 缓存最近事件和统计数据
4. **异步处理**: 使用 async/await 处理所有 I/O 操作

### 6.2 前端优化

1. **虚拟滚动**: 事件列表使用虚拟滚动
2. **懒加载**: 图表组件按需加载
3. **防抖节流**: WebSocket 消息处理使用防抖
4. **数据缓存**: 使用 Pinia 缓存数据

## 7. 安全考虑

### 7.1 WebSocket 认证

```python
async def websocket_endpoint(websocket: WebSocket, token: str):
    # 验证 JWT Token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
    except JWTError:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    # ...
```

### 7.2 数据脱敏

- 敏感信息（密钥、密码）不记录到进化事件
- 用户数据脱敏处理

## 8. 测试策略

### 8.1 单元测试

- 智能水平计算函数测试
- 数据库操作测试
- WebSocket 连接测试

### 8.2 集成测试

- API 端点测试
- WebSocket 推送测试
- 前后端集成测试

### 8.3 性能测试

- 并发连接测试（100+ 连接）
- 大数据量测试（10000+ 事件）
- 响应时间测试

## 9. 部署方案

### 9.1 开发环境

```bash
# 后端
cd main/backend
uvicorn main:app --reload

# 前端
cd main/frontend
npm run dev
```

### 9.2 生产环境

```bash
# 后端
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# 前端
npm run build
nginx -c nginx.conf
```

## 10. 监控告警

### 10.1 监控指标

- WebSocket 连接数
- API 响应时间
- 数据库查询时间
- 错误率

### 10.2 告警规则

- WebSocket 连接失败率 > 5%
- API 响应时间 > 1s
- 数据库查询时间 > 500ms
- 错误率 > 1%

## 11. 附录

### 11.1 参考资料

- ECharts 文档: https://echarts.apache.org/
- FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/
- Vue 3 文档: https://vuejs.org/

### 11.2 相关文件

- PRD: `main/docs/prds/evolution-visualization.md`
- 后端代码: `main/backend/api/routes/evolution_router.py`
- 前端代码: `main/frontend/pages/Evolution.vue`
