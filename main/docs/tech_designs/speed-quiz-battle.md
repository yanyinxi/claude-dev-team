# 技术设计文档：人与机器抢答功能

## 1. 系统架构

### 1.1 整体架构
```
┌─────────────┐      HTTP/REST      ┌──────────────┐
│   Vue 3     │ ◄─────────────────► │   FastAPI    │
│  Frontend   │                     │   Backend    │
└─────────────┘                     └──────────────┘
      │                                     │
      │                                     │
      ▼                                     ▼
┌─────────────┐                     ┌──────────────┐
│   Pinia     │                     │  SQLAlchemy  │
│   Store     │                     │     ORM      │
└─────────────┘                     └──────────────┘
                                            │
                                            ▼
                                    ┌──────────────┐
                                    │   SQLite     │
                                    │   Database   │
                                    └──────────────┘
```

### 1.2 核心模块

**后端模块：**
- `models/db.py` - 数据库模型（新增 SpeedQuizBattle, SpeedQuizDetail）
- `models/schema.py` - Pydantic 数据模型
- `services/speed_quiz_service.py` - 抢答业务逻辑
- `api/routes/speed_quiz_router.py` - API 路由

**前端模块：**
- `pages/SpeedQuiz.vue` - 抢答主页面
- `components/speed-quiz/` - 抢答相关组件
- `stores/speedQuizStore.ts` - 抢答状态管理
- `services/speedQuizService.ts` - API 调用

## 2. 数据库设计

### 2.1 新增表结构

**speed_quiz_battles 表**
```sql
CREATE TABLE speed_quiz_battles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    difficulty INTEGER NOT NULL,
    module VARCHAR(20) NOT NULL,
    total_questions INTEGER NOT NULL,
    user_correct INTEGER DEFAULT 0,
    ai_correct INTEGER DEFAULT 0,
    user_wins INTEGER DEFAULT 0,
    ai_wins INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**speed_quiz_details 表**
```sql
CREATE TABLE speed_quiz_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    battle_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer VARCHAR(1),
    user_time INTEGER,
    ai_answer VARCHAR(1) NOT NULL,
    ai_time INTEGER NOT NULL,
    correct_answer VARCHAR(1) NOT NULL,
    winner VARCHAR(10) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (battle_id) REFERENCES speed_quiz_battles(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
```

### 2.2 索引设计
- `speed_quiz_battles.user_id` - 查询用户战绩
- `speed_quiz_battles.created_at` - 按时间排序
- `speed_quiz_details.battle_id` - 查询对战详情

## 3. API 设计

### 3.1 开始抢答
**POST /api/speed-quiz/start**

请求：
```json
{
  "difficulty": 3,
  "module": "vocabulary",
  "rounds": 10
}
```

响应：
```json
{
  "battle_id": 123,
  "question": {
    "id": 456,
    "question_text": "What is the meaning of 'apple'?",
    "option_a": "苹果",
    "option_b": "香蕉",
    "option_c": "橙子",
    "option_d": "梨"
  }
}
```

### 3.2 提交答案
**POST /api/speed-quiz/submit**

请求：
```json
{
  "battle_id": 123,
  "question_id": 456,
  "answer": "A",
  "answer_time": 5200
}
```

响应：
```json
{
  "is_correct": true,
  "ai_answer": "A",
  "ai_time": 6800,
  "correct_answer": "A",
  "winner": "user",
  "next_question": { ... } | null
}
```

### 3.3 获取战绩
**GET /api/speed-quiz/stats**

响应：
```json
{
  "total_battles": 50,
  "wins": 32,
  "losses": 18,
  "win_rate": 0.64,
  "fastest_time": 3200,
  "max_streak": 8
}
```

### 3.4 获取历史记录
**GET /api/speed-quiz/history?page=1&page_size=10**

响应：
```json
{
  "battles": [
    {
      "id": 123,
      "difficulty": 3,
      "module": "vocabulary",
      "user_wins": 7,
      "ai_wins": 3,
      "created_at": "2026-01-19T10:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 10
}
```

## 4. AI 机器人算法

### 4.1 答题时间计算
```python
def calculate_ai_time(difficulty: int) -> int:
    """计算 AI 答题时间（毫秒）"""
    base_times = {
        1: (5000, 8000),
        2: (6000, 10000),
        3: (8000, 15000),
        4: (12000, 18000),
        5: (15000, 20000)
    }
    min_time, max_time = base_times.get(difficulty, (8000, 15000))
    base = random.randint(min_time, max_time)
    # 添加 ±20% 随机波动
    variation = random.uniform(0.8, 1.2)
    return int(base * variation)
```

### 4.2 答题正确率
```python
def ai_should_answer_correct(difficulty: int) -> bool:
    """判断 AI 是否答对"""
    accuracy_rates = {
        1: 0.90,
        2: 0.85,
        3: 0.80,
        4: 0.70,
        5: 0.65
    }
    rate = accuracy_rates.get(difficulty, 0.75)
    return random.random() < rate
```

### 4.3 答案选择
```python
def get_ai_answer(question: Question, should_correct: bool) -> str:
    """获取 AI 答案"""
    if should_correct:
        return question.correct_answer
    else:
        # 随机选择错误答案
        options = ['A', 'B', 'C', 'D']
        options.remove(question.correct_answer)
        return random.choice(options)
```

## 5. 前端组件设计

### 5.1 组件树
```
SpeedQuiz.vue (页面)
├── SpeedQuizEntry.vue (入口)
│   ├── DifficultySelector.vue
│   ├── ModuleSelector.vue
│   └── RoundsSelector.vue
├── SpeedQuizGame.vue (游戏)
│   ├── QuestionDisplay.vue
│   ├── PlayerStatus.vue (学生)
│   ├── AIStatus.vue (机器人)
│   └── Timer.vue
├── SpeedQuizResult.vue (结果)
│   ├── WinnerBadge.vue
│   └── AnswerComparison.vue
└── SpeedQuizStats.vue (战绩)
    ├── StatsCard.vue
    └── HistoryList.vue
```

### 5.2 状态管理（Pinia）
```typescript
interface SpeedQuizState {
  currentBattle: Battle | null
  currentQuestion: Question | null
  userAnswer: string | null
  userTime: number
  aiAnswer: string | null
  aiTime: number
  score: { user: number; ai: number }
  isAnswering: boolean
  showResult: boolean
}
```

## 6. 性能优化

### 6.1 后端优化
- 使用数据库连接池
- 题目预加载（一次加载所有题目）
- AI 答案异步计算
- 响应数据压缩

### 6.2 前端优化
- 组件懒加载
- 动画使用 CSS transform（GPU 加速）
- 防抖处理用户输入
- 虚拟滚动历史记录列表

## 7. 安全设计

### 7.1 防作弊措施
- 答案不在前端暴露
- 服务端验证答题时间合理性
- 记录客户端时间戳，服务端校验
- 限制答题速度（最快 1 秒）

### 7.2 数据完整性
- 使用事务保证数据一致性
- 外键约束
- 唯一性约束

## 8. 测试策略

### 8.1 后端测试
- 单元测试：AI 算法、业务逻辑
- 集成测试：API 端点
- 性能测试：并发用户

### 8.2 前端测试
- 组件测试：各个 Vue 组件
- 集成测试：完整流程
- E2E 测试：用户场景

## 9. 部署方案

### 9.1 数据库迁移
```bash
# 创建新表
python -m main.backend.migrations.add_speed_quiz_tables
```

### 9.2 依赖安装
无新增依赖

### 9.3 配置更新
无需配置更新

## 10. 监控和日志

### 10.1 关键指标
- API 响应时间
- 抢答完成率
- AI 胜率分布
- 用户留存率

### 10.2 日志记录
- 每场抢答的开始和结束
- AI 决策过程
- 异常情况记录
