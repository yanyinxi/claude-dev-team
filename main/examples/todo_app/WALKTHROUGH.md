# 完整全栈应用 - Todo App 步骤说明

## 使用方式

1. 在 Claude Code 中输入：
   ```
   "实现一个完整的待办事项管理应用，包括用户界面、后端 API、数据库、测试等完整功能"
   ```

2. 系统会自动：
   - 分析需求
   - 设计架构
   - 分配开发者（动态）
   - 并行开发前端、后端、数据库
   - 集成测试
   - 代码审查
   - 交付完整应用

## 预期输出

```
.claude/output/todo_app/
├── prd/
│   ├── todo_app_prd.md              # 产品需求文档
│   └── user_stories.md              # 用户故事
├── design/
│   ├── architecture.md              # 系统架构
│   ├── database_design.md           # 数据库设计
│   ├── api_design.md                # API 设计
│   └── task_assignment.json         # 任务分配
├── code/
│   ├── frontend/
│   │   ├── components/              # React 组件
│   │   ├── styles/                  # CSS 样式
│   │   └── types/                   # TypeScript 类型
│   ├── backend/
│   │   ├── api/                     # API 路由
│   │   ├── models/                  # 数据模型
│   │   ├── services/                # 业务逻辑
│   │   └── middleware/              # 中间件
│   └── database/
│       ├── migrations/              # 数据库迁移
│       └── seeds/                   # 测试数据
├── tests/
│   ├── unit_tests/                  # 单元测试
│   ├── integration_tests/           # 集成测试
│   ├── e2e_tests/                   # 端到端测试
│   └── test_report.json             # 测试报告
├── reviews/
│   ├── code_review.json             # 代码审查
│   └── architecture_review.md       # 架构审查
├── deployment/
│   ├── docker/                      # Docker 配置
│   └── deployment_guide.md          # 部署指南
└── reports/
    ├── development_report.md        # 开发报告
    └── delivery_report.md           # 交付报告
```

## 查看结果

```bash
# 查看产品需求
cat .claude/output/todo_app/prd/todo_app_prd.md

# 查看系统架构
cat .claude/output/todo_app/design/architecture.md

# 查看数据库设计
cat .claude/output/todo_app/design/database_design.md

# 查看 API 设计
cat .claude/output/todo_app/design/api_design.md

# 查看前端代码
ls .claude/output/todo_app/code/frontend/

# 查看后端代码
ls .claude/output/todo_app/code/backend/

# 查看测试报告
cat .claude/output/todo_app/tests/test_report.json

# 查看代码审查
cat .claude/output/todo_app/reviews/code_review.json

# 查看部署指南
cat .claude/output/todo_app/deployment/deployment_guide.md
```

## 学习要点

通过这个案例，你可以学到：

1. **需求分析** - 从需求到用户故事的转化
2. **系统架构** - 前后分离架构的设计
3. **数据库设计** - 关系型数据库的设计原则
4. **API 设计** - RESTful API 的最佳实践
5. **前端开发** - React + TypeScript 开发模式
6. **后端开发** - Express.js + Node.js 开发模式
7. **测试策略** - 单元测试、集成测试、端到端测试
8. **部署上线** - Docker 容器化和部署流程
