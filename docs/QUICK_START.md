# 快速开始

## 5 分钟上手

### 1. 安装

```bash
git clone https://github.com/yourusername/claude-dev-team.git
cd claude-dev-team
pip install -r requirements.txt
cp .env.example .env
```

### 2. 使用快捷命令

```bash
# 开发新功能
/develop "实现用户登录功能"

# 修复 Bug
/fix "登录按钮点击无响应"

# 代码审查
/review "PR #123"

# 查看状态
/status
```

### 3. 查看输出

```bash
# 查看需求文档
cat .claude/output/user_login/prd/user_login_prd.md

# 查看技术设计
cat .claude/output/user_login/design/user_login_design.md

# 查看代码
ls .claude/output/user_login/code/

# 查看测试报告
cat .claude/output/user_login/tests/test_report.json
```

## 下一步

- 查看完整文档：[参考文档](.claude/README.md)
- 查看示例：[示例项目](../examples/)
