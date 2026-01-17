# 故障排查

## 常见问题

### 1. 代理调用失败

**问题**：无法调用某个代理

**解决**：
- 检查代理配置文件是否存在
- 检查代理名称是否正确
- 查看 `.claude/logs/` 日志

### 2. 工作流卡住

**问题**：工作流执行到某个阶段后停止

**解决**：
- 使用 `/status` 查看当前状态
- 使用 `session_read()` 查看完整历史
- 检查 `.claude/logs/` 日志

### 3. 动态开发者不工作

**问题**：开发者数量总是固定的

**解决**：
- 检查 `settings.toml` 配置
- 确认 `enable_dynamic_workers = true`
- 检查复杂度评估逻辑

## 获取帮助

- 查看 [文档](.claude/README.md)
- 提交 [Issue](https://github.com/yourusername/claude-dev-team/issues)
