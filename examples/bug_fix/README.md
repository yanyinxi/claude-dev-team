# Bug Fix - 调试真实缺陷

**难度**：⭐⭐ | **时间**：1 小时

## 背景

真实缺陷案例：用户使用正确密码登录时，系统显示"验证码错误"。学习如何快速定位和修复问题。

## 文件结构

```
├── input/bug_report.txt       # 缺陷描述
├── expected/
│   ├── analysis.md            # 问题分析
│   ├── fix.md                 # 解决方案
│   └── test_report.md         # 验证报告
├── walkthrough.md            # 调试步骤
└── README.md                 # 本文件
```

## 如何实现

1. `cat input/bug_report.txt` - 理解缺陷
2. `cat walkthrough.md` - 学习调试步骤
3. `cat expected/` - 对比参考答案

## 如何使用

自己先分析原因，再查看 `expected/analysis.md` 对比。学习用日志、断点等工具定位问题。

## 注意事项

- 不要直接看答案，先自己分析
- 理解问题根因，而不是只修复表现
- 修复后要验证不引入新问题
