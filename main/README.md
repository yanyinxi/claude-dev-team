# Todo App - 待办事项管理应用

一个现代化的全栈待办事项管理应用，包含 React 前端和 Express 后端，采用 SQLite 数据库。

## 功能特性

- ✅ 创建、查看、更新和删除待办事项
- ✅ 标记任务完成状态
- ✅ 按状态筛选任务（待办/已完成）
- ✅ 响应式设计，支持各种设备
- ✅ RESTful API 接口
- ✅ 完整的单元测试覆盖
- ✅ 数据库自动初始化

## 技术栈

### 前端
- **React** - UI 框架
- **TypeScript** - 类型安全
- **Jest** - 单元测试框架
- **Babel** - JavaScript 编译器

### 后端
- **Express.js** - Web 框架
- **SQLite3** - 轻量级数据库
- **Node.js** - 运行时环境
- **Mocha/Chai** - 单元测试框架

## 项目结构

```
main/
├── src/
│   ├── backend/
│   │   ├── app.js              # Express 应用主文件
│   │   ├── init.js             # 数据库初始化脚本
│   │   ├── api/
│   │   │   └── todos.js        # 待办事项 API 路由
│   │   ├── data/               # 数据层
│   │   ├── models/
│   │   │   └── database.js     # 数据库配置
│   │   └── services/           # 业务逻辑层
│   ├── frontend/
│   │   ├── index.html          # HTML 入口
│   │   ├── TodoApp.tsx         # 主应用组件
│   │   ├── components/         # React 组件
│   │   │   ├── TodoForm.tsx    # 新增任务表单
│   │   │   ├── TodoList.tsx    # 待办列表
│   │   │   └── *.css           # 组件样式
│   │   ├── pages/              # 页面组件
│   │   ├── styles/             # 全局样式
│   │   └── types/              # TypeScript 类型定义
│   └── data/                   # 数据文件
├── tests/
│   ├── test_todos.js           # 后端 API 测试
│   ├── backend/                # 后端集成测试
│   └── frontend/               # 前端组件测试
│       ├── TodoForm.test.js
│       ├── TodoList.test.js
│       └── types.test.js
├── docs/                       # 文档
│   ├── api/
│   │   └── todo_app.yaml       # OpenAPI 规范
│   ├── prd/                    # 产品需求文档
│   ├── tech_designs/           # 技术设计文档
│   └── ...                     # 其他文档
├── package.json                # 项目配置
├── jest.config.js              # Jest 配置
└── babel.config.json           # Babel 配置
```

## 快速开始

### 前置要求

- Node.js >= 14.x
- npm >= 6.x

### 1. 克隆项目

```bash
cd 项目根目录
```

### 2. 安装依赖

```bash
npm install
```

### 3. 初始化数据库

```bash
npm run init-db
```

这将创建 SQLite 数据库并初始化必要的表。

### 4. 启动应用

```bash
npm start
```

应用将在 `http://localhost:3000` 启动。

## 使用指南

### 访问应用

打开浏览器，访问 `http://localhost:3000`

### 创建待办事项

1. 在"新增待办"表单中输入任务标题
2. 点击"添加"按钮
3. 新任务将出现在列表中

### 管理待办事项

- **标记完成**：点击任务前的复选框标记为完成
- **删除任务**：点击"删除"按钮移除任务
- **筛选**：使用状态筛选器查看待办或已完成的任务

## API 文档

### 获取所有待办事项

```
GET /api/todos?status=pending
```

**参数：**
- `status` (可选): `pending` 或 `completed`

**响应示例：**
```json
[
  {
    "id": 1,
    "title": "完成项目文档",
    "description": "编写项目的使用文档",
    "status": "pending",
    "createdAt": "2026-01-18T10:00:00Z",
    "updatedAt": "2026-01-18T10:00:00Z"
  }
]
```

### 创建待办事项

```
POST /api/todos
```

**请求体：**
```json
{
  "title": "学习 React",
  "description": "学习 React 框架的基础概念"
}
```

### 更新待办事项

```
PUT /api/todos/:id
```

**请求体：**
```json
{
  "title": "学习 React Hooks",
  "description": "深入学习 React Hooks",
  "status": "completed"
}
```

### 删除待办事项

```
DELETE /api/todos/:id
```

详细的 API 文档见 [todo_app.yaml](docs/api/todo_app.yaml)

## 测试

### 运行所有测试

```bash
npm test
```

### 运行后端测试

```bash
npm run test:backend
```

### 运行前端测试

```bash
npm run test:frontend
```

### 实时监听前端测试

```bash
npm run test:watch
```

## 开发

### 后端开发

编辑文件位置：
- API 路由：`src/backend/api/todos.js`
- 数据库模型：`src/backend/models/database.js`
- 业务逻辑：`src/backend/services/`

### 前端开发

编辑文件位置：
- 主应用：`src/frontend/TodoApp.tsx`
- 组件：`src/frontend/components/`
- 样式：`src/frontend/styles/` 和 `src/frontend/components/*.css`
- 类型定义：`src/frontend/types/`

## 常见问题

### Q: 应用无法连接到数据库？
A: 确保已运行 `npm run init-db` 初始化数据库。

### Q: 前端无法加载？
A: 检查 `http://localhost:3000` 是否可访问，确保后端已启动。

### Q: 如何更改服务器端口？
A: 编辑 `src/backend/app.js` 中的端口配置（默认为 3000）。

### Q: 如何重置数据库？
A: 删除 `data/` 目录中的数据库文件，然后运行 `npm run init-db`。

## 部署

### 生产环境部署

1. 设置环境变量
2. 运行 `npm install --production`
3. 执行 `npm run init-db`
4. 启动应用 `npm start`

### Docker 部署（可选）

如需 Docker 支持，请参考项目根目录的 Docker 配置文件。

## 文档

- [产品需求文档](docs/prd/todo_app.md) - 功能需求
- [技术设计文档](docs/tech_designs/todo_app.md) - 架构设计
- [API 规范](docs/api/todo_app.yaml) - RESTful API 文档
- [测试报告](docs/test_reports/todo_app.md) - 测试覆盖率
- [任务分配](docs/task_distribution/todo_app.md) - 开发任务

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

**最后更新**: 2026 年 1 月 18 日
