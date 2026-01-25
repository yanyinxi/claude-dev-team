# 简单 CRUD 用户管理功能 - 步骤说明

## 使用方式

1. 在 Claude Code 中输入：
   ```
   "实现简单的用户管理功能，包括创建、读取、更新、删除用户"
   ```

2. 系统会自动：
   - 分析需求
   - 设计架构
   - 分配开发者（动态）
   - 并行开发
   - 测试
   - 审查
   - 交付

## 预期输出

```
.claude/output/user_management/
├── prd/
│   └── user_management_prd.md
├── design/
│   ├── user_management_design.md
│   └── task_assignment.json
├── code/
│   ├── frontend/
│   │   └── user_management/
│   │       ├── worker1/
│   │       └── ...
│   └── backend/
│       └── user_management/
│           ├── worker1/
│           └── ...
├── tests/
│   └── test_report.json
├── reviews/
│   └── code_review.json
└── reports/
    └── delivery_report.md
```

## 查看结果

```bash
# 查看 PRD
cat .claude/output/user_management/prd/user_management_prd.md

# 查看设计
cat .claude/output/user_management/design/user_management_design.md

# 查看代码
ls .claude/output/user_management/code/

# 查看测试报告
cat .claude/output/user_management/tests/test_report.json

# 查看审查报告
cat .claude/output/user_management/reviews/code_review.json
```
