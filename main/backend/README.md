# KET备考系统 - 后端API

专为小学生设计的KET考试备考系统后端服务

## 技术栈

- Python 3.10+
- FastAPI 0.100+
- SQLAlchemy 2.x (异步ORM)
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

### 4. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 核心功能

### 认证接口

- `POST /api/v1/auth/login/student` - 学生登录（输入昵称，自动创建用户）
- `POST /api/v1/auth/login/admin` - 管理员登录（admin/admin）

### 题目接口

- `GET /api/v1/questions/random` - 随机获取题目（支持按模块和难度筛选）

### 答题接口

- `POST /api/v1/answers` - 提交答案（自动计算得分、连击、成就）

## 数据库

系统使用SQLite数据库，首次启动时会自动创建数据库和示例数据：

- 管理员账号：admin / admin
- 10道示例题目（词汇、语法、阅读）
- 4个成就徽章

## 项目结构

```
main/backend/
├── api/                 # API路由层
│   └── routes/
│       ├── auth_router.py      # 认证路由
│       ├── question_router.py  # 题目路由
│       └── answer_router.py    # 答题路由
├── services/            # 业务逻辑层
│   ├── auth_service.py         # 认证服务
│   ├── question_service.py     # 题目服务
│   └── progress_service.py     # 进度服务
├── models/              # 数据模型层
│   ├── db.py                   # SQLAlchemy模型
│   └── schema.py               # Pydantic模型
├── core/                # 核心配置
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── security.py             # 安全认证
│   └── exceptions.py           # 异常定义
├── main.py              # 应用入口
├── requirements.txt     # 依赖列表
└── .env.example         # 环境变量示例
```

## 核心逻辑

### 连击计算

系统会自动计算用户的连续答对题数（连击）：
- 答对：连击+1
- 答错：连击归零

### 得分计算

```
基础分 = 10分
连击加成:
  - 连击2-5: x1.5
  - 连击6-10: x2.0
  - 连击11+: x2.5
速度加成: 答题时间 < 10秒 ? 5分 : 0分

总分 = 基础分 * 连击系数 + 速度加成
```

### 成就系统

系统会自动检测并解锁成就：
- 初学者：完成第1道题目
- 勤奋学习：完成10道题目
- 连击高手：连续答对5题
- 学霸：完成50道题目

### 错题本

答错的题目会自动记录到错题本，包括：
- 错误次数
- 最后错误时间

## API使用示例

### 学生登录

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/student \
  -H "Content-Type: application/json" \
  -d '{"nickname": "小明"}'
```

### 获取随机题目

```bash
curl -X GET "http://localhost:8000/api/v1/questions/random?module=vocabulary&difficulty=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 提交答案

```bash
curl -X POST http://localhost:8000/api/v1/answers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "question_id": 1,
    "answer": "A",
    "answer_time": 8
  }'
```

## 开发说明

### 添加新题目

可以通过管理员接口或直接操作数据库添加题目。题目包含：
- module: vocabulary/grammar/reading
- difficulty: 1-5
- question_text: 题目文本
- option_a/b/c/d: 选项
- correct_answer: 正确答案 (A/B/C/D)
- explanation: 答案解析

### 扩展功能

系统设计支持以下扩展：
- 进度统计接口
- 学习日历
- 排行榜
- 家长端API
- 听力模块

## 注意事项

1. 生产环境请修改 `.env` 中的 `SECRET_KEY`
2. 生产环境建议使用 PostgreSQL 替代 SQLite
3. 建议配置 CORS 白名单限制跨域访问
4. 定期备份数据库文件 `ket_exam.db`

## 许可证

MIT License
