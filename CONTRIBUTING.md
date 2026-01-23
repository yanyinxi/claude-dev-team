# 🤝 贡献指南

感谢您对 Claude Dev Team 的贡献！

## 📝 提交规范

### 提交信息要求
- **必须使用中文**作为提交信息的主体内容
- 遵循[约定式提交规范](https://www.conventionalcommits.org/zh-hans/v1.0.0/)
- 格式：`<类型>[可选范围]: <中文描述>`

### 提交类型
- `🚀 feat`: 新功能
- `🔧 fix`: 修复bug
- `📚 docs`: 文档变更
- `💅 style`: 代码格式调整
- `♻️ refactor`: 代码重构
- `⚡ perf`: 性能优化
- `✅ test`: 测试相关
- `🔨 chore`: 构建过程或辅助工具的变动
- `⬆️ upgrade`: 升级依赖或版本

### 提交信息示例
```bash
# ✅ 正确示例
🚀 功能: 新增LLM驱动的质量评估系统
🔧 修复: 解决SubagentStop Hook执行超时问题
📚 文档: 更新README中的使用指南
♻️ 重构: 优化Hooks配置结构

# ❌ 错误示例
feat: add new feature
修复了一个bug
update documentation
```

### 提交前检查清单
- [ ] 代码通过所有测试 (`cd .claude && bash tests/test-hooks.sh`)
- [ ] 配置验证通过 (`cd .claude && bash tests/validate-config.sh`)
- [ ] 提交信息使用中文
- [ ] 提交信息遵循约定式提交规范

## 🛠️ 开发环境设置

### 环境要求
- Claude Code v0.1+
- Python 3.8+
- Node.js 16+

### 本地开发
```bash
# 克隆项目
git clone <repository-url>
cd claude-dev-team

# 验证环境
claude --version

# 运行测试
cd .claude
bash tests/validate-config.sh
bash tests/test-hooks.sh
```

## 🔧 功能开发流程

### 1. 创建功能分支
```bash
git checkout -b feature/新功能名称
```

### 2. 开发功能
- 遵循现有的代码结构
- 添加相应的测试用例
- 更新相关文档

### 3. 提交代码
```bash
# 添加文件
git add .

# 提交（必须使用中文）
git commit -m "🚀 功能: 新增XXX功能

详细描述功能变更内容"

# 推送
git push origin feature/新功能名称
```

### 4. 创建Pull Request
- 在GitHub上创建PR
- 详细描述变更内容
- 请求代码审查

## 📋 代码质量标准

### 配置文件规范
- `settings.json`: 必须通过配置验证
- Hook配置: 必须包含中文注释
- Skill定义: 必须包含完整的元数据

### 测试要求
- 新功能必须包含相应的测试用例
- 现有功能修改后测试不能失败
- 性能测试必须达到95%+标准

### 文档要求
- 新功能必须更新README.md
- API变更必须更新相关文档
- 复杂功能必须提供使用示例

## 🚨 注意事项

### 安全要求
- 不要提交敏感信息（如API密钥）
- 遵循最小权限原则配置权限
- 定期审查和更新依赖版本

### 兼容性要求
- 确保向后兼容性
- 避免破坏现有功能
- 渐进式功能发布

### 性能要求
- 新功能不能显著降低系统性能
- 必须通过性能基准测试
- 监控资源使用情况

## 📞 获取帮助

如果您在贡献过程中遇到问题：

1. 查看[故障排除指南](/docs/troubleshooting.md)
2. 在GitHub Issues中提出问题
3. 联系维护者

## 🙏 贡献者协议

通过提交代码，您同意：
- 您的贡献遵循项目的开源协议
- 您拥有贡献代码的版权或获得授权
- 您的贡献不会侵犯第三方权益

感谢您的贡献！🎉
