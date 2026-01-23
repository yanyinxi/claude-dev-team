# KET备考系统 - 后端 API

专为小学生设计的 KET 考试备考系统后端服务

## 技术栈

- Python 3.10+
- FastAPI 0.100+
- SQLAlchemy 2.x (异步 ORM)
- Pydantic 2.x (数据验证)
- SQLite (开发环境)
- JWT (身份认证)

## 快速开始

### 1. 安装依赖

```bash
cd main/backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并根据需要修改配置：

```bash
cp .env.example .env
```

### 3. 启动服务

```bash
# 开发模式（自动重载）
uvicorn main:app --reload

# 或者直接运行
python main.py
```

服务将在 http://localhost:8000 启动

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 目录结构

```
main/backend/               # 后端代码根目录
├── api/                   # API 路由层
│   └── routes/            # 路由文件
│       ├── auth_router.py         # 认证路由
│       ├── question_router.py     # 题目路由
│       ├── answer_router.py       # 答题路由
│       ├── progress_router.py     # 进度路由
│       ├── admin_router.py       # 管理员路由
│       ├── speed_quiz_router.py  # 抢答路由
│       └── monitor_router.py     # AlphaZero 监控路由
├── core/                  # 核心配置
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库连接
│   ├── security.py        # 安全认证
│   └── exceptions.py      # 异常定义
├── models/                # 数据模型层
│   ├── db.py              # SQLAlchemy 模型
│   └── schema.py          # Pydantic 模型
├── services/              # 业务逻辑层
│   ├── auth_service.py    # 认证服务
│   ├── question_service.py # 题目服务
│   ├── progress_service.py # 进度服务
│   └── speed_quiz_service.py # 抢答服务
├── tasks/                 # 定时任务
│   └── ai_digest/         # AI 日报任务
│       ├── router.py
│       ├── service.py
│       ├── models.py
│       └── schemas.py
├── scripts/               # 脚本文件
│   ├── create_admin.py    # 创建管理员账号
│   └── alphazero-status.py # AlphaZero 监控脚本
├── migrations/            # 数据库迁移
│   ├── add_speed_quiz_tables.py
│   └── add_ai_digest_table.py
├── db/                    # 数据库文件目录
│   ├── ket_exam.db        # 主数据库
│   ├── test.db            # 测试数据库
│   └── .gitignore         # 忽略数据库文件
├── main.py                # 应用入口
└── requirements.txt       # 依赖列表
```

## 目录结构约束（必须遵守）

| 内容类型 | 必须放在 | 禁止放在 |
|----------|----------|----------|
| **API 路由** | `main/backend/api/routes/` | 后端根目录 |
| **业务逻辑** | `main/backend/services/` | 后端根目录 |
| **数据模型** | `main/backend/models/` | 后端根目录 |
| **核心配置** | `main/backend/core/` | 后端根目录 |
| **定时任务** | `main/backend/tasks/` | 后端根目录 |
| **脚本文件** | `main/backend/scripts/` | 后端根目录 |
| **数据库文件** | `main/backend/db/` | 后端根目录 |
| **数据库迁移** | `main/backend/migrations/` | 后端根目录 |
| **应用入口** | `main/backend/main.py` | 其他位置 |

## 核心功能

### 认证接口

- `POST /api/v1/auth/login/student` - 学生登录（输入昵称，自动创建用户）
- `POST /api/v1/auth/login/admin` - 管理员登录（admin/admin123）

### 题目接口

- `GET /api/v1/questions/random` - 随机获取题目（支持按模块和难度筛选）

### 答题接口

- `POST /api/v1/answers` - 提交答案（自动计算得分、连击、成就）

### 监控接口（AlphaZero）

- `GET /api/v1/monitor/stats` - 系统状态统计
- `GET /api/v1/monitor/agents` - Agent 信息
- `GET /api/v1/monitor/rules` - 策略规则
- `GET /api/v1/monitor/experience` - 经验池
- `GET /api/v1/monitor/health` - 健康检查

## 数据库

系统使用 SQLite 数据库，数据库文件位于 `main/backend/db/` 目录：

- **主数据库**: `main/backend/db/ket_exam.db`
- **测试数据库**: `main/backend/db/test.db`

首次启动时会自动创建数据库和示例数据：

- 管理员账号：`admin / admin123`
- 10 道示例题目（词汇、语法、阅读）
- 4 个成就徽章

## 使用脚本

### 创建管理员账号

```bash
python scripts/create_admin.py
```

### AlphaZero 监控

```bash
python scripts/alphazero-status.py
```

## 开发说明

### 添加新 API

1. 在 `api/routes/` 下创建路由文件
2. 在 `api/routes/__init__.py` 中导出
3. 在 `main.py` 中注册路由

### 添加新服务

1. 在 `services/` 下创建服务文件
2. 实现业务逻辑
3. 在路由中调用服务

### 添加定时任务

1. 在 `tasks/` 下创建任务目录
2. 实现任务逻辑
3. 在 `main.py` 中注册任务

## 常见问题

1. **生产环境部署**：修改 `.env` 中的 `SECRET_KEY`
2. **数据库切换**：生产环境建议使用 PostgreSQL
3. **CORS 配置**：在 `main.py` 中修改白名单

## 许可证

MIT License
