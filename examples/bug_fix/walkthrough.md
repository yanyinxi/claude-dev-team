# 调试登录验证失败 - 步骤说明

## 使用方式

1. 在 Claude Code 中输入：
   ```
   "用户登录时，即使输入正确的用户名和密码，系统也提示'验证码错误'，请分析并修复这个问题"
   ```

2. 系统会自动：
   - 分析问题
   - 设计调试方案
   - 分配调试任务（动态）
   - 并行调试
   - 定位根因
   - 实现修复
   - 验证测试
   - 交付报告

## 预期输出

```
.claude/output/login_bug_fix/
├── analysis/
│   ├── problem_analysis.md          # 问题分析
│   ├── root_cause_analysis.md       # 根因分析
│   └── debug_steps.md               # 调试步骤
├── design/
│   ├── fix_design.md                # 修复方案设计
│   └── task_assignment.json         # 任务分配
├── code/
│   ├── before/
│   │   └── login.js                 # 原始代码
│   ├── after/
│   │   └── login.js                 # 修复后代码
│   └── diff/
│       └── changes.patch            # 代码变更
├── tests/
│   ├── test_cases.md                # 测试用例
│   ├── test_results.json            # 测试结果
│   └── regression_test.md           # 回归测试
├── reviews/
│   └── code_review.json             # 代码审查
└── reports/
    ├── debug_report.md              # 调试报告
    └── delivery_report.md           # 交付报告
```

## 查看结果

```bash
# 查看问题分析
cat .claude/output/login_bug_fix/analysis/problem_analysis.md

# 查看根因分析
cat .claude/output/login_bug_fix/analysis/root_cause_analysis.md

# 查看修复方案
cat .claude/output/login_bug_fix/design/fix_design.md

# 查看原始代码
cat .claude/output/login_bug_fix/code/before/login.js

# 查看修复后代码
cat .claude/output/login_bug_fix/code/after/login.js

# 查看代码变更
cat .claude/output/login_bug_fix/code/diff/changes.patch

# 查看测试结果
cat .claude/output/login_bug_fix/tests/test_results.json

# 查看调试报告
cat .claude/output/login_bug_fix/reports/debug_report.md
```

## 学习要点

通过这个案例，你可以学到：

1. **问题分析** - 如何快速理解问题的表现形式
2. **根因定位** - 如何通过日志、追踪找到真实原因
3. **调试工具** - 如何有效使用调试工具辅助分析
4. **修复验证** - 如何确保修复正确且不引入新问题
5. **回归测试** - 如何测试相关功能以防引入新缺陷
