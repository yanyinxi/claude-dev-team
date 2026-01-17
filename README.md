# AI 开发团队协作系统

## 简介

这是一个基于 Claude Code 构建的 AI 开发团队协作系统，模拟真实软件开发团队的角色分工和协作流程。

## 核心特性

- ✅ 6 个专业 AI 代理角色
- ✅ 8 个可复用技能包
- ✅ 3 种标准化工作流
- ✅ **动态开发者数量**（LLM 智能决定）
- ✅ 并行任务执行
- ✅ 质量关卡控制
- ✅ 完整的协作记录

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/claude-dev-team.git
cd claude-dev-team

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env
```

### 使用

```bash
# 使用快捷命令
/develop "实现用户登录功能"
/fix "修复登录验证失败的问题"
/review "审查 PR #123"
/status "查看项目状态"
```

## 文档

- [快速开始](docs/QUICK_START.md)
- [代理参考](.claude/AGENTS.md)
- [技能参考](.claude/SKILLS.md)
- [工作流参考](.claude/WORKFLOWS.md)
- [故障排查](docs/TROUBLESHOOTING.md)

## 示例

- [简单 CRUD](examples/simple_crud/)
- [完整应用](examples/fullstack_app/)
- [Bug 修复](examples/bug_fix/)

## 配置

### 动态开发者数量

系统支持 LLM 动态决定开发者数量：

- **前端**: 1-5 人（LLM 根据复杂度决定）
- **后端**: 1-5 人（LLM 根据复杂度决定）

配置方式：

1. **settings.toml**:
   ```toml
   [developers.max]
   frontend = 5
   backend = 5
   ```

2. **环境变量**:
   ```bash
   MAX_FRONTEND_WORKERS=5
   MAX_BACKEND_WORKERS=5
   ```

3. **命令行参数**:
   ```bash
   --max-frontend-workers 5 --max-backend-workers 5
   ```

## 技术栈

- Claude Code 原生能力
- Python 3.8+
- 工作流自动化
- 并行任务执行
- 质量关卡控制

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License

## 联系方式

- GitHub: https://github.com/yourusername/claude-dev-team
- Issues: https://github.com/yourusername/claude-dev-team/issues
