# Claude Dev Team 项目规范

## 项目概述

这是一个**自进化的AI开发团队系统**，使用Claude Code原生能力构建。系统通过8个专业AI代理协作完成软件开发全流程，并能从每次任务中学习和改进。

## 核心原则

1. **Agent优先**: 所有复杂任务必须委托给专业agent，不要在主会话直接实现大量代码
2. **记录优先**: 每个任务完成后必须调用Evolver记录经验，持续积累系统智慧
3. **测试优先**: 代码实现后立即编写测试，确保质量
4. **协作优先**: 跨领域任务使用orchestrator协调多个agent并行工作

## 技术栈约束

### 前端技术栈
- **框架**: React 18+
- **语言**: TypeScript 5+
- **测试**: Jest
- **代码风格**: ESLint + Prettier (2空格缩进)
- **构建**: Vite

### 后端技术栈
- **运行时**: 
- **框架**: FastAPI，Language，
- **测试**: Mocha + Chai
- **数据库**: SQLite3 (开发，生产)
- **代码风格**: ESLint + Prettier (2空格缩进)

### 通用规范
- **Git提交**: 使用语义化提交信息 (feat/fix/docs/refactor/test)
- **分支策略**: main (生产), develop (开发), feature/* (功能分支)
- **代码审查**: 所有PR必须经过code-reviewer审查

## 构建命令

### 全局命令
```bash
# 安装依赖
npm install

# 运行所有测试
npm test

# 代码格式化
npm run lint
npm run lint:fix
```

### 示例项目命令 (examples/*)
```bash
# 进入示例目录
cd examples/todo_app

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 运行测试
npm test
```

## Agent使用规范

### 标准工作流

```
用户需求
    ↓
orchestrator (协调整个流程)
    ↓
product-manager (需求分析 → 生成PRD)
    ↓
tech-lead (技术设计 → 架构方案 + API设计)
    ↓
frontend-developer / backend-developer (并行开发)
    ↓
test (测试计划 + 自动化测试)
    ↓
code-reviewer (代码审查 + 安全检查)
    ↓
orchestrator (最终决策)
    ↓
evolver (系统进化 - 记录最佳实践) ⭐
```

### Agent职责划分

| Agent | 职责 | 触发场景 |
|-------|------|---------|
| **orchestrator** | 流程协调、任务分配 | 复杂的多阶段任务 |
| **product-manager** | 需求分析、PRD生成 | 需要明确产品需求时 |
| **tech-lead** | 架构设计、技术选型、API设计 | 需要技术方案时 |
| **frontend-developer** | 前端组件、页面、测试 | 实现UI/前端逻辑 |
| **backend-developer** | API实现、数据库、业务逻辑 | 实现后端服务 |
| **test** | 测试计划、自动化测试、报告 | 质量保证环节 |
| **code-reviewer** | 代码审查、安全检查、最佳实践 | PR审查、安全审计 |
| **evolver** | 系统进化、经验记录 | 每个任务结束时 |

## 文档约定

### 文档存放位置

```
main/docs/
├── prds/              # 产品需求文档
├── tech_designs/      # 技术设计文档
├── api/               # API文档 (OpenAPI 3.0)
├── test_reports/      # 测试报告
├── reviews/           # 代码审查报告
└── task_distribution/ # 任务分配文档
```

### 文档命名规范

- PRD: `prds/{feature-name}.md`
- 技术设计: `tech_designs/{feature-name}.md`
- API文档: `api/{feature-name}.yaml`
- 测试报告: `test_reports/{feature-name}.md`

## 代码规范

### TypeScript/JavaScript

```typescript
// ✅ 好的实践
export const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle }) => {
  const handleClick = useCallback(() => {
    onToggle(todo.id);
  }, [todo.id, onToggle]);
  
  return (
    <div className="todo-item">
      <input type="checkbox" checked={todo.completed} onChange={handleClick} />
      <span>{todo.text}</span>
    </div>
  );
};

// ❌ 避免的实践
export const TodoItem = (props) => {  // 缺少类型
  return <div onClick={() => props.onToggle(props.todo.id)}>  // 内联函数
    <input type="checkbox" checked={props.todo.completed} />
    <span>{props.todo.text}</span>
  </div>
}
```

### API设计规范

遵循RESTful设计原则:

```
GET    /api/todos        # 列出所有
GET    /api/todos/:id    # 获取单个
POST   /api/todos        # 创建
PUT    /api/todos/:id    # 更新
DELETE /api/todos/:id    # 删除
```

响应格式:
```json
{
  "success": true,
  "data": { /* 实际数据 */ },
  "error": null
}
```

### 测试规范

- **单元测试**: 覆盖率 > 80%
- **集成测试**: 覆盖关键业务流程
- **命名**: `describe` + `it` 清晰描述测试场景

```javascript
describe('TodoList Component', () => {
  it('should render all todos', () => {
    // 测试实现
  });
  
  it('should toggle todo completion when clicked', () => {
    // 测试实现
  });
});
```

## 禁止行为

- ❌ **不要在主会话中直接写大量代码** - 应该委托给相应的developer agent
- ❌ **不要跳过测试环节** - 代码必须有对应的测试
- ❌ **不要忘记调用Evolver** - 每个任务结束必须记录经验
- ❌ **不要修改.git目录** - 保护版本控制完整性
- ❌ **不要提交敏感信息** - .env文件、密钥必须在.gitignore中
- ❌ **不要使用危险命令** - curl/wget需要明确授权

## 进化系统说明

### 工作原理

每次任务完成后，系统自动调用Evolver agent分析任务结果并更新agent配置:

```
任务执行完成
    ↓
Evolver分析执行结果
    ↓
提取最佳实践和教训
    ↓
更新对应Agent的配置文件 (追加到"📈 进化记录"章节)
    ↓
下次任务自动应用新学到的经验
```

### 查看进化历史

每个agent文件末尾都包含"📈 进化记录"章节，记录了:
- 执行时间
- 任务类型
- 新增最佳实践
- 关键洞察
- 注意事项

示例:
```markdown
## 📈 进化记录（自动生成）

### 基于 [用户登录功能开发] 的学习

**执行时间**: 2026-01-18 17:30

**新增最佳实践**:
- **JWT Token验证**: 使用bcrypt加密密码，Token过期时间设置为24小时
  - 适用场景：所有需要身份认证的API
  - 注意事项：必须在环境变量中配置JWT_SECRET
```

## 常用Slash命令

系统提供的快捷命令 (如果已配置):

- `/agents` - 查看所有可用代理
- `/config` - 打开配置界面
- `/cost` - 查看Token使用成本
- `/export` - 导出会话记录
- `/review` - 快速代码审查

## 性能要求

- **前端首屏加载**: < 3秒
- **API响应时间**: < 500ms (p95)
- **测试执行时间**: < 30秒 (单元测试套件)
- **构建时间**: < 2分钟

## 安全要求

- 所有API必须进行身份验证
- 敏感数据必须加密存储
- 定期运行 `npm audit` 检查依赖漏洞
- 代码审查必须包含安全检查清单

## 相关文档

- [Claude Code 官方文档](https://code.claude.com/docs/zh-CN)
- [Agent配置说明](.claude/README.md)
- [项目示例](examples/README.md)

---

**记住**: 这个文件是项目的"单一真相源"，所有agent在工作时都会参考这里的规范。保持更新！
