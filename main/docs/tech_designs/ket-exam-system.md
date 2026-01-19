# 技术设计文档：KET备考系统

## 1. 系统架构概述

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  小学生端    │  │  管理员端    │  │  家长端      │      │
│  │  (Vue 3)     │  │  (Vue 3)     │  │  (Vue 3)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                      前端层 (Vue 3)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Vue Router (路由)  │  Pinia (状态管理)              │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Components (组件)  │  Services (API调用)            │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Tailwind CSS (样式) │  Vite (构建工具)              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ RESTful API
┌─────────────────────────────────────────────────────────────┐
│                    后端层 (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes (路由层)                                  │  │
│  │  - 认证路由  - 题目路由  - 进度路由  - 管理路由      │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Services (业务逻辑层)                                │  │
│  │  - 用户服务  - 题目服务  - 奖励服务  - 统计服务      │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Models (数据模型层)                                  │  │
│  │  - SQLAlchemy ORM  - Pydantic Schema                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ SQL
┌─────────────────────────────────────────────────────────────┐
│                    数据层                                     │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  PostgreSQL      │  │  SQLite          │                │
│  │  (生产环境)      │  │  (开发环境)      │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈选型

| 层级 | 技术 | 版本 | 选型理由 |
|------|------|------|---------|
| 前端框架 | Vue 3 | 3.x | 轻量、易学、适合小学生UI |
| 前端语言 | TypeScript | 5.x | 类型安全、减少运行时错误 |
| 构建工具 | Vite | 5.x | 极速HMR、开发体验好 |
| 状态管理 | Pinia | 2.x | 简洁、TypeScript友好 |
| 路由 | Vue Router | 4.x | Vue官方路由方案 |
| CSS框架 | Tailwind CSS | 3.x | 原子类、快速开发 |
| 后端框架 | FastAPI | 0.100+ | 异步、高性能、自动文档 |
| 后端语言 | Python | 3.10+ | 生态丰富、易维护 |
| ORM | SQLAlchemy | 2.x | 功能强大、支持异步 |
| 数据验证 | Pydantic | 2.x | 自动验证、类型安全 |
| 数据库 | PostgreSQL | 16 | 生产环境、事务支持 |
| 开发数据库 | SQLite | 3.x | 轻量、无需配置 |

## 2. 前端架构设计

### 2.1 目录结构

```
main/frontend/
├── components/           # UI组件
│   ├── common/          # 通用组件
│   │   ├── Button.vue
│   │   ├── Card.vue
│   │   └── Loading.vue
│   ├── learning/        # 学习相关组件
│   │   ├── QuestionCard.vue
│   │   ├── AnswerOptions.vue
│   │   ├── RewardAnimation.vue
│   │   └── ProgressBar.vue
│   ├── achievement/     # 成就相关组件
│   │   ├── BadgeWall.vue
│   │   ├── ScoreDisplay.vue
│   │   └── Calendar.vue
│   └── admin/           # 管理后台组件
│       ├── QuestionManager.vue
│       └── UserManager.vue
├── pages/               # 页面组件
│   ├── Home.vue         # 首页
│   ├── Login.vue        # 登录页
│   ├── Learning.vue     # 学习页
│   ├── Profile.vue      # 个人主页
│   ├── Admin.vue        # 管理后台
│   └── NotFound.vue     # 404页面
├── stores/              # Pinia状态管理
│   ├── userStore.ts     # 用户状态
│   ├── questionStore.ts # 题目状态
│   ├── progressStore.ts # 进度状态
│   └── achievementStore.ts # 成就状态
├── services/            # API服务
│   ├── authService.ts   # 认证服务
│   ├── questionService.ts # 题目服务
│   ├── progressService.ts # 进度服务
│   └── adminService.ts  # 管理服务
├── utils/               # 工具函数
│   ├── request.ts       # HTTP请求封装
│   ├── storage.ts       # 本地存储
│   └── animation.ts     # 动画工具
├── styles/              # 样式文件
│   ├── global.css       # 全局样式
│   └── tailwind.css     # Tailwind配置
├── router/              # 路由配置
│   └── index.ts
├── App.vue              # 根组件
└── main.ts              # 入口文件
```

### 2.2 核心功能模块

#### 2.2.1 学习模块
- **QuestionCard**: 题目展示卡片
- **AnswerOptions**: 答案选项组件
- **RewardAnimation**: 奖励动画（星星、徽章）
- **ProgressBar**: 进度条显示

#### 2.2.2 成就模块
- **BadgeWall**: 徽章墙展示
- **ScoreDisplay**: 积分显示
- **Calendar**: 学习日历

#### 2.2.3 管理模块
- **QuestionManager**: 题库管理
- **UserManager**: 用户管理
- **Statistics**: 数据统计

### 2.3 状态管理设计

```typescript
// userStore.ts
interface UserState {
  id: number | null
  nickname: string
  role: 'student' | 'admin'
  isLoggedIn: boolean
  totalScore: number
  badges: Badge[]
}

// questionStore.ts
interface QuestionState {
  currentQuestion: Question | null
  questionHistory: Question[]
  wrongQuestions: Question[]
  currentModule: 'vocabulary' | 'grammar' | 'reading'
}

// progressStore.ts
interface ProgressState {
  totalQuestions: number
  correctAnswers: number
  streak: number
  dailyGoal: number
  completedToday: number
}
```

## 3. 后端架构设计

### 3.1 目录结构

```
main/backend/
├── api/                 # API路由层
│   └── routes/
│       ├── auth_router.py      # 认证路由
│       ├── question_router.py  # 题目路由
│       ├── progress_router.py  # 进度路由
│       ├── achievement_router.py # 成就路由
│       └── admin_router.py     # 管理路由
├── services/            # 业务逻辑层
│   ├── auth_service.py         # 认证服务
│   ├── question_service.py     # 题目服务
│   ├── progress_service.py     # 进度服务
│   ├── achievement_service.py  # 成就服务
│   └── admin_service.py        # 管理服务
├── models/              # 数据模型层
│   ├── db.py                   # SQLAlchemy模型
│   └── schema.py               # Pydantic模型
├── core/                # 核心配置
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── security.py             # 安全认证
│   └── exceptions.py           # 异常定义
├── utils/               # 工具函数
│   ├── logger.py               # 日志工具
│   └── validators.py           # 验证工具
├── main.py              # 应用入口
└── requirements.txt     # 依赖列表
```

### 3.2 API设计原则

1. **RESTful规范**: 使用标准HTTP方法
2. **统一响应格式**: `{code, message, data}`
3. **JWT认证**: 无状态认证
4. **异步处理**: 使用async/await
5. **自动文档**: FastAPI自动生成Swagger

## 4. 数据库设计

### 4.1 数据表设计

#### 4.1.1 users (用户表)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    password_hash VARCHAR(255),  -- 管理员密码
    total_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4.1.2 questions (题目表)
```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    module VARCHAR(20) NOT NULL,  -- vocabulary/grammar/reading
    difficulty INTEGER DEFAULT 1,  -- 1-5难度等级
    question_text TEXT NOT NULL,
    question_image VARCHAR(255),
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT,
    option_d TEXT,
    correct_answer CHAR(1) NOT NULL,  -- A/B/C/D
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4.1.3 user_progress (学习进度表)
```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question_id INTEGER REFERENCES questions(id),
    is_correct BOOLEAN NOT NULL,
    answer_time INTEGER,  -- 答题时间(秒)
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, question_id, answered_at)
);
```

#### 4.1.4 achievements (成就表)
```sql
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    badge_icon VARCHAR(255),
    requirement_type VARCHAR(50),  -- total_questions/streak/daily_login
    requirement_value INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4.1.5 user_achievements (用户成就关联表)
```sql
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    achievement_id INTEGER REFERENCES achievements(id),
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, achievement_id)
);
```

#### 4.1.6 wrong_questions (错题本表)
```sql
CREATE TABLE wrong_questions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    question_id INTEGER REFERENCES questions(id),
    wrong_count INTEGER DEFAULT 1,
    last_wrong_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, question_id)
);
```

### 4.2 数据库索引

```sql
-- 用户查询优化
CREATE INDEX idx_users_nickname ON users(nickname);

-- 题目查询优化
CREATE INDEX idx_questions_module ON questions(module);
CREATE INDEX idx_questions_difficulty ON questions(difficulty);

-- 进度查询优化
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_answered_at ON user_progress(answered_at);

-- 成就查询优化
CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);
```

## 5. 核心功能实现

### 5.1 认证流程

```
学生登录流程:
1. 输入昵称
2. 后端检查昵称是否存在
3. 不存在则自动创建用户
4. 生成JWT Token
5. 返回用户信息和Token

管理员登录流程:
1. 输入用户名和密码
2. 后端验证密码(bcrypt)
3. 验证成功生成JWT Token
4. 返回管理员信息和Token
```

### 5.2 答题流程

```
1. 前端请求题目 (GET /api/questions/random)
2. 后端随机返回一道题目
3. 用户选择答案
4. 前端提交答案 (POST /api/answers)
5. 后端验证答案
6. 计算得分和连击
7. 检查是否解锁成就
8. 返回结果和奖励信息
9. 前端显示奖励动画
```

### 5.3 奖励机制

```typescript
// 积分计算规则
基础分 = 10分
连击加成 = 基础分 * 连击系数
  - 连击2-5: x1.5
  - 连击6-10: x2.0
  - 连击11+: x2.5
速度加成 = 答题时间 < 10秒 ? 5分 : 0分

总分 = 基础分 + 连击加成 + 速度加成
```

## 6. 性能优化

### 6.1 前端优化
- 组件懒加载
- 图片懒加载
- 路由懒加载
- Vite代码分割
- Tailwind CSS按需加载

### 6.2 后端优化
- 数据库连接池
- 查询结果缓存
- 异步处理
- 批量操作
- 索引优化

### 6.3 数据库优化
- 合理使用索引
- 避免N+1查询
- 使用连接查询
- 定期清理过期数据

## 7. 安全设计

### 7.1 认证安全
- JWT Token过期时间: 24小时
- 管理员密码使用bcrypt加密
- Token存储在localStorage
- 敏感操作需要重新验证

### 7.2 数据安全
- SQL注入防护(使用ORM)
- XSS防护(Vue自动转义)
- CSRF防护(Token验证)
- 输入验证(Pydantic)

### 7.3 权限控制
- 学生只能访问学习相关接口
- 管理员可以访问所有接口
- 使用装饰器进行权限检查

## 8. 部署方案

### 8.1 开发环境
```bash
# 前端
cd main/frontend
npm install
npm run dev  # http://localhost:5173

# 后端
cd main/backend
poetry install
uvicorn main:app --reload  # http://localhost:8000
```

### 8.2 生产环境
```bash
# 前端构建
npm run build
# 输出到 dist/ 目录

# 后端部署
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 数据库
PostgreSQL 16
```

## 9. 风险评估

### 9.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 动画性能问题 | 中 | 中 | 提供性能模式，减少动画 |
| 数据库性能瓶颈 | 高 | 低 | 使用索引、缓存、连接池 |
| 并发问题 | 中 | 低 | 使用异步处理、事务 |

### 9.2 业务风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 题库内容质量 | 高 | 中 | 邀请英语教师审核 |
| 用户留存率低 | 高 | 中 | A/B测试、用户反馈 |
| 奖励机制过度游戏化 | 中 | 中 | 平衡学习和游戏 |

## 10. 后续扩展

### 10.1 短期扩展(1-3个月)
- 听力模块
- 排行榜功能
- 家长端应用
- 学习报告

### 10.2 长期扩展(3-6个月)
- AI智能推荐
- 语音识别
- 社交功能
- 多语言支持

---

**文档版本**: v1.0
**创建日期**: 2026-01-19
**创建人**: Tech Lead
**审核状态**: 待审核
